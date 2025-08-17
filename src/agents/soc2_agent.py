"""
SOC 2 Compliance Agent
======================
Implements SOC 2 Type I and Type II compliance assessment
based on the 5 Trust Service Criteria.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SOC2Control:
    """SOC 2 control definition"""
    control_id: str
    title: str
    description: str
    trust_service_criteria: str  # Security, Availability, Processing Integrity, Confidentiality, Privacy
    type: str  # Type I (design) or Type II (operating effectiveness)
    implementation_guidance: str
    evidence_requirements: List[str]

class SOC2Agent:
    """
    SOC 2 compliance assessment agent
    Covers all 5 Trust Service Criteria
    """
    
    def __init__(self):
        self.platform_name = "SOC 2 Compliance Agent"
        self.version = "1.0.0"
        self.trust_criteria = self._initialize_trust_criteria()
        self.controls = self._initialize_soc2_controls()
        
        logger.info("✅ SOC 2 compliance agent initialized")
    
    def _initialize_trust_criteria(self) -> Dict[str, str]:
        """Initialize the 5 Trust Service Criteria"""
        return {
            "security": "Protection against unauthorized access (logical and physical)",
            "availability": "System availability for operation and use",
            "processing_integrity": "System processing is complete, valid, accurate, timely, and authorized",
            "confidentiality": "Information designated as confidential is protected",
            "privacy": "Personal information is collected, used, retained, disclosed, and disposed of in conformity with commitments"
        }
    
    def _initialize_soc2_controls(self) -> Dict[str, SOC2Control]:
        """Initialize SOC 2 controls mapping"""
        return {
            "CC1.1": SOC2Control(
                control_id="CC1.1",
                title="Control Environment - Integrity and Ethical Values",
                description="The entity demonstrates a commitment to integrity and ethical values",
                trust_service_criteria="security",
                type="Type I",
                implementation_guidance="Establish code of conduct, ethics policies, and tone at the top",
                evidence_requirements=["Code of conduct", "Ethics training", "Policy documentation"]
            ),
            "CC1.2": SOC2Control(
                control_id="CC1.2", 
                title="Board Independence and Oversight",
                description="The board demonstrates independence and oversight of internal controls",
                trust_service_criteria="security",
                type="Type I",
                implementation_guidance="Independent board members, regular oversight meetings",
                evidence_requirements=["Board charter", "Meeting minutes", "Independence documentation"]
            ),
            "CC2.1": SOC2Control(
                control_id="CC2.1",
                title="Communication of Internal Control Information",
                description="Management communicates information about the internal control system",
                trust_service_criteria="security", 
                type="Type I",
                implementation_guidance="Regular communication of control responsibilities and changes",
                evidence_requirements=["Communication plans", "Training records", "Policy updates"]
            ),
            "CC3.1": SOC2Control(
                control_id="CC3.1",
                title="Risk Assessment Process",
                description="Entity specifies objectives with sufficient clarity to enable identification of risks",
                trust_service_criteria="security",
                type="Type I", 
                implementation_guidance="Define clear objectives and risk identification processes",
                evidence_requirements=["Risk register", "Objective documentation", "Risk assessment procedures"]
            ),
            "CC4.1": SOC2Control(
                control_id="CC4.1",
                title="Monitoring Activities - Ongoing Evaluations",
                description="The entity selects, develops, and performs ongoing evaluations",
                trust_service_criteria="security",
                type="Type II",
                implementation_guidance="Continuous monitoring, regular control testing",
                evidence_requirements=["Monitoring procedures", "Test results", "Remediation tracking"]
            ),
            "CC5.1": SOC2Control(
                control_id="CC5.1",
                title="Information and Communication",
                description="Entity obtains or generates and uses relevant, quality information",
                trust_service_criteria="security",
                type="Type I",
                implementation_guidance="Establish information quality standards and communication channels",
                evidence_requirements=["Data quality procedures", "Communication logs", "Information systems documentation"]
            ),
            "CC6.1": SOC2Control(
                control_id="CC6.1",
                title="Logical and Physical Access Controls",
                description="Entity implements logical and physical access controls",
                trust_service_criteria="security",
                type="Type II", 
                implementation_guidance="Multi-factor authentication, access reviews, physical security",
                evidence_requirements=["Access control lists", "MFA implementation", "Physical security logs"]
            ),
            "CC6.2": SOC2Control(
                control_id="CC6.2",
                title="Transmission and Disposal of Information",
                description="Entity implements controls for transmission and disposal of information",
                trust_service_criteria="security",
                type="Type II",
                implementation_guidance="Encryption in transit and at rest, secure disposal procedures",
                evidence_requirements=["Encryption standards", "Disposal logs", "Transmission logs"]
            ),
            "CC7.1": SOC2Control(
                control_id="CC7.1", 
                title="System Operations",
                description="Entity implements controls to ensure system operations",
                trust_service_criteria="security",
                type="Type II",
                implementation_guidance="Change management, system monitoring, capacity planning",
                evidence_requirements=["Change logs", "Monitoring alerts", "Capacity reports"]
            ),
            "A1.1": SOC2Control(
                control_id="A1.1",
                title="Availability - System Availability",
                description="Entity maintains system availability commitments",
                trust_service_criteria="availability",
                type="Type II",
                implementation_guidance="Redundancy, failover procedures, uptime monitoring",
                evidence_requirements=["Uptime reports", "Incident logs", "Disaster recovery testing"]
            ),
            "PI1.1": SOC2Control(
                control_id="PI1.1",
                title="Processing Integrity - Data Processing",
                description="Entity implements controls for complete and accurate processing",
                trust_service_criteria="processing_integrity", 
                type="Type II",
                implementation_guidance="Data validation, processing controls, error handling",
                evidence_requirements=["Validation procedures", "Error logs", "Processing reports"]
            ),
            "C1.1": SOC2Control(
                control_id="C1.1",
                title="Confidentiality - Information Classification",
                description="Entity implements controls to protect confidential information",
                trust_service_criteria="confidentiality",
                type="Type II",
                implementation_guidance="Data classification, encryption, access controls",
                evidence_requirements=["Classification procedures", "Encryption implementation", "Access logs"]
            ),
            "P1.1": SOC2Control(
                control_id="P1.1",
                title="Privacy - Collection and Use",
                description="Entity implements controls for privacy information collection and use",
                trust_service_criteria="privacy",
                type="Type II", 
                implementation_guidance="Privacy notices, consent management, data use controls",
                evidence_requirements=["Privacy notices", "Consent logs", "Data use policies"]
            )
        }
    
    async def assess_compliance(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess SOC 2 compliance for a company"""
        
        logger.info(f"🔍 Starting SOC 2 assessment for {company_profile.get('company_name', 'Unknown')}")
        
        assessment_results = {
            "assessment_date": datetime.now().isoformat(),
            "framework": "SOC 2",
            "company_profile": company_profile,
            "trust_criteria_assessment": {},
            "control_assessment": {},
            "overall_compliance": 0.0,
            "gaps_identified": [],
            "recommendations": [],
            "readiness_level": "Not Ready",
            "estimated_timeline": "12-18 months"
        }
        
        # Assess each trust service criteria
        for criteria_name, criteria_desc in self.trust_criteria.items():
            criteria_assessment = self._assess_trust_criteria(criteria_name, company_profile)
            assessment_results["trust_criteria_assessment"][criteria_name] = criteria_assessment
        
        # Assess individual controls
        for control_id, control in self.controls.items():
            control_assessment = self._assess_control(control, company_profile)
            assessment_results["control_assessment"][control_id] = control_assessment
        
        # Calculate overall compliance
        total_controls = len(self.controls)
        compliant_controls = sum(1 for c in assessment_results["control_assessment"].values() if c["status"] == "compliant")
        assessment_results["overall_compliance"] = (compliant_controls / total_controls) * 100
        
        # Determine readiness level
        if assessment_results["overall_compliance"] >= 80:
            assessment_results["readiness_level"] = "Audit Ready"
            assessment_results["estimated_timeline"] = "3-6 months"
        elif assessment_results["overall_compliance"] >= 60:
            assessment_results["readiness_level"] = "Partially Ready" 
            assessment_results["estimated_timeline"] = "6-12 months"
        else:
            assessment_results["readiness_level"] = "Not Ready"
            assessment_results["estimated_timeline"] = "12-18 months"
        
        # Generate recommendations
        assessment_results["recommendations"] = self._generate_recommendations(assessment_results)
        
        logger.info(f"✅ SOC 2 assessment complete - {assessment_results['overall_compliance']:.1f}% compliant")
        
        return assessment_results
    
    def _assess_trust_criteria(self, criteria_name: str, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess a specific trust service criteria"""
        
        # Get relevant controls for this criteria
        relevant_controls = [c for c in self.controls.values() if c.trust_service_criteria == criteria_name]
        
        # Simple assessment based on company characteristics
        score = 50  # Base score
        
        # Industry-specific adjustments
        industry = company_profile.get("industry", "").lower()
        if criteria_name == "privacy" and industry in ["healthcare", "finance"]:
            score += 20
        if criteria_name == "confidentiality" and industry in ["technology", "finance"]:
            score += 15
        if criteria_name == "availability" and industry == "technology":
            score += 20
        
        # Company size adjustments
        employee_count = company_profile.get("employee_count", 0)
        if employee_count > 100:
            score += 10
        if employee_count > 500:
            score += 10
        
        # Ensure score is within bounds
        score = min(100, max(0, score))
        
        return {
            "criteria": criteria_name,
            "score": score,
            "status": "compliant" if score >= 75 else "non_compliant",
            "relevant_controls": len(relevant_controls),
            "description": self.trust_criteria[criteria_name]
        }
    
    def _assess_control(self, control: SOC2Control, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess implementation of a specific SOC 2 control"""
        
        # Simple rule-based assessment
        score = 40  # Base score
        
        industry = company_profile.get("industry", "").lower()
        employee_count = company_profile.get("employee_count", 0)
        
        # Control-specific logic
        if "access" in control.title.lower():
            if employee_count > 50:
                score += 30
        elif "monitoring" in control.title.lower():
            if industry == "technology":
                score += 25
        elif "risk" in control.title.lower():
            if industry in ["finance", "healthcare"]:
                score += 35
        
        # Type II controls are generally harder to implement
        if control.type == "Type II":
            score -= 10
        
        # Ensure score is within bounds
        score = min(100, max(0, score))
        
        return {
            "control_id": control.control_id,
            "title": control.title,
            "status": "compliant" if score >= 70 else "non_compliant",
            "score": score,
            "type": control.type,
            "trust_criteria": control.trust_service_criteria,
            "evidence_requirements": control.evidence_requirements,
            "implementation_guidance": control.implementation_guidance
        }
    
    def _generate_recommendations(self, assessment_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate SOC 2 implementation recommendations"""
        
        recommendations = []
        
        # Find non-compliant controls
        non_compliant = [
            c for c in assessment_results["control_assessment"].values() 
            if c["status"] == "non_compliant"
        ]
        
        # Prioritize by trust criteria
        criteria_priority = ["security", "availability", "processing_integrity", "confidentiality", "privacy"]
        
        for criteria in criteria_priority:
            criteria_controls = [c for c in non_compliant if c["trust_criteria"] == criteria]
            
            for control in criteria_controls[:3]:  # Top 3 per criteria
                recommendations.append({
                    "control_id": control["control_id"],
                    "title": control["title"],
                    "priority": "HIGH" if control["trust_criteria"] == "security" else "MEDIUM",
                    "effort": "HIGH" if control["type"] == "Type II" else "MEDIUM",
                    "timeline": "3-6 months" if control["type"] == "Type I" else "6-12 months",
                    "guidance": control["implementation_guidance"],
                    "trust_criteria": control["trust_criteria"]
                })
        
        return recommendations[:10]  # Limit to top 10
    
    def get_framework_info(self) -> Dict[str, Any]:
        """Get SOC 2 framework information"""
        return {
            "name": "SOC 2",
            "version": "2017",
            "description": "System and Organization Controls for Service Organizations",
            "scope": "Service organizations providing services to user entities",
            "trust_criteria": list(self.trust_criteria.keys()),
            "total_controls": len(self.controls),
            "audit_types": ["Type I (Design)", "Type II (Operating Effectiveness)"],
            "typical_audit_duration": "3-6 months",
            "required_evidence": "Policies, procedures, testing evidence, management representations"
        }