"""
Enterprise Liability Protection & Human Escalation Framework
===========================================================
Comprehensive system to minimize legal liability and ensure proper human oversight.
Designed for SaaS deployment with clear responsibility boundaries.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class LiabilityLevel(Enum):
    """Classification of liability exposure levels"""
    MINIMAL = "minimal"        # Automated recommendations only
    MODERATE = "moderate"      # Human review recommended  
    HIGH = "high"             # Human expert required
    CRITICAL = "critical"     # Legal counsel required

class EscalationType(Enum):
    """Types of human escalation required"""
    COMPLIANCE_EXPERT = "compliance_expert"
    LEGAL_COUNSEL = "legal_counsel"
    INDUSTRY_SPECIALIST = "industry_specialist"
    CLIENT_STAKEHOLDER = "client_stakeholder"
    REGULATORY_AUTHORITY = "regulatory_authority"

@dataclass
class LiabilityDisclaimer:
    """Comprehensive liability disclaimer for different scenarios"""
    scenario: str
    disclaimer_text: str
    legal_risk_level: LiabilityLevel
    required_acknowledgment: bool
    escalation_trigger: Optional[EscalationType] = None

class EnterpriseComplianceLiabilityManager:
    """
    Manages liability protection and human escalation workflows.
    Designed to minimize platform legal exposure while ensuring quality.
    """
    
    def __init__(self):
        self.disclaimers = self._initialize_disclaimers()
        self.escalation_rules = self._initialize_escalation_rules()
        self.audit_trail = []
        
    def _initialize_disclaimers(self) -> Dict[str, LiabilityDisclaimer]:
        """Initialize comprehensive liability disclaimers"""
        return {
            "general_platform": LiabilityDisclaimer(
                scenario="general_platform",
                disclaimer_text="""
🚨 IMPORTANT LEGAL DISCLAIMERS

SentinelGRC PLATFORM LIABILITY LIMITATIONS:

1. ASSESSMENT TOOL ONLY
   • This platform is a DECISION SUPPORT TOOL, not a compliance determination service
   • Results are RECOMMENDATIONS requiring expert human validation
   • No guarantee of regulatory compliance or accuracy

2. NO PROFESSIONAL ADVICE
   • Platform does NOT provide legal, accounting, or professional compliance advice
   • Users must engage qualified compliance professionals for final decisions
   • Platform operators disclaim all professional liability

3. CLIENT RESPONSIBILITY
   • Client is SOLELY responsible for:
     - Accuracy of information provided to platform
     - Validation of platform recommendations
     - Final compliance decisions and implementation
     - Regulatory reporting and certifications

4. DATA ACCURACY DISCLAIMER  
   • Platform relies on CLIENT-PROVIDED data and public information
   • No warranty on data accuracy, completeness, or currency
   • Client must verify all information independently

5. REGULATORY CHANGE RISK
   • Compliance requirements change frequently
   • Platform may not reflect latest regulatory updates
   • Client responsible for monitoring current requirements

6. LIMITATION OF LIABILITY
   • Platform liability limited to fees paid (if any)
   • No consequential, indirect, or punitive damages
   • Maximum liability: Lesser of $1,000 or subscription fees

BY USING THIS PLATFORM, USER ACKNOWLEDGES AND ACCEPTS ALL LIMITATIONS.
                """,
                legal_risk_level=LiabilityLevel.MODERATE,
                required_acknowledgment=True
            ),
            
            "high_risk_assessment": LiabilityDisclaimer(
                scenario="high_risk_assessment", 
                disclaimer_text="""
⚠️ HIGH-RISK COMPLIANCE ASSESSMENT DETECTED

MANDATORY HUMAN EXPERT REVIEW REQUIRED:

This assessment involves HIGH-RISK compliance areas requiring expert validation:
• Financial services regulation (APRA, NYDFS, GLBA)
• Healthcare data protection (HIPAA, PHI handling)  
• Critical infrastructure security (SOCI Act, CISA)
• Cross-border data transfers (GDPR Article 44-49)
• Government contractor requirements (CMMC, NIST 800-53)

PLATFORM CANNOT SUBSTITUTE FOR HUMAN EXPERTISE IN THESE AREAS.

Required Actions:
✅ Engage qualified compliance professional
✅ Validate ALL platform recommendations  
✅ Obtain independent legal/regulatory review
✅ Document professional validation in audit trail

PLATFORM DISCLAIMS ALL LIABILITY FOR HIGH-RISK ASSESSMENTS.
Expert human validation is CLIENT RESPONSIBILITY.
                """,
                legal_risk_level=LiabilityLevel.HIGH,
                required_acknowledgment=True,
                escalation_trigger=EscalationType.COMPLIANCE_EXPERT
            ),
            
            "data_sovereignty": LiabilityDisclaimer(
                scenario="data_sovereignty",
                disclaimer_text="""
