"""
Unified Sentinel GRC Orchestrator
=================================
Integrates all agents (Essential 8, Privacy Act, APRA, SOCI) into main flow
with optional sidecar enhancements.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import numpy as np

# Import your existing components
from sentinel_grc_complete import (
    CompanyProfile, AssessmentResult, ConfidenceLevel, 
    EscalationType, Essential8Agent, RiskAnalysisAgent,
    EscalationManager, HumanReviewInterface
)

# Import new agents
from australian_compliance_agents import (
    PrivacyActAgent, APRACPSAgent, SOCIActAgent
)

# Import ML enhancement
from ml_integration import ComplianceMLEngine

# Import sidecar agents
from sidecar_agents_option_a import (
    SidecarOrchestrator, SidecarPriority, 
    Enhanced_ComplianceOrchestrator
)

# Import Groq integration
from groq_integration_secure import (
    SecureGroqClient, EnhancedLegalAgent, EnhancedThreatAgent
)

# Import Neo4j integration
from neo4j_sentinel_integration import GraphEnhancedAssessment

logger = logging.getLogger(__name__)

class UnifiedSentinelGRC:
    """
    Unified orchestrator that combines all agents and capabilities.
    Main assessment includes all applicable frameworks.
    Sidecar agents provide enhanced analysis in background.
    """
    
    def __init__(self, enable_sidecars: bool = True, enable_groq: bool = True, enable_neo4j: bool = True):
        # Core agents (always run)
        self.core_agents = {
            "essential8": Essential8Agent(),
            "risk": RiskAnalysisAgent(),
            "privacy": PrivacyActAgent(),
            "apra": APRACPSAgent(),
            "soci": SOCIActAgent()
        }
        
        # ML enhancement
        self.ml_engine = ComplianceMLEngine()
        
        # Human oversight
        self.escalation_manager = EscalationManager()
        self.review_interface = HumanReviewInterface()
        
        # Neo4j graph enhancement (optional)
        self.neo4j_enabled = enable_neo4j
        if enable_neo4j:
            try:
                self.graph_enhancer = GraphEnhancedAssessment()
                if not self.graph_enhancer.is_available():
                    logger.warning("Neo4j not available - disabling graph enhancement")
                    self.neo4j_enabled = False
            except Exception as e:
                logger.warning(f"Failed to initialize Neo4j: {e}")
                self.neo4j_enabled = False
        
        # Sidecar enhancement (optional)
        self.sidecars_enabled = enable_sidecars
        if enable_sidecars:
            self.sidecar_orchestrator = SidecarOrchestrator()
        
        # Groq enhancement (optional)
        self.groq_enabled = enable_groq
        if enable_groq:
            self.groq_client = SecureGroqClient()
            self.enhanced_legal_agent = EnhancedLegalAgent()
            self.enhanced_threat_agent = EnhancedThreatAgent()
        
        # Assessment cache
        self.assessment_cache = {}
        
        logger.info(f"Unified Sentinel GRC initialized - Neo4j: {self.neo4j_enabled}, Sidecars: {enable_sidecars}, Groq: {enable_groq}")
    
    async def conduct_comprehensive_assessment(
        self, 
        company_profile: CompanyProfile,
        requested_frameworks: List[str] = None
    ) -> Dict[str, Any]:
        """
        Conduct comprehensive compliance assessment.
        All applicable frameworks assessed in main flow.
        Enhanced analysis via sidecars if enabled.
        """
        
        assessment_start = datetime.now()
        logger.info(f"Starting comprehensive assessment for {company_profile.company_name}")
        
        # Determine applicable frameworks
        applicable_frameworks = self._determine_applicable_frameworks(
            company_profile, requested_frameworks
        )
        
        # Run main assessment (parallel agent execution)
        main_results = await self._run_main_assessment(
            company_profile, applicable_frameworks
        )
        
        # Build unified assessment result
        unified_result = await self._build_unified_assessment(
            company_profile, main_results, assessment_start
        )
        
        # Apply human-in-the-loop escalation logic
        unified_result = self.escalation_manager.evaluate_escalation(unified_result)
        
        # Enhance with Neo4j graph insights if enabled
        enhanced_data = {
            "assessment_result": unified_result,
            "company_profile": company_profile,
            "frameworks_assessed": applicable_frameworks
        }
        
        if self.neo4j_enabled:
            try:
                enhanced_data = self.graph_enhancer.enhance_assessment_with_graph(
                    enhanced_data, company_profile
                )
                # Update unified_result with graph-enhanced data
                unified_result = enhanced_data["assessment_result"]
                logger.info("Assessment enhanced with Neo4j graph insights")
            except Exception as e:
                logger.error(f"Neo4j enhancement failed: {e}")
        
        # Submit for sidecar enhancement if enabled
        sidecar_requests = {}
        if self.sidecars_enabled:
            sidecar_requests = await self._submit_sidecar_analysis(
                unified_result, company_profile
            )
        
        # Prepare final response
        response = {
            "assessment_result": unified_result,
            "frameworks_assessed": applicable_frameworks,
            "processing_time": (datetime.now() - assessment_start).total_seconds(),
            "sidecar_requests": sidecar_requests,
            "groq_enhanced": self.groq_enabled,
            "ml_enhanced": True,
            "neo4j_enhanced": self.neo4j_enabled,
            "graph_insights": enhanced_data.get("graph_insights", {}) if self.neo4j_enabled else {}
        }
        
        logger.info(f"Assessment completed in {response['processing_time']:.2f}s")
        
        return response
    
    def _determine_applicable_frameworks(
        self, 
        company_profile: CompanyProfile,
        requested_frameworks: Optional[List[str]]
    ) -> List[str]:
        """
        Determine which compliance frameworks apply to this company.
        """
        
        applicable = []
        
        # Essential 8 - applies to all Australian organizations
        applicable.append("Essential8")
        
        # Privacy Act - applies to most businesses with personal data
        if (company_profile.employee_count > 3 or  # Small business exemption threshold
            company_profile.industry in ["Healthcare", "Finance", "Education", "Technology"]):
            applicable.append("PrivacyAct")
        
        # APRA CPS 234 - financial services only
        if company_profile.industry in ["Finance", "Banking", "Insurance", "Superannuation"]:
            applicable.append("APRACPS234")
        
        # SOCI Act - critical infrastructure
        critical_sectors = ["Energy", "Telecommunications", "Banking", "Transport", 
                          "Healthcare", "Water", "Defence"]
        if (company_profile.industry in critical_sectors and 
            company_profile.employee_count > 100):  # Size threshold
            applicable.append("SOCIAct")
        
        # Risk analysis - always applicable
        applicable.append("RiskAnalysis")
        
        # Filter by requested frameworks if specified
        if requested_frameworks:
            applicable = [f for f in applicable if f in requested_frameworks]
        
        logger.info(f"Applicable frameworks: {applicable}")
        return applicable
    
    async def _run_main_assessment(
        self, 
        company_profile: CompanyProfile,
        frameworks: List[str]
    ) -> Dict[str, Any]:
        """
        Run main assessment with all applicable agents in parallel.
        """
        
        assessment_tasks = []
        agent_mapping = {
            "Essential8": "essential8",
            "PrivacyAct": "privacy", 
            "APRACPS234": "apra",
            "SOCIAct": "soci",
            "RiskAnalysis": "risk"
        }
        
        # Create assessment tasks for applicable frameworks
        for framework in frameworks:
            agent_key = agent_mapping.get(framework)
            if agent_key and agent_key in self.core_agents:
                task = self.core_agents[agent_key].assess(company_profile)
                assessment_tasks.append((framework, task))
        
        # Execute all assessments in parallel
        results = {}
        if assessment_tasks:
            task_results = await asyncio.gather(
                *[task for _, task in assessment_tasks],
                return_exceptions=True
            )
            
            # Map results back to frameworks
            for i, (framework, _) in enumerate(assessment_tasks):
                result = task_results[i]
                if not isinstance(result, Exception):
                    # Enhance with ML if available
                    if hasattr(self, 'ml_engine'):
                        ml_enhancement = self.ml_engine.enhance_agent_confidence(result)
                        result['ml_confidence'] = ml_enhancement.prediction
                        result['ml_explanation'] = ml_enhancement.explanation
                        
                        # Adjust final confidence
                        original_confidence = result.get('confidence', 0.7)
                        result['confidence'] = (
                            0.6 * ml_enhancement.prediction + 
                            0.4 * original_confidence
                        )
                    
                    results[framework] = result
                else:
                    logger.error(f"{framework} assessment failed: {result}")
                    results[framework] = {
                        "error": str(result),
                        "confidence": 0.3,
                        "framework": framework
                    }
        
        return results
    
    async def _build_unified_assessment(
        self,
        company_profile: CompanyProfile,
        framework_results: Dict[str, Any],
        assessment_start: datetime
    ) -> AssessmentResult:
        """
        Build unified assessment result from all framework assessments.
        """
        
        # Aggregate findings from all frameworks
        all_gaps = []
        all_recommendations = []
        all_controls_assessed = []
        confidence_scores = []
        
        primary_framework = "Essential8"  # Default primary framework
        
        for framework, result in framework_results.items():
            if isinstance(result, dict) and not result.get("error"):
                # Collect gaps
                gaps = result.get("gaps_identified", [])
                for gap in gaps:
                    gap["source_framework"] = framework
                all_gaps.extend(gaps)
                
                # Collect recommendations  
                recommendations = result.get("recommendations", [])
                for rec in recommendations:
                    rec["source_framework"] = framework
                all_recommendations.extend(recommendations)
                
                # Collect controls
                controls = result.get("controls_assessed", [])
                for control in controls:
                    control["source_framework"] = framework
                all_controls_assessed.extend(controls)
                
                # Collect confidence scores
                confidence_scores.append(result.get("confidence", 0.7))
        
        # Calculate overall metrics
        overall_confidence = np.mean(confidence_scores) if confidence_scores else 0.5
        
        # Calculate overall maturity (weighted by framework importance)
        framework_weights = {
            "Essential8": 0.4,
            "PrivacyAct": 0.3,
            "APRACPS234": 0.2,
            "SOCIAct": 0.1
        }
        
        weighted_maturity = 0.0
        total_weight = 0.0
        
        for framework, result in framework_results.items():
            if isinstance(result, dict) and not result.get("error"):
                weight = framework_weights.get(framework, 0.1)
                maturity = result.get("overall_maturity", result.get("compliance_score", 0.5))
                weighted_maturity += maturity * weight
                total_weight += weight
        
        overall_maturity = weighted_maturity / total_weight if total_weight > 0 else 0.5
        
        # Determine confidence level
        if overall_confidence >= 0.9:
            confidence_level = ConfidenceLevel.VERY_HIGH
        elif overall_confidence >= 0.8:
            confidence_level = ConfidenceLevel.HIGH
        elif overall_confidence >= 0.7:
            confidence_level = ConfidenceLevel.MEDIUM
        elif overall_confidence >= 0.6:
            confidence_level = ConfidenceLevel.LOW
        else:
            confidence_level = ConfidenceLevel.VERY_LOW
        
        # Create unified assessment result
        unified_result = AssessmentResult(
            framework="Multi-Framework Assessment",
            company_profile=company_profile,
            controls_assessed=all_controls_assessed,
            gaps_identified=all_gaps,
            recommendations=all_recommendations[:10],  # Top 10 recommendations
            overall_maturity=overall_maturity,
            confidence_score=overall_confidence,
            confidence_level=confidence_level,
            escalation_required=EscalationType.NONE,  # Will be set by escalation manager
            escalation_reasons=[],
            timestamp=assessment_start
        )
        
        # Add framework-specific results
        unified_result.framework_results = framework_results
        
        return unified_result
    
    async def _submit_sidecar_analysis(
        self,
        assessment_result: AssessmentResult,
        company_profile: CompanyProfile
    ) -> Dict[str, str]:
        """
        Submit assessment for enhanced sidecar analysis.
        """
        
        if not self.sidecars_enabled:
            return {}
        
        sidecar_requests = {}
        assessment_data = {
            "company_profile": company_profile,
            "assessment_result": assessment_result,
            "frameworks_assessed": getattr(assessment_result, 'framework_results', {}).keys()
        }
        
        # Determine priority
        priority = self._determine_sidecar_priority(assessment_result)
        
        # Submit for legal review if needed
        if self._needs_legal_review(assessment_result, company_profile):
            legal_request_id = self.sidecar_orchestrator.submit_for_legal_review(
                assessment_data, priority
            )
            sidecar_requests["legal_review"] = legal_request_id
        
        # Submit for threat modeling if needed  
        if self._needs_threat_modeling(assessment_result, company_profile):
            threat_request_id = self.sidecar_orchestrator.submit_for_threat_modeling(
                assessment_data, priority
            )
            sidecar_requests["threat_modeling"] = threat_request_id
        
        return sidecar_requests
    
    def _determine_sidecar_priority(self, assessment_result: AssessmentResult) -> SidecarPriority:
        """Determine priority for sidecar processing."""
        
        critical_gaps = len([g for g in assessment_result.gaps_identified 
                           if g.get("risk_level") == "HIGH"])
        
        if (assessment_result.company_profile.has_government_contracts or
            assessment_result.company_profile.industry in ["Healthcare", "Finance"]):
            return SidecarPriority.HIGH
        elif critical_gaps > 5:
            return SidecarPriority.HIGH
        elif assessment_result.confidence_score < 0.7:
            return SidecarPriority.MEDIUM
        else:
            return SidecarPriority.LOW
    
    def _needs_legal_review(self, assessment_result: AssessmentResult, 
                          company_profile: CompanyProfile) -> bool:
        """Determine if legal review is needed."""
        return (
            company_profile.has_government_contracts or
            company_profile.industry in ["Healthcare", "Finance", "Government"] or
            assessment_result.confidence_score < 0.6 or
            len([g for g in assessment_result.gaps_identified 
                if g.get("risk_level") == "HIGH"]) > 3
        )
    
    def _needs_threat_modeling(self, assessment_result: AssessmentResult,
                             company_profile: CompanyProfile) -> bool:
        """Determine if threat modeling is needed."""
        return (
            len(assessment_result.gaps_identified) > 2 or
            company_profile.get_risk_profile() == "HIGH" or
            bool(company_profile.previous_incidents) or
            company_profile.employee_count > 200
        )
    
    async def get_sidecar_results(self, sidecar_requests: Dict[str, str]) -> Dict[str, Any]:
        """
        Get sidecar analysis results if available.
        """
        
        if not self.sidecars_enabled:
            return {}
        
        sidecar_results = {}
        
        for analysis_type, request_id in sidecar_requests.items():
            result = self.sidecar_orchestrator.get_result(request_id)
            if result:
                sidecar_results[analysis_type] = {
                    "analysis": result.analysis_results,
                    "confidence": result.confidence,
                    "processing_time": result.processing_time,
                    "completed_at": result.completed_at.isoformat()
                }
            else:
                sidecar_results[analysis_type] = {
                    "status": "processing",
                    "message": "Analysis in progress..."
                }
        
        return sidecar_results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status and capabilities."""
        
        status = {
            "core_agents": list(self.core_agents.keys()),
            "ml_enhanced": hasattr(self, 'ml_engine'),
            "sidecars_enabled": self.sidecars_enabled,
            "groq_enhanced": self.groq_enabled and hasattr(self, 'groq_client'),
            "neo4j_enhanced": self.neo4j_enabled and hasattr(self, 'graph_enhancer'),
            "knowledge_sources": [
                "cyber.gov.au (Essential 8)",
                "oaic.gov.au (Privacy Act)",
                "apra.gov.au (CPS 234)",
                "homeaffairs.gov.au (SOCI Act)"
            ]
        }
        
        if self.sidecars_enabled:
            status["sidecar_queue"] = self.sidecar_orchestrator.get_queue_status()
        
        if self.groq_enabled and hasattr(self, 'groq_client'):
            status["groq_available"] = self.groq_client.is_available()
        
        if self.neo4j_enabled and hasattr(self, 'graph_enhancer'):
            status["neo4j_available"] = self.graph_enhancer.is_available()
            status["graph_features"] = [
                "Control relationship analysis",
                "Threat mapping",
                "Implementation path optimization",
                "Risk chain analysis"
            ]
        
        return status


