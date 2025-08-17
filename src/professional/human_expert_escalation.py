"""
Human Expert Escalation System for Cerberus AI
===============================================
Manages escalation workflows to human experts when AI confidence is insufficient
or professional judgment is required for complex compliance scenarios.
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid

logger = logging.getLogger(__name__)

class ExpertSpecialty(Enum):
    """Expert specialties for escalation routing"""
    COMPLIANCE_GENERALIST = "compliance_generalist"
    PRIVACY_SPECIALIST = "privacy_specialist"
    CYBERSECURITY_EXPERT = "cybersecurity_expert"
    REGULATORY_SPECIALIST = "regulatory_specialist"
    LEGAL_COUNSEL = "legal_counsel"
    INDUSTRY_EXPERT = "industry_expert"
    AUDIT_SPECIALIST = "audit_specialist"

class EscalationPriority(Enum):
    """Priority levels for expert escalation"""
    LOW = 1         # 48-72 hour response
    MEDIUM = 2      # 24-48 hour response  
    HIGH = 3        # 4-24 hour response
    CRITICAL = 4    # Immediate response required

class EscalationStatus(Enum):
    """Status of escalation requests"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    CLOSED = "closed"

@dataclass
class ExpertProfile:
    """Human expert profile for escalation routing"""
    expert_id: str
    name: str
    specialties: List[ExpertSpecialty]
    certifications: List[str]
    availability_hours: Dict[str, str]  # day_of_week: "start-end" 
    maximum_concurrent_cases: int
    current_workload: int
    response_time_sla: Dict[EscalationPriority, int]  # priority: hours
    contact_method: str
    cost_per_hour: float

@dataclass
class EscalationRequest:
    """Request for human expert escalation"""
    request_id: str
    company_profile: Dict[str, Any]
    assessment_results: Dict[str, Any]
    framework: str
    confidence_score: float
    complexity_indicators: List[str]
    escalation_reason: str
    required_specialty: ExpertSpecialty
    priority: EscalationPriority
    created_at: datetime
    due_date: datetime
    assigned_expert: Optional[str] = None
    status: EscalationStatus = EscalationStatus.PENDING
    expert_response: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None

