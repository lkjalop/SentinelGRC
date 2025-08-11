"""
Sidecar Agents for Option A - Legal and Threat Modeling
=======================================================
Lightweight implementation of legal review and threat modeling agents
that operate asynchronously without affecting main assessment latency.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import threading
import queue
import time

logger = logging.getLogger(__name__)

class SidecarPriority(Enum):
    """Priority levels for sidecar processing"""
    LOW = 1      # Background analysis
    MEDIUM = 2   # Standard review
    HIGH = 3     # Legal/liability concerns
    CRITICAL = 4 # Immediate attention required

@dataclass
class SidecarRequest:
    """Request for sidecar agent processing"""
    request_id: str
    agent_type: str  # 'legal' or 'threat'
    assessment_data: Dict[str, Any]
    priority: SidecarPriority
    created_at: datetime
    callback_url: Optional[str] = None

@dataclass 
class SidecarResponse:
    """Response from sidecar agent"""
    request_id: str
    agent_type: str
    analysis_results: Dict[str, Any]
    confidence: float
    processing_time: float
    completed_at: datetime
    warnings: List[str] = None

class SidecarOrchestrator:
    """
    Manages sidecar agents that run asynchronously.
    Main assessment continues while sidecars process in background.
    """
    
    def __init__(self):
        self.request_queue = queue.PriorityQueue()
        self.response_cache = {}
        self.active_requests = {}
        
        # Start background worker threads
        self.workers_active = True
        self.worker_threads = []
        
        # Initialize agents
        self.legal_agent = LegalReviewSidecar()
        self.threat_agent = ThreatModelingSidecar()
        
        # Start worker threads
        self._start_workers()
    
    def _start_workers(self):
        """Start background worker threads"""
        # Legal review worker
        legal_worker = threading.Thread(
            target=self._legal_worker,
            name="LegalReviewWorker",
            daemon=True
        )
        legal_worker.start()
        self.worker_threads.append(legal_worker)
        
        # Threat modeling worker
        threat_worker = threading.Thread(
            target=self._threat_worker,
            name="ThreatModelingWorker", 
            daemon=True
        )
        threat_worker.start()
        self.worker_threads.append(threat_worker)
        
        logger.info("Sidecar workers started")
    
    def submit_for_legal_review(self, assessment_data: Dict[str, Any], 
                               priority: SidecarPriority = SidecarPriority.MEDIUM) -> str:
        """
        Submit assessment for legal review (asynchronous).
        Returns request_id for later retrieval.
        """
        request_id = f"legal_{int(time.time())}_{id(assessment_data)}"
        
        request = SidecarRequest(
            request_id=request_id,
            agent_type="legal",
            assessment_data=assessment_data,
            priority=priority,
            created_at=datetime.now()
        )
        
        # Add to queue with priority
        self.request_queue.put((priority.value, request))
        self.active_requests[request_id] = request
        
        logger.info(f"Legal review requested: {request_id} (Priority: {priority.name})")
        return request_id
    
    def submit_for_threat_modeling(self, assessment_data: Dict[str, Any],
                                  priority: SidecarPriority = SidecarPriority.MEDIUM) -> str:
        """
        Submit assessment for threat modeling (asynchronous).
        Returns request_id for later retrieval.
        """
        request_id = f"threat_{int(time.time())}_{id(assessment_data)}"
        
        request = SidecarRequest(
            request_id=request_id,
            agent_type="threat",
            assessment_data=assessment_data,
            priority=priority,
            created_at=datetime.now()
        )
        
        self.request_queue.put((priority.value, request))
        self.active_requests[request_id] = request
        
        logger.info(f"Threat modeling requested: {request_id} (Priority: {priority.name})")
        return request_id
    
    def get_result(self, request_id: str) -> Optional[SidecarResponse]:
        """Get sidecar analysis result if available"""
        return self.response_cache.get(request_id)
    
    def is_ready(self, request_id: str) -> bool:
        """Check if sidecar analysis is complete"""
        return request_id in self.response_cache
    
    def _legal_worker(self):
        """Background worker for legal reviews"""
        while self.workers_active:
            try:
                # Get next legal review request
                priority, request = self.request_queue.get(timeout=1.0)
                
                if request.agent_type != "legal":
                    # Put back in queue if not legal request
                    self.request_queue.put((priority, request))
                    continue
                
                # Process legal review
                start_time = time.time()
                result = self.legal_agent.review_assessment(request.assessment_data)
                processing_time = time.time() - start_time
                
                # Create response
                response = SidecarResponse(
                    request_id=request.request_id,
                    agent_type="legal",
                    analysis_results=result,
                    confidence=result.get("confidence", 0.8),
                    processing_time=processing_time,
                    completed_at=datetime.now(),
                    warnings=result.get("warnings", [])
                )
                
                # Store result
                self.response_cache[request.request_id] = response
                
                # Clean up
                if request.request_id in self.active_requests:
                    del self.active_requests[request.request_id]
                
                self.request_queue.task_done()
                
                logger.info(f"Legal review completed: {request.request_id} ({processing_time:.2f}s)")
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Legal worker error: {e}")
    
    def _threat_worker(self):
        """Background worker for threat modeling"""
        while self.workers_active:
            try:
                # Get next threat modeling request
                priority, request = self.request_queue.get(timeout=1.0)
                
                if request.agent_type != "threat":
                    # Put back in queue if not threat request
                    self.request_queue.put((priority, request))
                    continue
                
                # Process threat modeling
                start_time = time.time()
                result = self.threat_agent.model_threats(request.assessment_data)
                processing_time = time.time() - start_time
                
                # Create response
                response = SidecarResponse(
                    request_id=request.request_id,
                    agent_type="threat",
                    analysis_results=result,
                    confidence=result.get("confidence", 0.7),
                    processing_time=processing_time,
                    completed_at=datetime.now(),
                    warnings=result.get("warnings", [])
                )
                
                # Store result
                self.response_cache[request.request_id] = response
                
                # Clean up
                if request.request_id in self.active_requests:
                    del self.active_requests[request.request_id]
                
                self.request_queue.task_done()
                
                logger.info(f"Threat modeling completed: {request.request_id} ({processing_time:.2f}s)")
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Threat worker error: {e}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue and processing status"""
        return {
            "queued_requests": self.request_queue.qsize(),
            "active_requests": len(self.active_requests),
            "completed_requests": len(self.response_cache),
            "workers_active": self.workers_active
        }
    
    def shutdown(self):
        """Shutdown sidecar orchestrator"""
        self.workers_active = False
        for thread in self.worker_threads:
            thread.join(timeout=5.0)
        logger.info("Sidecar orchestrator shut down")


