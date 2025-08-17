"""
Australian Compliance Agents - Extended Framework Support
=========================================================
Additional agents for Privacy Act, APRA CPS 234, and SOCI Act compliance.
These complement the existing Essential 8 agent.
"""

import asyncio
import json
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from abc import ABC

# Import from core types to avoid circular dependencies
from ..core.core_types import (
    BaseComplianceAgent, CompanyProfile, Config,
    ConfidenceLevel, EscalationType, AssessmentResult,
    AssessmentStatus, RiskLevel, get_risk_level
)

# ============================================================================
# PRIVACY ACT 1988 AGENT
# ============================================================================

class PrivacyActAgent(BaseComplianceAgent):
    """
    Specialized agent for Privacy Act 1988 compliance assessment.
    Focuses on Australian Privacy Principles (APP) 1-13.
    """
    
    def __init__(self):
        super().__init__(
            name="PrivacyActAgent",
            expertise="Privacy Act 1988 and Australian Privacy Principles",
            framework="Privacy Act 1988"  # For shared knowledge graph
        )
        self.privacy_principles = self._initialize_privacy_principles()
    
    def _initialize_privacy_principles(self):
        """Initialize the 13 Australian Privacy Principles"""
        return {
            "APP1": {
                "name": "Open and transparent management of personal information",
                "description": "Manage personal information in an open and transparent way",
                "requirements": [
                    "Have a privacy policy",
                    "Make privacy policy available free of charge",
                    "Take reasonable steps to implement practices consistent with APP"
                ],
                "risk_level": "HIGH",
                "typical_implementation": "Privacy policy, privacy officer, staff training"
            },
            "APP2": {
                "name": "Anonymity and pseudonymity",
                "description": "Give individuals option to remain anonymous or use pseudonym",
                "requirements": [
                    "Provide anonymity option where practicable",
                    "Allow pseudonym use where practicable"
                ],
                "risk_level": "MEDIUM",
                "typical_implementation": "Anonymous forms, pseudonym acceptance procedures"
            },
            "APP3": {
                "name": "Collection of solicited personal information",
                "description": "Only collect personal information reasonably necessary",
                "requirements": [
                    "Only collect if reasonably necessary for functions/activities",
                    "Collect by lawful and fair means",
                    "Take reasonable steps to notify of collection"
                ],
                "risk_level": "HIGH",
                "typical_implementation": "Data minimization, collection notices, lawful basis"
            },
            "APP4": {
                "name": "Dealing with unsolicited personal information",
                "description": "Handle unsolicited personal information appropriately",
                "requirements": [
                    "Determine if collection would be permitted under APP 3",
                    "Destroy/de-identify if not permitted and lawful to do so"
                ],
                "risk_level": "MEDIUM",
                "typical_implementation": "Unsolicited data procedures, deletion policies"
            },
            "APP5": {
                "name": "Notification of collection",
                "description": "Notify individuals when collecting personal information",
                "requirements": [
                    "Notify at time of collection or as soon as practicable after",
                    "Specify identity, purposes, consequences of not providing"
                ],
                "risk_level": "HIGH",
                "typical_implementation": "Privacy notices, collection statements"
            },
            "APP6": {
                "name": "Use or disclosure",
                "description": "Only use/disclose for primary purpose or related secondary purpose",
                "requirements": [
                    "Use only for primary purpose collected",
                    "Secondary use must be related and reasonably expected",
                    "Obtain consent for unrelated secondary purposes"
                ],
                "risk_level": "CRITICAL",
                "typical_implementation": "Purpose limitation, consent mechanisms, use policies"
            },
            "APP7": {
                "name": "Direct marketing",
                "description": "Restrictions on using personal information for direct marketing",
                "requirements": [
                    "Only use if reasonable to expect or consented",
                    "Provide simple opt-out mechanism",
                    "Don't use sensitive information unless consented"
                ],
                "risk_level": "MEDIUM",
                "typical_implementation": "Marketing preferences, opt-out systems"
            },
            "APP8": {
                "name": "Cross-border disclosure",
                "description": "Restrictions on disclosing personal information overseas",
                "requirements": [
                    "Take reasonable steps to ensure overseas recipient complies",
                    "Remain accountable for overseas handling"
                ],
                "risk_level": "HIGH",
                "typical_implementation": "International transfer policies, adequacy assessments"
            },
            "APP9": {
                "name": "Adoption, use or disclosure of government identifiers",
                "description": "Restrictions on using government identifiers",
                "requirements": [
                    "Don't adopt government identifier as own identifier",
                    "Don't use/disclose unless required by law or specific exceptions"
                ],
                "risk_level": "MEDIUM",
                "typical_implementation": "Identifier management policies"
            },
            "APP10": {
                "name": "Quality of personal information",
                "description": "Ensure personal information is accurate and up-to-date",
                "requirements": [
                    "Take reasonable steps to ensure accuracy when collecting",
                    "Take reasonable steps to ensure accuracy when using/disclosing"
                ],
                "risk_level": "MEDIUM",
                "typical_implementation": "Data quality procedures, verification processes"
            },
            "APP11": {
                "name": "Security of personal information",
                "description": "Take reasonable steps to protect personal information",
                "requirements": [
                    "Protect from misuse, interference, loss",
                    "Protect from unauthorized access, modification, disclosure",
                    "Destroy/de-identify when no longer needed and lawful to do so"
                ],
                "risk_level": "CRITICAL",
                "typical_implementation": "Information security controls, retention policies"
            },
            "APP12": {
                "name": "Access to personal information",
                "description": "Give individuals access to their personal information",
                "requirements": [
                    "Provide access on request unless exception applies",
                    "Give access in manner requested if reasonable and practicable",
                    "May charge reasonable fee"
                ],
                "risk_level": "HIGH",
                "typical_implementation": "Subject access procedures, request handling"
            },
            "APP13": {
                "name": "Correction of personal information",
                "description": "Correct personal information on request",
                "requirements": [
                    "Correct if inaccurate, out-of-date, incomplete, irrelevant, misleading",
                    "Take reasonable steps to notify third parties of corrections"
                ],
                "risk_level": "MEDIUM",
                "typical_implementation": "Correction procedures, third-party notification"
            }
        }
    
    async def assess(self, company_profile: CompanyProfile) -> AssessmentResult:
        """
        Assess Privacy Act compliance with enterprise-grade error handling.
        Evaluates implementation of Australian Privacy Principles.
        """
        
        assessment_data = {
            "framework": "Privacy Act 1988",
            "company": company_profile.company_name,
            "timestamp": datetime.now(),
            "apps_assessed": [],
            "gaps_identified": [],
            "compliance_score": 0.0,
            "privacy_risk_level": "UNKNOWN",
            "data_handling_assessment": {},
            "breach_risk_assessment": {},
            "evidence": [],
            "errors": [],
            "warnings": []
        }
        
        try:
            # Assess each APP with individual error handling
            total_score = 0
            successful_apps = 0
            
            for app_id, principle in self.privacy_principles.items():
                try:
                    app_assessment = await self._assess_privacy_principle(
                        app_id, principle, company_profile
                    )
                    
                    assessment_data["apps_assessed"].append(app_assessment)
                    total_score += app_assessment["compliance_score"]
                    successful_apps += 1
                    
                except asyncio.TimeoutError:
                    error_msg = f"Timeout assessing APP {app_id}"
                    logger.error(error_msg)
                    assessment_data["errors"].append(error_msg)
                    assessment_data["apps_assessed"].append({
                        "app_id": app_id,
                        "status": "ERROR_TIMEOUT",
                        "compliance_score": 0.0,
                        "error": "Assessment timeout"
                    })
                    
                except Exception as app_error:
                    error_msg = f"Error assessing APP {app_id}: {str(app_error)}"
                    logger.error(error_msg)
                    assessment_data["errors"].append(error_msg)
                    assessment_data["apps_assessed"].append({
                        "app_id": app_id,
                        "status": "ERROR",
                        "compliance_score": 0.0,
                        "error": str(app_error)
                    })
            
            # Calculate final compliance score
            if successful_apps > 0:
                assessment_data["compliance_score"] = total_score / len(self.privacy_principles)
            else:
                assessment_data["compliance_score"] = 0.0
                assessment_data["warnings"].append("No APPs assessed successfully")
            
            # Identify gaps from completed assessments
            for app_data in assessment_data["apps_assessed"]:
                if app_data.get("compliance_score", 0) < 0.7:
                    assessment_data["gaps_identified"].append({
                        "principle": app_data.get("app_id", "unknown"),
                        "gap_description": app_data.get("gap_description", "Low compliance score"),
                        "risk_level": "MEDIUM",
                        "recommendations": app_data.get("recommendations", [])
                    })
        
            # Assess privacy risk level with error handling
            try:
                assessment_data["privacy_risk_level"] = self._calculate_privacy_risk(
                    company_profile, assessment_data["gaps_identified"]
                )
            except Exception as risk_error:
                logger.error(f"Error calculating privacy risk: {risk_error}")
                assessment_data["privacy_risk_level"] = "HIGH"  # Conservative default
                assessment_data["errors"].append("Failed to calculate privacy risk")
            
            # Data handling assessment with error handling
            try:
                assessment_data["data_handling_assessment"] = await self._assess_data_handling(
                    company_profile
                )
            except Exception as data_error:
                logger.error(f"Error assessing data handling: {data_error}")
                assessment_data["data_handling_assessment"] = {"status": "ERROR", "error": str(data_error)}
                assessment_data["errors"].append("Failed to assess data handling")
            
            # Breach risk assessment with error handling
            try:
                assessment_data["breach_risk_assessment"] = self._assess_breach_risk(
                    company_profile, assessment_data["gaps_identified"]
                )
            except Exception as breach_error:
                logger.error(f"Error assessing breach risk: {breach_error}")
                assessment_data["breach_risk_assessment"] = {"risk_level": "HIGH", "error": str(breach_error)}
                assessment_data["errors"].append("Failed to assess breach risk")
            
            # Generate recommendations with error handling
            try:
                recommendations = await self._generate_privacy_recommendations(
                    assessment_data["gaps_identified"], company_profile
                )
            except Exception as rec_error:
                logger.error(f"Error generating recommendations: {rec_error}")
                recommendations = []
                assessment_data["errors"].append("Failed to generate recommendations")
            
            # Calculate confidence with error handling
            try:
                confidence = self.calculate_confidence(assessment_data)
            except Exception as conf_error:
                logger.error(f"Error calculating confidence: {conf_error}")
                confidence = 0.3  # Low confidence due to errors
                assessment_data["errors"].append("Failed to calculate confidence")
            
            # Adjust confidence based on errors
            if assessment_data["errors"]:
                confidence = max(0.1, confidence * 0.5)
            
            # Create standardized assessment result
            return AssessmentResult(
                framework="Privacy Act 1988",
                company=company_profile.company_name,
                timestamp=datetime.now(),
                status=AssessmentStatus.COMPLETED if not assessment_data["errors"] else AssessmentStatus.FAILED,
                confidence=confidence,
                risk_level=get_risk_level(assessment_data["compliance_score"]),
                controls_assessed=assessment_data["apps_assessed"],
                gaps_identified=assessment_data["gaps_identified"],
                recommendations=recommendations,
                evidence=assessment_data.get("evidence", []),
                overall_score=assessment_data["compliance_score"],
                control_scores={app["app_id"]: app.get("compliance_score", 0.0) 
                              for app in assessment_data["apps_assessed"] if "app_id" in app},
                maturity_scores={},  # Not applicable for Privacy Act
                executive_summary=f"Privacy Act assessment completed with {len(assessment_data['gaps_identified'])} gaps identified",
                business_impact=f"Privacy risk level: {assessment_data['privacy_risk_level']}"
            )
            
        except Exception as critical_error:
            # Critical failure - return minimal safe assessment
            logger.critical(f"Critical error in PrivacyActAgent assessment: {critical_error}")
            return AssessmentResult(
                framework="Privacy Act 1988",
                company=company_profile.company_name,
                timestamp=datetime.now(),
                status=AssessmentStatus.FAILED,
                confidence=0.0,
                risk_level=RiskLevel.CRITICAL,
                controls_assessed=[],
                gaps_identified=[],
                recommendations=[],
                evidence=[],
                overall_score=0.0,
                control_scores={},
                maturity_scores={},
                executive_summary="Critical assessment failure requires human review",
                business_impact="Unable to determine privacy compliance status"
            )
    
    async def _assess_privacy_principle(self, app_id: str, principle: Dict, 
                                      company_profile: CompanyProfile) -> Dict[str, Any]:
        """Assess implementation of a specific Privacy Principle"""
        
        # Industry-specific assessments
        industry_factors = self._get_industry_privacy_factors(company_profile.industry)
        
        # Base compliance assumption
        compliance_score = 0.3  # Conservative default
        gap_description = f"No evidence of {principle['name']} implementation"
        recommendations = []
        
        # Assessment logic based on industry and company characteristics
        if app_id == "APP11":  # Security principle - high importance
            if "Backups" in company_profile.current_controls:
                compliance_score += 0.3
            if "MFA" in company_profile.current_controls:
                compliance_score += 0.2
            if "Access Control" in company_profile.current_controls:
                compliance_score += 0.3
            
            if compliance_score < 0.7:
                gap_description = "Insufficient security controls for personal information protection"
                recommendations = [
                    "Implement encryption for personal data at rest and in transit",
                    "Establish access controls and user authentication",
                    "Create data retention and secure deletion policies"
                ]
        
        elif app_id == "APP6":  # Use and disclosure - critical principle
            compliance_score = 0.4  # Default medium compliance
            
            if company_profile.industry in ["Healthcare", "Finance"]:
                compliance_score += 0.2  # Regulated industries typically have better controls
            
            if compliance_score < 0.7:
                gap_description = "Lack of documented purpose limitation and consent management"
                recommendations = [
                    "Document all purposes for personal information collection",
                    "Implement consent management system",
                    "Create use and disclosure policies"
                ]
        
        elif app_id in ["APP1", "APP5"]:  # Transparency principles
            compliance_score = 0.5  # Assume moderate compliance
            
            if company_profile.employee_count > 100:
                compliance_score += 0.2  # Larger companies more likely to have privacy policies
            
            if compliance_score < 0.7:
                gap_description = f"Missing or inadequate {principle['name'].lower()}"
                recommendations = [
                    "Create comprehensive privacy policy",
                    "Implement collection notices and privacy statements",
                    "Establish privacy officer role"
                ]
        
        else:
            # Generic assessment for other principles
            compliance_score = 0.4 + (industry_factors.get("privacy_maturity", 0) * 0.3)
        
        return {
            "app_id": app_id,
            "principle_name": principle["name"],
            "compliance_score": min(compliance_score, 1.0),
            "gap_description": gap_description if compliance_score < 0.7 else None,
            "recommendations": recommendations,
            "risk_level": principle["risk_level"],
            "confidence": 0.7  # Conservative confidence for privacy assessments
        }
    
    def _get_industry_privacy_factors(self, industry: str) -> Dict[str, float]:
        """Get industry-specific privacy factors"""
        factors = {
            "Healthcare": {"privacy_maturity": 0.8, "breach_risk": 0.9, "regulatory_focus": 0.9},
            "Finance": {"privacy_maturity": 0.8, "breach_risk": 0.8, "regulatory_focus": 0.9},
            "Technology": {"privacy_maturity": 0.6, "breach_risk": 0.7, "regulatory_focus": 0.5},
            "Education": {"privacy_maturity": 0.5, "breach_risk": 0.6, "regulatory_focus": 0.7},
            "Government": {"privacy_maturity": 0.7, "breach_risk": 0.8, "regulatory_focus": 1.0},
            "Retail": {"privacy_maturity": 0.4, "breach_risk": 0.6, "regulatory_focus": 0.4}
        }
        return factors.get(industry, {"privacy_maturity": 0.5, "breach_risk": 0.6, "regulatory_focus": 0.5})
    
    def _calculate_privacy_risk(self, company_profile: CompanyProfile, gaps: List[Dict]) -> str:
        """Calculate overall privacy risk level"""
        
        base_risk = 0.3
        
        # Industry risk
        industry_factors = self._get_industry_privacy_factors(company_profile.industry)
        base_risk += industry_factors["breach_risk"] * 0.3
        
        # Size risk
        if company_profile.employee_count > 500:
            base_risk += 0.2
        
        # Gap risk
        critical_gaps = [g for g in gaps if g["risk_level"] in ["CRITICAL", "HIGH"]]
        base_risk += len(critical_gaps) * 0.1
        
        # Previous incidents
        if company_profile.previous_incidents:
            base_risk += 0.2
        
        if base_risk > 0.8:
            return "CRITICAL"
        elif base_risk > 0.6:
            return "HIGH"
        elif base_risk > 0.4:
            return "MEDIUM"
        return "LOW"
    
    async def _assess_data_handling(self, company_profile: CompanyProfile) -> Dict[str, Any]:
        """Assess data handling practices"""
        
        data_types = self._identify_likely_data_types(company_profile.industry)
        
        return {
            "likely_data_types": data_types,
            "cross_border_transfers": self._assess_cross_border_risk(company_profile),
            "data_retention": {"policy_exists": False, "risk": "MEDIUM"},
            "data_minimization": {"implemented": False, "risk": "MEDIUM"}
        }
    
    def _identify_likely_data_types(self, industry: str) -> List[str]:
        """Identify likely personal data types based on industry"""
        
        industry_data_map = {
            "Healthcare": ["health records", "contact details", "financial information", "sensitive health data"],
            "Finance": ["financial records", "identity verification", "transaction data", "credit information"],
            "Education": ["student records", "academic performance", "contact details", "health information"],
            "Technology": ["user profiles", "usage data", "contact details", "device information"],
            "Retail": ["customer details", "payment information", "purchase history", "loyalty program data"],
            "Government": ["citizen data", "identity documents", "service records", "sensitive personal data"]
        }
        
        return industry_data_map.get(industry, ["contact details", "customer information"])
    
    def _assess_cross_border_risk(self, company_profile: CompanyProfile) -> Dict[str, Any]:
        """Assess cross-border data transfer risks"""
        
        # Simple assessment based on company characteristics
        risk_level = "LOW"
        
        if company_profile.employee_count > 200:
            risk_level = "MEDIUM"  # Larger companies more likely to use international services
        
        if company_profile.industry in ["Technology", "Finance"]:
            risk_level = "HIGH"  # These industries commonly use international cloud services
        
        return {
            "risk_level": risk_level,
            "likely_transfers": risk_level != "LOW",
            "app8_compliance_required": True
        }
    
    def _assess_breach_risk(self, company_profile: CompanyProfile, gaps: List[Dict]) -> Dict[str, Any]:
        """Assess likelihood and impact of a notifiable data breach"""
        
        # Calculate breach probability
        security_gaps = [g for g in gaps if g["principle"] in ["APP11"]]
        transparency_gaps = [g for g in gaps if g["principle"] in ["APP1", "APP5"]]
        
        breach_probability = 0.3  # Base probability
        
        if security_gaps:
            breach_probability += 0.3
        
        if company_profile.employee_count > 500:
            breach_probability += 0.2  # Larger attack surface
        
        if company_profile.previous_incidents:
            breach_probability += 0.2
        
        # Calculate potential impact
        industry_factors = self._get_industry_privacy_factors(company_profile.industry)
        impact_score = industry_factors["breach_risk"]
        
        return {
            "breach_probability": min(breach_probability, 1.0),
            "potential_impact": "HIGH" if impact_score > 0.7 else "MEDIUM" if impact_score > 0.4 else "LOW",
            "oaic_notification_required": True,
            "estimated_individuals_affected": self._estimate_affected_individuals(company_profile),
            "recommended_breach_response": [
                "Develop incident response plan",
                "Establish OAIC notification procedures",
                "Create affected individual communication templates"
            ]
        }
    
    def _estimate_affected_individuals(self, company_profile: CompanyProfile) -> str:
        """Estimate number of individuals that could be affected in a breach"""
        
        if company_profile.industry == "Healthcare":
            multiplier = 5  # Patients per employee
        elif company_profile.industry == "Education":
            multiplier = 20  # Students per employee
        elif company_profile.industry == "Retail":
            multiplier = 100  # Customers per employee
        else:
            multiplier = 10  # Generic multiplier
        
        estimated = company_profile.employee_count * multiplier
        
        if estimated > 10000:
            return "10,000+"
        elif estimated > 1000:
            return "1,000-10,000"
        elif estimated > 100:
            return "100-1,000"
        else:
            return "<100"
    
    async def _generate_privacy_recommendations(self, gaps: List[Dict], 
                                              company_profile: CompanyProfile) -> List[Dict]:
        """Generate prioritized privacy implementation recommendations"""
        
        recommendations = []
        
        # High-priority security recommendations
        security_gaps = [g for g in gaps if g["principle"] == "APP11"]
        if security_gaps:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Information Security (APP 11)",
                "action": "Implement comprehensive information security controls",
                "timeline": "30 days",
                "effort": "HIGH",
                "business_impact": "CRITICAL",
                "specific_steps": [
                    "Conduct data mapping exercise",
                    "Implement encryption for personal data",
                    "Establish access controls and authentication",
                    "Create data retention and deletion policies",
                    "Develop incident response procedures"
                ]
            })
        
        # Transparency and governance recommendations
        governance_gaps = [g for g in gaps if g["principle"] in ["APP1", "APP5"]]
        if governance_gaps:
            recommendations.append({
                "priority": "HIGH",
                "category": "Privacy Governance (APP 1, 5)",
                "action": "Establish privacy governance framework",
                "timeline": "45 days",
                "effort": "MEDIUM",
                "business_impact": "HIGH",
                "specific_steps": [
                    "Develop comprehensive privacy policy",
                    "Create collection notices and privacy statements",
                    "Establish privacy officer role",
                    "Implement privacy impact assessment process",
                    "Conduct staff privacy training"
                ]
            })
        
        # Use and disclosure controls
        use_gaps = [g for g in gaps if g["principle"] == "APP6"]
        if use_gaps:
            recommendations.append({
                "priority": "HIGH",
                "category": "Use and Disclosure Controls (APP 6)",
                "action": "Implement purpose limitation and consent management",
                "timeline": "60 days",
                "effort": "MEDIUM",
                "business_impact": "HIGH",
                "specific_steps": [
                    "Document all collection and use purposes",
                    "Implement consent management system",
                    "Create use and disclosure policies",
                    "Establish third-party data sharing agreements",
                    "Regular purpose limitation audits"
                ]
            })
        
        return recommendations[:5]  # Return top 5 recommendations