🌍 CROSS-BORDER DATA COMPLIANCE NOTICE

DATA SOVEREIGNTY RESPONSIBILITY DISCLAIMER:

• Platform provides GENERAL guidance only on data location requirements
• Client SOLELY responsible for data sovereignty compliance
• Complex cross-border requirements require specialized legal advice

CLIENT MUST INDEPENDENTLY:
✅ Verify data residency requirements for their jurisdiction
✅ Ensure compliance with local data protection laws
✅ Obtain legal advice for cross-border data transfers
✅ Implement appropriate data governance controls

Platform operators accept NO LIABILITY for data sovereignty violations.
                """,
                legal_risk_level=LiabilityLevel.CRITICAL,
                required_acknowledgment=True,
                escalation_trigger=EscalationType.LEGAL_COUNSEL
            ),
            
            "international_demo": LiabilityDisclaimer(
                scenario="international_demo",
                disclaimer_text="""
🌏 INTERNATIONAL DEMO VERSION - LIMITED LIABILITY

DEMONSTRATION PURPOSES ONLY:
• This demo uses generalized compliance frameworks
• NOT customized for specific local requirements
• Results are ILLUSTRATIVE, not definitive

FOR PRODUCTION USE:
• Engage local compliance professionals
• Validate all recommendations against local law
• Obtain independent regulatory guidance

US/EU colleagues: This platform was designed for Australian compliance.
Framework adaptations are APPROXIMATIONS requiring expert validation.

