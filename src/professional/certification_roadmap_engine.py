"""
Cross-Framework Certification Roadmap Engine
==========================================

Intelligent certification pathway recommendations based on current compliance posture,
industry requirements, and strategic business objectives.

Author: Sentinel GRC Platform
Version: 1.0.0-production
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class CertificationPriority(Enum):
    CRITICAL = "Critical"
    HIGH = "High" 
    MEDIUM = "Medium"
    LOW = "Low"
    DEFERRED = "Deferred"

class IndustryType(Enum):
    TECHNOLOGY = "Technology"
    FINANCIAL_SERVICES = "Financial Services"
    HEALTHCARE = "Healthcare"
    GOVERNMENT = "Government"
    MANUFACTURING = "Manufacturing"
    EDUCATION = "Education"
    RETAIL = "Retail"
    OTHER = "Other"

@dataclass
class CertificationRecommendation:
    framework_name: str
    priority: CertificationPriority
    readiness_score: float
    estimated_timeline: str
    estimated_cost: str
    strategic_value: str
    prerequisite_frameworks: List[str]
    business_drivers: List[str]
    implementation_phases: List[Dict[str, Any]]
    roi_factors: List[str]
    risk_mitigation: List[str]

@dataclass
class CertificationPathway:
    pathway_name: str
    description: str
    total_timeline: str
    total_investment: str
    certification_sequence: List[CertificationRecommendation]
    synergy_benefits: List[str]
    success_probability: float

class CertificationRoadmapEngine:
    """
    Advanced certification roadmap engine with cross-framework optimization
    """
    
    def __init__(self):
        self.framework_profiles = self._initialize_framework_profiles()
        self.industry_requirements = self._initialize_industry_requirements()
        self.synergy_matrix = self._initialize_synergy_matrix()
        self.cost_models = self._initialize_cost_models()
        
    def _initialize_framework_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive framework profiles"""
        return {
            "iso_27001": {
                "name": "ISO 27001:2022 Information Security Management System",
                "type": "Management System",
                "global_recognition": 95,
                "implementation_complexity": 8,  # 1-10 scale
                "maintenance_effort": 7,
                "typical_timeline": "12-18 months",
                "cost_range": (15000, 75000),  # Annual
                "prerequisites": [],
                "target_industries": ["all"],
                "business_drivers": [
                    "Global market access",
                    "Customer trust and confidence", 
                    "Risk management framework",
                    "Competitive differentiation",
                    "Insurance premium reduction",
                    "Third-party risk management"
                ],
                "technical_requirements": [
                    "Information security policy framework",
                    "Risk management process",
                    "Asset management program",
                    "Access control systems",
                    "Incident management process",
                    "Business continuity planning"
                ],
                "certification_body": "Accredited ISO certification body",
                "surveillance_frequency": "Annual",
                "certificate_validity": "3 years"
            },
            
            "soc2": {
                "name": "SOC 2 Type II Trust Service Criteria",
                "type": "Assurance Report",
                "global_recognition": 85,
                "implementation_complexity": 7,
                "maintenance_effort": 8,
                "typical_timeline": "6-12 months",
                "cost_range": (25000, 150000),
                "prerequisites": ["Established internal controls"],
                "target_industries": ["Technology", "SaaS", "Cloud Services", "Financial Services"],
                "business_drivers": [
                    "Customer requirement for SaaS/cloud services",
                    "Competitive necessity in technology sector",
                    "Vendor assessment streamlining",
                    "Sales enablement tool",
                    "Trust and transparency demonstration"
                ],
                "technical_requirements": [
                    "Security control framework",
                    "Change management process",
                    "Logical access controls",
                    "System monitoring and logging",
                    "Incident response procedures",
                    "Data backup and recovery"
                ],
                "certification_body": "Licensed CPA firm",
                "surveillance_frequency": "Annual",
                "certificate_validity": "1 year (Type II report)"
            },
            
            "nist_sp_800_53": {
                "name": "NIST SP 800-53 Rev 5 Security Controls",
                "type": "Control Framework",
                "global_recognition": 90,
                "implementation_complexity": 9,
                "maintenance_effort": 9,
                "typical_timeline": "18-36 months",
                "cost_range": (50000, 200000),
                "prerequisites": ["Strong technical security foundation"],
                "target_industries": ["Government", "Defense", "Critical Infrastructure"],
                "business_drivers": [
                    "Federal government contracts",
                    "FedRAMP authorization requirement",
                    "Critical infrastructure protection",
                    "Defense contractor compliance",
                    "Comprehensive security framework"
                ],
                "technical_requirements": [
                    "Comprehensive control implementation",
                    "Continuous monitoring program",
                    "Configuration management",
                    "Vulnerability management",
                    "Incident response capability",
                    "Supply chain risk management"
                ],
                "certification_body": "FedRAMP authorization or self-attestation",
                "surveillance_frequency": "Continuous monitoring",
                "certificate_validity": "Ongoing with annual reviews"
            },
            
            "privacy_act": {
                "name": "Privacy Act 1988 (Commonwealth)",
                "type": "Legal Compliance",
                "global_recognition": 60,
                "implementation_complexity": 5,
                "maintenance_effort": 6,
                "typical_timeline": "3-6 months",
                "cost_range": (5000, 30000),
                "prerequisites": ["Privacy policy", "Data mapping"],
                "target_industries": ["All Australian organizations"],
                "business_drivers": [
                    "Legal compliance requirement",
                    "OAIC audit preparation",
                    "Data breach penalty avoidance",
                    "Customer privacy protection",
                    "Cross-border data transfer compliance"
                ],
                "technical_requirements": [
                    "Privacy policy framework",
                    "Consent management systems",
                    "Data subject rights processes",
                    "Breach notification procedures",
                    "Data retention and deletion",
                    "Cross-border transfer controls"
                ],
                "certification_body": "Self-certification with OAIC oversight",
                "surveillance_frequency": "As needed",
                "certificate_validity": "Ongoing compliance"
            },
            
            "essential_eight": {
                "name": "ACSC Essential Eight Maturity",
                "type": "Technical Controls",
                "global_recognition": 70,
                "implementation_complexity": 6,
                "maintenance_effort": 7,
                "typical_timeline": "6-12 months",
                "cost_range": (10000, 50000),
                "prerequisites": ["Basic IT infrastructure"],
                "target_industries": ["Government", "Critical Infrastructure", "Technology"],
                "business_drivers": [
                    "Australian government requirements",
                    "Critical infrastructure protection",
                    "Cyber security baseline",
                    "ACSC alignment",
                    "Threat mitigation"
                ],
                "technical_requirements": [
                    "Application control implementation",
                    "Patch management program",
                    "Microsoft Office macro configuration",
                    "User application hardening",
                    "Administrative privilege restriction",
                    "Operating system patching",
                    "Multi-factor authentication",
                    "Regular backup procedures"
                ],
                "certification_body": "Self-assessment with ACSC alignment",
                "surveillance_frequency": "Annual self-assessment",
                "certificate_validity": "Ongoing maintenance"
            },
            
            "nist_csf": {
                "name": "NIST Cybersecurity Framework",
                "type": "Risk Management Framework",
                "global_recognition": 85,
                "implementation_complexity": 6,
                "maintenance_effort": 6,
                "typical_timeline": "9-15 months",
                "cost_range": (20000, 80000),
                "prerequisites": ["Basic risk management process"],
                "target_industries": ["Critical Infrastructure", "Financial Services", "Technology"],
                "business_drivers": [
                    "Risk management maturity",
                    "Cybersecurity framework alignment",
                    "Industry best practices",
                    "Board-level reporting",
                    "Vendor assessment criteria"
                ],
                "technical_requirements": [
                    "Asset identification and management",
                    "Risk assessment methodology",
                    "Protective controls implementation",
                    "Detection capabilities",
                    "Incident response planning",
                    "Recovery procedures"
                ],
                "certification_body": "Various third-party assessors",
                "surveillance_frequency": "Annual assessment",
                "certificate_validity": "Assessment-specific"
            }
        }
    
    def _initialize_industry_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Initialize industry-specific framework requirements"""
        return {
            "Technology": {
                "mandatory": ["soc2"],
                "highly_recommended": ["iso_27001"],
                "recommended": ["nist_csf"],
                "market_drivers": [
                    "Customer due diligence requirements",
                    "Competitive necessity",
                    "Investor requirements",
                    "Global market access"
                ]
            },
            "Financial Services": {
                "mandatory": ["privacy_act", "soc2"],
                "highly_recommended": ["iso_27001", "nist_sp_800_53"],
                "recommended": ["nist_csf"],
                "market_drivers": [
                    "Regulatory compliance",
                    "Customer trust",
                    "Risk management",
                    "Operational resilience"
                ]
            },
            "Healthcare": {
                "mandatory": ["privacy_act"],
                "highly_recommended": ["iso_27001"],
                "recommended": ["soc2", "nist_csf"],
                "market_drivers": [
                    "Patient data protection",
                    "Regulatory compliance",
                    "Trust and confidence",
                    "Risk mitigation"
                ]
            },
            "Government": {
                "mandatory": ["essential_eight", "privacy_act"],
                "highly_recommended": ["nist_sp_800_53", "iso_27001"],
                "recommended": ["nist_csf"],
                "market_drivers": [
                    "Government requirements",
                    "Security baseline",
                    "Public trust",
                    "Critical infrastructure protection"
                ]
            },
            "Manufacturing": {
                "mandatory": [],
                "highly_recommended": ["iso_27001"],
                "recommended": ["essential_eight", "nist_csf"],
                "market_drivers": [
                    "Operational technology security",
                    "Supply chain requirements",
                    "Industrial control systems",
                    "Business continuity"
                ]
            }
        }
    
    def _initialize_synergy_matrix(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Initialize framework synergy and integration benefits"""
        return {
            "iso_27001": {
                "soc2": {
                    "synergy_score": 85,
                    "shared_controls": [
                        "Access control management",
                        "Change management",
                        "Incident response",
                        "Risk management",
                        "Security monitoring"
                    ],
                    "efficiency_gain": 40,  # Percentage reduction in implementation effort
                    "documentation_overlap": 60,
                    "audit_synergy": "ISO 27001 ISMS provides strong foundation for SOC 2 Security criteria"
                },
                "nist_sp_800_53": {
                    "synergy_score": 90,
                    "shared_controls": [
                        "Access Control (AC)",
                        "Audit and Accountability (AU)",
                        "Configuration Management (CM)",
                        "Incident Response (IR)",
                        "Risk Assessment (RA)"
                    ],
                    "efficiency_gain": 50,
                    "documentation_overlap": 70,
                    "audit_synergy": "Many ISO 27001 Annex A controls map directly to NIST controls"
                },
                "essential_eight": {
                    "synergy_score": 75,
                    "shared_controls": [
                        "Application control",
                        "Patch management",
                        "Access control",
                        "Backup procedures"
                    ],
                    "efficiency_gain": 30,
                    "documentation_overlap": 40,
                    "audit_synergy": "Essential Eight technical controls complement ISO 27001 Annex A requirements"
                }
            },
            "soc2": {
                "privacy_act": {
                    "synergy_score": 70,
                    "shared_controls": [
                        "Data access controls",
                        "Privacy policy framework",
                        "Incident response",
                        "Data retention"
                    ],
                    "efficiency_gain": 35,
                    "documentation_overlap": 45,
                    "audit_synergy": "Privacy controls directly support SOC 2 Privacy Trust Service Criteria"
                },
                "nist_csf": {
                    "synergy_score": 80,
                    "shared_controls": [
                        "Asset management",
                        "Risk assessment", 
                        "Protective controls",
                        "Detection systems",
                        "Response procedures"
                    ],
                    "efficiency_gain": 45,
                    "documentation_overlap": 55,
                    "audit_synergy": "SOC 2 security controls align with NIST CSF implementation"
                }
            }
        }
    
    def _initialize_cost_models(self) -> Dict[str, Dict[str, Any]]:
        """Initialize cost modeling for different organization sizes"""
        return {
            "small": {  # < 50 employees
                "multiplier": 0.6,
                "complexity_reduction": 0.7,
                "timeline_reduction": 0.8
            },
            "medium": {  # 50-500 employees
                "multiplier": 1.0,
                "complexity_reduction": 1.0,
                "timeline_reduction": 1.0
            },
            "large": {  # 500-2000 employees
                "multiplier": 1.5,
                "complexity_reduction": 1.2,
                "timeline_reduction": 1.2
            },
            "enterprise": {  # 2000+ employees
                "multiplier": 2.0,
                "complexity_reduction": 1.5,
                "timeline_reduction": 1.4
            }
        }
    
    def generate_certification_roadmap(self, 
                                     company_profile: Dict[str, Any],
                                     assessment_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive certification roadmap with cross-framework optimization
        """
        try:
            logger.info(f"Generating certification roadmap for {company_profile.get('name', 'organization')}")
            
            # Analyze company characteristics
            company_analysis = self._analyze_company_profile(company_profile)
            
            # Generate framework recommendations
            framework_recommendations = self._generate_framework_recommendations(
                company_analysis, assessment_results
            )
            
            # Optimize certification pathways
            optimal_pathways = self._optimize_certification_pathways(
                framework_recommendations, company_analysis
            )
            
            # Calculate investment analysis
            investment_analysis = self._calculate_investment_analysis(
                optimal_pathways, company_analysis
            )
            
            # Generate timeline and milestones
            implementation_timeline = self._generate_implementation_timeline(
                optimal_pathways, company_analysis
            )
            
            return {
                "company_analysis": company_analysis,
                "framework_recommendations": framework_recommendations,
                "optimal_pathways": optimal_pathways,
                "investment_analysis": investment_analysis,
                "implementation_timeline": implementation_timeline,
                "success_factors": self._identify_success_factors(company_analysis),
                "risk_mitigation": self._identify_risk_mitigation_strategies(company_analysis),
                "generated_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating certification roadmap: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_company_profile(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze company profile for roadmap optimization"""
        
        # Determine company size category
        employee_count = company_profile.get('employee_count', 100)
        if employee_count < 50:
            size_category = "small"
        elif employee_count < 500:
            size_category = "medium"
        elif employee_count < 2000:
            size_category = "large"
        else:
            size_category = "enterprise"
        
        # Analyze industry requirements
        industry = company_profile.get('industry', 'Other')
        industry_reqs = self.industry_requirements.get(industry, self.industry_requirements['Technology'])
        
        # Assess current maturity
        current_maturity = self._assess_overall_maturity(company_profile)
        
        # Identify business drivers
        business_drivers = self._identify_business_drivers(company_profile, industry)
        
        return {
            "company_name": company_profile.get('name', 'Organization'),
            "size_category": size_category,
            "employee_count": employee_count,
            "industry": industry,
            "industry_requirements": industry_reqs,
            "current_maturity": current_maturity,
            "business_drivers": business_drivers,
            "geographic_scope": company_profile.get('geographic_scope', ['Australia']),
            "existing_certifications": company_profile.get('existing_certifications', []),
            "budget_category": self._estimate_budget_category(size_category),
            "risk_tolerance": company_profile.get('risk_tolerance', 'Medium'),
            "timeline_preference": company_profile.get('timeline_preference', 'Balanced')
        }
    
    def _assess_overall_maturity(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall organizational maturity"""
        
        # Basic maturity indicators
        maturity_score = 50  # Base score
        
        # Adjust based on company characteristics
        if company_profile.get('employee_count', 0) > 500:
            maturity_score += 15
        
        if company_profile.get('industry') in ['Financial Services', 'Technology', 'Healthcare']:
            maturity_score += 10
        
        if company_profile.get('existing_certifications'):
            maturity_score += 20
        
        # Determine maturity level
        if maturity_score >= 80:
            level = "Advanced"
        elif maturity_score >= 65:
            level = "Intermediate"
        elif maturity_score >= 50:
            level = "Developing"
        else:
            level = "Basic"
        
        return {
            "overall_score": maturity_score,
            "maturity_level": level,
            "strengths": self._identify_maturity_strengths(company_profile),
            "development_areas": self._identify_development_areas(company_profile)
        }
    
    def _identify_maturity_strengths(self, company_profile: Dict[str, Any]) -> List[str]:
        """Identify organizational maturity strengths"""
        strengths = []
        
        if company_profile.get('employee_count', 0) > 100:
            strengths.append("Sufficient organizational scale for formal processes")
        
        if company_profile.get('industry') in ['Financial Services', 'Technology']:
            strengths.append("Industry experience with compliance requirements")
        
        if company_profile.get('existing_certifications'):
            strengths.append("Experience with certification processes")
        
        return strengths
    
    def _identify_development_areas(self, company_profile: Dict[str, Any]) -> List[str]:
        """Identify areas requiring development"""
        areas = []
        
        if company_profile.get('employee_count', 0) < 50:
            areas.append("Resource allocation for compliance activities")
        
        if not company_profile.get('existing_certifications'):
            areas.append("Certification process experience and methodology")
        
        return areas
    
    def _identify_business_drivers(self, company_profile: Dict[str, Any], industry: str) -> List[str]:
        """Identify key business drivers for certification"""
        drivers = []
        
        # Industry-specific drivers
        industry_reqs = self.industry_requirements.get(industry, {})
        if industry_reqs.get('market_drivers'):
            drivers.extend(industry_reqs['market_drivers'])
        
        # Company-specific drivers
        if company_profile.get('geographic_scope') and 'International' in company_profile['geographic_scope']:
            drivers.append("International market access")
        
        if company_profile.get('customer_requirements_compliance', False):
            drivers.append("Customer compliance requirements")
        
        return list(set(drivers))  # Remove duplicates
    
    def _estimate_budget_category(self, size_category: str) -> str:
        """Estimate budget category based on company size"""
        budget_mapping = {
            "small": "Conservative ($50K-$150K annually)",
            "medium": "Moderate ($100K-$300K annually)", 
            "large": "Substantial ($250K-$750K annually)",
            "enterprise": "Comprehensive ($500K-$1.5M annually)"
        }
        return budget_mapping.get(size_category, "Moderate")
    
    def _generate_framework_recommendations(self, 
                                          company_analysis: Dict[str, Any],
                                          assessment_results: Dict[str, Dict[str, Any]]) -> List[CertificationRecommendation]:
        """Generate prioritized framework recommendations"""
        
        recommendations = []
        industry = company_analysis['industry']
        size_category = company_analysis['size_category']
        
        # Get industry requirements
        industry_reqs = company_analysis['industry_requirements']
        
        # Generate recommendations for each relevant framework
        for framework_name, framework_profile in self.framework_profiles.items():
            
            # Check if framework is relevant for industry
            if self._is_framework_relevant(framework_name, industry, industry_reqs):
                
                # Get assessment results for this framework
                assessment = assessment_results.get(framework_name, {})
                readiness_score = assessment.get('overall_score', 0)
                
                # Calculate priority
                priority = self._calculate_framework_priority(
                    framework_name, readiness_score, industry_reqs, company_analysis
                )
                
                # Adjust costs for company size
                cost_model = self.cost_models[size_category]
                min_cost, max_cost = framework_profile['cost_range']
                adjusted_min = int(min_cost * cost_model['multiplier'])
                adjusted_max = int(max_cost * cost_model['multiplier'])
                estimated_cost = f"${adjusted_min:,} - ${adjusted_max:,} annually"
                
                # Adjust timeline for company size
                timeline_multiplier = cost_model['timeline_reduction']
                estimated_timeline = self._adjust_timeline(
                    framework_profile['typical_timeline'], timeline_multiplier
                )
                
                # Determine strategic value
                strategic_value = self._determine_strategic_value(
                    framework_name, industry, company_analysis
                )
                
                # Create recommendation
                recommendation = CertificationRecommendation(
                    framework_name=framework_profile['name'],
                    priority=priority,
                    readiness_score=readiness_score,
                    estimated_timeline=estimated_timeline,
                    estimated_cost=estimated_cost,
                    strategic_value=strategic_value,
                    prerequisite_frameworks=framework_profile.get('prerequisites', []),
                    business_drivers=framework_profile['business_drivers'],
                    implementation_phases=self._generate_implementation_phases(framework_name, readiness_score),
                    roi_factors=self._identify_roi_factors(framework_name, company_analysis),
                    risk_mitigation=self._identify_framework_risk_mitigation(framework_name)
                )
                
                recommendations.append(recommendation)
        
        # Sort by priority and readiness
        recommendations.sort(key=lambda x: (
            self._priority_to_numeric(x.priority),
            -x.readiness_score
        ))
        
        return recommendations
    
    def _is_framework_relevant(self, framework_name: str, industry: str, 
                             industry_reqs: Dict[str, List[str]]) -> bool:
        """Determine if framework is relevant for the organization"""
        
        # Check mandatory frameworks
        if framework_name in industry_reqs.get('mandatory', []):
            return True
        
        # Check highly recommended frameworks
        if framework_name in industry_reqs.get('highly_recommended', []):
            return True
        
        # Check recommended frameworks
        if framework_name in industry_reqs.get('recommended', []):
            return True
        
        # Check if framework targets all industries
        framework_profile = self.framework_profiles.get(framework_name, {})
        if 'all' in framework_profile.get('target_industries', []):
            return True
        
        return False
    
    def _calculate_framework_priority(self, framework_name: str, readiness_score: float,
                                    industry_reqs: Dict[str, List[str]], 
                                    company_analysis: Dict[str, Any]) -> CertificationPriority:
        """Calculate framework certification priority"""
        
        # Check mandatory status
        if framework_name in industry_reqs.get('mandatory', []):
            if readiness_score >= 75:
                return CertificationPriority.HIGH
            else:
                return CertificationPriority.CRITICAL
        
        # Check highly recommended status
        if framework_name in industry_reqs.get('highly_recommended', []):
            if readiness_score >= 75:
                return CertificationPriority.HIGH
            else:
                return CertificationPriority.MEDIUM
        
        # Check recommended status
        if framework_name in industry_reqs.get('recommended', []):
            if readiness_score >= 80:
                return CertificationPriority.MEDIUM
            else:
                return CertificationPriority.LOW
        
        # Default priority based on readiness
        if readiness_score >= 85:
            return CertificationPriority.MEDIUM
        else:
            return CertificationPriority.LOW
    
    def _priority_to_numeric(self, priority: CertificationPriority) -> int:
        """Convert priority to numeric for sorting"""
        mapping = {
            CertificationPriority.CRITICAL: 1,
            CertificationPriority.HIGH: 2,
            CertificationPriority.MEDIUM: 3,
            CertificationPriority.LOW: 4,
            CertificationPriority.DEFERRED: 5
        }
        return mapping.get(priority, 6)
    
    def _adjust_timeline(self, base_timeline: str, multiplier: float) -> str:
        """Adjust timeline based on company size and complexity"""
        # Simple timeline adjustment - could be more sophisticated
        if multiplier < 1.0:
            return base_timeline  # Smaller organizations might be faster
        elif multiplier > 1.2:
            # Larger organizations take longer
            if "6-12" in base_timeline:
                return "9-18 months"
            elif "12-18" in base_timeline:
                return "15-24 months"
            elif "18-36" in base_timeline:
                return "24-48 months"
        
        return base_timeline
    
    def _determine_strategic_value(self, framework_name: str, industry: str,
                                 company_analysis: Dict[str, Any]) -> str:
        """Determine strategic value of framework for organization"""
        
        framework_profile = self.framework_profiles[framework_name]
        recognition = framework_profile['global_recognition']
        
        if recognition >= 90:
            return "Very High - Global recognition and market requirement"
        elif recognition >= 80:
            return "High - Strong market recognition and competitive advantage"
        elif recognition >= 70:
            return "Medium - Industry recognition and compliance value"
        else:
            return "Low - Specialized or limited recognition"
    
    def _generate_implementation_phases(self, framework_name: str, 
                                      readiness_score: float) -> List[Dict[str, Any]]:
        """Generate implementation phases for framework"""
        
        phases = []
        
        if readiness_score < 60:
            phases.append({
                "phase": "Foundation",
                "duration": "3-6 months",
                "description": "Establish fundamental processes and documentation",
                "key_activities": [
                    "Policy development",
                    "Process documentation",
                    "Role definition",
                    "Initial training"
                ]
            })
        
        if readiness_score < 80:
            phases.append({
                "phase": "Implementation", 
                "duration": "6-12 months",
                "description": "Implement controls and operational processes",
                "key_activities": [
                    "Control implementation",
                    "Process operationalization",
                    "Staff training",
                    "Internal testing"
                ]
            })
        
        phases.append({
            "phase": "Certification Preparation",
            "duration": "3-6 months", 
            "description": "Prepare for external assessment and certification",
            "key_activities": [
                "Gap remediation",
                "Evidence collection",
                "Pre-assessment audit",
                "Certification audit"
            ]
        })
        
        phases.append({
            "phase": "Maintenance",
            "duration": "Ongoing",
            "description": "Maintain certification and continuous improvement",
            "key_activities": [
                "Surveillance audits",
                "Continuous monitoring",
                "Process improvement",
                "Recertification"
            ]
        })
        
        return phases
    
    def _identify_roi_factors(self, framework_name: str, 
                            company_analysis: Dict[str, Any]) -> List[str]:
        """Identify ROI factors for framework certification"""
        
        common_roi_factors = [
            "Risk reduction and insurance premium savings",
            "Operational efficiency improvements",
            "Competitive advantage and market differentiation",
            "Customer trust and confidence enhancement"
        ]
        
        framework_specific = {
            "iso_27001": [
                "Global market access and credibility",
                "Systematic risk management framework",
                "Third-party assessment streamlining"
            ],
            "soc2": [
                "Sales enablement for technology services",
                "Customer due diligence satisfaction",
                "Vendor management efficiency"
            ],
            "privacy_act": [
                "Legal compliance and penalty avoidance",
                "Customer privacy trust",
                "Data breach cost reduction"
            ]
        }
        
        roi_factors = common_roi_factors.copy()
        roi_factors.extend(framework_specific.get(framework_name, []))
        
        return roi_factors
    
    def _identify_framework_risk_mitigation(self, framework_name: str) -> List[str]:
        """Identify risk mitigation benefits of framework"""
        
        framework_risks = {
            "iso_27001": [
                "Information security incident reduction",
                "Data breach prevention",
                "Business continuity assurance",
                "Regulatory compliance alignment"
            ],
            "soc2": [
                "Service delivery risk reduction",
                "Customer data protection",
                "Operational control assurance",
                "Trust service reliability"
            ],
            "privacy_act": [
                "Privacy breach penalty avoidance",
                "Data subject rights compliance",
                "Cross-border transfer risk management",
                "Regulatory investigation preparedness"
            ]
        }
        
        return framework_risks.get(framework_name, ["General compliance risk reduction"])
    
    def _optimize_certification_pathways(self, 
                                       recommendations: List[CertificationRecommendation],
                                       company_analysis: Dict[str, Any]) -> List[CertificationPathway]:
        """Optimize certification pathways for maximum efficiency"""
        
        pathways = []
        
        # Create different pathway strategies
        
        # Pathway 1: Priority-based sequential
        priority_pathway = self._create_priority_pathway(recommendations, company_analysis)
        pathways.append(priority_pathway)
        
        # Pathway 2: Synergy-optimized
        synergy_pathway = self._create_synergy_pathway(recommendations, company_analysis)
        pathways.append(synergy_pathway)
        
        # Pathway 3: Quick wins first
        quick_wins_pathway = self._create_quick_wins_pathway(recommendations, company_analysis)
        pathways.append(quick_wins_pathway)
        
        # Calculate success probability for each pathway
        for pathway in pathways:
            pathway.success_probability = self._calculate_pathway_success_probability(
                pathway, company_analysis
            )
        
        # Sort by success probability
        pathways.sort(key=lambda x: x.success_probability, reverse=True)
        
        return pathways
    
    def _create_priority_pathway(self, recommendations: List[CertificationRecommendation],
                               company_analysis: Dict[str, Any]) -> CertificationPathway:
        """Create priority-based pathway"""
        
        # Sort by priority and readiness
        sorted_recs = sorted(recommendations, key=lambda x: (
            self._priority_to_numeric(x.priority), -x.readiness_score
        ))
        
        total_timeline = self._calculate_total_timeline(sorted_recs)
        total_investment = self._calculate_total_investment(sorted_recs)
        synergy_benefits = self._calculate_pathway_synergies(sorted_recs)
        
        return CertificationPathway(
            pathway_name="Priority-Based Sequential",
            description="Pursue certifications in order of business priority and regulatory requirement",
            total_timeline=total_timeline,
            total_investment=total_investment,
            certification_sequence=sorted_recs,
            synergy_benefits=synergy_benefits,
            success_probability=0.0  # Will be calculated later
        )
    
    def _create_synergy_pathway(self, recommendations: List[CertificationRecommendation],
                              company_analysis: Dict[str, Any]) -> CertificationPathway:
        """Create synergy-optimized pathway"""
        
        # Find optimal sequence based on synergies
        optimized_sequence = self._optimize_for_synergies(recommendations)
        
        total_timeline = self._calculate_total_timeline(optimized_sequence, apply_synergy_reduction=True)
        total_investment = self._calculate_total_investment(optimized_sequence, apply_synergy_reduction=True)
        synergy_benefits = self._calculate_pathway_synergies(optimized_sequence)
        
        return CertificationPathway(
            pathway_name="Synergy-Optimized",
            description="Optimize certification sequence to maximize control overlap and efficiency gains",
            total_timeline=total_timeline,
            total_investment=total_investment,
            certification_sequence=optimized_sequence,
            synergy_benefits=synergy_benefits,
            success_probability=0.0
        )
    
    def _create_quick_wins_pathway(self, recommendations: List[CertificationRecommendation],
                                 company_analysis: Dict[str, Any]) -> CertificationPathway:
        """Create quick wins pathway"""
        
        # Sort by readiness score (highest first)
        quick_wins = sorted(recommendations, key=lambda x: x.readiness_score, reverse=True)
        
        total_timeline = self._calculate_total_timeline(quick_wins)
        total_investment = self._calculate_total_investment(quick_wins)
        synergy_benefits = ["Early certification success builds momentum", "Demonstrates capability and commitment"]
        
        return CertificationPathway(
            pathway_name="Quick Wins First",
            description="Pursue most ready certifications first to build momentum and demonstrate success",
            total_timeline=total_timeline,
            total_investment=total_investment,
            certification_sequence=quick_wins,
            synergy_benefits=synergy_benefits,
            success_probability=0.0
        )
    
    def _optimize_for_synergies(self, recommendations: List[CertificationRecommendation]) -> List[CertificationRecommendation]:
        """Optimize certification sequence for maximum synergies"""
        
        # Simple optimization - start with highest synergy pair
        optimized = []
        remaining = recommendations.copy()
        
        while remaining:
            if not optimized:
                # Start with highest priority
                next_cert = min(remaining, key=lambda x: self._priority_to_numeric(x.priority))
            else:
                # Find certification with highest synergy to already selected
                next_cert = self._find_highest_synergy_cert(optimized, remaining)
            
            optimized.append(next_cert)
            remaining.remove(next_cert)
        
        return optimized
    
    def _find_highest_synergy_cert(self, selected: List[CertificationRecommendation],
                                 remaining: List[CertificationRecommendation]) -> CertificationRecommendation:
        """Find certification with highest synergy to already selected certifications"""
        
        best_cert = remaining[0]
        best_synergy_score = 0
        
        for cert in remaining:
            total_synergy = 0
            for selected_cert in selected:
                synergy_score = self._get_synergy_score(selected_cert.framework_name, cert.framework_name)
                total_synergy += synergy_score
            
            if total_synergy > best_synergy_score:
                best_synergy_score = total_synergy
                best_cert = cert
        
        return best_cert
    
    def _get_synergy_score(self, framework1: str, framework2: str) -> float:
        """Get synergy score between two frameworks"""
        
        # Convert display names to internal keys
        key1 = self._framework_name_to_key(framework1)
        key2 = self._framework_name_to_key(framework2)
        
        if key1 in self.synergy_matrix and key2 in self.synergy_matrix[key1]:
            return self.synergy_matrix[key1][key2]['synergy_score']
        elif key2 in self.synergy_matrix and key1 in self.synergy_matrix[key2]:
            return self.synergy_matrix[key2][key1]['synergy_score']
        else:
            return 0
    
    def _framework_name_to_key(self, framework_name: str) -> str:
        """Convert framework display name to internal key"""
        name_mapping = {
            "ISO 27001:2022 Information Security Management System": "iso_27001",
            "SOC 2 Type II Trust Service Criteria": "soc2",
            "NIST SP 800-53 Rev 5 Security Controls": "nist_sp_800_53",
            "Privacy Act 1988 (Commonwealth)": "privacy_act",
            "ACSC Essential Eight Maturity": "essential_eight",
            "NIST Cybersecurity Framework": "nist_csf"
        }
        return name_mapping.get(framework_name, framework_name.lower().replace(' ', '_'))
    
    def _calculate_total_timeline(self, recommendations: List[CertificationRecommendation],
                                apply_synergy_reduction: bool = False) -> str:
        """Calculate total implementation timeline"""
        
        # Simple calculation - assumes some parallel work possible
        if not recommendations:
            return "0 months"
        
        # Parse timeline from first recommendation
        first_timeline = recommendations[0].estimated_timeline
        
        if len(recommendations) == 1:
            return first_timeline
        elif len(recommendations) <= 3:
            return "18-36 months"
        else:
            return "24-48 months"
    
    def _calculate_total_investment(self, recommendations: List[CertificationRecommendation],
                                  apply_synergy_reduction: bool = False) -> str:
        """Calculate total investment estimate"""
        
        total_min = 0
        total_max = 0
        
        for rec in recommendations:
            # Parse cost range
            cost_str = rec.estimated_cost.replace('$', '').replace(',', '').replace(' annually', '')
            if ' - ' in cost_str:
                try:
                    min_cost, max_cost = cost_str.split(' - ')
                    total_min += int(min_cost)
                    total_max += int(max_cost)
                except:
                    pass
        
        if apply_synergy_reduction and len(recommendations) > 1:
            # Apply efficiency gains from synergies
            reduction_factor = 0.85  # 15% reduction
            total_min = int(total_min * reduction_factor)
            total_max = int(total_max * reduction_factor)
        
        if total_min > 0 and total_max > 0:
            return f"${total_min:,} - ${total_max:,} annually"
        else:
            return "Cost varies by implementation approach"
    
    def _calculate_pathway_synergies(self, recommendations: List[CertificationRecommendation]) -> List[str]:
        """Calculate synergy benefits for pathway"""
        
        synergies = []
        
        if len(recommendations) >= 2:
            synergies.append("Shared documentation and evidence collection")
            synergies.append("Common control implementation efforts")
        
        if len(recommendations) >= 3:
            synergies.append("Integrated risk management framework")
            synergies.append("Consolidated audit and assessment activities")
        
        return synergies
    
    def _calculate_pathway_success_probability(self, pathway: CertificationPathway,
                                             company_analysis: Dict[str, Any]) -> float:
        """Calculate success probability for pathway"""
        
        base_probability = 0.7  # Base 70% success rate
        
        # Adjust based on company maturity
        maturity_score = company_analysis['current_maturity']['overall_score']
        if maturity_score >= 80:
            base_probability += 0.2
        elif maturity_score >= 65:
            base_probability += 0.1
        elif maturity_score < 50:
            base_probability -= 0.1
        
        # Adjust based on pathway characteristics
        if "Quick Wins" in pathway.pathway_name:
            base_probability += 0.15  # Higher success with ready frameworks
        
        if "Synergy" in pathway.pathway_name:
            base_probability += 0.1   # Efficiency gains improve success
        
        # Adjust based on number of certifications
        cert_count = len(pathway.certification_sequence)
        if cert_count > 4:
            base_probability -= 0.1  # More complexity reduces success probability
        
        return min(0.95, max(0.3, base_probability))  # Bound between 30% and 95%
    
    def _calculate_investment_analysis(self, pathways: List[CertificationPathway],
                                     company_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive investment analysis"""
        
        if not pathways:
            return {}
        
        recommended_pathway = pathways[0]  # Highest success probability
        
        return {
            "recommended_pathway": recommended_pathway.pathway_name,
            "total_investment": recommended_pathway.total_investment,
            "timeline": recommended_pathway.total_timeline,
            "success_probability": f"{recommended_pathway.success_probability:.1%}",
            "roi_timeline": "18-36 months to realize significant benefits",
            "break_even_analysis": self._calculate_break_even(recommended_pathway, company_analysis),
            "risk_factors": self._identify_investment_risks(recommended_pathway, company_analysis),
            "cost_optimization_opportunities": self._identify_cost_optimizations(recommended_pathway)
        }
    
    def _calculate_break_even(self, pathway: CertificationPathway,
                            company_analysis: Dict[str, Any]) -> str:
        """Calculate break-even timeline for certification investment"""
        
        # Simplified break-even calculation
        size_category = company_analysis['size_category']
        
        if size_category == "small":
            return "2-3 years through insurance savings and efficiency gains"
        elif size_category == "medium":
            return "18-30 months through new business and operational efficiency"
        else:
            return "12-24 months through risk reduction and market opportunities"
    
    def _identify_investment_risks(self, pathway: CertificationPathway,
                                 company_analysis: Dict[str, Any]) -> List[str]:
        """Identify investment risks"""
        
        risks = []
        
        if company_analysis['current_maturity']['maturity_level'] == "Basic":
            risks.append("Limited organizational maturity may require additional foundational investment")
        
        if len(pathway.certification_sequence) > 3:
            risks.append("Complex multi-certification pathway may strain resources")
        
        if company_analysis['size_category'] == "small":
            risks.append("Resource constraints may impact implementation timeline")
        
        return risks
    
    def _identify_cost_optimizations(self, pathway: CertificationPathway) -> List[str]:
        """Identify cost optimization opportunities"""
        
        optimizations = []
        
        if len(pathway.certification_sequence) > 1:
            optimizations.append("Leverage shared controls and documentation across frameworks")
            optimizations.append("Coordinate audit activities to reduce assessment costs")
        
        optimizations.append("Phase implementation to spread costs over time")
        optimizations.append("Consider gap assessment before full implementation")
        
        return optimizations
    
    def _generate_implementation_timeline(self, pathways: List[CertificationPathway],
                                        company_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed implementation timeline"""
        
        if not pathways:
            return {}
        
        recommended_pathway = pathways[0]
        
        # Generate quarterly milestones
        milestones = []
        start_date = datetime.now()
        
        for i, cert in enumerate(recommended_pathway.certification_sequence):
            cert_start = start_date + timedelta(days=i * 180)  # 6-month stagger
            cert_end = cert_start + timedelta(days=365)  # Assume 12-month certification process
            
            milestones.append({
                "framework": cert.framework_name,
                "start_date": cert_start.strftime("%Y-%m-%d"),
                "target_completion": cert_end.strftime("%Y-%m-%d"),
                "key_phases": cert.implementation_phases,
                "critical_path_items": [
                    "Leadership commitment and resource allocation",
                    "Documentation development and approval",
                    "Control implementation and testing",
                    "Pre-assessment and gap remediation",
                    "Certification audit"
                ]
            })
        
        return {
            "pathway_name": recommended_pathway.pathway_name,
            "total_duration": recommended_pathway.total_timeline,
            "certification_milestones": milestones,
            "resource_requirements": self._calculate_resource_requirements(recommended_pathway, company_analysis),
            "success_factors": self._identify_timeline_success_factors(),
            "risk_mitigation": self._identify_timeline_risks()
        }
    
    def _calculate_resource_requirements(self, pathway: CertificationPathway,
                                       company_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate resource requirements for pathway"""
        
        size_category = company_analysis['size_category']
        
        # Base resource requirements by company size
        resource_mapping = {
            "small": {
                "dedicated_fte": "0.5-1.0 FTE",
                "project_management": "0.25 FTE",
                "external_consulting": "25-50 days annually",
                "training_budget": "$10K-25K"
            },
            "medium": {
                "dedicated_fte": "1.0-2.0 FTE", 
                "project_management": "0.5 FTE",
                "external_consulting": "50-100 days annually",
                "training_budget": "$25K-50K"
            },
            "large": {
                "dedicated_fte": "2.0-3.0 FTE",
                "project_management": "1.0 FTE", 
                "external_consulting": "75-150 days annually",
                "training_budget": "$50K-100K"
            },
            "enterprise": {
                "dedicated_fte": "3.0-5.0 FTE",
                "project_management": "1.5 FTE",
                "external_consulting": "100-200 days annually", 
                "training_budget": "$100K-200K"
            }
        }
        
        base_requirements = resource_mapping.get(size_category, resource_mapping["medium"])
        
        # Adjust for number of certifications
        cert_count = len(pathway.certification_sequence)
        if cert_count > 2:
            multiplier = min(1.5, 1.0 + (cert_count - 2) * 0.2)
            for key, value in base_requirements.items():
                if "FTE" in value:
                    # Adjust FTE requirements
                    pass  # Keep as-is for now
                elif "$" in value:
                    # Adjust budget requirements
                    pass  # Keep as-is for now
        
        return base_requirements
    
    def _identify_timeline_success_factors(self) -> List[str]:
        """Identify critical success factors for timeline adherence"""
        
        return [
            "Strong executive sponsorship and resource commitment",
            "Dedicated project management and coordination",
            "Early engagement with certification bodies",
            "Proactive gap identification and remediation",
            "Cross-functional team collaboration",
            "Regular progress monitoring and adjustment"
        ]
    
    def _identify_timeline_risks(self) -> List[str]:
        """Identify timeline risks and mitigation strategies"""
        
        return [
            "Resource allocation conflicts with other priorities",
            "Longer than expected gap remediation requirements",
            "Certification body scheduling constraints",
            "Technical implementation complexity",
            "Change management and adoption challenges"
        ]
    
    def _identify_success_factors(self, company_analysis: Dict[str, Any]) -> List[str]:
        """Identify critical success factors for certification program"""
        
        return [
            "Executive leadership commitment and visible support",
            "Adequate resource allocation and dedicated team members",
            "Clear communication of benefits and requirements",
            "Systematic project management and milestone tracking",
            "Early identification and resolution of implementation gaps",
            "Cultural change management and staff engagement",
            "Regular progress review and course correction"
        ]
    
    def _identify_risk_mitigation_strategies(self, company_analysis: Dict[str, Any]) -> List[str]:
        """Identify risk mitigation strategies"""
        
        return [
            "Conduct preliminary gap assessments before committing to certification",
            "Engage experienced consultants for complex implementations",
            "Phase implementation to manage resource demands",
            "Establish clear roles, responsibilities, and accountability",
            "Implement change management program for organizational adoption",
            "Plan for contingencies and timeline buffers",
            "Regular risk assessment and mitigation planning"
        ]