# ============================================================================
# APRA CPS 234 AGENT 
# ============================================================================

class APRACPSAgent(BaseComplianceAgent):
    """
    Specialized agent for APRA CPS 234 Information Security assessment.
    Focuses on prudential requirements for financial institutions.
    """
    
    def __init__(self):
        super().__init__(
            name="APRACPSAgent", 
            expertise="APRA CPS 234 Information Security Standard"
        )
        self.cps234_requirements = self._initialize_cps234_requirements()
    
    def _initialize_cps234_requirements(self):
        """Initialize CPS 234 requirements"""
        return {
            "information_security_capability": {
                "description": "Maintain information security capability commensurate with information security vulnerabilities and threats",
                "requirements": [
                    "Implement information security controls",
                    "Regular vulnerability assessments",
                    "Threat monitoring and response"
                ],
                "maturity_levels": ["Basic", "Managed", "Comprehensive"],
                "risk_rating": "CRITICAL"
            },
            "information_security_policy": {
                "description": "Maintain written information security policy",
                "requirements": [
                    "Board-approved information security policy",
                    "Regular policy review and update",
                    "Policy covers all information assets"
                ],
                "maturity_levels": ["Basic", "Managed", "Comprehensive"],
                "risk_rating": "HIGH"
            },
            "incident_management": {
                "description": "Maintain incident response capability",
                "requirements": [
                    "Incident response plan",
                    "Incident detection and response procedures",
                    "APRA notification procedures"
                ],
                "maturity_levels": ["Basic", "Managed", "Comprehensive"],
                "risk_rating": "CRITICAL"
            },
            "testing_and_assurance": {
                "description": "Regular testing of information security controls",
                "requirements": [
                    "Regular control testing",
                    "Penetration testing",
                    "Independent assurance"
                ],
                "maturity_levels": ["Annual", "Bi-annual", "Continuous"],
                "risk_rating": "HIGH"
            },
            "service_provider_management": {
                "description": "Manage information security risks from service providers",
                "requirements": [
                    "Due diligence on service providers",
                    "Contractual information security requirements",
                    "Ongoing monitoring of service providers"
                ],
                "maturity_levels": ["Basic", "Managed", "Comprehensive"],
                "risk_rating": "HIGH"
            }
        }
    
    async def assess(self, company_profile: CompanyProfile) -> Dict[str, Any]:
        """
        Assess APRA CPS 234 compliance.
        Only applicable to financial institutions under APRA supervision.
        """
        
        # Check if CPS 234 applies
        if not self._is_apra_regulated(company_profile):
            return {
                "framework": "APRA CPS 234",
                "applicable": False,
                "reason": "Not an APRA-regulated financial institution",
                "confidence": 1.0
            }
        
        assessment = {
            "framework": "APRA CPS 234",
            "company": company_profile.company_name,
            "applicable": True,
            "timestamp": datetime.now(),
            "requirements_assessed": [],
            "gaps_identified": [],
            "maturity_scores": {},
            "overall_maturity": 0.0,
            "regulatory_risk": "UNKNOWN"
        }
        
        # Assess each requirement
        total_score = 0
        for req_id, requirement in self.cps234_requirements.items():
            req_assessment = await self._assess_cps234_requirement(
                req_id, requirement, company_profile
            )
            
            assessment["requirements_assessed"].append(req_assessment)
            assessment["maturity_scores"][req_id] = req_assessment["maturity_score"]
            total_score += req_assessment["maturity_score"]
            
            # Identify gaps
            if req_assessment["maturity_score"] < 2.0:  # Below "Managed" level
                assessment["gaps_identified"].append({
                    "requirement": req_id,
                    "description": requirement["description"],
                    "current_maturity": req_assessment["maturity_level"],
                    "gap_description": req_assessment["gap_description"],
                    "risk_rating": requirement["risk_rating"]
                })
        
        # Calculate overall maturity
        assessment["overall_maturity"] = total_score / len(self.cps234_requirements)
        
        # Calculate regulatory risk
        assessment["regulatory_risk"] = self._calculate_regulatory_risk(
            assessment["overall_maturity"], assessment["gaps_identified"]
        )
        
        # Generate recommendations
        assessment["recommendations"] = await self._generate_cps234_recommendations(
            assessment["gaps_identified"], company_profile
        )
        
        # Calculate confidence
        assessment["confidence"] = self.calculate_confidence(assessment)
        
        return assessment
    
    def _is_apra_regulated(self, company_profile: CompanyProfile) -> bool:
        """Determine if company is APRA-regulated"""
        
        # Simple industry-based check
        apra_industries = [
            "Finance", "Banking", "Insurance", "Superannuation",
            "Credit Union", "Building Society", "Financial Services"
        ]
        
        return company_profile.industry in apra_industries
    
    async def _assess_cps234_requirement(self, req_id: str, requirement: Dict,
                                       company_profile: CompanyProfile) -> Dict[str, Any]:
        """Assess implementation of a specific CPS 234 requirement"""
        
        # Default conservative assessment
        maturity_score = 0.5  # Basic implementation
        gap_description = f"Limited implementation of {requirement['description']}"
        
        # Adjust based on company characteristics and declared controls
        if req_id == "information_security_capability":
            if "MFA" in company_profile.current_controls:
                maturity_score += 0.3
            if "Access Control" in company_profile.current_controls:
                maturity_score += 0.4
            if "Monitoring" in company_profile.current_controls:
                maturity_score += 0.5
        
        elif req_id == "incident_management":
            if company_profile.previous_incidents:
                maturity_score += 0.3  # Experience with incidents suggests some capability
            if "Monitoring" in company_profile.current_controls:
                maturity_score += 0.4
        
        elif req_id == "testing_and_assurance":
            if company_profile.employee_count > 500:
                maturity_score += 0.3  # Larger institutions more likely to have testing
            if company_profile.industry == "Banking":
                maturity_score += 0.4  # Banks typically have better testing
        
        # Cap maturity score
        maturity_score = min(maturity_score, 3.0)
        
        # Determine maturity level
        if maturity_score >= 2.5:
            maturity_level = "Comprehensive"
        elif maturity_score >= 1.5:
            maturity_level = "Managed"
        else:
            maturity_level = "Basic"
        
        if maturity_score < 2.0:
            gap_description = f"Requires enhancement to achieve 'Managed' level for {requirement['description']}"
        
        return {
            "requirement_id": req_id,
            "requirement_description": requirement["description"],
            "maturity_score": maturity_score,
            "maturity_level": maturity_level,
            "gap_description": gap_description if maturity_score < 2.0 else None,
            "risk_rating": requirement["risk_rating"],
            "confidence": 0.6  # Conservative confidence for regulatory assessments
        }
    
    def _calculate_regulatory_risk(self, overall_maturity: float, gaps: List[Dict]) -> str:
        """Calculate regulatory compliance risk"""
        
        critical_gaps = [g for g in gaps if g["risk_rating"] == "CRITICAL"]
        
        if overall_maturity < 1.0 or len(critical_gaps) > 2:
            return "HIGH"
        elif overall_maturity < 1.5 or len(critical_gaps) > 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def _generate_cps234_recommendations(self, gaps: List[Dict], 
                                             company_profile: CompanyProfile) -> List[Dict]:
        """Generate CPS 234 implementation recommendations"""
        
        recommendations = []
        
        # Critical security capability recommendations
        security_gaps = [g for g in gaps if "security_capability" in g["requirement"]]
        if security_gaps:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Information Security Capability",
                "action": "Establish comprehensive information security capability",
                "regulatory_requirement": "CPS 234 Paragraph 34",
                "timeline": "90 days",
                "effort": "HIGH",
                "specific_steps": [
                    "Conduct information security risk assessment",
                    "Implement security controls framework",
                    "Establish security monitoring capability",
                    "Deploy vulnerability management program"
                ]
            })
        
        return recommendations[:3]  # Top 3 recommendations