class LegalReviewSidecar:
    """
    Lightweight legal review agent for Option A.
    Focuses on essential legal validation without complex infrastructure.
    """
    
    def __init__(self):
        self.legal_knowledge = self._initialize_legal_knowledge()
    
    def _initialize_legal_knowledge(self) -> Dict[str, Any]:
        """Initialize basic legal knowledge for Australian compliance"""
        return {
            "privacy_act_requirements": {
                "notification_deadlines": "72 hours for OAIC notification",
                "penalties": "Up to $2.22M for serious or repeated breaches",
                "data_breach_threshold": "Likely to result in serious harm"
            },
            "professional_liability": {
                "disclaimer_required": True,
                "insurance_recommended": "Professional indemnity insurance",
                "advice_boundaries": "Technical guidance only, not legal advice"
            },
            "industry_regulations": {
                "healthcare": ["Privacy Act", "Therapeutic Goods Act"],
                "finance": ["Privacy Act", "APRA CPS 234", "Corporations Act"],
                "critical_infrastructure": ["SOCI Act", "Privacy Act"]
            },
            "compliance_safe_harbors": {
                "essential8": "Following ACSC guidance provides regulatory protection",
                "privacy_act": "Reasonable steps defense available"
            }
        }
    
    def review_assessment(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lightweight legal review focusing on key liability areas.
        """
        try:
            company_profile = assessment_data.get("company_profile")
            frameworks = assessment_data.get("frameworks_assessed", [])
            confidence = assessment_data.get("confidence_score", 0.7)
            
            legal_analysis = {
                "legal_review_required": False,
                "liability_risks": [],
                "required_disclaimers": [],
                "regulatory_considerations": [],
                "professional_advice_boundaries": [],
                "confidence": 0.8,
                "warnings": []
            }
            
            # Check if legal review is required
            legal_analysis["legal_review_required"] = self._requires_legal_review(
                company_profile, confidence
            )
            
            # Assess liability risks
            legal_analysis["liability_risks"] = self._assess_liability_risks(
                company_profile, frameworks
            )
            
            # Generate required disclaimers
            legal_analysis["required_disclaimers"] = self._generate_disclaimers(
                company_profile, frameworks
            )
            
            # Industry-specific regulatory considerations
            legal_analysis["regulatory_considerations"] = self._get_regulatory_considerations(
                company_profile
            )
            
            # Define professional advice boundaries
            legal_analysis["professional_advice_boundaries"] = self._define_advice_boundaries(
                frameworks
            )
            
            # Add warnings for high-risk scenarios
            legal_analysis["warnings"] = self._generate_warnings(
                company_profile, confidence, frameworks
            )
            
            return legal_analysis
            
        except Exception as e:
            logger.error(f"Legal review error: {e}")
            return {
                "legal_review_required": True,
                "error": str(e),
                "confidence": 0.3,
                "warnings": ["Legal review failed - manual review required"]
            }
    
    def _requires_legal_review(self, company_profile, confidence: float) -> bool:
        """Determine if human legal review is required"""
        
        # Always require legal review for:
        if hasattr(company_profile, 'has_government_contracts') and company_profile.has_government_contracts:
            return True
        
        if hasattr(company_profile, 'industry') and company_profile.industry in ["Healthcare", "Finance"]:
            return True
        
        if confidence < 0.7:
            return True
        
        if hasattr(company_profile, 'employee_count') and company_profile.employee_count > 500:
            return True
        
        return False
    
    def _assess_liability_risks(self, company_profile, frameworks: List[str]) -> List[Dict]:
        """Assess professional liability risks"""
        
        risks = []
        
        # Data breach liability
        if "Privacy Act" in frameworks:
            risks.append({
                "type": "Data Breach Liability",
                "risk_level": "HIGH",
                "description": "Potential OAIC penalties up to $2.22M",
                "mitigation": "Professional indemnity insurance required"
            })
        
        # Regulatory compliance advice
        if hasattr(company_profile, 'industry'):
            if company_profile.industry == "Finance":
                risks.append({
                    "type": "Financial Services Regulation", 
                    "risk_level": "CRITICAL",
                    "description": "APRA enforcement action possible",
                    "mitigation": "Legal expert validation required"
                })
        
        # Professional advice boundaries
        risks.append({
            "type": "Professional Advice Scope",
            "risk_level": "MEDIUM", 
            "description": "Risk of providing unauthorized legal advice",
            "mitigation": "Clear disclaimer and scope limitation"
        })
        
        return risks
    
    def _generate_disclaimers(self, company_profile, frameworks: List[str]) -> List[str]:
        """Generate required legal disclaimers"""
        
        disclaimers = [
            "This assessment is provided for informational purposes only and does not constitute professional compliance or legal advice.",
            "You should consult with qualified compliance and legal professionals before making decisions based on this assessment.",
            "The assessment is based on publicly available information and general industry practices."
        ]
        
        # Framework-specific disclaimers
        if "Privacy Act" in frameworks:
            disclaimers.append(
                "Privacy Act compliance requirements may vary based on specific circumstances. "
                "Consult with privacy professionals for definitive guidance."
            )
        
        # Industry-specific disclaimers
        if hasattr(company_profile, 'industry'):
            if company_profile.industry == "Finance":
                disclaimers.append(
                    "Financial services regulation is complex and subject to APRA supervision. "
                    "Obtain professional financial services compliance advice."
                )
        
        return disclaimers
    
    def _get_regulatory_considerations(self, company_profile) -> List[Dict]:
        """Get industry-specific regulatory considerations"""
        
        considerations = []
        
        if not hasattr(company_profile, 'industry'):
            return considerations
        
        industry_regs = self.legal_knowledge["industry_regulations"].get(
            company_profile.industry.lower(), []
        )
        
        for regulation in industry_regs:
            considerations.append({
                "regulation": regulation,
                "applies_to": company_profile.industry,
                "compliance_required": True,
                "regulator": self._get_regulator(regulation)
            })
        
        return considerations
    
    def _get_regulator(self, regulation: str) -> str:
        """Map regulation to regulator"""
        regulator_map = {
            "Privacy Act": "OAIC",
            "APRA CPS 234": "APRA", 
            "SOCI Act": "Department of Home Affairs",
            "Corporations Act": "ASIC"
        }
        return regulator_map.get(regulation, "Various")
    
    def _define_advice_boundaries(self, frameworks: List[str]) -> List[str]:
        """Define what constitutes technical vs legal advice"""
        
        boundaries = [
            "Technical recommendations: Control implementation, security configurations",
            "Compliance guidance: Framework requirements, maturity assessments", 
            "Risk analysis: Threat modeling, vulnerability assessment"
        ]
        
        boundaries.append("Legal advice (NOT PROVIDED): Regulatory interpretation, liability assessment, legal strategy")
        
        return boundaries
    
    def _generate_warnings(self, company_profile, confidence: float, 
                          frameworks: List[str]) -> List[str]:
        """Generate warnings for high-risk scenarios"""
        
        warnings = []
        
        if confidence < 0.6:
            warnings.append("LOW CONFIDENCE: Manual expert review strongly recommended")
        
        if hasattr(company_profile, 'has_government_contracts') and company_profile.has_government_contracts:
            warnings.append("GOVERNMENT CONTRACTOR: Additional security requirements may apply")
        
        if hasattr(company_profile, 'previous_incidents') and company_profile.previous_incidents:
            warnings.append("PREVIOUS INCIDENTS: Enhanced scrutiny and controls may be required")
        
        return warnings


class ThreatModelingSidecar:
    """
    Lightweight threat modeling agent for Option A.
    Provides tactical threat analysis without complex infrastructure.
    """
    
    def __init__(self):
        self.threat_intelligence = self._initialize_threat_intelligence()
    
    def _initialize_threat_intelligence(self) -> Dict[str, Any]:
        """Initialize threat intelligence database"""
        return {
            "mitre_mappings": {
                # Essential 8 controls -> MITRE ATT&CK techniques
                "E8_1": ["T1566.001", "T1204.002"],  # Application Control -> Spearphishing, User Execution
                "E8_2": ["T1068"],  # Patch Applications -> Exploitation for Privilege Escalation
                "E8_3": ["T1566.001", "T1204.002"],  # Macro Settings -> Spearphishing, User Execution
                "E8_5": ["T1078"],  # Admin Privileges -> Valid Accounts
                "E8_7": ["T1078", "T1110"],  # MFA -> Valid Accounts, Brute Force
                "E8_8": ["T1490", "T1486"]  # Backups -> Inhibit Recovery, Data Encrypted for Impact
            },
            "australian_threats": {
                "ransomware": {"prevalence": "HIGH", "sectors": ["Healthcare", "Education", "Government"]},
                "supply_chain": {"prevalence": "MEDIUM", "sectors": ["Technology", "Manufacturing"]},
                "insider_threat": {"prevalence": "MEDIUM", "sectors": ["Finance", "Government"]},
                "phishing": {"prevalence": "CRITICAL", "sectors": ["All"]}
            },
            "industry_attack_patterns": {
                "healthcare": ["Ransomware", "Data theft", "Insider threat"],
                "finance": ["Fraud", "Data breach", "Regulatory evasion"],
                "technology": ["IP theft", "Supply chain", "Credential stuffing"],
                "government": ["Espionage", "Insider threat", "Advanced persistent threat"]
            }
        }
    
    def model_threats(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lightweight threat modeling based on compliance gaps.
        """
        try:
            company_profile = assessment_data.get("company_profile")
            gaps = assessment_data.get("gaps_identified", [])
            controls = assessment_data.get("controls_assessed", [])
            
            threat_model = {
                "attack_scenarios": [],
                "prioritized_threats": [],
                "attack_surface_analysis": {},
                "compensating_controls": [],
                "penetration_testing_focus": [],
                "confidence": 0.7,
                "warnings": []
            }
            
            # Generate attack scenarios based on gaps
            threat_model["attack_scenarios"] = self._generate_attack_scenarios(gaps, company_profile)
            
            # Prioritize threats by likelihood and impact
            threat_model["prioritized_threats"] = self._prioritize_threats(company_profile)
            
            # Analyze attack surface
            threat_model["attack_surface_analysis"] = self._analyze_attack_surface(gaps, company_profile)
            
            # Suggest compensating controls
            threat_model["compensating_controls"] = self._suggest_compensating_controls(gaps)
            
            # Generate penetration testing recommendations
            threat_model["penetration_testing_focus"] = self._generate_pentest_focus(gaps, company_profile)
            
            return threat_model
            
        except Exception as e:
            logger.error(f"Threat modeling error: {e}")
            return {
                "attack_scenarios": [],
                "error": str(e),
                "confidence": 0.3,
                "warnings": ["Threat modeling failed - manual analysis required"]
            }
    
    def _generate_attack_scenarios(self, gaps: List[Dict], company_profile) -> List[Dict]:
        """Generate realistic attack scenarios based on compliance gaps"""
        
        scenarios = []
        
        # Map gaps to attack scenarios
        gap_controls = [g.get("control", "") for g in gaps]
        
        # Ransomware scenario (if backup or application control gaps)
        if any("E8_8" in str(gap) or "E8_1" in str(gap) for gap in gap_controls):
            scenarios.append({
                "attack_type": "Ransomware Attack",
                "likelihood": "HIGH",
                "attack_chain": [
                    "1. Spear-phishing email with malicious attachment",
                    "2. User executes malware (E8_1 gap: no application control)",
                    "3. Malware encrypts files and spreads laterally", 
                    "4. Ransom demand (E8_8 gap: no reliable backups for recovery)"
                ],
                "business_impact": self._calculate_ransomware_impact(company_profile),
                "mitigation_priority": "CRITICAL",
                "controls_needed": ["E8_1", "E8_8", "E8_3"]
            })
        
        # Credential compromise (if MFA gap)
        if any("E8_7" in str(gap) for gap in gap_controls):
            scenarios.append({
                "attack_type": "Credential Compromise",
                "likelihood": "HIGH",
                "attack_chain": [
                    "1. Password spray or phishing attack",
                    "2. Valid account compromise (E8_7 gap: no MFA)",
                    "3. Lateral movement to sensitive systems",
                    "4. Data exfiltration or system compromise"
                ],
                "business_impact": self._calculate_credential_impact(company_profile),
                "mitigation_priority": "HIGH",
                "controls_needed": ["E8_7", "E8_5"]
            })
        
        # Privilege escalation (if admin control gaps)
        if any("E8_5" in str(gap) for gap in gap_controls):
            scenarios.append({
                "attack_type": "Privilege Escalation",
                "likelihood": "MEDIUM",
                "attack_chain": [
                    "1. Initial access via phishing or credential compromise",
                    "2. Exploitation of excessive admin privileges (E8_5 gap)",
                    "3. Administrative access to critical systems",
                    "4. Installation of persistence mechanisms"
                ],
                "business_impact": self._calculate_privilege_impact(company_profile),
                "mitigation_priority": "HIGH", 
                "controls_needed": ["E8_5", "E8_7"]
            })
        
        return scenarios
    
    def _calculate_ransomware_impact(self, company_profile) -> Dict[str, str]:
        """Calculate business impact of ransomware attack"""
        
        if not hasattr(company_profile, 'employee_count'):
            return {"financial": "Unknown", "operational": "Severe", "timeline": "1-4 weeks"}
        
        # Simple impact model based on company size
        if company_profile.employee_count > 500:
            return {
                "financial": "$500K - $2M",
                "operational": "Critical systems down 1-2 weeks", 
                "reputational": "Severe - media attention likely",
                "regulatory": "OAIC notification required"
            }
        elif company_profile.employee_count > 100:
            return {
                "financial": "$50K - $500K",
                "operational": "Systems down 3-7 days",
                "reputational": "Moderate - customer impact",
                "regulatory": "Possible OAIC notification"
            }
        else:
            return {
                "financial": "$10K - $50K",
                "operational": "Systems down 1-3 days",
                "reputational": "Low to moderate",
                "regulatory": "Minimal"
            }
    
    def _calculate_credential_impact(self, company_profile) -> Dict[str, str]:
        """Calculate impact of credential compromise"""
        
        return {
            "financial": "$20K - $200K",
            "operational": "Potential data access/theft",
            "reputational": "Moderate - customer trust impact",
            "regulatory": "Privacy Act breach possible"
        }
    
    def _calculate_privilege_impact(self, company_profile) -> Dict[str, str]:
        """Calculate impact of privilege escalation"""
        
        return {
            "financial": "$50K - $500K",
            "operational": "Full system compromise possible",
            "reputational": "High - complete breach",
            "regulatory": "Multiple regulatory notifications"
        }
    
    def _prioritize_threats(self, company_profile) -> List[Dict]:
        """Prioritize threats based on industry and profile"""
        
        threats = []
        
        if not hasattr(company_profile, 'industry'):
            return threats
        
        # Get industry-specific threats
        industry_threats = self.threat_intelligence["industry_attack_patterns"].get(
            company_profile.industry.lower(), ["Phishing", "Ransomware"]
        )
        
        for threat in industry_threats:
            threat_data = self.threat_intelligence["australian_threats"].get(
                threat.lower(), {"prevalence": "MEDIUM", "sectors": ["All"]}
            )
            
            threats.append({
                "threat_type": threat,
                "likelihood": threat_data["prevalence"],
                "relevant_sectors": threat_data["sectors"],
                "priority": self._calculate_threat_priority(threat, company_profile)
            })
        
        # Sort by priority
        priority_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        threats.sort(key=lambda x: priority_order.get(x["priority"], 1), reverse=True)
        
        return threats
    
    def _calculate_threat_priority(self, threat: str, company_profile) -> str:
        """Calculate threat priority for specific company"""
        
        # High priority threats for all
        if threat.lower() in ["ransomware", "phishing"]:
            return "HIGH"
        
        # Industry-specific priorities
        if hasattr(company_profile, 'industry'):
            if company_profile.industry == "Healthcare" and threat.lower() == "ransomware":
                return "CRITICAL"
            if company_profile.industry == "Finance" and threat.lower() == "fraud":
                return "CRITICAL"
        
        return "MEDIUM"
    
    def _analyze_attack_surface(self, gaps: List[Dict], company_profile) -> Dict[str, Any]:
        """Analyze attack surface based on gaps"""
        
        attack_surface = {
            "external_exposure": "MEDIUM",  # Default assumption
            "internal_segmentation": "UNKNOWN",
            "critical_assets": [],
            "high_risk_gaps": []
        }
        
        # Identify high-risk gaps
        for gap in gaps:
            if gap.get("risk_level") == "HIGH":
                attack_surface["high_risk_gaps"].append({
                    "gap": gap.get("control", "Unknown"),
                    "risk": gap.get("risk_level", "UNKNOWN"),
                    "description": gap.get("gap_description", "")
                })
        
        # Estimate attack surface based on company size
        if hasattr(company_profile, 'employee_count'):
            if company_profile.employee_count > 200:
                attack_surface["external_exposure"] = "HIGH"
            elif company_profile.employee_count < 50:
                attack_surface["external_exposure"] = "LOW"
        
        return attack_surface
    
    def _suggest_compensating_controls(self, gaps: List[Dict]) -> List[Dict]:
        """Suggest compensating controls for gaps that can't be immediately fixed"""
        
        compensating = []
        
        gap_controls = [g.get("control", "") for g in gaps]
        
        # Application control compensating controls
        if any("E8_1" in str(gap) for gap in gap_controls):
            compensating.append({
                "for_control": "E8_1 (Application Control)",
                "compensating_control": "Enhanced email security and user training",
                "effectiveness": "MEDIUM",
                "implementation": "Deploy email security solution, conduct phishing training"
            })
        
        # Backup compensating controls  
        if any("E8_8" in str(gap) for gap in gap_controls):
            compensating.append({
                "for_control": "E8_8 (Regular Backups)",
                "compensating_control": "Incident response and recovery procedures", 
                "effectiveness": "LOW",
                "implementation": "Document recovery procedures, identify critical systems"
            })
        
        return compensating
    
    def _generate_pentest_focus(self, gaps: List[Dict], company_profile) -> List[str]:
        """Generate penetration testing focus areas"""
        
        focus_areas = []
        
        gap_controls = [g.get("control", "") for g in gaps]
        
        # Focus areas based on gaps
        if any("E8_7" in str(gap) for gap in gap_controls):
            focus_areas.append("Password attacks and authentication bypass")
        
        if any("E8_1" in str(gap) for gap in gap_controls):
            focus_areas.append("Malware delivery and execution testing")
        
        if any("E8_5" in str(gap) for gap in gap_controls):
            focus_areas.append("Privilege escalation and lateral movement")
        
        # Industry-specific focus
        if hasattr(company_profile, 'industry'):
            if company_profile.industry == "Healthcare":
                focus_areas.append("Medical device security assessment")
            elif company_profile.industry == "Finance":
                focus_areas.append("Payment system penetration testing")
        
        # Default recommendations
        if not focus_areas:
            focus_areas = [
                "External network perimeter testing",
                "Social engineering assessment", 
                "Web application security testing"
            ]
        
        return focus_areas


# Integration with main system
class Enhanced_ComplianceOrchestrator:
    """
    Enhanced orchestrator that includes optional sidecar agents.
    Maintains backward compatibility with Option A.
    """
    
    def __init__(self, enable_sidecars: bool = True):
        # Initialize main orchestrator (your existing code)
        from sentinel_grc_complete import ComplianceOrchestrator
        self.main_orchestrator = ComplianceOrchestrator()
        
        # Initialize sidecars if enabled
        self.sidecars_enabled = enable_sidecars
        if enable_sidecars:
            self.sidecar_orchestrator = SidecarOrchestrator()
    
    async def conduct_assessment(self, company_profile, requested_frameworks=None):
        """
        Enhanced assessment with optional sidecar analysis.
        Main assessment completes normally, sidecars run in background.
        """
        
        # Run main assessment (your existing code)
        main_result = await self.main_orchestrator.conduct_assessment(
            company_profile, requested_frameworks
        )
        
        # Submit for sidecar analysis if enabled
        sidecar_requests = {}
        
        if self.sidecars_enabled:
            # Determine priority based on main assessment
            priority = self._determine_sidecar_priority(main_result)
            
            # Submit for legal review if needed
            if self._needs_legal_review(main_result):
                legal_request_id = self.sidecar_orchestrator.submit_for_legal_review(
                    {"company_profile": company_profile, "assessment": main_result},
                    priority
                )
                sidecar_requests["legal"] = legal_request_id
            
            # Submit for threat modeling if needed
            if self._needs_threat_modeling(main_result):
                threat_request_id = self.sidecar_orchestrator.submit_for_threat_modeling(
                    {"company_profile": company_profile, "assessment": main_result},
                    priority
                )
                sidecar_requests["threat"] = threat_request_id
        
        # Add sidecar request IDs to main result
        main_result.sidecar_requests = sidecar_requests
        
        return main_result
    
    def _determine_sidecar_priority(self, assessment) -> SidecarPriority:
        """Determine priority for sidecar processing"""
        
        if assessment.escalation_required.value in ["legal_required", "executive_required"]:
            return SidecarPriority.CRITICAL
        elif assessment.confidence_score < 0.7:
            return SidecarPriority.HIGH
        elif len(assessment.gaps_identified) > 5:
            return SidecarPriority.MEDIUM
        else:
            return SidecarPriority.LOW
    
    def _needs_legal_review(self, assessment) -> bool:
        """Determine if legal review is needed"""
        return (
            assessment.company_profile.has_government_contracts or
            assessment.company_profile.industry in ["Healthcare", "Finance"] or
            assessment.confidence_score < 0.6
        )
    
    def _needs_threat_modeling(self, assessment) -> bool:
        """Determine if threat modeling is needed"""
        return (
            len(assessment.gaps_identified) > 2 or
            assessment.company_profile.get_risk_profile() == "HIGH" or
            bool(assessment.company_profile.previous_incidents)
        )
    
    def get_sidecar_results(self, request_ids: Dict[str, str]) -> Dict[str, Any]:
        """Get sidecar analysis results if available"""
        
        if not self.sidecars_enabled:
            return {}
        
        results = {}
        
        for analysis_type, request_id in request_ids.items():
            result = self.sidecar_orchestrator.get_result(request_id)
            if result:
                results[analysis_type] = result.analysis_results
        
        return results


# Example usage
if __name__ == "__main__":
    # Test sidecar integration
    async def test_sidecars():
        from sentinel_grc_complete import CompanyProfile
        
        # Test company
        test_company = CompanyProfile(
            company_name="Test Healthcare Corp",
            industry="Healthcare",
            employee_count=300,
            has_government_contracts=True,
            current_controls=["MFA"],
            previous_incidents=["Ransomware 2023"]
        )
        
        # Enhanced orchestrator with sidecars
        orchestrator = Enhanced_ComplianceOrchestrator(enable_sidecars=True)
        
        # Run assessment
        result = await orchestrator.conduct_assessment(test_company)
        print(f"Main assessment completed - Confidence: {result.confidence_score:.2f}")
        print(f"Sidecar requests: {result.sidecar_requests}")
        
        # Check sidecar results after some time
        import time
        time.sleep(2)  # Wait for background processing
        
        sidecar_results = orchestrator.get_sidecar_results(result.sidecar_requests)
        for analysis_type, analysis_result in sidecar_results.items():
            print(f"{analysis_type.title()} analysis: {len(analysis_result)} findings")
    
    asyncio.run(test_sidecars())