class HumanExpertEscalationSystem:
    """
    Manages escalation of complex compliance assessments to human experts
    when AI confidence is insufficient or professional judgment is required.
    """
    
    def __init__(self):
        self.expert_network = self._initialize_expert_network()
        self.escalation_rules = self._initialize_escalation_rules()
        self.active_escalations = {}
        self.escalation_history = []
        self.routing_algorithms = self._initialize_routing_algorithms()
        
        logger.info("✅ Human Expert Escalation System initialized")
    
    def _initialize_expert_network(self) -> Dict[str, ExpertProfile]:
        """Initialize network of human experts (demo profiles)"""
        
        return {
            "expert_001": ExpertProfile(
                expert_id="expert_001",
                name="Dr. Sarah Chen - Compliance Director",
                specialties=[ExpertSpecialty.COMPLIANCE_GENERALIST, ExpertSpecialty.PRIVACY_SPECIALIST],
                certifications=["CISSP", "CISA", "Privacy Professional (CIPP/A)"],
                availability_hours={"monday": "09:00-17:00", "tuesday": "09:00-17:00", "wednesday": "09:00-17:00", "thursday": "09:00-17:00", "friday": "09:00-15:00"},
                maximum_concurrent_cases=5,
                current_workload=2,
                response_time_sla={EscalationPriority.CRITICAL: 2, EscalationPriority.HIGH: 8, EscalationPriority.MEDIUM: 24, EscalationPriority.LOW: 48},
                contact_method="secure_portal",
                cost_per_hour=350.0
            ),
            
            "expert_002": ExpertProfile(
                expert_id="expert_002", 
                name="Michael Rodriguez - Cybersecurity Architect",
                specialties=[ExpertSpecialty.CYBERSECURITY_EXPERT, ExpertSpecialty.AUDIT_SPECIALIST],
                certifications=["CISSP", "SABSA", "TOGAF", "ISO 27001 Lead Auditor"],
                availability_hours={"monday": "08:00-18:00", "tuesday": "08:00-18:00", "wednesday": "08:00-18:00", "thursday": "08:00-18:00", "friday": "08:00-16:00"},
                maximum_concurrent_cases=4,
                current_workload=1,
                response_time_sla={EscalationPriority.CRITICAL: 1, EscalationPriority.HIGH: 4, EscalationPriority.MEDIUM: 16, EscalationPriority.LOW: 36},
                contact_method="secure_portal",
                cost_per_hour=425.0
            ),
            
            "expert_003": ExpertProfile(
                expert_id="expert_003",
                name="Jennifer Liu - Financial Services Regulatory Specialist", 
                specialties=[ExpertSpecialty.REGULATORY_SPECIALIST, ExpertSpecialty.INDUSTRY_EXPERT],
                certifications=["CRM", "FRM", "APRA Advisory Experience", "AUSTRAC Compliance"],
                availability_hours={"monday": "09:00-17:00", "tuesday": "09:00-17:00", "wednesday": "09:00-17:00", "thursday": "09:00-17:00", "friday": "09:00-17:00"},
                maximum_concurrent_cases=3,
                current_workload=0,
                response_time_sla={EscalationPriority.CRITICAL: 3, EscalationPriority.HIGH: 12, EscalationPriority.MEDIUM: 24, EscalationPriority.LOW: 48},
                contact_method="secure_portal",
                cost_per_hour=500.0
            ),
            
            "expert_004": ExpertProfile(
                expert_id="expert_004",
                name="Robert Thompson - Legal Counsel (Tech Law)",
                specialties=[ExpertSpecialty.LEGAL_COUNSEL, ExpertSpecialty.PRIVACY_SPECIALIST],
                certifications=["Admitted Solicitor (NSW)", "Privacy Law Specialist", "Technology Law Focus"],
                availability_hours={"monday": "09:00-18:00", "tuesday": "09:00-18:00", "wednesday": "09:00-18:00", "thursday": "09:00-18:00", "friday": "09:00-16:00"},
                maximum_concurrent_cases=2,
                current_workload=1,
                response_time_sla={EscalationPriority.CRITICAL: 2, EscalationPriority.HIGH: 6, EscalationPriority.MEDIUM: 24, EscalationPriority.LOW: 72},
                contact_method="secure_portal",
                cost_per_hour=650.0
            )
        }
    
    def _initialize_escalation_rules(self) -> Dict[str, Any]:
        """Initialize escalation decision rules"""
        
        return {
            "confidence_thresholds": {
                "automatic_escalation": 0.5,    # Below this = always escalate
                "review_recommended": 0.7,      # Below this = recommend escalation
                "high_confidence": 0.9          # Above this = minimal escalation risk
            },
            
            "complexity_indicators": {
                "high_risk_industry": ["Finance", "Healthcare", "Government", "Critical Infrastructure"],
                "regulatory_complexity": ["Multiple frameworks", "Cross-border requirements", "Government contracts"],
                "technical_complexity": ["Cloud-native architecture", "AI/ML systems", "Complex integrations"],
                "business_complexity": ["M&A activity", "Rapid growth", "International operations"]
            },
            
            "automatic_escalation_triggers": [
                "Legal interpretation required",
                "Regulatory enforcement action possible",
                "Material business impact identified",
                "Novel compliance scenario",
                "Conflicting framework requirements",
                "High-profile client or case"
            ],
            
            "specialty_routing": {
                "privacy_act": ExpertSpecialty.PRIVACY_SPECIALIST,
                "apra_cps234": ExpertSpecialty.REGULATORY_SPECIALIST,
                "soci_act": ExpertSpecialty.REGULATORY_SPECIALIST,
                "essential8": ExpertSpecialty.CYBERSECURITY_EXPERT,
                "nist_csf": ExpertSpecialty.CYBERSECURITY_EXPERT,
                "gdpr": ExpertSpecialty.PRIVACY_SPECIALIST,
                "sox": ExpertSpecialty.AUDIT_SPECIALIST,
                "hipaa": ExpertSpecialty.REGULATORY_SPECIALIST
            }
        }
    
    def _initialize_routing_algorithms(self) -> Dict[str, Callable]:
        """Initialize expert routing algorithms"""
        
        return {
            "workload_balanced": self._route_by_workload,
            "expertise_matched": self._route_by_expertise,
            "cost_optimized": self._route_by_cost,
            "sla_optimized": self._route_by_sla
        }
    
    def evaluate_escalation_need(self, 
                                assessment_results: Dict[str, Any],
                                company_profile: Dict[str, Any],
                                framework: str) -> Dict[str, Any]:
        """
        Evaluate whether human expert escalation is needed based on
        confidence scores, complexity, and risk factors.
        """
        
        confidence = assessment_results.get("overall_confidence", 0.0)
        gaps = assessment_results.get("gaps_identified", [])
        
        escalation_decision = {
            "escalation_required": False,
            "escalation_recommended": False,
            "priority": EscalationPriority.LOW,
            "required_specialty": ExpertSpecialty.COMPLIANCE_GENERALIST,
            "reasoning": [],
            "estimated_cost": 0.0,
            "estimated_timeline": "N/A"
        }
        
        # Confidence-based escalation
        if confidence < self.escalation_rules["confidence_thresholds"]["automatic_escalation"]:
            escalation_decision["escalation_required"] = True
            escalation_decision["priority"] = EscalationPriority.HIGH
            escalation_decision["reasoning"].append(f"Low confidence score ({confidence:.2f}) requires expert validation")
        
        elif confidence < self.escalation_rules["confidence_thresholds"]["review_recommended"]:
            escalation_decision["escalation_recommended"] = True
            escalation_decision["priority"] = EscalationPriority.MEDIUM
            escalation_decision["reasoning"].append(f"Medium confidence ({confidence:.2f}) - expert review recommended")
        
        # Complexity-based escalation
        complexity_score = self._calculate_complexity_score(company_profile, assessment_results)
        if complexity_score >= 7:
            escalation_decision["escalation_required"] = True
            escalation_decision["priority"] = max(escalation_decision["priority"], EscalationPriority.HIGH)
            escalation_decision["reasoning"].append(f"High complexity score ({complexity_score}/10) requires expert judgment")
        
        # Risk-based escalation  
        if len(gaps) > 8 or any(gap.get("risk_level") == "CRITICAL" for gap in gaps):
            escalation_decision["escalation_required"] = True
            escalation_decision["priority"] = EscalationPriority.CRITICAL
            escalation_decision["reasoning"].append("Critical compliance gaps identified")
        
        # Industry-specific escalation
        industry = company_profile.get("industry", "").lower()
        if industry in ["finance", "healthcare", "government"]:
            escalation_decision["escalation_recommended"] = True
            escalation_decision["reasoning"].append(f"High-risk industry ({industry}) requires expert oversight")
        
        # Framework-specific routing
        escalation_decision["required_specialty"] = self.escalation_rules["specialty_routing"].get(
            framework, ExpertSpecialty.COMPLIANCE_GENERALIST
        )
        
        # Cost and timeline estimation
        if escalation_decision["escalation_required"] or escalation_decision["escalation_recommended"]:
            cost_estimate = self._estimate_escalation_cost(escalation_decision["priority"], complexity_score)
            timeline_estimate = self._estimate_escalation_timeline(escalation_decision["priority"])
            
            escalation_decision["estimated_cost"] = cost_estimate
            escalation_decision["estimated_timeline"] = timeline_estimate
        
        logger.info(f"🔍 Escalation evaluation for {framework}: Required={escalation_decision['escalation_required']}, Recommended={escalation_decision['escalation_recommended']}")
        
        return escalation_decision
    
    def _calculate_complexity_score(self, company_profile: Dict[str, Any], 
                                  assessment_results: Dict[str, Any]) -> int:
        """Calculate complexity score (0-10) for escalation decisions"""
        
        score = 0
        
        # Company size complexity
        employee_count = company_profile.get("employee_count", 0)
        if employee_count > 1000:
            score += 2
        elif employee_count > 200:
            score += 1
        
        # Industry complexity
        industry = company_profile.get("industry", "")
        high_risk_industries = self.escalation_rules["complexity_indicators"]["high_risk_industry"]
        if any(risk_industry.lower() in industry.lower() for risk_industry in high_risk_industries):
            score += 2
        
        # Government contracts
        if company_profile.get("has_government_contracts", False):
            score += 2
        
        # Previous incidents
        if company_profile.get("previous_incidents") and len(company_profile["previous_incidents"]) > 0:
            score += 1
        
        # Assessment complexity
        frameworks_count = len(assessment_results.get("frameworks_assessed", []))
        if frameworks_count > 2:
            score += 1
        
        # Gap severity
        gaps = assessment_results.get("gaps_identified", [])
        critical_gaps = sum(1 for gap in gaps if gap.get("risk_level") == "CRITICAL")
        if critical_gaps > 0:
            score += 2
        
        return min(score, 10)  # Cap at 10
    
    def _estimate_escalation_cost(self, priority: EscalationPriority, complexity_score: int) -> float:
        """Estimate cost of expert escalation"""
        
        base_hours = {
            EscalationPriority.LOW: 2,
            EscalationPriority.MEDIUM: 4,
            EscalationPriority.HIGH: 6,
            EscalationPriority.CRITICAL: 8
        }
        
        complexity_multiplier = 1.0 + (complexity_score * 0.1)
        estimated_hours = base_hours[priority] * complexity_multiplier
        
        # Use average expert hourly rate
        average_rate = 475.0  # Average from expert network
        
        return estimated_hours * average_rate
    
    def _estimate_escalation_timeline(self, priority: EscalationPriority) -> str:
        """Estimate timeline for expert escalation"""
        
        timelines = {
            EscalationPriority.LOW: "2-3 business days",
            EscalationPriority.MEDIUM: "1-2 business days", 
            EscalationPriority.HIGH: "4-8 hours",
            EscalationPriority.CRITICAL: "1-2 hours"
        }
        
        return timelines[priority]
    
    async def create_escalation_request(self,
                                       company_profile: Dict[str, Any],
                                       assessment_results: Dict[str, Any],
                                       framework: str,
                                       escalation_decision: Dict[str, Any]) -> EscalationRequest:
        """Create formal escalation request for human expert"""
        
        request_id = f"ESC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
        priority = escalation_decision["priority"]
        due_date = datetime.now() + timedelta(hours=self._get_sla_hours(priority))
        
        escalation_request = EscalationRequest(
            request_id=request_id,
            company_profile=company_profile,
            assessment_results=assessment_results,
            framework=framework,
            confidence_score=assessment_results.get("overall_confidence", 0.0),
            complexity_indicators=escalation_decision["reasoning"],
            escalation_reason="; ".join(escalation_decision["reasoning"]),
            required_specialty=escalation_decision["required_specialty"],
            priority=priority,
            created_at=datetime.now(),
            due_date=due_date
        )
        
        # Route to appropriate expert
        assigned_expert = await self.route_to_expert(escalation_request)
        escalation_request.assigned_expert = assigned_expert
        escalation_request.status = EscalationStatus.ASSIGNED
        
        # Store escalation request
        self.active_escalations[request_id] = escalation_request
        
        logger.info(f"📤 Escalation request created: {request_id} → Expert: {assigned_expert}")
        
        return escalation_request
    
    async def route_to_expert(self, escalation_request: EscalationRequest) -> str:
        """Route escalation request to most appropriate available expert"""
        
        # Get experts with required specialty
        qualified_experts = [
            expert for expert in self.expert_network.values()
            if escalation_request.required_specialty in expert.specialties
            and expert.current_workload < expert.maximum_concurrent_cases
        ]
        
        if not qualified_experts:
            # Fallback to any available expert
            qualified_experts = [
                expert for expert in self.expert_network.values()
                if expert.current_workload < expert.maximum_concurrent_cases
            ]
        
        if not qualified_experts:
            logger.warning("⚠️ No available experts - escalation queued")
            return "QUEUED_NO_AVAILABLE_EXPERTS"
        
        # Route using workload balancing by default
        selected_expert = self.routing_algorithms["workload_balanced"](
            qualified_experts, escalation_request
        )
        
        # Update expert workload
        selected_expert.current_workload += 1
        
        return selected_expert.expert_id
    
    def _route_by_workload(self, experts: List[ExpertProfile], 
                          request: EscalationRequest) -> ExpertProfile:
        """Route to expert with lowest current workload"""
        return min(experts, key=lambda e: e.current_workload)
    
    def _route_by_expertise(self, experts: List[ExpertProfile],
                           request: EscalationRequest) -> ExpertProfile:
        """Route to expert with best specialty match"""
        # Prioritize exact specialty match
        exact_matches = [e for e in experts if request.required_specialty in e.specialties]
        if exact_matches:
            return min(exact_matches, key=lambda e: e.current_workload)
        return min(experts, key=lambda e: e.current_workload)
    
    def _route_by_cost(self, experts: List[ExpertProfile],
                      request: EscalationRequest) -> ExpertProfile:
        """Route to most cost-effective expert"""
        return min(experts, key=lambda e: e.cost_per_hour)
    
    def _route_by_sla(self, experts: List[ExpertProfile],
                     request: EscalationRequest) -> ExpertProfile:
        """Route to expert with best SLA for request priority"""
        return min(experts, key=lambda e: e.response_time_sla.get(request.priority, 999))
    
    def _get_sla_hours(self, priority: EscalationPriority) -> int:
        """Get SLA hours for priority level"""
        sla_hours = {
            EscalationPriority.CRITICAL: 2,
            EscalationPriority.HIGH: 8,
            EscalationPriority.MEDIUM: 24,
            EscalationPriority.LOW: 48
        }
        return sla_hours[priority]
    
    def get_escalation_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of escalation request"""
        
        escalation = self.active_escalations.get(request_id)
        if not escalation:
            return None
        
        return {
            "request_id": escalation.request_id,
            "status": escalation.status.value,
            "assigned_expert": escalation.assigned_expert,
            "priority": escalation.priority.value,
            "created_at": escalation.created_at.isoformat(),
            "due_date": escalation.due_date.isoformat(),
            "days_remaining": (escalation.due_date - datetime.now()).days,
            "expert_response_available": escalation.expert_response is not None
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get escalation system performance metrics"""
        
        total_experts = len(self.expert_network)
        available_experts = sum(1 for e in self.expert_network.values() 
                              if e.current_workload < e.maximum_concurrent_cases)
        
        active_count = len(self.active_escalations)
        completed_count = len([e for e in self.escalation_history if e.status == EscalationStatus.COMPLETED])
        
        return {
            "expert_network": {
                "total_experts": total_experts,
                "available_experts": available_experts,
                "utilization_rate": ((total_experts - available_experts) / total_experts * 100) if total_experts > 0 else 0
            },
            "escalations": {
                "active_requests": active_count,
                "completed_requests": completed_count,
                "average_resolution_time": "Calculated in production",
                "expert_satisfaction_rate": "Calculated in production"
            },
            "system_health": {
                "escalation_system": "Operational",
                "expert_availability": "Good" if available_experts > 0 else "Limited",
                "response_time_compliance": "Monitored in production"
            }
        }