# ============================================================================
# SOCI ACT AGENT
# ============================================================================

class SOCIActAgent(BaseComplianceAgent):
    """
    Specialized agent for Security of Critical Infrastructure Act 2018 compliance.
    Focuses on critical infrastructure protection requirements.
    """
    
    def __init__(self):
        super().__init__(
            name="SOCIActAgent",
            expertise="Security of Critical Infrastructure Act 2018"
        )
        self.critical_sectors = self._initialize_critical_sectors()
    
    def _initialize_critical_sectors(self):
        """Initialize critical infrastructure sectors under SOCI Act"""
        return {
            "electricity": {"risk_level": "CRITICAL", "oversight": "Enhanced"},
            "gas": {"risk_level": "CRITICAL", "oversight": "Enhanced"}, 
            "water": {"risk_level": "CRITICAL", "oversight": "Enhanced"},
            "telecommunications": {"risk_level": "HIGH", "oversight": "Standard"},
            "transport": {"risk_level": "HIGH", "oversight": "Standard"},
            "banking": {"risk_level": "HIGH", "oversight": "Enhanced"},
            "data_storage": {"risk_level": "MEDIUM", "oversight": "Standard"},
            "domain_name": {"risk_level": "MEDIUM", "oversight": "Standard"},
            "food_grocery": {"risk_level": "MEDIUM", "oversight": "Standard"},
            "healthcare": {"risk_level": "HIGH", "oversight": "Standard"},
            "higher_education": {"risk_level": "MEDIUM", "oversight": "Standard"},
            "aviation": {"risk_level": "HIGH", "oversight": "Enhanced"}
        }
    
    async def assess(self, company_profile: CompanyProfile) -> Dict[str, Any]:
        """
        Assess SOCI Act compliance.
        Only applicable to critical infrastructure entities.
        """
        
        # Check if SOCI Act applies
        sector_classification = self._classify_critical_infrastructure(company_profile)
        
        if not sector_classification["is_critical"]:
            return {
                "framework": "SOCI Act 2018",
                "applicable": False,
                "reason": "Not classified as critical infrastructure",
                "confidence": 0.8
            }
        
        assessment = {
            "framework": "SOCI Act 2018", 
            "company": company_profile.company_name,
            "applicable": True,
            "sector": sector_classification["sector"],
            "risk_level": sector_classification["risk_level"],
            "oversight_level": sector_classification["oversight"],
            "timestamp": datetime.now(),
            "obligations_assessed": [],
            "gaps_identified": [],
            "security_maturity": 0.0,
            "regulatory_obligations": {}
        }
        
        # Assess key obligations
        obligations = self._get_soci_obligations(sector_classification)
        
        for obligation in obligations:
            obligation_assessment = await self._assess_soci_obligation(
                obligation, company_profile
            )
            assessment["obligations_assessed"].append(obligation_assessment)
            
            if obligation_assessment["compliance_level"] < 0.7:
                assessment["gaps_identified"].append({
                    "obligation": obligation["name"],
                    "description": obligation["description"],
                    "gap_severity": obligation_assessment["gap_severity"],
                    "regulatory_risk": obligation["regulatory_risk"]
                })
        
        # Calculate security maturity
        if assessment["obligations_assessed"]:
            avg_compliance = np.mean([
                oa["compliance_level"] for oa in assessment["obligations_assessed"]
            ])
            assessment["security_maturity"] = avg_compliance
        
        # Generate recommendations
        assessment["recommendations"] = await self._generate_soci_recommendations(
            assessment["gaps_identified"], sector_classification
        )
        
        assessment["confidence"] = self.calculate_confidence(assessment)
        
        return assessment
    
    def _classify_critical_infrastructure(self, company_profile: CompanyProfile) -> Dict[str, Any]:
        """Classify if company operates critical infrastructure"""
        
        industry_mapping = {
            "Energy": "electricity",
            "Utilities": "electricity",
            "Telecommunications": "telecommunications",
            "Transport": "transport",
            "Banking": "banking",
            "Finance": "banking",
            "Healthcare": "healthcare",
            "Technology": "data_storage",  # Potential for data centers
            "Education": "higher_education"
        }
        
        sector = industry_mapping.get(company_profile.industry)
        
        if sector and company_profile.employee_count > 100:  # Size threshold
            return {
                "is_critical": True,
                "sector": sector,
                "risk_level": self.critical_sectors[sector]["risk_level"],
                "oversight": self.critical_sectors[sector]["oversight"]
            }
        
        return {"is_critical": False, "sector": None, "risk_level": "LOW", "oversight": "None"}
    
    def _get_soci_obligations(self, sector_classification: Dict) -> List[Dict]:
        """Get applicable SOCI Act obligations based on sector"""
        
        base_obligations = [
            {
                "name": "Risk Management Program",
                "description": "Maintain risk management program for critical infrastructure",
                "regulatory_risk": "HIGH",
                "applies_to": "all"
            },
            {
                "name": "Incident Reporting",
                "description": "Report cybersecurity incidents to government",
                "regulatory_risk": "CRITICAL",
                "applies_to": "all"
            },
            {
                "name": "Government Assistance",
                "description": "Provide reasonable assistance to government during incidents",
                "regulatory_risk": "HIGH",
                "applies_to": "all"
            }
        ]
        
        # Enhanced obligations for high-risk sectors
        if sector_classification["oversight"] == "Enhanced":
            base_obligations.extend([
                {
                    "name": "Enhanced Cyber Standards",
                    "description": "Comply with enhanced cybersecurity standards",
                    "regulatory_risk": "CRITICAL",
                    "applies_to": "enhanced"
                },
                {
                    "name": "Vulnerability Assessments",
                    "description": "Regular vulnerability assessments and penetration testing",
                    "regulatory_risk": "HIGH",
                    "applies_to": "enhanced"
                }
            ])
        
        return base_obligations
    
    async def _assess_soci_obligation(self, obligation: Dict, 
                                    company_profile: CompanyProfile) -> Dict[str, Any]:
        """Assess compliance with specific SOCI obligation"""
        
        # Conservative assessment
        compliance_level = 0.3
        gap_severity = "HIGH"
        
        if obligation["name"] == "Risk Management Program":
            if company_profile.employee_count > 500:
                compliance_level += 0.3  # Larger orgs more likely to have programs
            if "Risk Assessment" in company_profile.current_controls:
                compliance_level += 0.4
        
        elif obligation["name"] == "Incident Reporting":
            if company_profile.previous_incidents:
                compliance_level += 0.2  # Some incident experience
            if "Monitoring" in company_profile.current_controls:
                compliance_level += 0.3
        
        # Determine gap severity
        if compliance_level >= 0.7:
            gap_severity = "LOW"
        elif compliance_level >= 0.5:
            gap_severity = "MEDIUM"
        else:
            gap_severity = "HIGH"
        
        return {
            "obligation": obligation["name"],
            "compliance_level": compliance_level,
            "gap_severity": gap_severity,
            "regulatory_risk": obligation["regulatory_risk"]
        }
    
    async def _generate_soci_recommendations(self, gaps: List[Dict], 
                                           sector_classification: Dict) -> List[Dict]:
        """Generate SOCI Act compliance recommendations"""
        
        recommendations = []
        
        critical_gaps = [g for g in gaps if g["gap_severity"] in ["HIGH", "CRITICAL"]]
        
        if critical_gaps:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "SOCI Act Compliance",
                "action": "Establish critical infrastructure protection program",
                "regulatory_timeline": "Immediate - regulatory requirement",
                "effort": "HIGH",
                "specific_steps": [
                    "Develop risk management program for critical assets",
                    "Implement incident detection and reporting procedures",
                    "Establish government liaison and assistance protocols",
                    "Create business continuity and disaster recovery plans"
                ]
            })
        
        return recommendations