# Convenience wrapper for easy use
class SentinelGRC:
    """
    Main entry point for Sentinel GRC system.
    Simplified interface for common use cases.
    """
    
    def __init__(self, **kwargs):
        self.unified_system = UnifiedSentinelGRC(**kwargs)
    
    async def assess_company(
        self,
        company_name: str,
        industry: str, 
        employee_count: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Simple assessment interface.
        """
        
        # Build company profile
        company_profile = CompanyProfile(
            company_name=company_name,
            industry=industry,
            employee_count=employee_count,
            country=kwargs.get("country", "Australia"),
            has_government_contracts=kwargs.get("has_government_contracts", False),
            annual_revenue=kwargs.get("annual_revenue"),
            current_controls=kwargs.get("current_controls", []),
            previous_incidents=kwargs.get("previous_incidents", [])
        )
        
        # Run comprehensive assessment
        return await self.unified_system.conduct_comprehensive_assessment(
            company_profile,
            kwargs.get("requested_frameworks")
        )
    
    async def get_enhanced_results(self, sidecar_requests: Dict[str, str]) -> Dict[str, Any]:
        """Get enhanced analysis results."""
        return await self.unified_system.get_sidecar_results(sidecar_requests)
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status."""
        return self.unified_system.get_system_status()


# Example usage and testing
if __name__ == "__main__":
    async def test_unified_system():
        """Test the unified system with realistic scenarios."""
        
        print("Testing Unified Sentinel GRC System")
        print("=" * 40)
        
        # Initialize system
        sentinel = SentinelGRC(enable_sidecars=True, enable_groq=True, enable_neo4j=True)
        
        # Test company profiles
        test_companies = [
            {
                "company_name": "HealthTech Solutions",
                "industry": "Healthcare",
                "employee_count": 150,
                "current_controls": ["MFA", "Backups"],
                "has_government_contracts": True
            },
            {
                "company_name": "Community Bank",
                "industry": "Finance", 
                "employee_count": 500,
                "current_controls": ["MFA", "Access Control", "Monitoring"],
                "annual_revenue": 50000000
            },
            {
                "company_name": "Tech Startup",
                "industry": "Technology",
                "employee_count": 25,
                "current_controls": ["MFA"]
            }
        ]
        
        for i, company_data in enumerate(test_companies, 1):
            print(f"\n--- Test {i}: {company_data['company_name']} ---")
            
            # Run assessment
            result = await sentinel.assess_company(**company_data)
            
            print(f"Frameworks assessed: {result['frameworks_assessed']}")
            print(f"Processing time: {result['processing_time']:.2f}s")
            print(f"Overall confidence: {result['assessment_result'].confidence_score:.2f}")
            print(f"Gaps identified: {len(result['assessment_result'].gaps_identified)}")
            print(f"Escalation required: {result['assessment_result'].escalation_required.value}")
            
            if result['sidecar_requests']:
                print(f"Background analysis: {list(result['sidecar_requests'].keys())}")
                
                # Wait a moment and check for sidecar results
                await asyncio.sleep(2)
                enhanced_results = await sentinel.get_enhanced_results(result['sidecar_requests'])
                
                for analysis_type, analysis_result in enhanced_results.items():
                    if analysis_result.get('status') != 'processing':
                        print(f"  {analysis_type}: Completed in {analysis_result.get('processing_time', 0):.2f}s")
        
        # System status
        print(f"\nSystem Status:")
        status = sentinel.get_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    # Run test
    asyncio.run(test_unified_system())