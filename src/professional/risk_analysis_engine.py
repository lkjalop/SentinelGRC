"""
Risk Analysis Engine for Enterprise PDF Reports
==============================================

Provides comprehensive risk analysis, scoring, and visualization data
for enterprise-grade compliance reports. Integrates with executive summary
and professional visualization systems.

Author: Sentinel GRC Platform
Version: 1.0.0-enterprise
"""

import json
import logging
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"

class ImpactCategory(Enum):
    """Business impact categories"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    REPUTATION = "reputation"
    REGULATORY = "regulatory"
    STRATEGIC = "strategic"

@dataclass
class RiskMetric:
    """Individual risk metric"""
    category: str
    description: str
    current_score: float
    target_score: float
    impact_level: RiskLevel
    mitigation_priority: int
    cost_to_remediate: int
    timeline_weeks: int

@dataclass
class RiskHeatMapData:
    """Data for risk heat map visualization"""
    risk_items: List[Dict[str, Any]]
    likelihood_axis: List[str]
    impact_axis: List[str]
    color_matrix: List[List[str]]
    
@dataclass
class ComplianceMatrix:
    """Compliance matrix data for visualization"""
    frameworks: List[str]
    control_categories: List[str]
    compliance_scores: List[List[int]]
    gap_analysis: List[List[str]]

@dataclass
class RiskAnalysisReport:
    """Complete risk analysis for enterprise reports"""
    overall_risk_score: float
    risk_level: RiskLevel
    risk_metrics: List[RiskMetric]
    heat_map_data: RiskHeatMapData
    compliance_matrix: ComplianceMatrix
    trend_analysis: Dict[str, Any]
    benchmarking_data: Dict[str, Any]
    risk_appetite_analysis: Dict[str, Any]
    residual_risk_assessment: Dict[str, Any]

class RiskAnalysisEngine:
    """
    Advanced risk analysis engine for enterprise compliance reporting
    """
    
    def __init__(self):
        self.risk_weights = self._initialize_risk_weights()
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.regulatory_impacts = self._load_regulatory_impacts()
        self.cost_models = self._load_cost_models()
        
        # Risk scoring algorithms
        self.scoring_algorithms = {
            "NIST": self._calculate_nist_risk_score,
            "ISO": self._calculate_iso_risk_score,
            "FAIR": self._calculate_fair_risk_score,
            "OCTAVE": self._calculate_octave_risk_score
        }
    
    def generate_risk_analysis(self, 
                             assessment_data: Dict[str, Any],
                             framework: str,
                             customer_context: Dict[str, Any],
                             algorithm: str = "NIST") -> RiskAnalysisReport:
        """
        Generate comprehensive risk analysis report
        """
        logger.info(f"Generating risk analysis using {algorithm} methodology")
        
        # Calculate overall risk metrics
        overall_score = self._calculate_overall_risk_score(assessment_data, algorithm)
        risk_level = self._determine_risk_level(overall_score)
        
        # Generate detailed risk metrics
        risk_metrics = self._generate_risk_metrics(assessment_data, customer_context)
        
        # Create visualization data
        heat_map_data = self._generate_heat_map_data(assessment_data, framework)
        compliance_matrix = self._generate_compliance_matrix(assessment_data, framework)
        
        # Generate analysis components
        trend_analysis = self._generate_trend_analysis(assessment_data)
        benchmarking = self._generate_benchmarking_data(assessment_data, customer_context)
        risk_appetite = self._analyze_risk_appetite(assessment_data, customer_context)
        residual_risk = self._assess_residual_risk(assessment_data, risk_metrics)
        
        return RiskAnalysisReport(
            overall_risk_score=overall_score,
            risk_level=risk_level,
            risk_metrics=risk_metrics,
            heat_map_data=heat_map_data,
            compliance_matrix=compliance_matrix,
            trend_analysis=trend_analysis,
            benchmarking_data=benchmarking,
            risk_appetite_analysis=risk_appetite,
            residual_risk_assessment=residual_risk
        )
    
    def _calculate_overall_risk_score(self, assessment_data: Dict[str, Any], algorithm: str) -> float:
        """Calculate overall organizational risk score"""
        try:
            scoring_func = self.scoring_algorithms.get(algorithm, self._calculate_nist_risk_score)
            return scoring_func(assessment_data)
        except Exception as e:
            logger.warning(f"Error calculating risk score: {e}")
            return 5.0  # Default medium risk
    
    def _calculate_nist_risk_score(self, assessment_data: Dict[str, Any]) -> float:
        """NIST-based risk scoring (1-10 scale)"""
        try:
            findings = assessment_data.get('findings', [])
            controls = assessment_data.get('controls', [])
            
            # Threat likelihood (1-10)
            threat_indicators = len([f for f in findings if 'vulnerability' in f.get('type', '').lower()])
            likelihood = min(10, max(1, 3 + (threat_indicators * 0.5)))
            
            # Impact assessment (1-10)
            critical_assets = len([c for c in controls if c.get('criticality') == 'high'])
            failing_critical = len([c for c in controls 
                                  if c.get('criticality') == 'high' and c.get('status') != 'implemented'])
            
            impact = 1
            if critical_assets > 0:
                impact = min(10, max(1, 3 + (failing_critical / critical_assets) * 7))
            
            # Risk = Likelihood × Impact (scaled to 1-10)
            risk_score = (likelihood * impact) / 10
            
            return round(min(10, max(1, risk_score)), 1)
            
        except Exception as e:
            logger.warning(f"Error in NIST risk calculation: {e}")
            return 5.0
    
    def _calculate_iso_risk_score(self, assessment_data: Dict[str, Any]) -> float:
        """ISO 27005-based risk scoring"""
        try:
            # Simplified ISO risk assessment
            findings = assessment_data.get('findings', [])
            
            # Asset criticality impact
            asset_scores = []
            for finding in findings:
                criticality = finding.get('asset_criticality', 'medium')
                score_map = {'low': 2, 'medium': 5, 'high': 8, 'critical': 10}
                asset_scores.append(score_map.get(criticality, 5))
            
            # Threat probability
            threat_scores = []
            for finding in findings:
                probability = finding.get('threat_probability', 'possible')
                prob_map = {'rare': 1, 'unlikely': 3, 'possible': 5, 'likely': 7, 'certain': 10}
                threat_scores.append(prob_map.get(probability, 5))
            
            if asset_scores and threat_scores:
                avg_asset = statistics.mean(asset_scores)
                avg_threat = statistics.mean(threat_scores)
                risk_score = (avg_asset + avg_threat) / 2
            else:
                risk_score = 5.0
            
            return round(min(10, max(1, risk_score)), 1)
            
        except Exception as e:
            logger.warning(f"Error in ISO risk calculation: {e}")
            return 5.0
    
    def _calculate_fair_risk_score(self, assessment_data: Dict[str, Any]) -> float:
        """FAIR (Factor Analysis of Information Risk) scoring"""
        try:
            # FAIR focuses on frequency and magnitude
            findings = assessment_data.get('findings', [])
            
            # Contact frequency (threat events per year)
            contact_freq = len(findings) * 2  # Assume each finding represents 2 events/year
            
            # Probability of action (threat acts on contact)
            action_prob = 0.3  # 30% of contacts result in action
            
            # Vulnerability (probability of success)
            critical_vulns = len([f for f in findings if f.get('severity') == 'critical'])
            vulnerability = min(0.9, 0.1 + (critical_vulns * 0.1))
            
            # Loss event frequency
            loss_freq = contact_freq * action_prob * vulnerability
            
            # Loss magnitude (1-10 scale)
            avg_impact = 5  # Default medium impact
            if findings:
                impact_scores = []
                for finding in findings:
                    severity = finding.get('severity', 'medium')
                    impact_map = {'low': 2, 'medium': 5, 'high': 8, 'critical': 10}
                    impact_scores.append(impact_map.get(severity, 5))
                avg_impact = statistics.mean(impact_scores)
            
            # FAIR risk score (frequency × magnitude, normalized to 1-10)
            fair_score = min(10, (loss_freq * avg_impact) / 10)
            
            return round(max(1, fair_score), 1)
            
        except Exception as e:
            logger.warning(f"Error in FAIR risk calculation: {e}")
            return 5.0
    
    def _calculate_octave_risk_score(self, assessment_data: Dict[str, Any]) -> float:
        """OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation) scoring"""
        try:
            # OCTAVE focuses on organizational risk
            controls = assessment_data.get('controls', [])
            findings = assessment_data.get('findings', [])
            
            # Asset criticality
            critical_assets = len([c for c in controls if c.get('criticality') == 'high'])
            total_assets = len(controls) if controls else 1
            asset_criticality = (critical_assets / total_assets) * 10
            
            # Threat scenarios
            threat_scenarios = len(findings)
            threat_score = min(10, threat_scenarios)
            
            # Organizational vulnerabilities
            org_vulns = len([f for f in findings if 'process' in f.get('type', '').lower()])
            vuln_score = min(10, org_vulns * 2)
            
            # OCTAVE risk = weighted average
            octave_score = (asset_criticality * 0.4) + (threat_score * 0.3) + (vuln_score * 0.3)
            
            return round(min(10, max(1, octave_score)), 1)
            
        except Exception as e:
            logger.warning(f"Error in OCTAVE risk calculation: {e}")
            return 5.0
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determine risk level from numerical score"""
        if risk_score >= 8.5:
            return RiskLevel.CRITICAL
        elif risk_score >= 6.5:
            return RiskLevel.HIGH
        elif risk_score >= 4.0:
            return RiskLevel.MEDIUM
        elif risk_score >= 2.0:
            return RiskLevel.LOW
        else:
            return RiskLevel.NEGLIGIBLE
    
    def _generate_risk_metrics(self, assessment_data: Dict[str, Any], 
                             customer_context: Dict[str, Any]) -> List[RiskMetric]:
        """Generate detailed risk metrics by category"""
        metrics = []
        
        try:
            findings = assessment_data.get('findings', [])
            controls = assessment_data.get('controls', [])
            
            # Financial risk metrics
            financial_findings = [f for f in findings if 'financial' in f.get('impact_category', '').lower()]
            if financial_findings or any('financial' in str(f).lower() for f in findings):
                metrics.append(RiskMetric(
                    category="Financial",
                    description="Potential monetary losses from security incidents",
                    current_score=self._calculate_category_risk(financial_findings, 'financial'),
                    target_score=2.0,
                    impact_level=RiskLevel.HIGH,
                    mitigation_priority=1,
                    cost_to_remediate=150000,
                    timeline_weeks=12
                ))
            
            # Operational risk metrics
            operational_findings = [f for f in findings if 'operational' in f.get('impact_category', '').lower()]
            metrics.append(RiskMetric(
                category="Operational",
                description="Business disruption and service availability risks",
                current_score=self._calculate_category_risk(operational_findings, 'operational'),
                target_score=2.5,
                impact_level=RiskLevel.MEDIUM,
                mitigation_priority=2,
                cost_to_remediate=100000,
                timeline_weeks=8
            ))
            
            # Regulatory risk metrics
            regulatory_findings = [f for f in findings if 'compliance' in f.get('type', '').lower()]
            metrics.append(RiskMetric(
                category="Regulatory",
                description="Non-compliance fines and regulatory actions",
                current_score=self._calculate_category_risk(regulatory_findings, 'regulatory'),
                target_score=1.5,
                impact_level=RiskLevel.HIGH,
                mitigation_priority=1,
                cost_to_remediate=200000,
                timeline_weeks=16
            ))
            
            # Reputation risk metrics
            reputation_findings = [f for f in findings if f.get('severity') in ['critical', 'high']]
            metrics.append(RiskMetric(
                category="Reputation",
                description="Brand damage and customer trust erosion",
                current_score=self._calculate_category_risk(reputation_findings, 'reputation'),
                target_score=2.0,
                impact_level=RiskLevel.MEDIUM,
                mitigation_priority=3,
                cost_to_remediate=75000,
                timeline_weeks=6
            ))
            
            # Strategic risk metrics
            strategic_controls = [c for c in controls if c.get('strategic_importance', False)]
            metrics.append(RiskMetric(
                category="Strategic",
                description="Impact on competitive advantage and growth",
                current_score=self._calculate_strategic_risk(strategic_controls),
                target_score=2.5,
                impact_level=RiskLevel.MEDIUM,
                mitigation_priority=4,
                cost_to_remediate=125000,
                timeline_weeks=20
            ))
            
            return sorted(metrics, key=lambda x: x.mitigation_priority)
            
        except Exception as e:
            logger.warning(f"Error generating risk metrics: {e}")
            return [
                RiskMetric(
                    category="Overall",
                    description="General security and compliance risks",
                    current_score=5.0,
                    target_score=2.0,
                    impact_level=RiskLevel.MEDIUM,
                    mitigation_priority=1,
                    cost_to_remediate=100000,
                    timeline_weeks=12
                )
            ]
    
    def _calculate_category_risk(self, findings: List[Dict[str, Any]], category: str) -> float:
        """Calculate risk score for specific category"""
        if not findings:
            return 3.0  # Default medium-low risk
        
        severity_scores = {
            'critical': 10,
            'high': 8,
            'medium': 5,
            'low': 2
        }
        
        scores = [severity_scores.get(f.get('severity', 'medium'), 5) for f in findings]
        avg_score = statistics.mean(scores) if scores else 5
        
        # Apply category-specific weighting
        category_weights = {
            'financial': 1.2,
            'regulatory': 1.1,
            'operational': 1.0,
            'reputation': 0.9,
            'strategic': 0.8
        }
        
        weighted_score = avg_score * category_weights.get(category, 1.0)
        return round(min(10, max(1, weighted_score)), 1)
    
    def _calculate_strategic_risk(self, strategic_controls: List[Dict[str, Any]]) -> float:
        """Calculate strategic risk based on control implementation"""
        if not strategic_controls:
            return 4.0
        
        implemented = len([c for c in strategic_controls if c.get('status') == 'implemented'])
        total = len(strategic_controls)
        
        implementation_rate = implemented / total if total > 0 else 0
        risk_score = 10 * (1 - implementation_rate)
        
        return round(min(10, max(1, risk_score)), 1)
    
    def _generate_heat_map_data(self, assessment_data: Dict[str, Any], framework: str) -> RiskHeatMapData:
        """Generate data for risk heat map visualization"""
        try:
            findings = assessment_data.get('findings', [])
            
            # Create risk items for heat map
            risk_items = []
            for finding in findings:
                likelihood = self._map_to_likelihood(finding.get('probability', 'medium'))
                impact = self._map_to_impact(finding.get('severity', 'medium'))
                
                risk_items.append({
                    'name': finding.get('title', 'Security Finding'),
                    'likelihood': likelihood,
                    'impact': impact,
                    'severity': finding.get('severity', 'medium'),
                    'category': finding.get('category', 'general')
                })
            
            # Define axes
            likelihood_axis = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
            impact_axis = ['Negligible', 'Minor', 'Moderate', 'Major', 'Severe']
            
            # Generate color matrix for heat map
            color_matrix = self._generate_color_matrix()
            
            return RiskHeatMapData(
                risk_items=risk_items,
                likelihood_axis=likelihood_axis,
                impact_axis=impact_axis,
                color_matrix=color_matrix
            )
            
        except Exception as e:
            logger.warning(f"Error generating heat map data: {e}")
            return RiskHeatMapData(
                risk_items=[],
                likelihood_axis=['Low', 'Medium', 'High'],
                impact_axis=['Low', 'Medium', 'High'],
                color_matrix=[['green', 'yellow', 'red']]
            )
    
    def _generate_compliance_matrix(self, assessment_data: Dict[str, Any], framework: str) -> ComplianceMatrix:
        """Generate compliance matrix for cross-framework analysis"""
        try:
            controls = assessment_data.get('controls', [])
            
            # Map framework to common control categories
            framework_mappings = {
                'SOC 2': ['Security', 'Availability', 'Confidentiality', 'Processing Integrity', 'Privacy'],
                'ISO 27001': ['Information Security Policies', 'Organization of Information Security', 
                             'Human Resource Security', 'Asset Management', 'Access Control'],
                'NIST CSF': ['Identify', 'Protect', 'Detect', 'Respond', 'Recover'],
                'Essential 8': ['Application Control', 'Patch Applications', 'Configure Microsoft Office',
                               'User Application Hardening', 'Restrict Admin Privileges']
            }
            
            categories = framework_mappings.get(framework, ['Security', 'Compliance', 'Operations'])
            
            # Calculate compliance scores by category
            compliance_scores = []
            gap_analysis = []
            
            for category in categories:
                category_controls = [c for c in controls 
                                   if category.lower() in c.get('category', '').lower()]
                
                if category_controls:
                    implemented = len([c for c in category_controls 
                                     if c.get('status') == 'implemented'])
                    score = int((implemented / len(category_controls)) * 100)
                else:
                    score = 0
                
                compliance_scores.append([score])
                
                # Gap analysis
                if score >= 90:
                    gap_analysis.append(['Compliant'])
                elif score >= 70:
                    gap_analysis.append(['Minor Gaps'])
                elif score >= 50:
                    gap_analysis.append(['Moderate Gaps'])
                else:
                    gap_analysis.append(['Major Gaps'])
            
            return ComplianceMatrix(
                frameworks=[framework],
                control_categories=categories,
                compliance_scores=compliance_scores,
                gap_analysis=gap_analysis
            )
            
        except Exception as e:
            logger.warning(f"Error generating compliance matrix: {e}")
            return ComplianceMatrix(
                frameworks=[framework],
                control_categories=['Security'],
                compliance_scores=[[50]],
                gap_analysis=[['Assessment Required']]
            )
    
    def _generate_trend_analysis(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trend analysis data"""
        # In production, this would analyze historical data
        return {
            "risk_trend": "stable",
            "compliance_trend": "improving",
            "incident_frequency": "decreasing",
            "remediation_velocity": "increasing",
            "projected_compliance": {
                "3_months": 75,
                "6_months": 85,
                "12_months": 95
            }
        }
    
    def _generate_benchmarking_data(self, assessment_data: Dict[str, Any], 
                                  customer_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate industry benchmarking data"""
        industry = customer_context.get('industry', 'technology')
        
        # Industry benchmark data (would come from database in production)
        benchmarks = self.industry_benchmarks.get(industry, {
            "avg_compliance": 75,
            "avg_risk_score": 5.5,
            "avg_incidents": 12,
            "avg_remediation_time": 45
        })
        
        # Calculate current position vs benchmarks
        current_compliance = self._calculate_current_compliance(assessment_data)
        current_risk = self._calculate_overall_risk_score(assessment_data, "NIST")
        
        return {
            "industry": industry,
            "industry_avg_compliance": benchmarks["avg_compliance"],
            "current_compliance": current_compliance,
            "compliance_vs_industry": current_compliance - benchmarks["avg_compliance"],
            "industry_avg_risk": benchmarks["avg_risk_score"],
            "current_risk": current_risk,
            "risk_vs_industry": current_risk - benchmarks["avg_risk_score"],
            "percentile_ranking": self._calculate_percentile(current_compliance, industry)
        }
    
    def _analyze_risk_appetite(self, assessment_data: Dict[str, Any], 
                             customer_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze organizational risk appetite"""
        # Risk appetite analysis based on industry and company characteristics
        industry = customer_context.get('industry', 'technology')
        size = customer_context.get('size', 'medium')
        
        # Industry risk tolerances
        industry_tolerances = {
            'financial': {'max_risk': 3.0, 'target_risk': 1.5},
            'healthcare': {'max_risk': 3.5, 'target_risk': 2.0},
            'technology': {'max_risk': 5.0, 'target_risk': 3.0},
            'manufacturing': {'max_risk': 4.0, 'target_risk': 2.5}
        }
        
        tolerance = industry_tolerances.get(industry, {'max_risk': 4.0, 'target_risk': 2.5})
        current_risk = self._calculate_overall_risk_score(assessment_data, "NIST")
        
        return {
            "max_acceptable_risk": tolerance['max_risk'],
            "target_risk_level": tolerance['target_risk'],
            "current_risk_level": current_risk,
            "risk_appetite_status": "within_tolerance" if current_risk <= tolerance['max_risk'] else "exceeds_tolerance",
            "risk_reduction_needed": max(0, current_risk - tolerance['target_risk'])
        }
    
    def _assess_residual_risk(self, assessment_data: Dict[str, Any], 
                            risk_metrics: List[RiskMetric]) -> Dict[str, Any]:
        """Assess residual risk after planned mitigations"""
        current_risk = self._calculate_overall_risk_score(assessment_data, "NIST")
        
        # Calculate risk reduction from planned mitigations
        total_risk_reduction = 0
        for metric in risk_metrics:
            reduction = metric.current_score - metric.target_score
            weight = 1.0 / metric.mitigation_priority  # Higher priority = more weight
            total_risk_reduction += reduction * weight
        
        # Normalize risk reduction
        if risk_metrics:
            avg_reduction = total_risk_reduction / len(risk_metrics)
            residual_risk = max(1.0, current_risk - avg_reduction)
        else:
            residual_risk = current_risk
        
        return {
            "current_risk": current_risk,
            "residual_risk": residual_risk,
            "risk_reduction": current_risk - residual_risk,
            "residual_risk_level": self._determine_risk_level(residual_risk).value,
            "acceptable": residual_risk <= 3.0,
            "additional_controls_needed": residual_risk > 3.0
        }
    
    # Helper methods
    def _map_to_likelihood(self, probability: str) -> int:
        """Map probability string to numerical likelihood (1-5)"""
        mapping = {
            'very_low': 1, 'low': 2, 'medium': 3, 'high': 4, 'very_high': 5,
            'rare': 1, 'unlikely': 2, 'possible': 3, 'likely': 4, 'certain': 5
        }
        return mapping.get(probability.lower(), 3)
    
    def _map_to_impact(self, severity: str) -> int:
        """Map severity string to numerical impact (1-5)"""
        mapping = {
            'negligible': 1, 'minor': 2, 'moderate': 3, 'major': 4, 'severe': 5,
            'low': 2, 'medium': 3, 'high': 4, 'critical': 5
        }
        return mapping.get(severity.lower(), 3)
    
    def _generate_color_matrix(self) -> List[List[str]]:
        """Generate color matrix for risk heat map"""
        # 5x5 matrix: rows=impact, cols=likelihood
        return [
            ['#90EE90', '#90EE90', '#FFFF00', '#FFFF00', '#FFA500'],  # Negligible
            ['#90EE90', '#FFFF00', '#FFFF00', '#FFA500', '#FFA500'],  # Minor
            ['#FFFF00', '#FFFF00', '#FFA500', '#FFA500', '#FF6347'],  # Moderate
            ['#FFFF00', '#FFA500', '#FFA500', '#FF6347', '#FF0000'],  # Major
            ['#FFA500', '#FFA500', '#FF6347', '#FF0000', '#8B0000']   # Severe
        ]
    
    def _calculate_current_compliance(self, assessment_data: Dict[str, Any]) -> int:
        """Calculate current compliance percentage"""
        controls = assessment_data.get('controls', [])
        if not controls:
            return 0
        
        implemented = len([c for c in controls if c.get('status') == 'implemented'])
        return int((implemented / len(controls)) * 100)
    
    def _calculate_percentile(self, score: int, industry: str) -> int:
        """Calculate percentile ranking within industry"""
        # Simplified percentile calculation
        benchmarks = self.industry_benchmarks.get(industry, {"avg_compliance": 75})
        avg = benchmarks["avg_compliance"]
        
        if score >= avg + 20:
            return 90
        elif score >= avg + 10:
            return 75
        elif score >= avg:
            return 60
        elif score >= avg - 10:
            return 40
        else:
            return 25
    
    def _initialize_risk_weights(self) -> Dict[str, float]:
        """Initialize risk category weights"""
        return {
            "financial": 1.2,
            "regulatory": 1.1,
            "operational": 1.0,
            "reputation": 0.9,
            "strategic": 0.8
        }
    
    def _load_industry_benchmarks(self) -> Dict[str, Any]:
        """Load industry benchmark data"""
        return {
            "financial": {
                "avg_compliance": 82,
                "avg_risk_score": 4.2,
                "avg_incidents": 8,
                "avg_remediation_time": 30
            },
            "healthcare": {
                "avg_compliance": 78,
                "avg_risk_score": 4.8,
                "avg_incidents": 12,
                "avg_remediation_time": 35
            },
            "technology": {
                "avg_compliance": 75,
                "avg_risk_score": 5.2,
                "avg_incidents": 15,
                "avg_remediation_time": 25
            },
            "manufacturing": {
                "avg_compliance": 70,
                "avg_risk_score": 5.8,
                "avg_incidents": 18,
                "avg_remediation_time": 40
            }
        }
    
    def _load_regulatory_impacts(self) -> Dict[str, Any]:
        """Load regulatory impact data"""
        return {
            "GDPR": {"max_fine": 20000000, "avg_fine": 2000000},
            "HIPAA": {"max_fine": 1500000, "avg_fine": 500000},
            "SOX": {"max_fine": 5000000, "avg_fine": 1000000},
            "PCI_DSS": {"max_fine": 500000, "avg_fine": 100000}
        }
    
    def _load_cost_models(self) -> Dict[str, Any]:
        """Load cost estimation models"""
        return {
            "breach_cost_per_record": 150,
            "regulatory_fine_probability": 0.15,
            "reputation_damage_multiplier": 2.5,
            "business_disruption_cost_per_day": 50000
        }


# Example usage and testing
if __name__ == "__main__":
    # Sample assessment data
    sample_data = {
        "controls": [
            {"id": "AC-1", "status": "implemented", "criticality": "high", "category": "access_control"},
            {"id": "AC-2", "status": "partial", "criticality": "medium", "category": "access_control"},
            {"id": "AU-1", "status": "not_implemented", "criticality": "high", "category": "audit"}
        ],
        "findings": [
            {"title": "MFA gaps", "severity": "critical", "type": "access", "probability": "high"},
            {"title": "Log retention", "severity": "medium", "type": "audit", "probability": "medium"}
        ]
    }
    
    customer_context = {
        "industry": "technology",
        "size": "medium"
    }
    
    # Test risk analysis
    engine = RiskAnalysisEngine()
    analysis = engine.generate_risk_analysis(sample_data, "SOC 2", customer_context)
    
    print(f"Overall Risk Score: {analysis.overall_risk_score}")
    print(f"Risk Level: {analysis.risk_level.value}")
    print(f"Risk Metrics: {len(analysis.risk_metrics)}")
    print(f"Heat Map Items: {len(analysis.heat_map_data.risk_items)}")