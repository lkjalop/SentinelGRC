"""
Secure Groq API Integration for Sentinel GRC
=============================================
Handles Groq API key securely and provides enhanced LLM capabilities for agents.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    """Response from LLM API"""
    content: str
    confidence: float
    model_used: str
    tokens_used: int
    processing_time: float

class SecureGroqClient:
    """
    Secure wrapper for Groq API with fallback capabilities.
    Handles API key securely and provides error handling.
    """
    
    def __init__(self):
        self.client = None
        self.api_key = None
        self.models_available = []
        
        # Try to initialize Groq client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client securely"""
        
        # Try multiple methods to get API key
        self.api_key = (
            os.getenv('GROQ_API_KEY') or
            self._load_from_secure_config() or
            self._load_from_env_file()
        )
        
        if self.api_key:
            try:
                import groq
                self.client = groq.Client(api_key=self.api_key)
                self.models_available = self._get_available_models()
                logger.info(f"Groq client initialized successfully - Models: {len(self.models_available)}")
                return True
            except ImportError:
                logger.warning("Groq package not installed. Run: pip install groq")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        else:
            logger.warning("No Groq API key found. LLM features will use fallback responses.")
        
        return False
    
    def _load_from_secure_config(self) -> Optional[str]:
        """Load API key from secure config if available"""
        try:
            from secure_config import SecureConfig
            config = SecureConfig()
            return config.get_secret("GROQ_API_KEY")
        except (ImportError, Exception):
            return None
    
    def _load_from_env_file(self) -> Optional[str]:
        """Load API key from .env file"""
        try:
            from pathlib import Path
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('GROQ_API_KEY='):
                            return line.split('=', 1)[1].strip()
        except Exception:
            pass
        return None
    
    def _get_available_models(self) -> List[str]:
        """Get list of available Groq models"""
        try:
            if self.client:
                models = self.client.models.list()
                return [model.id for model in models.data if 'chat' in model.id.lower()]
        except Exception as e:
            logger.warning(f"Could not fetch Groq models: {e}")
        
        # Return known Groq models as fallback
        return [
            "llama3-8b-8192",
            "llama3-70b-8192", 
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
    
    def is_available(self) -> bool:
        """Check if Groq client is available"""
        return self.client is not None
    
    async def generate_response(self, 
                               prompt: str, 
                               system_message: str = None,
                               model: str = "llama3-8b-8192",
                               max_tokens: int = 1000,
                               temperature: float = 0.3) -> LLMResponse:
        """
        Generate response using Groq API with fallback.
        """
        
        if not self.is_available():
            return self._fallback_response(prompt)
        
        try:
            import time
            start_time = time.time()
            
            # Prepare messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            processing_time = time.time() - start_time
            
            # Extract response
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Calculate confidence based on response quality
            confidence = self._calculate_response_confidence(content, prompt)
            
            return LLMResponse(
                content=content,
                confidence=confidence,
                model_used=model,
                tokens_used=tokens_used,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return self._fallback_response(prompt, error=str(e))
    
    def _calculate_response_confidence(self, response: str, prompt: str) -> float:
        """Calculate confidence score for LLM response"""
        
        confidence = 0.7  # Base confidence
        
        # Length-based confidence
        if len(response) > 100:
            confidence += 0.1
        if len(response) > 500:
            confidence += 0.1
        
        # Structure-based confidence
        if any(marker in response.lower() for marker in ['recommendation', 'assessment', 'analysis']):
            confidence += 0.1
        
        # Specific content confidence
        if 'compliance' in prompt.lower() and 'compliance' in response.lower():
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _fallback_response(self, prompt: str, error: str = None) -> LLMResponse:
        """Provide fallback response when Groq is unavailable"""
        
        fallback_content = """
        [AI Analysis Not Available]
        
        This analysis requires AI language model capabilities that are currently unavailable.
        
        Fallback recommendations:
        • Consult with compliance professionals for detailed analysis
        • Review relevant compliance frameworks directly
        • Consider manual assessment using standard checklists
        
        Please ensure Groq API access is configured for enhanced AI analysis.
        """
        
        if error:
            fallback_content += f"\n\nTechnical details: {error}"
        
        return LLMResponse(
            content=fallback_content,
            confidence=0.3,
            model_used="fallback",
            tokens_used=0,
            processing_time=0.0
        )


class EnhancedLegalAgent:
    """
    Legal agent enhanced with Groq LLM capabilities.
    Falls back gracefully when LLM is unavailable.
    """
    
    def __init__(self):
        self.groq_client = SecureGroqClient()
    
    async def analyze_legal_compliance(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced legal analysis using LLM when available"""
        
        if self.groq_client.is_available():
            return await self._llm_enhanced_analysis(assessment_data)
        else:
            return await self._rule_based_analysis(assessment_data)
    
    async def _llm_enhanced_analysis(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """LLM-enhanced legal analysis"""
        
        company_profile = assessment_data.get("company_profile")
        frameworks = assessment_data.get("frameworks_assessed", [])
        gaps = assessment_data.get("gaps_identified", [])
        
        # Create detailed prompt
        prompt = f"""
        Analyze the legal compliance implications for this assessment:
        
        Company: {company_profile.company_name if company_profile else 'Unknown'}
        Industry: {company_profile.industry if company_profile else 'Unknown'}
        Employee Count: {company_profile.employee_count if company_profile else 'Unknown'}
        Frameworks: {', '.join(frameworks)}
        Compliance Gaps: {len(gaps)} identified
        
        Please provide:
        1. Legal risk assessment
        2. Required disclaimers
        3. Professional liability considerations
        4. Regulatory notification requirements
        5. Recommended next steps
        
        Focus on Australian compliance law and professional practice requirements.
        """
        
        system_message = """
        You are a legal compliance expert specializing in Australian cybersecurity and privacy law.
        Provide practical, actionable legal guidance while clearly distinguishing between 
        technical recommendations and legal advice. Always include appropriate disclaimers.
        """
        
        try:
            # Get LLM response
            llm_response = await self.groq_client.generate_response(
                prompt=prompt,
                system_message=system_message,
                model="llama3-70b-8192",  # Use larger model for legal analysis
                max_tokens=1500,
                temperature=0.2  # Low temperature for consistent legal analysis
            )
            
            # Parse and structure the response
            legal_analysis = {
                "legal_assessment": llm_response.content,
                "confidence": llm_response.confidence,
                "model_used": llm_response.model_used,
                "analysis_type": "llm_enhanced",
                "disclaimer": "This AI-generated analysis is for informational purposes only and does not constitute legal advice.",
                "professional_review_required": llm_response.confidence < 0.8
            }
            
            return legal_analysis
            
        except Exception as e:
            logger.error(f"LLM legal analysis failed: {e}")
            return await self._rule_based_analysis(assessment_data)
    
    async def _rule_based_analysis(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based legal analysis"""
        
        # Use your existing rule-based legal analysis
        from sidecar_agents_option_a import LegalReviewSidecar
        legal_sidecar = LegalReviewSidecar()
        
        rule_based_result = legal_sidecar.review_assessment(assessment_data)
        rule_based_result["analysis_type"] = "rule_based"
        rule_based_result["model_used"] = "rules_engine"
        
        return rule_based_result


class EnhancedThreatAgent:
    """
    Threat modeling agent enhanced with Groq LLM capabilities.
    """
    
    def __init__(self):
        self.groq_client = SecureGroqClient()
    
    async def analyze_threat_landscape(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced threat analysis using LLM when available"""
        
        if self.groq_client.is_available():
            return await self._llm_enhanced_threat_analysis(assessment_data)
        else:
            return await self._rule_based_threat_analysis(assessment_data)
    
    async def _llm_enhanced_threat_analysis(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """LLM-enhanced threat modeling"""
        
        company_profile = assessment_data.get("company_profile")
        gaps = assessment_data.get("gaps_identified", [])
        
        # Create threat analysis prompt
        prompt = f"""
        Perform threat modeling analysis for:
        
        Company: {company_profile.company_name if company_profile else 'Unknown'}
        Industry: {company_profile.industry if company_profile else 'Unknown'}
        Size: {company_profile.employee_count if company_profile else 'Unknown'} employees
        
        Identified Security Gaps:
        {chr(10).join([f"- {gap.get('control', 'Unknown')}: {gap.get('gap_description', '')}" for gap in gaps[:5]])}
        
        Previous Security Incidents: {company_profile.previous_incidents if company_profile and hasattr(company_profile, 'previous_incidents') else 'None reported'}
        
        Please provide:
        1. Most likely attack scenarios based on these gaps
        2. Attack chain analysis (step-by-step)
        3. Business impact assessment
        4. Prioritized mitigation recommendations
        5. Specific threat intelligence for this industry in Australia
        
        Focus on current Australian threat landscape and MITRE ATT&CK techniques.
        """
        
        system_message = """
        You are a cybersecurity threat intelligence analyst specializing in Australian threat landscape.
        Provide detailed, technical threat modeling based on current attack patterns and the specific
        compliance gaps identified. Reference MITRE ATT&CK techniques where relevant.
        """
        
        try:
            # Get LLM response
            llm_response = await self.groq_client.generate_response(
                prompt=prompt,
                system_message=system_message,
                model="llama3-70b-8192",
                max_tokens=2000,
                temperature=0.3
            )
            
            threat_analysis = {
                "threat_assessment": llm_response.content,
                "confidence": llm_response.confidence,
                "model_used": llm_response.model_used,
                "analysis_type": "llm_enhanced",
                "threat_intelligence_date": "Current",
                "requires_validation": llm_response.confidence < 0.7
            }
            
            return threat_analysis
            
        except Exception as e:
            logger.error(f"LLM threat analysis failed: {e}")
            return await self._rule_based_threat_analysis(assessment_data)
    
    async def _rule_based_threat_analysis(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based threat analysis"""
        
        # Use your existing rule-based threat analysis
        from sidecar_agents_option_a import ThreatModelingSidecar
        threat_sidecar = ThreatModelingSidecar()
        
        rule_based_result = threat_sidecar.model_threats(assessment_data)
        rule_based_result["analysis_type"] = "rule_based"
        rule_based_result["model_used"] = "rules_engine"
        
        return rule_based_result


# Setup utility for Groq API key
def setup_groq_api():
    """Interactive setup for Groq API key"""
    
    print("Groq API Setup for Sentinel GRC")
    print("=" * 35)
    print("\nYou can get a free Groq API key from: https://console.groq.com/keys")
    print("Free tier includes: 14,400 requests per day")
    
    api_key = input("\nEnter your Groq API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Save to .env file
        env_content = f"GROQ_API_KEY={api_key}\n"
        
        # Append to existing .env or create new one
        try:
            with open('.env', 'a') as f:
                f.write(env_content)
            print("✅ Groq API key saved to .env file")
            
            # Test the connection
            client = SecureGroqClient()
            if client.is_available():
                print("✅ Groq API connection successful!")
                print(f"Available models: {len(client.models_available)}")
                return True
            else:
                print("❌ Failed to connect to Groq API")
                return False
                
        except Exception as e:
            print(f"❌ Error saving API key: {e}")
            return False
    else:
        print("⚠️ Skipping Groq setup - enhanced AI features will not be available")
        return False


# Example usage
if __name__ == "__main__":
    # Run setup
    setup_groq_api()
    
    # Test enhanced agents
    async def test_enhanced_agents():
        test_data = {
            "company_profile": type('obj', (object,), {
                'company_name': 'Test Corp',
                'industry': 'Healthcare',
                'employee_count': 200,
                'previous_incidents': ['Phishing 2023']
            }),
            "frameworks_assessed": ["Essential8", "Privacy Act"],
            "gaps_identified": [
                {"control": "E8_7", "gap_description": "No MFA implemented"},
                {"control": "E8_1", "gap_description": "No application control"}
            ]
        }
        
        # Test enhanced legal agent
        legal_agent = EnhancedLegalAgent()
        legal_result = await legal_agent.analyze_legal_compliance(test_data)
        print(f"Legal Analysis Type: {legal_result.get('analysis_type')}")
        print(f"Legal Confidence: {legal_result.get('confidence', 0):.2f}")
        
        # Test enhanced threat agent
        threat_agent = EnhancedThreatAgent()
        threat_result = await threat_agent.analyze_threat_landscape(test_data)
        print(f"Threat Analysis Type: {threat_result.get('analysis_type')}")
        print(f"Threat Confidence: {threat_result.get('confidence', 0):.2f}")
    
    # Run async test
    asyncio.run(test_enhanced_agents())