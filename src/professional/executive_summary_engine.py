"""
Executive Summary Engine for Enterprise-Grade PDF Reports
========================================================

Generates strategic executive summaries that match Big 4 consulting standards.
Provides business impact analysis, risk quantification, and actionable recommendations.

Author: Sentinel GRC Platform
Version: 1.0.0-enterprise
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import statistics
import math

logger = logging.getLogger(__name__)

@dataclass
class BusinessImpact:
    """Business impact metrics for executive summary"""
    current_risk_exposure: str
    remediation_investment: str
    roi_timeline: str
    certification_timeline: str
    competitive_advantage: str

@dataclass
class StrategicRecommendation:
    """Strategic recommendation with business context"""
    title: str
    description: str
    business_rationale: str
    timeline: str
    investment: str
    risk_level: str
    expected_outcome: str

@dataclass
class ExecutiveSummary:
    """Complete executive summary for enterprise reports"""
    assessment_overview: str
    key_findings: List[str]
    compliance_score: int
    business_impact: BusinessImpact
    strategic_recommendations: List[StrategicRecommendation]
    critical_actions: List[str]
    next_steps: List[str]
    executive_talking_points: List[str]

class ExecutiveSummaryEngine:
    """
    Generates executive summaries that match Big 4 consulting quality standards
    """
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.cost_models = self._load_cost_models()
        self.risk_quantification = self._load_risk_models()
        
        # Executive communication patterns
        self.executive_phrases = {
            "positive": [
                "demonstrates strong commitment to security governance",
                "positions the organization competitively",
                "enables sustainable growth and market expansion",
                "reduces regulatory exposure and operational risk",
                "strengthens stakeholder confidence and trust"
            ],
            "concern": [
                "requires immediate executive attention",
                "presents material risk to business operations",
                "could impact customer trust and market position",
                "may result in regulatory scrutiny or penalties",
                "needs strategic investment to address gaps"
            ],
            "neutral": [
                "follows industry standard practices",
                "aligns with regulatory expectations",
                "supports ongoing business operations",
                "maintains baseline security posture",
                "requires continued monitoring and improvement"
            ]
        }
    
    def generate_executive_summary(self, 
                                 assessment_data: Dict[str, Any],
                                 framework: str,
                                 customer_context: Dict[str, Any]) -> ExecutiveSummary:
        """
        Generate comprehensive executive summary
        """
        logger.info(f"Generating executive summary for {framework} assessment")
        
        # Calculate core metrics
        compliance_score = self._calculate_compliance_score(assessment_data)
        risk_level = self._assess_overall_risk(assessment_data)
        industry = customer_context.get('industry', 'general')
        company_size = customer_context.get('size', 'medium')
        
        # Generate each section
        overview = self._generate_assessment_overview(framework, compliance_score, industry)
        key_findings = self._generate_key_findings(assessment_data, framework, compliance_score)
        business_impact = self._calculate_business_impact(assessment_data, industry, company_size)
        strategic_recs = self._generate_strategic_recommendations(assessment_data, framework, business_impact)
        critical_actions = self._identify_critical_actions(assessment_data)
        next_steps = self._generate_next_steps(framework, compliance_score)
        talking_points = self._generate_executive_talking_points(compliance_score, business_impact, framework)
        
        return ExecutiveSummary(
            assessment_overview=overview,
            key_findings=key_findings,
            compliance_score=compliance_score,
            business_impact=business_impact,
            strategic_recommendations=strategic_recs,
            critical_actions=critical_actions,
            next_steps=next_steps,
            executive_talking_points=talking_points
        )
    
    def _calculate_compliance_score(self, assessment_data: Dict[str, Any]) -> int:
        """Calculate overall compliance score"""
        try:
            controls = assessment_data.get('controls', [])
            if not controls:
                return 0
            
            total_controls = len(controls)
            passing_controls = sum(1 for control in controls 
                                 if control.get('status') in ['implemented', 'compliant', 'effective'])
            
            score = int((passing_controls / total_controls) * 100) if total_controls > 0 else 0
            
            # Add weighted scoring for critical controls
            critical_controls = [c for c in controls if c.get('criticality') == 'high']
            if critical_controls:
                critical_passing = sum(1 for c in critical_controls 
                                     if c.get('status') in ['implemented', 'compliant', 'effective'])
                critical_score = (critical_passing / len(critical_controls)) * 100
                
                # Weight: 70% overall, 30% critical controls
                score = int((score * 0.7) + (critical_score * 0.3))
            
            return max(0, min(100, score))
            
        except Exception as e:
            logger.warning(f"Error calculating compliance score: {e}")
            return 0
    
    def _assess_overall_risk(self, assessment_data: Dict[str, Any]) -> str:
        """Assess overall organizational risk level"""
        try:
            findings = assessment_data.get('findings', [])
            
            critical_findings = sum(1 for f in findings if f.get('severity') == 'critical')
            high_findings = sum(1 for f in findings if f.get('severity') == 'high')
            medium_findings = sum(1 for f in findings if f.get('severity') == 'medium')
            
            # Risk scoring algorithm
            risk_score = (critical_findings * 10) + (high_findings * 5) + (medium_findings * 2)
            
            if risk_score >= 50:
                return "critical"
            elif risk_score >= 25:
                return "high"
            elif risk_score >= 10:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            logger.warning(f"Error assessing risk: {e}")
            return "medium"
    
    def _generate_assessment_overview(self, framework: str, compliance_score: int, industry: str) -> str:
        """Generate assessment overview paragraph"""
        
        framework_context = {
            "SOC 2": "SOC 2 Type II examination of security, availability, and confidentiality controls",
            "ISO 27001": "ISO 27001:2022 Information Security Management System (ISMS) assessment",
            "NIST CSF": "NIST Cybersecurity Framework implementation evaluation",
            "Essential 8": "Australian Government Essential Eight security controls assessment",
            "NIST SP 800-53": "NIST SP 800-53 security controls compliance evaluation"
        }
        
        industry_context = {
            "healthcare": "healthcare industry regulatory requirements and risk landscape",
            "financial": "financial services regulatory environment and threat profile",
            "technology": "technology sector security standards and market expectations",
            "manufacturing": "operational technology and industrial control system security",
            "retail": "payment card industry and customer data protection requirements"
        }
        
        score_assessment = ""
        if compliance_score >= 90:
            score_assessment = "demonstrates exceptional security maturity and readiness for certification"
        elif compliance_score >= 80:
            score_assessment = "shows strong security foundations with targeted improvements needed"
        elif compliance_score >= 70:
            score_assessment = "indicates developing security program requiring strategic investment"
        elif compliance_score >= 60:
            score_assessment = "reveals significant gaps requiring immediate executive attention"
        else:
            score_assessment = "identifies critical deficiencies requiring comprehensive remediation"
        
        return f"""
        This report presents a comprehensive assessment of the organization's security and compliance posture 
        against {framework_context.get(framework, f'{framework} compliance requirements')}. The evaluation was 
        conducted using industry-standard methodologies and considers the {industry_context.get(industry, 'industry-specific')} 
        context. With an overall compliance score of {compliance_score}%, the organization 
        {score_assessment}. This assessment provides strategic recommendations for achieving certification, 
        reducing risk exposure, and establishing sustainable compliance practices that support business objectives.
        """.strip()
    
    def _generate_key_findings(self, assessment_data: Dict[str, Any], framework: str, compliance_score: int) -> List[str]:
        """Generate top 3-5 key findings for executive summary"""
        findings = []
        
        try:
            # Analyze assessment data for key patterns
            controls = assessment_data.get('controls', [])
            issues = assessment_data.get('findings', [])
            
            # Finding 1: Overall compliance status
            if compliance_score >= 85:
                findings.append(f"Strong compliance foundation with {compliance_score}% of controls implemented - certification achievable within 6-8 weeks")
            elif compliance_score >= 70:
                findings.append(f"Solid security baseline at {compliance_score}% compliance - strategic gaps require 3-4 months remediation")
            else:
                findings.append(f"Significant compliance gaps at {compliance_score}% - comprehensive program required over 6-12 months")
            
            # Finding 2: Critical vulnerabilities
            critical_issues = [f for f in issues if f.get('severity') == 'critical']
            if critical_issues:
                findings.append(f"{len(critical_issues)} critical security deficiencies requiring immediate remediation to prevent operational disruption")
            
            # Finding 3: Quick wins identification
            easy_fixes = [c for c in controls if c.get('effort') == 'low' and c.get('status') != 'implemented']
            if easy_fixes:
                findings.append(f"{len(easy_fixes)} quick-win opportunities identified that could improve compliance by 15-20% within 4 weeks")
            
            # Finding 4: Framework-specific insights
            if framework == "SOC 2":
                findings.append("Access management and logging controls require enhancement to meet Type II examination standards")
            elif framework == "ISO 27001":
                findings.append("Information security policies and risk management procedures need alignment with ISO 27001:2022 requirements")
            elif framework == "NIST CSF":
                findings.append("Incident response and recovery capabilities require strengthening to achieve target maturity levels")
            
            # Finding 5: Business impact
            high_business_impact = [f for f in issues if f.get('business_impact') == 'high']
            if high_business_impact:
                findings.append(f"{len(high_business_impact)} findings directly impact business operations and customer trust")
            
            return findings[:5]  # Limit to top 5 findings
            
        except Exception as e:
            logger.warning(f"Error generating key findings: {e}")
            return [
                f"Compliance assessment completed for {framework}",
                f"Overall compliance score: {compliance_score}%",
                "Detailed findings and recommendations provided in full report"
            ]
    
    def _calculate_business_impact(self, assessment_data: Dict[str, Any], industry: str, company_size: str) -> BusinessImpact:
        """Calculate business impact metrics"""
        try:
            # Industry-specific fine calculations
            industry_fines = {
                "healthcare": {"base": 1000000, "per_record": 50},
                "financial": {"base": 2000000, "per_record": 100},
                "technology": {"base": 500000, "per_record": 25},
                "retail": {"base": 750000, "per_record": 30}
            }
            
            # Company size multipliers
            size_multipliers = {
                "small": 0.5,
                "medium": 1.0,
                "large": 2.0,
                "enterprise": 3.0
            }
            
            base_fine = industry_fines.get(industry, {"base": 500000, "per_record": 25})["base"]
            size_mult = size_multipliers.get(company_size, 1.0)
            
            # Risk exposure calculation
            findings = assessment_data.get('findings', [])
            critical_findings = len([f for f in findings if f.get('severity') == 'critical'])
            high_findings = len([f for f in findings if f.get('severity') == 'high'])
            
            risk_multiplier = 1 + (critical_findings * 0.5) + (high_findings * 0.2)
            estimated_exposure = int(base_fine * size_mult * risk_multiplier)
            
            # Remediation cost calculation
            controls = assessment_data.get('controls', [])
            failing_controls = [c for c in controls if c.get('status') != 'implemented']
            
            cost_per_control = 5000  # Base estimate
            total_remediation = len(failing_controls) * cost_per_control
            
            # ROI timeline calculation
            months_to_roi = max(6, min(24, int(total_remediation / 50000)))
            
            return BusinessImpact(
                current_risk_exposure=f"${estimated_exposure:,} potential regulatory fine exposure",
                remediation_investment=f"${total_remediation:,} total implementation investment required",
                roi_timeline=f"Break-even achieved in {months_to_roi} months through risk reduction and operational efficiency",
                certification_timeline=f"Certification achievable in {max(8, len(failing_controls) // 10)} weeks with focused remediation",
                competitive_advantage="Certification enables access to enterprise customers requiring compliance validation"
            )
            
        except Exception as e:
            logger.warning(f"Error calculating business impact: {e}")
            return BusinessImpact(
                current_risk_exposure="Material regulatory and operational risk exposure",
                remediation_investment="Strategic investment required for compliance program",
                roi_timeline="ROI achieved through risk reduction and operational efficiency",
                certification_timeline="Certification timeline dependent on remediation scope",
                competitive_advantage="Compliance enables market expansion and customer trust"
            )
    
    def _generate_strategic_recommendations(self, assessment_data: Dict[str, Any], 
                                          framework: str, business_impact: BusinessImpact) -> List[StrategicRecommendation]:
        """Generate strategic recommendations for executives"""
        recommendations = []
        
        try:
            findings = assessment_data.get('findings', [])
            controls = assessment_data.get('controls', [])
            
            # Recommendation 1: Quick wins
            quick_wins = [f for f in findings if f.get('effort') == 'low' and f.get('impact') == 'high']
            if quick_wins:
                recommendations.append(StrategicRecommendation(
                    title="Immediate Quick Wins Implementation",
                    description=f"Address {len(quick_wins)} high-impact, low-effort security improvements",
                    business_rationale="Rapid compliance improvement with minimal resource investment",
                    timeline="4-6 weeks",
                    investment="$25,000 - $50,000",
                    risk_level="Low",
                    expected_outcome="15-25% compliance improvement, enhanced security posture"
                ))
            
            # Recommendation 2: Critical gaps
            critical_gaps = [f for f in findings if f.get('severity') == 'critical']
            if critical_gaps:
                recommendations.append(StrategicRecommendation(
                    title="Critical Security Gap Remediation",
                    description=f"Resolve {len(critical_gaps)} critical security deficiencies",
                    business_rationale="Prevent operational disruption and regulatory violations",
                    timeline="8-12 weeks",
                    investment="$75,000 - $150,000",
                    risk_level="High if not addressed",
                    expected_outcome="Eliminates major risk exposure, enables certification path"
                ))
            
            # Recommendation 3: Framework-specific strategic initiative
            if framework == "SOC 2":
                recommendations.append(StrategicRecommendation(
                    title="SOC 2 Type II Certification Program",
                    description="Implement comprehensive SOC 2 compliance program",
                    business_rationale="Enables enterprise customer acquisition and market expansion",
                    timeline="6-9 months",
                    investment="$100,000 - $200,000",
                    risk_level="Medium",
                    expected_outcome="SOC 2 Type II certification, enterprise sales enablement"
                ))
            elif framework == "ISO 27001":
                recommendations.append(StrategicRecommendation(
                    title="ISO 27001 ISMS Implementation",
                    description="Establish mature Information Security Management System",
                    business_rationale="Global market access and enterprise customer requirements",
                    timeline="9-12 months",
                    investment="$150,000 - $300,000",
                    risk_level="Medium",
                    expected_outcome="ISO 27001 certification, international market access"
                ))
            
            # Recommendation 4: Continuous improvement
            recommendations.append(StrategicRecommendation(
                title="Continuous Compliance Program",
                description="Establish ongoing monitoring and improvement processes",
                business_rationale="Sustain compliance, reduce audit costs, enable business agility",
                timeline="Ongoing",
                investment="$50,000 annually",
                risk_level="Low",
                expected_outcome="Sustained compliance, reduced audit burden, operational efficiency"
            ))
            
            return recommendations[:4]  # Limit to top 4 recommendations
            
        except Exception as e:
            logger.warning(f"Error generating strategic recommendations: {e}")
            return [
                StrategicRecommendation(
                    title="Compliance Program Enhancement",
                    description="Implement strategic security improvements",
                    business_rationale="Risk reduction and regulatory compliance",
                    timeline="3-6 months",
                    investment="Strategic investment required",
                    risk_level="Medium",
                    expected_outcome="Improved security posture and compliance"
                )
            ]
    
    def _identify_critical_actions(self, assessment_data: Dict[str, Any]) -> List[str]:
        """Identify actions requiring immediate attention"""
        critical_actions = []
        
        try:
            findings = assessment_data.get('findings', [])
            
            # Critical severity findings
            critical_findings = [f for f in findings if f.get('severity') == 'critical']
            for finding in critical_findings[:3]:  # Top 3 critical
                action = f"Address {finding.get('title', 'critical security gap')} within 2 weeks"
                critical_actions.append(action)
            
            # High business impact items
            high_impact = [f for f in findings if f.get('business_impact') == 'high']
            for finding in high_impact[:2]:  # Top 2 high impact
                action = f"Implement {finding.get('title', 'high-impact control')} within 4 weeks"
                critical_actions.append(action)
            
            # Default critical actions if none found
            if not critical_actions:
                critical_actions = [
                    "Review and approve security policy updates within 1 week",
                    "Assign compliance program ownership and resources within 2 weeks",
                    "Initiate vendor selection for security tool gaps within 3 weeks"
                ]
            
            return critical_actions[:5]  # Limit to 5 actions
            
        except Exception as e:
            logger.warning(f"Error identifying critical actions: {e}")
            return [
                "Review assessment findings with security team",
                "Prioritize remediation activities based on risk",
                "Allocate budget for compliance improvements"
            ]
    
    def _generate_next_steps(self, framework: str, compliance_score: int) -> List[str]:
        """Generate next steps for the organization"""
        next_steps = []
        
        # Timeline-based next steps
        if compliance_score >= 85:
            next_steps = [
                "Schedule pre-assessment with certified auditor within 4 weeks",
                "Complete remaining control implementations (6-8 weeks)",
                "Conduct internal audit and remediate gaps (2-3 weeks)",
                "Begin formal certification audit process (8-12 weeks)"
            ]
        elif compliance_score >= 70:
            next_steps = [
                "Develop detailed remediation project plan (1-2 weeks)",
                "Secure executive sponsorship and budget approval (2-3 weeks)",
                "Implement high-priority controls (8-12 weeks)",
                "Conduct quarterly progress reviews and adjustments"
            ]
        else:
            next_steps = [
                "Establish compliance program governance structure (2 weeks)",
                "Conduct detailed gap analysis and risk assessment (4 weeks)",
                "Develop multi-phase implementation roadmap (2 weeks)",
                "Begin foundational security control implementation (12+ weeks)"
            ]
        
        # Framework-specific next steps
        framework_steps = {
            "SOC 2": "Engage SOC 2 audit firm for readiness assessment",
            "ISO 27001": "Select ISO 27001 certification body and schedule Stage 1 audit",
            "NIST CSF": "Align remediation plan with NIST CSF implementation tiers",
            "Essential 8": "Report progress to Australian Cyber Security Centre (ACSC)"
        }
        
        if framework in framework_steps:
            next_steps.append(framework_steps[framework])
        
        return next_steps
    
    def _generate_executive_talking_points(self, compliance_score: int, 
                                         business_impact: BusinessImpact, framework: str) -> List[str]:
        """Generate talking points for executive communications"""
        talking_points = []
        
        # Board/investor talking points
        if compliance_score >= 80:
            talking_points.append(f"Security program demonstrates strong governance with {compliance_score}% compliance achievement")
            talking_points.append("Organization positioned competitively for enterprise customer acquisition")
        else:
            talking_points.append(f"Strategic security investment required to address {100-compliance_score}% compliance gap")
            talking_points.append("Remediation program will strengthen market position and reduce risk exposure")
        
        # Customer/partner talking points
        talking_points.extend([
            f"Active {framework} compliance program demonstrates commitment to security excellence",
            "Continuous improvement approach ensures sustained protection of customer data",
            "Investment in security infrastructure supports business growth and customer trust"
        ])
        
        # Regulatory/compliance talking points
        talking_points.extend([
            "Proactive compliance approach demonstrates due diligence and risk management",
            "Regular assessments and improvements align with regulatory expectations",
            "Documentation and evidence collection supports audit readiness"
        ])
        
        return talking_points
    
    def _load_industry_benchmarks(self) -> Dict[str, Any]:
        """Load industry benchmark data"""
        # In production, this would load from database or API
        return {
            "healthcare": {"avg_compliance": 78, "certification_time": 8},
            "financial": {"avg_compliance": 82, "certification_time": 6},
            "technology": {"avg_compliance": 75, "certification_time": 10},
            "manufacturing": {"avg_compliance": 70, "certification_time": 12},
            "retail": {"avg_compliance": 72, "certification_time": 10}
        }
    
    def _load_cost_models(self) -> Dict[str, Any]:
        """Load cost estimation models"""
        # In production, this would load from database or cost modeling service
        return {
            "control_implementation": 5000,
            "policy_development": 2000,
            "training_per_person": 500,
            "audit_preparation": 10000,
            "certification_costs": 25000
        }
    
    def _load_risk_models(self) -> Dict[str, Any]:
        """Load risk quantification models"""
        # In production, this would load from risk database
        return {
            "data_breach_cost": 4240000,  # Average cost per breach
            "regulatory_fine_rates": {
                "GDPR": 20000000,  # Up to €20M
                "HIPAA": 1500000,  # Up to $1.5M
                "SOX": 5000000,    # Up to $5M
                "PCI_DSS": 500000  # Up to $500K
            }
        }


# Example usage for testing
if __name__ == "__main__":
    # Sample assessment data for testing
    sample_assessment = {
        "controls": [
            {"id": "AC-1", "status": "implemented", "criticality": "high", "effort": "low"},
            {"id": "AC-2", "status": "partial", "criticality": "medium", "effort": "medium"},
            {"id": "AC-3", "status": "not_implemented", "criticality": "high", "effort": "high"}
        ],
        "findings": [
            {"title": "Multi-factor authentication gaps", "severity": "critical", "business_impact": "high", "effort": "low"},
            {"title": "Logging configuration issues", "severity": "high", "business_impact": "medium", "effort": "medium"},
            {"title": "Access review procedures", "severity": "medium", "business_impact": "low", "effort": "low"}
        ]
    }
    
    customer_context = {
        "industry": "technology",
        "size": "medium",
        "name": "TechCorp Inc"
    }
    
    # Initialize engine and generate summary
    engine = ExecutiveSummaryEngine()
    summary = engine.generate_executive_summary(
        assessment_data=sample_assessment,
        framework="SOC 2",
        customer_context=customer_context
    )
    
    print("Executive Summary Generated:")
    print(f"Compliance Score: {summary.compliance_score}%")
    print(f"Key Findings: {len(summary.key_findings)}")
    print(f"Strategic Recommendations: {len(summary.strategic_recommendations)}")
    print(f"Business Impact: {summary.business_impact.current_risk_exposure}")