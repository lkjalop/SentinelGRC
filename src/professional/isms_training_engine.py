"""
ISMS Training Engine for Cerberus AI
=====================================
Transforms ISMS training documentation into actionable agent knowledge
and professional report generation capabilities.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class ISMSGuidance:
    """ISMS guidance structure for agents"""
    topic: str
    agent_focus_areas: List[str]
    human_expertise_required: List[str]
    assessment_criteria: List[str]
    professional_language: str
    risk_indicators: List[str]

@dataclass
class ComplianceReportSection:
    """Professional report section"""
    section_title: str
    content: str
    recommendations: List[str]
    confidence_level: str
    expert_review_required: bool

class ISMSTrainingEngine:
    """
    ISMS Training Engine that teaches agents professional compliance language
    and report generation standards.
    """
    
    def __init__(self):
        self.isms_knowledge = self._load_isms_training()
        self.professional_templates = self._initialize_templates()
        self.assessment_frameworks = self._initialize_assessment_frameworks()
        
        logger.info("✅ ISMS Training Engine initialized")
    
    def _load_isms_training(self) -> Dict[str, ISMSGuidance]:
        """Load ISMS training knowledge from documentation"""
        
        # Core ISMS concepts that agents must understand
        isms_guidance = {
            "policy_framework": ISMSGuidance(
                topic="Information Security Policy Framework",
                agent_focus_areas=[
                    "Policy document completeness",
                    "Version control evidence", 
                    "Management approval signatures",
                    "Distribution and awareness records"
                ],
                human_expertise_required=[
                    "Policy effectiveness assessment",
                    "Business alignment validation",
                    "Cultural adoption evaluation"
                ],
                assessment_criteria=[
                    "Policies are documented and current",
                    "Clear ownership and accountability",
                    "Regular review and update cycles",
                    "Evidence of operational application"
                ],
                professional_language="The organization's information security policy framework provides the foundational governance structure, establishing clear security intentions and management commitments that guide all security-related activities.",
                risk_indicators=[
                    "Outdated policy documents",
                    "Lack of management approval",
                    "Unclear accountability structures",
                    "No evidence of policy application"
                ]
            ),
            
            "risk_management": ISMSGuidance(
                topic="Risk Management Processes",
                agent_focus_areas=[
                    "Risk register completeness",
                    "Risk assessment methodology documentation",
                    "Treatment plan implementation status",
                    "Risk monitoring and reporting schedules"
                ],
                human_expertise_required=[
                    "Risk appetite interpretation",
                    "Business impact assessment",
                    "Treatment option evaluation",
                    "Residual risk acceptance decisions"
                ],
                assessment_criteria=[
                    "Systematic risk identification process",
                    "Consistent risk assessment methodology",
                    "Appropriate risk treatment measures",
                    "Regular risk monitoring and review"
                ],
                professional_language="The organization maintains a comprehensive risk management program that systematically identifies, assesses, treats, and monitors information security risks in alignment with business objectives and risk appetite.",
                risk_indicators=[
                    "Incomplete risk assessments",
                    "Outdated risk registers", 
                    "Unclear treatment responsibilities",
                    "No evidence of risk monitoring"
                ]
            ),
            
            "control_implementation": ISMSGuidance(
                topic="Security Control Implementation",
                agent_focus_areas=[
                    "Control implementation evidence",
                    "Control effectiveness testing results",
                    "Exception management processes",
                    "Control monitoring and reporting"
                ],
                human_expertise_required=[
                    "Control design adequacy",
                    "Operating effectiveness evaluation",
                    "Business process integration",
                    "Control optimization recommendations"
                ],
                assessment_criteria=[
                    "Controls are properly designed",
                    "Controls operate effectively",
                    "Controls are monitored regularly",
                    "Control deficiencies are addressed"
                ],
                professional_language="Security controls are implemented comprehensively across technical, administrative, and physical domains, with regular monitoring to ensure continued effectiveness in mitigating identified risks.",
                risk_indicators=[
                    "Ineffective control design",
                    "Control implementation gaps",
                    "Lack of control monitoring",
                    "Unaddressed control deficiencies"
                ]
            ),
            
            "continuous_improvement": ISMSGuidance(
                topic="Continuous Improvement Mechanisms", 
                agent_focus_areas=[
                    "Internal audit program evidence",
                    "Management review documentation",
                    "Corrective action tracking",
                    "Performance metrics and trends"
                ],
                human_expertise_required=[
                    "Audit program adequacy",
                    "Management review effectiveness",
                    "Improvement opportunity identification",
                    "ISMS maturity assessment"
                ],
                assessment_criteria=[
                    "Regular internal audits conducted",
                    "Management reviews are effective",
                    "Corrective actions are timely",
                    "Continuous improvement is evident"
                ],
                professional_language="The organization demonstrates commitment to continuous improvement through systematic internal auditing, regular management reviews, and timely corrective actions that enhance the overall effectiveness of the ISMS.",
                risk_indicators=[
                    "Irregular audit schedules",
                    "Ineffective management reviews",
                    "Delayed corrective actions",
                    "No improvement evidence"
                ]
            )
        }
        
        return isms_guidance
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize professional report templates"""
        
        return {
            "executive_summary": """
**Executive Summary**

This compliance assessment provides a comprehensive evaluation of {company_name}'s information security management system against applicable regulatory frameworks. The assessment was conducted using automated analysis combined with professional expertise to ensure accuracy and completeness.

**Key Findings:**
• Overall compliance score: {compliance_score}%
• Frameworks assessed: {frameworks_assessed}
• Critical gaps identified: {critical_gaps}
• Risk level: {risk_level}

**Management Attention Required:**
{management_recommendations}

**Confidence Level:** {confidence_level}
**Assessment Date:** {assessment_date}
""",
            
            "framework_assessment": """
**{framework_name} Compliance Assessment**

**Scope and Methodology:**
This assessment evaluates {company_name}'s compliance with {framework_name} requirements using a risk-based approach that combines automated analysis with professional judgment.

**Current Status:**
• Implementation Status: {implementation_status}
• Control Effectiveness: {control_effectiveness} 
• Compliance Percentage: {compliance_percentage}%
• Risk Rating: {risk_rating}

**Identified Gaps:**
{gap_analysis}

**Recommendations:**
{recommendations}

**Resource Requirements:**
{resource_requirements}
""",
            
            "risk_assessment": """
**Risk Assessment Summary**

**Risk Profile:**
The organization's current risk profile indicates {risk_profile_summary}. Key risk factors include:

{risk_factors}

**Risk Treatment:**
{risk_treatment_summary}

**Residual Risk:**
Following implementation of recommended controls, residual risk is assessed as {residual_risk_level}.

**Management Decisions Required:**
{management_decisions}
"""
        }
    
    def _initialize_assessment_frameworks(self) -> Dict[str, Dict]:
        """Initialize assessment frameworks with ISMS alignment"""
        
        return {
            "essential8": {
                "isms_alignment": "Application Control, Patch Management, Security Configuration",
                "assessment_approach": "Technical control implementation with policy framework validation",
                "professional_context": "Essential Eight controls form the foundation of cyber resilience"
            },
            "privacy_act": {
                "isms_alignment": "Privacy Management, Data Protection, Breach Management", 
                "assessment_approach": "Privacy framework assessment with ISMS integration",
                "professional_context": "Privacy compliance requires systematic data protection management"
            },
            "apra_cps234": {
                "isms_alignment": "Information Security, Operational Risk, Third Party Risk",
                "assessment_approach": "Risk-based assessment aligned with APRA expectations",
                "professional_context": "CPS 234 mandates comprehensive information security capability"
            },
            "nist_csf": {
                "isms_alignment": "Cybersecurity Framework Functions across ISMS lifecycle",
                "assessment_approach": "Function-based assessment with maturity evaluation", 
                "professional_context": "NIST CSF provides structured cybersecurity risk management"
            }
        }
    
    def train_agent_for_framework(self, framework: str, agent_capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """Train an agent with ISMS knowledge for specific framework"""
        
        framework_info = self.assessment_frameworks.get(framework, {})
        
        training_enhancement = {
            "professional_language_patterns": self._get_professional_language_patterns(),
            "isms_assessment_criteria": self._get_isms_criteria_for_framework(framework),
            "report_generation_guidelines": self._get_report_guidelines(),
            "escalation_triggers": self._get_escalation_triggers(),
            "confidence_calibration": self._get_confidence_guidelines()
        }
        
        logger.info(f"✅ Agent trained for {framework} with ISMS professional standards")
        return training_enhancement
    
    def _get_professional_language_patterns(self) -> List[str]:
        """Professional language patterns for compliance reporting"""
        
        return [
            "Implementation of [control] demonstrates [evidence] consistent with [standard] requirements",
            "The organization maintains [process] that provides [assurance] regarding [objective]",
            "Assessment indicates [finding] which [impact] the overall [area] posture",
            "Management attention is required to [action] in order to [outcome]",
            "Current controls provide [level] assurance regarding [risk area]",
            "Recommendations focus on [priority areas] to enhance [capability]"
        ]
    
    def _get_isms_criteria_for_framework(self, framework: str) -> Dict[str, List[str]]:
        """ISMS-aligned assessment criteria for specific framework"""
        
        base_criteria = {
            "policy_framework": [
                "Documented policies addressing framework requirements",
                "Management approval and periodic review",
                "Communication and awareness programs",
                "Operational implementation evidence"
            ],
            "risk_management": [
                "Framework-specific risks identified and assessed", 
                "Risk treatment aligned with business objectives",
                "Regular risk monitoring and reporting",
                "Risk appetite alignment"
            ],
            "control_implementation": [
                "Framework controls properly implemented",
                "Control effectiveness regularly tested",
                "Control gaps identified and addressed",
                "Integration with broader control environment"
            ],
            "continuous_improvement": [
                "Framework compliance regularly assessed",
                "Improvement opportunities identified",
                "Corrective actions implemented timely",
                "Management oversight and review"
            ]
        }
        
        return base_criteria
    
    def _get_report_guidelines(self) -> Dict[str, str]:
        """Professional report generation guidelines"""
        
        return {
            "tone": "Professional, objective, constructive",
            "structure": "Executive summary, detailed findings, recommendations, appendices",
            "language": "Clear, precise, avoiding jargon while maintaining professional standards",
            "evidence": "Specific, verifiable, linked to assessment activities",
            "recommendations": "Actionable, prioritized, resource-conscious",
            "risk_framing": "Business-focused, contextualized, forward-looking"
        }
    
    def _get_escalation_triggers(self) -> List[str]:
        """Situations requiring human expert escalation"""
        
        return [
            "Complex regulatory interpretation required",
            "Significant business impact assessment needed",
            "Multi-framework compliance conflicts identified",
            "High-risk findings with strategic implications",
            "Unusual control environments requiring expert judgment",
            "Assessment confidence below professional threshold"
        ]
    
    def _get_confidence_guidelines(self) -> Dict[str, str]:
        """Confidence level calibration guidelines"""
        
        return {
            "high_confidence_90_plus": "Clear evidence, standard control environment, minimal interpretation required",
            "medium_confidence_70_89": "Good evidence with some gaps, professional judgment applied",
            "low_confidence_50_69": "Limited evidence, significant professional judgment required",
            "escalation_required_below_50": "Insufficient evidence for professional opinion, expert review required"
        }
    
    def generate_professional_assessment(self, 
                                       company_profile: Dict[str, Any],
                                       assessment_results: Dict[str, Any],
                                       framework: str) -> ComplianceReportSection:
        """Generate professional assessment using ISMS training"""
        
        isms_guidance = self.isms_knowledge.get("risk_management")  # Default to risk management
        framework_info = self.assessment_frameworks.get(framework, {})
        
        # Professional assessment content
        professional_content = f"""
**{framework.upper()} Compliance Assessment**

**Organization:** {company_profile.get('company_name', 'Unknown')}
**Industry:** {company_profile.get('industry', 'Unknown')}
**Assessment Framework:** {framework_info.get('professional_context', framework)}

**ISMS Alignment:**
{framework_info.get('isms_alignment', 'Standard compliance assessment')}

**Assessment Approach:**
{framework_info.get('assessment_approach', 'Risk-based assessment methodology')}

**Key Findings:**
{self._format_findings(assessment_results)}

**Professional Opinion:**
{self._generate_professional_opinion(assessment_results, isms_guidance)}

**Risk Considerations:**
{self._format_risk_considerations(assessment_results)}
"""
        
        # Determine if expert review is required
        confidence = assessment_results.get('overall_confidence', 0.0)
        expert_review_required = confidence < 0.7 or len(assessment_results.get('gaps_identified', [])) > 5
        
        return ComplianceReportSection(
            section_title=f"{framework.upper()} Professional Assessment",
            content=professional_content,
            recommendations=self._generate_professional_recommendations(assessment_results, isms_guidance),
            confidence_level=self._determine_confidence_level(confidence),
            expert_review_required=expert_review_required
        )
    
    def _format_findings(self, assessment_results: Dict[str, Any]) -> str:
        """Format findings in professional language"""
        
        compliance_score = assessment_results.get('overall_confidence', 0.0) * 100
        gaps = assessment_results.get('gaps_identified', [])
        
        findings = []
        
        if compliance_score >= 80:
            findings.append("• The organization demonstrates strong compliance posture with established control frameworks")
        elif compliance_score >= 60:
            findings.append("• The organization maintains adequate compliance with opportunities for enhancement")
        else:
            findings.append("• The organization requires significant improvement to achieve acceptable compliance levels")
        
        if gaps:
            findings.append(f"• {len(gaps)} control gaps identified requiring management attention")
        
        return "\n".join(findings)
    
    def _generate_professional_opinion(self, assessment_results: Dict[str, Any], 
                                     isms_guidance: ISMSGuidance) -> str:
        """Generate professional opinion using ISMS knowledge"""
        
        confidence = assessment_results.get('overall_confidence', 0.0)
        
        if confidence >= 0.8:
            return isms_guidance.professional_language + " Current implementation provides reasonable assurance regarding compliance objectives."
        elif confidence >= 0.6:
            return isms_guidance.professional_language + " Implementation requires enhancement to provide adequate assurance."
        else:
            return "Professional assessment indicates significant gaps requiring comprehensive remediation program."
    
    def _format_risk_considerations(self, assessment_results: Dict[str, Any]) -> str:
        """Format risk considerations professionally"""
        
        risk_level = assessment_results.get('risk_level', 'MEDIUM')
        
        risk_statements = {
            'HIGH': "• Significant risk exposure requiring immediate management attention and resource allocation",
            'MEDIUM': "• Moderate risk exposure that should be addressed through planned improvement initiatives", 
            'LOW': "• Limited risk exposure with standard monitoring and continuous improvement processes"
        }
        
        return risk_statements.get(risk_level, risk_statements['MEDIUM'])
    
    def _generate_professional_recommendations(self, assessment_results: Dict[str, Any],
                                             isms_guidance: ISMSGuidance) -> List[str]:
        """Generate professional recommendations"""
        
        recommendations = []
        gaps = assessment_results.get('gaps_identified', [])
        
        if gaps:
            recommendations.append("Develop comprehensive remediation program to address identified control gaps")
            recommendations.append("Implement regular monitoring and reporting to track improvement progress")
        
        recommendations.append("Conduct regular management review to ensure ongoing effectiveness")
        recommendations.append("Consider independent validation of control implementation and effectiveness")
        
        return recommendations
    
    def _determine_confidence_level(self, confidence: float) -> str:
        """Determine professional confidence level"""
        
        if confidence >= 0.9:
            return "High Confidence"
        elif confidence >= 0.7:
            return "Medium Confidence"
        elif confidence >= 0.5:
            return "Low Confidence"
        else:
            return "Expert Review Required"
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get summary of ISMS training capabilities"""
        
        return {
            "isms_knowledge_areas": len(self.isms_knowledge),
            "professional_templates": len(self.professional_templates),
            "assessment_frameworks": list(self.assessment_frameworks.keys()),
            "training_status": "Active",
            "capabilities": [
                "Professional language generation",
                "ISMS-aligned assessment criteria",
                "Risk-based reporting",
                "Expert escalation triggers",
                "Confidence calibration"
            ]
        }


# Integration function for main system
def integrate_isms_training_with_agents(agents_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate ISMS training with existing agents"""
    
    training_engine = ISMSTrainingEngine()
    enhanced_agents = {}
    
    for agent_name, agent in agents_dict.items():
        # Determine framework for agent
        framework_mapping = {
            "essential_eight": "essential8",
            "privacy_act": "privacy_act", 
            "apra_cps234": "apra_cps234",
            "nist_csf": "nist_csf"
        }
        
        framework = framework_mapping.get(agent_name, agent_name)
        
        # Train agent with ISMS knowledge
        if hasattr(agent, '__dict__'):
            training_enhancement = training_engine.train_agent_for_framework(
                framework, agent.__dict__
            )
            
            # Add ISMS capabilities to agent
            agent.isms_training = training_enhancement
            agent.training_engine = training_engine
        
        enhanced_agents[agent_name] = agent
    
    logger.info(f"✅ ISMS training integrated with {len(enhanced_agents)} agents")
    return enhanced_agents