PLATFORM ACCEPTS NO LIABILITY FOR INTERNATIONAL USE.
                """,
                legal_risk_level=LiabilityLevel.MODERATE, 
                required_acknowledgment=True
            )
        }
    
    def _initialize_escalation_rules(self) -> Dict[str, Dict]:
        """Define when human escalation is required"""
        return {
            "confidence_threshold": {
                "critical": 0.95,  # Above 95% = proceed with caution
                "high": 0.85,      # 85-95% = human review recommended  
                "moderate": 0.70,  # 70-85% = expert validation required
                "low": 0.70        # Below 70% = mandatory human review
            },
            
            "industry_triggers": {
                "banking": [EscalationType.COMPLIANCE_EXPERT, EscalationType.LEGAL_COUNSEL],
                "healthcare": [EscalationType.COMPLIANCE_EXPERT, EscalationType.INDUSTRY_SPECIALIST],
                "defense": [EscalationType.COMPLIANCE_EXPERT, EscalationType.REGULATORY_AUTHORITY],
                "critical_infrastructure": [EscalationType.COMPLIANCE_EXPERT],
                "government": [EscalationType.REGULATORY_AUTHORITY]
            },
            
            "framework_triggers": {
                "HIPAA": [EscalationType.COMPLIANCE_EXPERT, EscalationType.INDUSTRY_SPECIALIST],
                "APRA CPS 234": [EscalationType.COMPLIANCE_EXPERT, EscalationType.LEGAL_COUNSEL],
                "CMMC": [EscalationType.COMPLIANCE_EXPERT, EscalationType.REGULATORY_AUTHORITY],
                "GDPR": [EscalationType.LEGAL_COUNSEL],
                "SOX": [EscalationType.COMPLIANCE_EXPERT, EscalationType.LEGAL_COUNSEL]
            }
        }
    
    def assess_liability_risk(self, assessment_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess liability risk and determine required disclaimers/escalations"""
        
        risk_factors = []
        required_disclaimers = ["general_platform"]  # Always required
        required_escalations = []
        
        # Industry risk assessment
        industry = assessment_context.get("industry", "").lower()
        if industry in ["banking", "financial services", "healthcare", "defense"]:
            risk_factors.append(f"high_risk_industry_{industry}")
            required_disclaimers.append("high_risk_assessment")
            required_escalations.extend(self.escalation_rules["industry_triggers"].get(industry, []))
        
        # Framework risk assessment  
        frameworks = assessment_context.get("frameworks", [])
        high_risk_frameworks = ["HIPAA", "APRA CPS 234", "CMMC", "GDPR", "SOX"]
        for framework in frameworks:
            if framework in high_risk_frameworks:
                risk_factors.append(f"high_risk_framework_{framework}")
                required_disclaimers.append("high_risk_assessment")
                required_escalations.extend(self.escalation_rules["framework_triggers"].get(framework, []))
        
        # Cross-border data risk
        if assessment_context.get("cross_border_data", False):
            risk_factors.append("cross_border_data")
            required_disclaimers.append("data_sovereignty")
            required_escalations.append(EscalationType.LEGAL_COUNSEL)
        
        # International demo risk
        if assessment_context.get("international_demo", False):
            risk_factors.append("international_demo")
            required_disclaimers.append("international_demo")
        
        # Calculate overall risk level
        if len(risk_factors) >= 3:
            overall_risk = LiabilityLevel.CRITICAL
        elif len(risk_factors) >= 2:
            overall_risk = LiabilityLevel.HIGH
        elif len(risk_factors) >= 1:
            overall_risk = LiabilityLevel.MODERATE
        else:
            overall_risk = LiabilityLevel.MINIMAL
        
        return {
            "overall_risk_level": overall_risk,
            "risk_factors": risk_factors,
            "required_disclaimers": list(set(required_disclaimers)),
            "required_escalations": list(set(required_escalations)),
            "liability_score": len(risk_factors) * 25,  # 0-100 scale
            "human_review_mandatory": overall_risk.value in ["high", "critical"]
        }
    
    def generate_liability_report(self, assessment_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive liability protection report"""
        
        risk_assessment = self.assess_liability_risk(assessment_context)
        
        # Generate disclaimer text
        disclaimer_texts = []
        for disclaimer_key in risk_assessment["required_disclaimers"]:
            if disclaimer_key in self.disclaimers:
                disclaimer_texts.append(self.disclaimers[disclaimer_key].disclaimer_text)
        
        # Create audit trail entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "assessment_id": assessment_context.get("assessment_id", "unknown"),
            "client_info": assessment_context.get("client_info", {}),
            "risk_assessment": risk_assessment,
            "disclaimers_shown": risk_assessment["required_disclaimers"],
            "user_acknowledgment": False,  # To be updated when user acknowledges
            "escalations_triggered": risk_assessment["required_escalations"]
        }
        
        self.audit_trail.append(audit_entry)
        
        return {
            "liability_protection": {
                "risk_level": risk_assessment["overall_risk_level"].value,
                "disclaimers": disclaimer_texts,
                "escalation_requirements": risk_assessment["required_escalations"],
                "human_review_required": risk_assessment["human_review_mandatory"],
                "audit_trail_id": len(self.audit_trail) - 1
            },
            "recommendations": self._generate_risk_mitigation_recommendations(risk_assessment)
        }
    
    def _generate_risk_mitigation_recommendations(self, risk_assessment: Dict) -> List[str]:
        """Generate recommendations to mitigate identified risks"""
        recommendations = []
        
        if risk_assessment["overall_risk_level"] == LiabilityLevel.CRITICAL:
            recommendations.extend([
                "🔴 CRITICAL: Mandatory legal counsel review before proceeding",
                "🔴 CRITICAL: Independent compliance expert validation required", 
                "🔴 CRITICAL: Client must provide written acknowledgment of limitations",
                "🔴 CRITICAL: All recommendations subject to professional override"
            ])
        
        elif risk_assessment["overall_risk_level"] == LiabilityLevel.HIGH:
            recommendations.extend([
                "🟠 HIGH: Compliance expert review strongly recommended",
                "🟠 HIGH: Independent validation of high-risk findings", 
                "🟠 HIGH: Client responsible for regulatory interpretation",
                "🟠 HIGH: Platform results are advisory only"
            ])
        
        if EscalationType.LEGAL_COUNSEL in risk_assessment["required_escalations"]:
            recommendations.append("⚖️ Legal counsel consultation required for regulatory interpretation")
            
        if EscalationType.REGULATORY_AUTHORITY in risk_assessment["required_escalations"]:
            recommendations.append("🏛️ Direct regulatory authority guidance recommended")
        
        recommendations.append("📋 Maintain comprehensive audit trail for all decisions")
        recommendations.append("🔄 Regular review of platform recommendations required")
        
        return recommendations

# Export for main application
def create_liability_manager() -> EnterpriseComplianceLiabilityManager:
    """Factory function to create liability manager"""
    return EnterpriseComplianceLiabilityManager()

if __name__ == "__main__":
    # Test the liability framework
    manager = EnterpriseComplianceLiabilityManager()
    
    # Test high-risk scenario
    test_context = {
        "assessment_id": "TEST-001",
        "industry": "banking",
        "frameworks": ["APRA CPS 234", "HIPAA"],
        "cross_border_data": True,
        "international_demo": False,
        "client_info": {"name": "Test Bank", "region": "australia"}
    }
    
    report = manager.generate_liability_report(test_context)
    print("Liability Report Generated:")
    print(f"Risk Level: {report['liability_protection']['risk_level']}")
    print(f"Escalations Required: {len(report['liability_protection']['escalation_requirements'])}")
    print(f"Human Review Required: {report['liability_protection']['human_review_required']}")
    print(f"Recommendations: {len(report['recommendations'])}")