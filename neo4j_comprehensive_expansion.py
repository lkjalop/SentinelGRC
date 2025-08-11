"""
Neo4j Comprehensive Knowledge Graph Expansion
============================================
Expands beyond Essential 8 to include ALL frameworks, modern threats,
and comprehensive compliance relationships.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ComprehensiveComplianceGraph:
    """
    Comprehensive compliance knowledge graph covering:
    - All Australian frameworks (Essential 8, Privacy Act, APRA CPS 234, SOCI Act)
    - Modern threat landscape (API, AI, Cloud, Supply Chain)
    - International frameworks (NIST, ISO 27001, GDPR)
    - Control relationships and dependencies
    """
    
    def __init__(self):
        try:
            from neo4j import GraphDatabase
            self.uri = "bolt://localhost:7687"
            self.username = "neo4j"
            self.password = "Ag3nt-GRC"
            
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            logger.info("Connected to Neo4j for comprehensive expansion")
            
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def create_comprehensive_schema(self):
        """Create comprehensive schema for multi-framework knowledge graph"""
        
        with self.driver.session() as session:
            
            # Extended constraints
            constraints = [
                # Existing
                "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Control) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Threat) REQUIRE t.id IS UNIQUE", 
                "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Framework) REQUIRE f.name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (company:Company) REQUIRE company.name IS UNIQUE",
                
                # New nodes
                "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Principle) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (req:Requirement) REQUIRE req.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (obl:Obligation) REQUIRE obl.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (att:AttackTechnique) REQUIRE att.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (vuln:Vulnerability) REQUIRE vuln.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (asset:Asset) REQUIRE asset.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (actor:ThreatActor) REQUIRE actor.id IS UNIQUE"
            ]
            
            for constraint in constraints:
                session.run(constraint)
                logger.info(f"Created constraint: {constraint[:50]}...")
    
    def load_privacy_act_framework(self):
        """Load Privacy Act 1988 - 13 Australian Privacy Principles"""
        
        with self.driver.session() as session:
            
            # Create Privacy Act framework
            session.run("""
                MERGE (f:Framework {name: 'Privacy Act 1988'})
                SET f.country = 'Australia',
                    f.type = 'Privacy Legislation',
                    f.authority = 'OAIC',
                    f.description = 'Australian Privacy Principles for personal information'
            """)
            
            # 13 Australian Privacy Principles
            privacy_principles = [
                {
                    'id': 'APP1', 'name': 'Open and transparent management of personal information',
                    'category': 'Governance', 'risk_level': 'MEDIUM',
                    'description': 'Manage personal information in an open and transparent way'
                },
                {
                    'id': 'APP2', 'name': 'Anonymity and pseudonymity', 
                    'category': 'Individual Rights', 'risk_level': 'LOW',
                    'description': 'Give individuals option to not identify themselves'
                },
                {
                    'id': 'APP3', 'name': 'Collection of solicited personal information',
                    'category': 'Collection', 'risk_level': 'HIGH',  
                    'description': 'Only collect personal information reasonably necessary'
                },
                {
                    'id': 'APP4', 'name': 'Dealing with unsolicited personal information',
                    'category': 'Collection', 'risk_level': 'MEDIUM',
                    'description': 'Handle unsolicited personal information appropriately'  
                },
                {
                    'id': 'APP5', 'name': 'Notification of collection of personal information',
                    'category': 'Transparency', 'risk_level': 'HIGH',
                    'description': 'Notify individuals when collecting personal information'
                },
                {
                    'id': 'APP6', 'name': 'Use or disclosure of personal information', 
                    'category': 'Use and Disclosure', 'risk_level': 'CRITICAL',
                    'description': 'Only use/disclose for primary purpose or with consent'
                },
                {
                    'id': 'APP7', 'name': 'Direct marketing',
                    'category': 'Use and Disclosure', 'risk_level': 'MEDIUM',
                    'description': 'Use personal information for direct marketing appropriately'
                },
                {
                    'id': 'APP8', 'name': 'Cross-border disclosure of personal information',
                    'category': 'Cross-border', 'risk_level': 'HIGH', 
                    'description': 'Take reasonable steps before disclosing overseas'
                },
                {
                    'id': 'APP9', 'name': 'Adoption, use or disclosure of government related identifiers',
                    'category': 'Government ID', 'risk_level': 'MEDIUM',
                    'description': 'Do not adopt government identifiers as own identifiers'
                },
                {
                    'id': 'APP10', 'name': 'Quality of personal information',
                    'category': 'Data Quality', 'risk_level': 'MEDIUM', 
                    'description': 'Take reasonable steps to ensure information quality'
                },
                {
                    'id': 'APP11', 'name': 'Security of personal information',
                    'category': 'Security', 'risk_level': 'CRITICAL',
                    'description': 'Take reasonable steps to secure personal information'
                },
                {
                    'id': 'APP12', 'name': 'Access to personal information', 
                    'category': 'Individual Rights', 'risk_level': 'MEDIUM',
                    'description': 'Give individuals access to their personal information'
                },
                {
                    'id': 'APP13', 'name': 'Correction of personal information',
                    'category': 'Individual Rights', 'risk_level': 'MEDIUM',
                    'description': 'Correct personal information when requested'
                }
            ]
            
            # Create privacy principles as controls
            for principle in privacy_principles:
                session.run("""
                    MATCH (f:Framework {name: 'Privacy Act 1988'})
                    MERGE (p:Principle:Control {id: $id})
                    SET p.name = $name,
                        p.category = $category,
                        p.risk_level = $risk_level, 
                        p.description = $description,
                        p.type = 'Privacy Principle'
                    MERGE (p)-[:BELONGS_TO]->(f)
                """, **principle)
                
                logger.info(f"Created Privacy Principle: {principle['name']}")
    
    def load_apra_cps234_framework(self):
        """Load APRA CPS 234 Information Security Standard"""
        
        with self.driver.session() as session:
            
            # Create APRA framework
            session.run("""
                MERGE (f:Framework {name: 'APRA CPS 234'})
                SET f.country = 'Australia',
                    f.type = 'Financial Services Regulation',
                    f.authority = 'APRA', 
                    f.description = 'Information Security Standard for APRA-regulated entities'
            """)
            
            # APRA CPS 234 requirements
            apra_requirements = [
                {
                    'id': 'CPS234_7', 'name': 'Information Security Capability',
                    'category': 'Governance', 'risk_level': 'HIGH',
                    'description': 'Maintain information security capability commensurate with information security vulnerabilities and threats'
                },
                {
                    'id': 'CPS234_8', 'name': 'Information Security Policy',
                    'category': 'Policy', 'risk_level': 'MEDIUM',
                    'description': 'Maintain information security policy approved by Board'
                },
                {
                    'id': 'CPS234_10', 'name': 'Information Asset Identification',
                    'category': 'Asset Management', 'risk_level': 'HIGH',
                    'description': 'Identify and classify information assets'
                },
                {
                    'id': 'CPS234_12', 'name': 'Implementation of Controls',
                    'category': 'Controls', 'risk_level': 'CRITICAL',
                    'description': 'Implement controls to protect information assets'
                },
                {
                    'id': 'CPS234_14', 'name': 'Incident Response Capability',
                    'category': 'Incident Response', 'risk_level': 'CRITICAL',
                    'description': 'Maintain incident response capability'
                },
                {
                    'id': 'CPS234_15', 'name': 'Testing of Controls',
                    'category': 'Testing', 'risk_level': 'HIGH',
                    'description': 'Test effectiveness of controls through systematic testing program'
                },
                {
                    'id': 'CPS234_16', 'name': 'Monitoring and Logging',
                    'category': 'Monitoring', 'risk_level': 'HIGH', 
                    'description': 'Monitor systems and maintain security logs'
                },
                {
                    'id': 'CPS234_18', 'name': 'Reporting to APRA',
                    'category': 'Reporting', 'risk_level': 'CRITICAL',
                    'description': 'Notify APRA of material information security incidents'
                }
            ]
            
            # Create APRA requirements  
            for requirement in apra_requirements:
                session.run("""
                    MATCH (f:Framework {name: 'APRA CPS 234'})
                    MERGE (r:Requirement:Control {id: $id})
                    SET r.name = $name,
                        r.category = $category,
                        r.risk_level = $risk_level,
                        r.description = $description,
                        r.type = 'APRA Requirement'
                    MERGE (r)-[:BELONGS_TO]->(f)
                """, **requirement)
                
                logger.info(f"Created APRA Requirement: {requirement['name']}")
    
    def load_soci_act_framework(self):
        """Load Security of Critical Infrastructure (SOCI) Act obligations"""
        
        with self.driver.session() as session:
            
            # Create SOCI framework
            session.run("""
                MERGE (f:Framework {name: 'SOCI Act'})
                SET f.country = 'Australia',
                    f.type = 'Critical Infrastructure Security',
                    f.authority = 'Department of Home Affairs',
                    f.description = 'Security obligations for critical infrastructure entities'
            """)
            
            # SOCI Act obligations
            soci_obligations = [
                {
                    'id': 'SOCI_RMP', 'name': 'Risk Management Program',
                    'category': 'Risk Management', 'risk_level': 'CRITICAL',
                    'description': 'Adopt and maintain risk management program'
                },
                {
                    'id': 'SOCI_ANNUAL', 'name': 'Annual Risk Management Program Report',
                    'category': 'Reporting', 'risk_level': 'HIGH',
                    'description': 'Provide annual report on risk management program'
                },
                {
                    'id': 'SOCI_INCIDENT', 'name': 'Cybersecurity Incident Reporting',
                    'category': 'Incident Response', 'risk_level': 'CRITICAL', 
                    'description': 'Report cybersecurity incidents to ASD within 12/72 hours'
                },
                {
                    'id': 'SOCI_VULN', 'name': 'Vulnerability Assessments',
                    'category': 'Assessment', 'risk_level': 'HIGH',
                    'description': 'Conduct regular vulnerability assessments of critical assets'
                },
                {
                    'id': 'SOCI_PERSONNEL', 'name': 'Personnel Security',
                    'category': 'Personnel', 'risk_level': 'HIGH',
                    'description': 'Implement personnel security controls for privileged users'
                },
                {
                    'id': 'SOCI_SUPPLY', 'name': 'Supply Chain Security',
                    'category': 'Supply Chain', 'risk_level': 'HIGH',
                    'description': 'Assess and manage supply chain security risks'
                },
                {
                    'id': 'SOCI_ACCESS', 'name': 'Access Control',
                    'category': 'Access Control', 'risk_level': 'CRITICAL',
                    'description': 'Implement access controls for critical infrastructure assets'
                }
            ]
            
            # Create SOCI obligations
            for obligation in soci_obligations:
                session.run("""
                    MATCH (f:Framework {name: 'SOCI Act'})
                    MERGE (o:Obligation:Control {id: $id})
                    SET o.name = $name,
                        o.category = $category,
                        o.risk_level = $risk_level,
                        o.description = $description,
                        o.type = 'SOCI Obligation'
                    MERGE (o)-[:BELONGS_TO]->(f)
                """, **obligation)
                
                logger.info(f"Created SOCI Obligation: {obligation['name']}")
    
    def load_modern_threat_landscape(self):
        """Load comprehensive modern threat landscape including AI, API, Cloud threats"""
        
        with self.driver.session() as session:
            
            # Modern threat categories
            modern_threats = [
                # AI/ML Specific Threats
                {
                    'id': 'T_AI_POISONING', 'name': 'AI Model Poisoning',
                    'category': 'AI/ML Security', 'severity': 'HIGH',
                    'description': 'Malicious manipulation of training data or model parameters',
                    'attack_vector': 'Supply Chain', 'mitre_id': 'T1199'
                },
                {
                    'id': 'T_PROMPT_INJECTION', 'name': 'LLM Prompt Injection', 
                    'category': 'AI/ML Security', 'severity': 'MEDIUM',
                    'description': 'Manipulation of LLM inputs to produce harmful outputs',
                    'attack_vector': 'Application', 'mitre_id': 'T1190'
                },
                {
                    'id': 'T_AI_BIAS', 'name': 'AI Algorithmic Bias',
                    'category': 'AI/ML Security', 'severity': 'MEDIUM', 
                    'description': 'Discriminatory AI decision-making affecting individuals',
                    'attack_vector': 'Process', 'mitre_id': 'T1005'
                },
                
                # API Security Threats
                {
                    'id': 'T_API_INJECTION', 'name': 'API Injection Attacks',
                    'category': 'API Security', 'severity': 'CRITICAL',
                    'description': 'SQL, NoSQL, Command injection through API endpoints', 
                    'attack_vector': 'Network', 'mitre_id': 'T1190'
                },
                {
                    'id': 'T_API_AUTH', 'name': 'Broken API Authentication',
                    'category': 'API Security', 'severity': 'CRITICAL',
                    'description': 'Weak or missing API authentication mechanisms',
                    'attack_vector': 'Network', 'mitre_id': 'T1078'
                },
                {
                    'id': 'T_API_RATE', 'name': 'API Rate Limiting Abuse',
                    'category': 'API Security', 'severity': 'MEDIUM',
                    'description': 'Resource exhaustion through API abuse',
                    'attack_vector': 'Network', 'mitre_id': 'T1499'
                },
                {
                    'id': 'T_API_EXPOSURE', 'name': 'Excessive API Data Exposure',
                    'category': 'API Security', 'severity': 'HIGH',
                    'description': 'APIs exposing more data than necessary',
                    'attack_vector': 'Network', 'mitre_id': 'T1530'
                },
                
                # Cloud Security Threats
                {
                    'id': 'T_CLOUD_CONFIG', 'name': 'Cloud Misconfiguration',
                    'category': 'Cloud Security', 'severity': 'CRITICAL',
                    'description': 'Insecure cloud service configurations exposing data',
                    'attack_vector': 'Configuration', 'mitre_id': 'T1538'
                },
                {
                    'id': 'T_CLOUD_IAM', 'name': 'Cloud Identity Compromise',
                    'category': 'Cloud Security', 'severity': 'CRITICAL', 
                    'description': 'Compromised cloud service accounts and permissions',
                    'attack_vector': 'Identity', 'mitre_id': 'T1078.004'
                },
                {
                    'id': 'T_SERVERLESS', 'name': 'Serverless Function Abuse',
                    'category': 'Cloud Security', 'severity': 'HIGH',
                    'description': 'Malicious code execution in serverless environments',
                    'attack_vector': 'Application', 'mitre_id': 'T1609'
                },
                
                # Supply Chain Threats
                {
                    'id': 'T_SUPPLY_SOFTWARE', 'name': 'Software Supply Chain Attack',
                    'category': 'Supply Chain', 'severity': 'CRITICAL',
                    'description': 'Compromise of software dependencies and build pipelines',
                    'attack_vector': 'Supply Chain', 'mitre_id': 'T1195.002'
                },
                {
                    'id': 'T_SUPPLY_HARDWARE', 'name': 'Hardware Supply Chain Attack',
                    'category': 'Supply Chain', 'severity': 'HIGH',
                    'description': 'Malicious hardware implants in IT equipment',
                    'attack_vector': 'Supply Chain', 'mitre_id': 'T1195.003'
                },
                
                # Advanced Persistent Threats
                {
                    'id': 'T_APT_LATERAL', 'name': 'Advanced Lateral Movement',
                    'category': 'APT', 'severity': 'CRITICAL',
                    'description': 'Sophisticated movement across network segments',
                    'attack_vector': 'Network', 'mitre_id': 'T1021'
                },
                {
                    'id': 'T_LIVING_LAND', 'name': 'Living off the Land',
                    'category': 'APT', 'severity': 'HIGH', 
                    'description': 'Use of legitimate tools for malicious purposes',
                    'attack_vector': 'Process', 'mitre_id': 'T1105'
                },
                
                # IoT and OT Threats
                {
                    'id': 'T_IOT_DEFAULT', 'name': 'IoT Default Credentials',
                    'category': 'IoT Security', 'severity': 'HIGH',
                    'description': 'Exploitation of default or weak IoT device credentials',
                    'attack_vector': 'Network', 'mitre_id': 'T1078'
                },
                {
                    'id': 'T_OT_DISRUPTION', 'name': 'OT System Disruption',
                    'category': 'OT Security', 'severity': 'CRITICAL',
                    'description': 'Attacks on operational technology and industrial systems',
                    'attack_vector': 'Network', 'mitre_id': 'T0809'
                }
            ]
            
            # Create modern threats
            for threat in modern_threats:
                session.run("""
                    MERGE (t:Threat {id: $id})
                    SET t.name = $name,
                        t.category = $category,
                        t.severity = $severity,
                        t.description = $description,
                        t.attack_vector = $attack_vector,
                        t.mitre_id = $mitre_id,
                        t.type = 'Modern Threat'
                """, **threat)
                
                logger.info(f"Created Modern Threat: {threat['name']}")
    
    def create_cross_framework_relationships(self):
        """Create relationships between controls across different frameworks"""
        
        with self.driver.session() as session:
            
            # Essential 8 ↔ Privacy Act relationships
            privacy_relationships = [
                # E8_7 (MFA) supports APP11 (Security)
                ("E8_7", "APP11", "SUPPORTS", "MFA enhances personal information security"),
                # E8_8 (Backups) supports APP11 (Security) 
                ("E8_8", "APP11", "SUPPORTS", "Backups protect personal information availability"),
                # E8_5 (Admin Privileges) supports APP11 (Security)
                ("E8_5", "APP11", "SUPPORTS", "Restricted admin access protects personal data"),
                # E8_1 (App Control) supports APP6 (Use/Disclosure)
                ("E8_1", "APP6", "SUPPORTS", "Application control prevents unauthorized data access"),
            ]
            
            for source, target, rel_type, description in privacy_relationships:
                session.run("""
                    MATCH (s:Control {id: $source})
                    MATCH (t:Control {id: $target})
                    MERGE (s)-[r:SUPPORTS]->(t)
                    SET r.description = $description,
                        r.type = $rel_type
                """, source=source, target=target, rel_type=rel_type, description=description)
            
            # Essential 8 ↔ APRA CPS 234 relationships  
            apra_relationships = [
                # E8_7 (MFA) supports CPS234_12 (Controls)
                ("E8_7", "CPS234_12", "SUPPORTS", "MFA is a key security control for financial services"),
                # E8_14 (Incident Response) supports CPS234_14 (Incident Response)
                ("E8_8", "CPS234_14", "SUPPORTS", "Backup systems enable incident recovery"),
                # E8_6 (Patch OS) supports CPS234_15 (Testing)
                ("E8_6", "CPS234_15", "SUPPORTS", "OS patching demonstrates control effectiveness"),
            ]
            
            for source, target, rel_type, description in apra_relationships:
                session.run("""
                    MATCH (s:Control {id: $source})
                    MATCH (t:Control {id: $target})
                    MERGE (s)-[r:SUPPORTS]->(t)  
                    SET r.description = $description,
                        r.type = $rel_type
                """, source=source, target=target, rel_type=rel_type, description=description)
            
            # Essential 8 ↔ SOCI Act relationships
            soci_relationships = [
                # E8_5 (Admin Privileges) supports SOCI_ACCESS (Access Control)
                ("E8_5", "SOCI_ACCESS", "SUPPORTS", "Administrative privilege controls support critical infrastructure access control"),
                # E8_8 (Backups) supports SOCI_RMP (Risk Management)
                ("E8_8", "SOCI_RMP", "SUPPORTS", "Backup systems are part of critical infrastructure risk management"),
                # E8_1 (App Control) supports SOCI_VULN (Vulnerability Assessment)
                ("E8_1", "SOCI_VULN", "SUPPORTS", "Application control reduces attack surface for vulnerability assessments"),
            ]
            
            for source, target, rel_type, description in soci_relationships:
                session.run("""
                    MATCH (s:Control {id: $source})
                    MATCH (t:Control {id: $target})
                    MERGE (s)-[r:SUPPORTS]->(t)
                    SET r.description = $description,
                        r.type = $rel_type  
                """, source=source, target=target, rel_type=rel_type, description=description)
            
            logger.info("Created cross-framework control relationships")
    
    def map_modern_threats_to_controls(self):
        """Map modern threats to controls across all frameworks"""
        
        with self.driver.session() as session:
            
            # Modern threat → control mappings
            threat_mappings = [
                # AI/ML Threats
                ("T_AI_POISONING", ["E8_1", "SOCI_SUPPLY", "CPS234_10"], "Application control and supply chain security prevent AI model poisoning"),
                ("T_PROMPT_INJECTION", ["E8_4", "CPS234_12"], "User application hardening and security controls prevent prompt injection"),
                
                # API Security Threats  
                ("T_API_INJECTION", ["E8_1", "E8_4", "CPS234_12"], "Application controls prevent API injection attacks"),
                ("T_API_AUTH", ["E8_7", "E8_5", "SOCI_ACCESS"], "MFA and access controls secure API authentication"),
                ("T_API_EXPOSURE", ["APP6", "APP11", "CPS234_10"], "Privacy principles and asset identification prevent data exposure"),
                
                # Cloud Security Threats
                ("T_CLOUD_CONFIG", ["E8_5", "CPS234_12", "SOCI_ACCESS"], "Access controls and security configurations prevent cloud misconfigurations"),
                ("T_CLOUD_IAM", ["E8_7", "E8_5", "SOCI_PERSONNEL"], "MFA and privilege controls secure cloud identities"),
                
                # Supply Chain Threats
                ("T_SUPPLY_SOFTWARE", ["E8_1", "E8_2", "SOCI_SUPPLY"], "Application control and patching prevent supply chain attacks"),
                ("T_SUPPLY_HARDWARE", ["SOCI_SUPPLY", "CPS234_10"], "Supply chain security and asset identification prevent hardware attacks"),
                
                # Advanced Threats
                ("T_APT_LATERAL", ["E8_5", "E8_7", "SOCI_ACCESS"], "Privilege controls and MFA prevent lateral movement"),
                ("T_LIVING_LAND", ["E8_1", "E8_5", "CPS234_16"], "Application control and monitoring detect living-off-the-land attacks"),
                
                # IoT/OT Threats
                ("T_IOT_DEFAULT", ["E8_7", "SOCI_PERSONNEL", "CPS234_12"], "Authentication controls secure IoT devices"),
                ("T_OT_DISRUPTION", ["SOCI_RMP", "SOCI_VULN", "CPS234_14"], "Risk management and incident response protect OT systems")
            ]
            
            for threat_id, control_ids, reasoning in threat_mappings:
                for control_id in control_ids:
                    session.run("""
                        MATCH (c:Control {id: $control_id})
                        MATCH (t:Threat {id: $threat_id})
                        MERGE (c)-[r:PREVENTS]->(t)
                        SET r.reasoning = $reasoning,
                            r.effectiveness = 'HIGH'
                    """, control_id=control_id, threat_id=threat_id, reasoning=reasoning)
                
                logger.info(f"Mapped threat {threat_id} to {len(control_ids)} controls")
    
    def load_international_frameworks(self):
        """Load key international frameworks for comparison"""
        
        with self.driver.session() as session:
            
            # NIST Cybersecurity Framework
            session.run("""
                MERGE (f:Framework {name: 'NIST CSF'})
                SET f.country = 'USA',
                    f.type = 'Cybersecurity Framework',
                    f.authority = 'NIST',
                    f.description = 'Framework for improving critical infrastructure cybersecurity'
            """)
            
            # ISO 27001
            session.run("""
                MERGE (f:Framework {name: 'ISO 27001'})
                SET f.country = 'International',
                    f.type = 'Information Security Management',
                    f.authority = 'ISO',
                    f.description = 'International standard for information security management systems'
            """)
            
            # GDPR (for comparison with Privacy Act)
            session.run("""
                MERGE (f:Framework {name: 'GDPR'})
                SET f.country = 'EU',
                    f.type = 'Privacy Regulation', 
                    f.authority = 'EU',
                    f.description = 'General Data Protection Regulation'
            """)
            
            logger.info("Created international framework nodes")
    
    def load_comprehensive_knowledge_graph(self):
        """Load the complete comprehensive knowledge graph"""
        
        print("Loading comprehensive compliance knowledge graph...")
        print("=" * 55)
        
        try:
            # 1. Create schema
            print("1. Creating comprehensive schema...")
            self.create_comprehensive_schema()
            
            # 2. Load all Australian frameworks
            print("2. Loading Privacy Act 1988...")
            self.load_privacy_act_framework()
            
            print("3. Loading APRA CPS 234...")
            self.load_apra_cps234_framework()
            
            print("4. Loading SOCI Act...")
            self.load_soci_act_framework()
            
            # 3. Load modern threat landscape
            print("5. Loading modern threat landscape...")
            self.load_modern_threat_landscape()
            
            # 4. Create relationships
            print("6. Creating cross-framework relationships...")
            self.create_cross_framework_relationships()
            
            print("7. Mapping modern threats to controls...")
            self.map_modern_threats_to_controls()
            
            # 5. Load international frameworks for comparison
            print("8. Loading international frameworks...")
            self.load_international_frameworks()
            
            print("\nSUCCESS: Comprehensive knowledge graph loaded!")
            print("Graph now includes:")
            print("  • Essential 8 (8 controls)")
            print("  • Privacy Act 1988 (13 principles)")
            print("  • APRA CPS 234 (8 requirements)")
            print("  • SOCI Act (7 obligations)")
            print("  • Modern threats (17 threat categories)")
            print("  • Cross-framework relationships")
            print("  • International frameworks for comparison")
            
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to load comprehensive graph - {e}")
            return False
    
    def get_comprehensive_statistics(self):
        """Get statistics on the comprehensive knowledge graph"""
        
        with self.driver.session() as session:
            
            stats = {}
            
            # Count nodes by type
            result = session.run("MATCH (n:Framework) RETURN count(n) as count")
            stats['frameworks'] = result.single()['count']
            
            result = session.run("MATCH (n:Control) RETURN count(n) as count") 
            stats['controls'] = result.single()['count']
            
            result = session.run("MATCH (n:Threat) RETURN count(n) as count")
            stats['threats'] = result.single()['count']
            
            # Count relationships
            result = session.run("MATCH ()-[r:PREVENTS]->() RETURN count(r) as count")
            stats['prevention_relationships'] = result.single()['count']
            
            result = session.run("MATCH ()-[r:SUPPORTS]->() RETURN count(r) as count")
            stats['support_relationships'] = result.single()['count']
            
            result = session.run("MATCH ()-[r:BELONGS_TO]->() RETURN count(r) as count")
            stats['framework_relationships'] = result.single()['count']
            
            return stats
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")


def setup_comprehensive_knowledge_graph():
    """Setup the comprehensive knowledge graph"""
    
    try:
        graph = ComprehensiveComplianceGraph()
        success = graph.load_comprehensive_knowledge_graph()
        
        if success:
            stats = graph.get_comprehensive_statistics()
            
            print("\nFINAL STATISTICS:")
            print("=" * 20)
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        graph.close()
        return success
        
    except Exception as e:
        print(f"SETUP FAILED: {e}")
        return False

# Example usage
if __name__ == "__main__":
    setup_comprehensive_knowledge_graph()