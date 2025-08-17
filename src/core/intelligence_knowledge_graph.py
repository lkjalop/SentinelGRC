"""
Intelligence-Powered Knowledge Graph for Compliance Relationships
This is the restored "brain" of the Sentinel GRC platform
"""

import logging
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class ControlRelationship:
    """Represents a relationship between controls"""
    source_control: str
    target_control: str
    relationship_type: str  # 'requires', 'conflicts', 'supports', 'implements'
    strength: float  # 0.0 to 1.0
    frameworks: List[str]
    context: Dict[str, Any]

@dataclass 
class FrameworkMapping:
    """Cross-framework control mapping"""
    control_id: str
    framework: str
    equivalent_controls: List[Tuple[str, str, float]]  # (framework, control_id, similarity)
    implementation_guidance: str
    business_context: str

class IntelligenceKnowledgeGraph:
    """
    The restored intelligence core that understands compliance relationships
    This is what makes Sentinel GRC unique in the market
    """
    
    def __init__(self):
        self.neo4j_available = False
        self.driver = None
        self.fallback_graph = {}  # In-memory fallback
        
        # Try to initialize Neo4j connection
        self._initialize_neo4j()
        
        # Initialize the knowledge base
        self._initialize_intelligence_base()
        
        logger.info("🧠 Intelligence Knowledge Graph initialized")
    
    def _initialize_neo4j(self):
        """Initialize Neo4j connection with fallback to in-memory"""
        try:
            from neo4j import GraphDatabase
            from .secure_neo4j_config import get_secure_neo4j_config
            
            config = get_secure_neo4j_config()
            self.driver = GraphDatabase.driver(
                config.uri,
                auth=(config.username, config.password)
            )
            
            # Test connection
            self.driver.verify_connectivity()
            self.neo4j_available = True
            
            # Initialize schema
            self._initialize_neo4j_schema()
            
            logger.info("✅ Neo4j knowledge graph connected")
            
        except Exception as e:
            logger.warning(f"⚠️ Neo4j not available, using in-memory fallback: {e}")
            self.neo4j_available = False
    
    def _initialize_neo4j_schema(self):
        """Create Neo4j schema for compliance intelligence"""
        
        if not self.neo4j_available:
            return
            
        with self.driver.session() as session:
            # Create constraints for data integrity
            constraints = [
                "CREATE CONSTRAINT control_id_unique IF NOT EXISTS FOR (c:Control) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT framework_name_unique IF NOT EXISTS FOR (f:Framework) REQUIRE f.name IS UNIQUE", 
                "CREATE CONSTRAINT threat_id_unique IF NOT EXISTS FOR (t:Threat) REQUIRE t.id IS UNIQUE",
                "CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (org:Organization) REQUIRE org.id IS UNIQUE"
            ]
            
            # Create indexes for performance
            indexes = [
                "CREATE INDEX control_name_idx IF NOT EXISTS FOR (c:Control) ON (c.name)",
                "CREATE INDEX control_family_idx IF NOT EXISTS FOR (c:Control) ON (c.family)",
                "CREATE INDEX framework_type_idx IF NOT EXISTS FOR (f:Framework) ON (f.type)",
                "CREATE INDEX threat_severity_idx IF NOT EXISTS FOR (t:Threat) ON (t.severity)",
                "CREATE INDEX company_industry_idx IF NOT EXISTS FOR (org:Organization) ON (org.industry)"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    logger.debug(f"Constraint already exists or failed: {e}")
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    logger.debug(f"Index already exists or failed: {e}")
                    
            logger.info("🏗️ Neo4j schema initialized")
    
    def _initialize_intelligence_base(self):
        """Initialize the core compliance intelligence"""
        
        # Framework definitions with cross-references
        self.frameworks = {
            'nist_800_53': {
                'name': 'NIST SP 800-53',
                'type': 'security_controls',
                'domain': 'federal',
                'control_families': ['AC', 'AU', 'AT', 'CM', 'CP', 'IA', 'IR', 'MA', 'MP', 'PS', 'PE', 'PL', 'PM', 'RA', 'CA', 'SC', 'SI', 'SA', 'SR'],
                'total_controls': 1006
            },
            'iso_27001': {
                'name': 'ISO/IEC 27001:2022',
                'type': 'management_system',
                'domain': 'international',
                'control_families': ['A.5', 'A.6', 'A.7', 'A.8', 'A.9', 'A.10', 'A.11', 'A.12', 'A.13', 'A.14', 'A.15', 'A.16', 'A.17', 'A.18'],
                'total_controls': 114
            },
            'soc2': {
                'name': 'SOC 2 Type II',
                'type': 'audit_standard',
                'domain': 'commercial',
                'trust_principles': ['Security', 'Availability', 'Processing Integrity', 'Confidentiality', 'Privacy'],
                'total_controls': 64
            },
            'essential_eight': {
                'name': 'Essential Eight',
                'type': 'cybersecurity_framework',
                'domain': 'australia',
                'maturity_levels': ['Level 1', 'Level 2', 'Level 3'],
                'strategies': 8
            }
        }
        
        # Cross-framework control mappings (this is the intelligence!)
        self.control_mappings = {
            'access_control': {
                'nist_800_53': ['AC-2', 'AC-3', 'AC-5', 'AC-6'],
                'iso_27001': ['A.9.2.1', 'A.9.2.2', 'A.9.4.1'],
                'soc2': ['CC6.1', 'CC6.2', 'CC6.3'],
                'essential_eight': ['Strategy 5: Restrict Administrative Privileges']
            },
            'vulnerability_management': {
                'nist_800_53': ['SI-2', 'SI-3', 'SI-4', 'RA-5'],
                'iso_27001': ['A.12.6.1', 'A.14.2.3'],
                'soc2': ['CC7.1', 'CC7.2'],
                'essential_eight': ['Strategy 2: Patch Applications', 'Strategy 6: Patch Operating Systems']
            },
            'incident_response': {
                'nist_800_53': ['IR-1', 'IR-2', 'IR-4', 'IR-6', 'IR-8'],
                'iso_27001': ['A.16.1.1', 'A.16.1.2', 'A.16.1.4'],
                'soc2': ['CC7.4', 'CC7.5'],
                'essential_eight': ['Related to all strategies for detection and response']
            }
        }
        
        # Threat intelligence mappings
        self.threat_mappings = {
            'ransomware': {
                'severity': 'CRITICAL',
                'mitigated_by': ['access_control', 'vulnerability_management', 'backup_recovery'],
                'frameworks_addressing': ['nist_800_53', 'iso_27001', 'essential_eight']
            },
            'insider_threats': {
                'severity': 'HIGH',
                'mitigated_by': ['access_control', 'monitoring', 'hr_security'],
                'frameworks_addressing': ['nist_800_53', 'iso_27001', 'soc2']
            },
            'supply_chain_attacks': {
                'severity': 'HIGH', 
                'mitigated_by': ['vendor_management', 'code_integrity', 'vulnerability_management'],
                'frameworks_addressing': ['nist_800_53', 'iso_27001', 'soc2']
            }
        }
        
        logger.info("🎯 Intelligence base initialized with cross-framework mappings")
    
    async def get_dynamic_control_selection(self, 
                                          company_profile: Dict[str, Any],
                                          target_certification: str,
                                          risk_tolerance: str = "medium") -> Dict[str, Any]:
        """
        THE KILLER FEATURE: Dynamic control selection based on company context
        This is what no other platform can do!
        """
        
        logger.info(f"🎯 Generating dynamic control selection for {target_certification}")
        
        # Analyze company context
        industry = company_profile.get('industry', 'technology')
        employee_count = company_profile.get('employee_count', 100)
        cloud_usage = company_profile.get('cloud_usage', 'hybrid')
        regulatory_requirements = company_profile.get('regulatory_requirements', [])
        
        # Get base controls for certification
        base_controls = self._get_certification_controls(target_certification)
        
        # Apply intelligence-based prioritization
        prioritized_controls = []
        
        for control in base_controls:
            # Calculate control importance based on company context
            importance_score = self._calculate_control_importance(
                control, company_profile, target_certification
            )
            
            # Get implementation guidance specific to company
            guidance = self._get_contextual_guidance(control, company_profile)
            
            # Find cross-framework mappings
            cross_mappings = self._find_cross_framework_mappings(control, target_certification)
            
            # Estimate implementation effort and timeline
            implementation = self._estimate_implementation(control, company_profile)
            
            prioritized_controls.append({
                'control_id': control['id'],
                'title': control['title'],
                'description': control['description'],
                'importance_score': importance_score,
                'priority': self._score_to_priority(importance_score),
                'implementation_effort': implementation['effort'],
                'estimated_timeline': implementation['timeline'],
                'business_justification': guidance['business_rationale'],
                'technical_guidance': guidance['technical_steps'],
                'cross_framework_mappings': cross_mappings,
                'company_context': self._get_company_specific_context(control, company_profile)
            })
        
        # Sort by importance score
        prioritized_controls.sort(key=lambda x: x['importance_score'], reverse=True)
        
        # Create implementation roadmap
        roadmap = self._create_implementation_roadmap(prioritized_controls, company_profile)
        
        return {
            'certification': target_certification,
            'company_profile': company_profile,
            'total_controls': len(prioritized_controls),
            'high_priority_controls': len([c for c in prioritized_controls if c['priority'] == 'HIGH']),
            'estimated_total_timeline': roadmap['total_timeline'],
            'estimated_cost': roadmap['estimated_cost'],
            'prioritized_controls': prioritized_controls,
            'implementation_roadmap': roadmap,
            'intelligence_insights': self._generate_intelligence_insights(prioritized_controls, company_profile),
            'generated_at': datetime.now().isoformat()
        }
    
    def _get_certification_controls(self, certification: str) -> List[Dict[str, Any]]:
        """Get base controls for a certification"""
        
        if certification.lower() == 'iso_27001':
            return [
                {'id': 'A.5.1', 'title': 'Policies for information security', 'description': 'Information security policy and topic-specific policies', 'family': 'A.5'},
                {'id': 'A.8.1', 'title': 'User access management', 'description': 'Formal user access provisioning process', 'family': 'A.8'},
                {'id': 'A.8.2', 'title': 'Privileged access rights', 'description': 'Allocation and use of privileged access rights', 'family': 'A.8'},
                {'id': 'A.8.3', 'title': 'Information access restriction', 'description': 'Access to information and application system functions', 'family': 'A.8'},
                {'id': 'A.12.2', 'title': 'Protection from malware', 'description': 'Protection against malware', 'family': 'A.12'},
                {'id': 'A.12.6', 'title': 'Management of technical vulnerabilities', 'description': 'Timely information about technical vulnerabilities', 'family': 'A.12'},
                {'id': 'A.16.1', 'title': 'Management of information security incidents', 'description': 'Management responsibilities and procedures', 'family': 'A.16'},
                {'id': 'A.17.1', 'title': 'Information security continuity', 'description': 'Business continuity planning', 'family': 'A.17'}
            ]
        elif certification.lower() == 'soc2':
            return [
                {'id': 'CC6.1', 'title': 'Logical Access Controls', 'description': 'User access provisioning and review', 'family': 'Common Criteria'},
                {'id': 'CC6.2', 'title': 'Access Controls - Authentication', 'description': 'Multi-factor authentication implementation', 'family': 'Common Criteria'},
                {'id': 'CC7.1', 'title': 'System Monitoring', 'description': 'System monitoring and threat detection', 'family': 'Common Criteria'},
                {'id': 'CC8.1', 'title': 'Change Management', 'description': 'Change management procedures', 'family': 'Common Criteria'}
            ]
        elif certification.lower() == 'essential_eight':
            return [
                {'id': 'E8-1', 'title': 'Application Control', 'description': 'Prevent execution of unapproved programs', 'family': 'Strategy 1'},
                {'id': 'E8-2', 'title': 'Patch Applications', 'description': 'Patch applications within timeframes', 'family': 'Strategy 2'},
                {'id': 'E8-5', 'title': 'Restrict Administrative Privileges', 'description': 'Restrict admin privileges to authorized users', 'family': 'Strategy 5'},
                {'id': 'E8-7', 'title': 'Multi-factor Authentication', 'description': 'MFA for privileged users and remote access', 'family': 'Strategy 7'}
            ]
        else:
            return []
    
    def _calculate_control_importance(self, control: Dict[str, Any], 
                                    company_profile: Dict[str, Any],
                                    certification: str) -> float:
        """Calculate control importance based on company context and intelligence"""
        
        base_importance = 0.5
        
        # Industry-specific adjustments
        industry = company_profile.get('industry', '').lower()
        if 'financial' in industry or 'healthcare' in industry:
            if 'access' in control['title'].lower() or 'authentication' in control['title'].lower():
                base_importance += 0.3
        
        # Company size adjustments
        employee_count = company_profile.get('employee_count', 100)
        if employee_count > 500:
            if 'management' in control['title'].lower() or 'policy' in control['title'].lower():
                base_importance += 0.2
        
        # Cloud usage adjustments
        cloud_usage = company_profile.get('cloud_usage', 'hybrid')
        if cloud_usage in ['cloud-first', 'cloud-native']:
            if 'vulnerability' in control['title'].lower() or 'access' in control['title'].lower():
                base_importance += 0.25
        
        # Regulatory requirements
        regulatory_reqs = company_profile.get('regulatory_requirements', [])
        if 'gdpr' in regulatory_reqs and 'information' in control['title'].lower():
            base_importance += 0.2
        
        # Cross-framework intelligence boost
        cross_mappings = self._find_cross_framework_mappings(control, certification)
        if len(cross_mappings) > 2:  # Control maps to multiple frameworks
            base_importance += 0.15
        
        return min(base_importance, 1.0)
    
    def _get_contextual_guidance(self, control: Dict[str, Any], 
                               company_profile: Dict[str, Any]) -> Dict[str, str]:
        """Get implementation guidance specific to company context"""
        
        industry = company_profile.get('industry', 'technology')
        employee_count = company_profile.get('employee_count', 100)
        
        # Generate contextual business rationale
        business_rationale = f"For a {industry} organization with {employee_count} employees, implementing {control['title']} provides critical risk reduction by addressing industry-specific threats and regulatory requirements."
        
        # Generate technical guidance based on company profile
        if employee_count < 50:
            technical_steps = f"Small organization implementation: Start with cloud-based solutions for {control['title']}. Leverage SaaS tools and managed services to minimize overhead."
        elif employee_count < 500:
            technical_steps = f"Mid-size implementation: Implement {control['title']} with a mix of in-house and managed services. Focus on automation and scalable processes."
        else:
            technical_steps = f"Enterprise implementation: Deploy {control['title']} with comprehensive governance, dedicated security team ownership, and integration with enterprise tools."
        
        return {
            'business_rationale': business_rationale,
            'technical_steps': technical_steps
        }
    
    def _find_cross_framework_mappings(self, control: Dict[str, Any], 
                                     source_framework: str) -> List[Dict[str, str]]:
        """Find equivalent controls in other frameworks"""
        
        mappings = []
        control_title_lower = control['title'].lower()
        
        # Use intelligence to find semantic matches
        for control_category, framework_controls in self.control_mappings.items():
            # Check if this control relates to the category
            if any(keyword in control_title_lower for keyword in ['access', 'authentication', 'user']):
                if 'access_control' in control_category:
                    for framework, controls in framework_controls.items():
                        if framework != source_framework:
                            for mapped_control in controls:
                                mappings.append({
                                    'framework': framework,
                                    'control_id': mapped_control,
                                    'relationship': 'equivalent',
                                    'similarity': 0.85
                                })
            
            elif any(keyword in control_title_lower for keyword in ['vulnerability', 'patch', 'malware']):
                if 'vulnerability_management' in control_category:
                    for framework, controls in framework_controls.items():
                        if framework != source_framework:
                            for mapped_control in controls:
                                mappings.append({
                                    'framework': framework,
                                    'control_id': mapped_control,
                                    'relationship': 'related',
                                    'similarity': 0.75
                                })
        
        return mappings
    
    def _estimate_implementation(self, control: Dict[str, Any], 
                               company_profile: Dict[str, Any]) -> Dict[str, str]:
        """Estimate implementation effort and timeline"""
        
        employee_count = company_profile.get('employee_count', 100)
        current_maturity = company_profile.get('security_maturity', 'medium')
        
        # Base estimates
        if 'policy' in control['title'].lower():
            effort = 'LOW' if current_maturity == 'high' else 'MEDIUM'
            timeline = '2-4 weeks' if employee_count < 100 else '4-8 weeks'
        elif 'management' in control['title'].lower() or 'process' in control['title'].lower():
            effort = 'MEDIUM' if current_maturity == 'high' else 'HIGH'
            timeline = '1-2 months' if employee_count < 100 else '2-4 months'
        else:
            effort = 'MEDIUM'
            timeline = '2-6 weeks'
        
        return {
            'effort': effort,
            'timeline': timeline
        }
    
    def _score_to_priority(self, score: float) -> str:
        """Convert importance score to priority level"""
        if score >= 0.8:
            return 'HIGH'
        elif score >= 0.6:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_company_specific_context(self, control: Dict[str, Any], 
                                    company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get company-specific implementation context"""
        
        return {
            'industry_considerations': f"Industry-specific guidance for {company_profile.get('industry', 'technology')} sector",
            'size_considerations': f"Tailored for organization with {company_profile.get('employee_count', 100)} employees",
            'tech_stack_alignment': f"Optimized for {company_profile.get('cloud_usage', 'hybrid')} technology approach",
            'regulatory_alignment': company_profile.get('regulatory_requirements', [])
        }
    
    def _create_implementation_roadmap(self, controls: List[Dict[str, Any]], 
                                     company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create an implementation roadmap"""
        
        high_priority = [c for c in controls if c['priority'] == 'HIGH']
        medium_priority = [c for c in controls if c['priority'] == 'MEDIUM']
        low_priority = [c for c in controls if c['priority'] == 'LOW']
        
        return {
            'total_timeline': '6-12 months',
            'estimated_cost': f"${len(controls) * 5000:,} - ${len(controls) * 15000:,}",
            'phase_1': f"High Priority Controls ({len(high_priority)} controls) - Months 1-3",
            'phase_2': f"Medium Priority Controls ({len(medium_priority)} controls) - Months 4-8", 
            'phase_3': f"Low Priority Controls ({len(low_priority)} controls) - Months 9-12",
            'quick_wins': [c['control_id'] for c in controls[:3] if c['implementation_effort'] == 'LOW'],
            'resource_requirements': f"{max(2, len(controls) // 10)} security professionals + compliance consultant"
        }
    
    def _generate_intelligence_insights(self, controls: List[Dict[str, Any]], 
                                      company_profile: Dict[str, Any]) -> List[str]:
        """Generate AI-powered insights about the control selection"""
        
        insights = []
        
        # Analyze cross-framework coverage
        all_mappings = []
        for control in controls:
            all_mappings.extend(control.get('cross_framework_mappings', []))
        
        unique_frameworks = set(m['framework'] for m in all_mappings)
        if len(unique_frameworks) > 2:
            insights.append(f"🎯 This control selection provides coverage across {len(unique_frameworks)} additional frameworks, maximizing compliance ROI")
        
        # Analyze implementation effort distribution
        high_effort_count = sum(1 for c in controls if c['implementation_effort'] == 'HIGH')
        if high_effort_count > len(controls) * 0.3:
            insights.append("⚠️ Consider phased implementation approach due to high complexity controls")
        
        # Industry-specific insights
        industry = company_profile.get('industry', '').lower()
        if 'financial' in industry:
            insights.append("🏦 Financial services organizations should prioritize access controls and audit trails for regulatory compliance")
        elif 'healthcare' in industry:
            insights.append("🏥 Healthcare organizations must emphasize data protection and privacy controls for HIPAA compliance")
        
        # Size-based insights
        employee_count = company_profile.get('employee_count', 100)
        if employee_count < 50:
            insights.append("🚀 Small organization advantage: Focus on cloud-native solutions and managed services to reduce overhead")
        elif employee_count > 1000:
            insights.append("🏢 Enterprise consideration: Ensure controls integrate with existing governance frameworks and tools")
        
        return insights
    
    async def store_assessment_result(self, assessment_result: Dict[str, Any]):
        """Store assessment results in the knowledge graph for learning"""
        
        if self.neo4j_available:
            await self._store_in_neo4j(assessment_result)
        else:
            await self._store_in_memory(assessment_result)
    
    async def _store_in_neo4j(self, assessment_result: Dict[str, Any]):
        """Store results in Neo4j for persistent learning"""
        
        with self.driver.session() as session:
            # Create organization node
            org_query = """
            MERGE (org:Organization {id: $org_id})
            SET org.name = $name,
                org.industry = $industry,
                org.employee_count = $employee_count,
                org.last_assessment = $timestamp
            """
            
            session.run(org_query, 
                org_id=assessment_result.get('company_profile', {}).get('company_name', 'unknown'),
                name=assessment_result.get('company_profile', {}).get('company_name', 'Unknown'),
                industry=assessment_result.get('company_profile', {}).get('industry', 'Unknown'),
                employee_count=assessment_result.get('company_profile', {}).get('employee_count', 0),
                timestamp=datetime.now().isoformat()
            )
            
            logger.info("📊 Assessment result stored in Neo4j knowledge graph")
    
    async def _store_in_memory(self, assessment_result: Dict[str, Any]):
        """Store results in memory fallback"""
        
        company_id = assessment_result.get('company_profile', {}).get('company_name', 'unknown')
        self.fallback_graph[company_id] = {
            'assessment_result': assessment_result,
            'stored_at': datetime.now().isoformat()
        }
        
        logger.info("📁 Assessment result stored in memory fallback")
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.close()
            logger.info("🔌 Neo4j connection closed")

# Global instance for the application
_knowledge_graph_instance = None

def get_intelligence_graph() -> IntelligenceKnowledgeGraph:
    """Get the global knowledge graph instance (singleton pattern)"""
    global _knowledge_graph_instance
    
    if _knowledge_graph_instance is None:
        _knowledge_graph_instance = IntelligenceKnowledgeGraph()
    
    return _knowledge_graph_instance