# Example integration with existing system
if __name__ == "__main__":
    # Test the new agents
    async def test_agents():
        # Test company profile
        test_company = CompanyProfile(
            company_name="Test Healthcare Corp",
            industry="Healthcare",
            employee_count=300,
            current_controls=["MFA", "Backups", "Access Control"],
            previous_incidents=["Phishing attack 2023"]
        )
        
        # Test Privacy Act agent
        privacy_agent = PrivacyActAgent()
        privacy_result = await privacy_agent.assess(test_company)
        print(f"Privacy Act Assessment - Compliance Score: {privacy_result['compliance_score']:.2f}")
        print(f"Privacy Risk Level: {privacy_result['privacy_risk_level']}")
        
        # Test APRA agent (for finance company)
        finance_company = CompanyProfile(
            company_name="Test Bank",
            industry="Banking",
            employee_count=1000,
            current_controls=["MFA", "Monitoring", "Access Control"]
        )
        
        apra_agent = APRACPSAgent()
        apra_result = await apra_agent.assess(finance_company)
        print(f"\nAPRA CPS 234 Assessment - Applicable: {apra_result['applicable']}")
        if apra_result['applicable']:
            print(f"Overall Maturity: {apra_result['overall_maturity']:.2f}")
        
        # Test SOCI agent (for critical infrastructure)
        critical_company = CompanyProfile(
            company_name="Power Grid Corp",
            industry="Energy",
            employee_count=500,
            current_controls=["Access Control", "Monitoring"]
        )
        
        soci_agent = SOCIActAgent()
        soci_result = await soci_agent.assess(critical_company)
        print(f"\nSOCI Act Assessment - Applicable: {soci_result['applicable']}")
        if soci_result['applicable']:
            print(f"Sector: {soci_result['sector']}")
            print(f"Security Maturity: {soci_result['security_maturity']:.2f}")
    
    # Run tests
    asyncio.run(test_agents())


# Export function for main application integration
def load_australian_agents():
    """
    Load and return Australian compliance agents for use in main application.
    This function is called by the unified platform.
    """
    return {
        'privacy_act': PrivacyActAgent(),
        'apra_cps234': APRACPSAgent(),
        'soci_act': SOCIActAgent(),
        'essential8': None,  # Would need to import from main system
    }