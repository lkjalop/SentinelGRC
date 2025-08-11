"""
Add Enterprise Frameworks to Neo4j
====================================
Adds HIPAA, PCI DSS, and ISO 27001 to expand market reach.
These are the most requested frameworks for healthcare, finance, and general security.
"""

from neo4j import GraphDatabase
import logging
from typing import Dict, List, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnterpriseFrameworkExpansion:
    """Adds key enterprise frameworks to Neo4j knowledge graph"""
    
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.username = "neo4j"
        self.password = "Ag3nt-GRC"
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            logger.info("Connected to Neo4j for enterprise framework expansion")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def add_hipaa_framework(self):
        """Add HIPAA (Health Insurance Portability and Accountability Act)"""
        
        with self.driver.session() as session:
            # Create HIPAA framework
            session.run("""
                MERGE (f:Framework {name: 'HIPAA'})
                SET f.country = 'USA',
                    f.type = 'Healthcare Privacy and Security',
                    f.authority = 'HHS',
                    f.description = 'US healthcare data privacy and security standards',
                    f.full_name = 'Health Insurance Portability and Accountability Act'
            """)
            
            # HIPAA Security Rule - Key Safeguards
            hipaa_controls = [
                # Administrative Safeguards
                {
                    'id': 'HIPAA_A1', 'name': 'Security Officer Designation',
                    'category': 'Administrative', 'type': 'Required',
                    'description': 'Designate security official responsible for HIPAA compliance'
                },
                {
                    'id': 'HIPAA_A2', 'name': 'Workforce Training',
                    'category': 'Administrative', 'type': 'Required',
                    'description': 'Security awareness training for all workforce members'
                },
                {
                    'id': 'HIPAA_A3', 'name': 'Access Management',
                    'category': 'Administrative', 'type': 'Required',
                    'description': 'Procedures for authorizing access to ePHI'
                },
                {
                    'id': 'HIPAA_A4', 'name': 'Risk Assessment',
                    'category': 'Administrative', 'type': 'Required',
                    'description': 'Conduct accurate and thorough risk assessment'
                },
                
                # Physical Safeguards
                {
                    'id': 'HIPAA_P1', 'name': 'Facility Access Controls',
                    'category': 'Physical', 'type': 'Required',
                    'description': 'Limit physical access to ePHI systems'
                },
                {
                    'id': 'HIPAA_P2', 'name': 'Device and Media Controls',
                    'category': 'Physical', 'type': 'Required',
                    'description': 'Disposal and re-use procedures for hardware and media'
                },
                
                # Technical Safeguards
                {
                    'id': 'HIPAA_T1', 'name': 'Access Control',
                    'category': 'Technical', 'type': 'Required',
                    'description': 'Unique user identification, automatic logoff, encryption'
                },
                {
                    'id': 'HIPAA_T2', 'name': 'Audit Controls',
                    'category': 'Technical', 'type': 'Required',
                    'description': 'Hardware, software, procedural mechanisms for audit logs'
                },
                {
                    'id': 'HIPAA_T3', 'name': 'Integrity Controls',
                    'category': 'Technical', 'type': 'Required',
                    'description': 'ePHI not improperly altered or destroyed'
                },
                {
                    'id': 'HIPAA_T4', 'name': 'Transmission Security',
                    'category': 'Technical', 'type': 'Required',
                    'description': 'Protect ePHI during transmission over networks'
                }
            ]
            
            for control in hipaa_controls:
                session.run("""
                    MATCH (f:Framework {name: 'HIPAA'})
                    MERGE (c:Control {id: $id})
                    SET c.name = $name,
                        c.category = $category,
                        c.type = $type,
                        c.description = $description,
                        c.framework_type = 'HIPAA'
                    MERGE (c)-[:BELONGS_TO]->(f)
                """, **control)
            
            logger.info(f"Added HIPAA framework with {len(hipaa_controls)} controls")
    
    def add_pci_dss_framework(self):
        """Add PCI DSS (Payment Card Industry Data Security Standard)"""
        
        with self.driver.session() as session:
            # Create PCI DSS framework
            session.run("""
                MERGE (f:Framework {name: 'PCI DSS'})
                SET f.country = 'International',
                    f.type = 'Payment Card Security',
                    f.authority = 'PCI Security Standards Council',
                    f.description = 'Security standards for organizations handling credit cards',
                    f.version = '4.0'
            """)
            
            # PCI DSS v4.0 - Key Requirements
            pci_controls = [
                # Build and Maintain Secure Networks
                {
                    'id': 'PCI_1', 'name': 'Firewall Configuration',
                    'category': 'Network Security', 'priority': 'CRITICAL',
                    'description': 'Install and maintain firewall configuration to protect cardholder data'
                },
                {
                    'id': 'PCI_2', 'name': 'Default Security Parameters',
                    'category': 'Configuration', 'priority': 'HIGH',
                    'description': 'Do not use vendor-supplied defaults for system passwords'
                },
                
                # Protect Cardholder Data
                {
                    'id': 'PCI_3', 'name': 'Protect Stored Data',
                    'category': 'Data Protection', 'priority': 'CRITICAL',
                    'description': 'Protect stored cardholder data with encryption'
                },
                {
                    'id': 'PCI_4', 'name': 'Encrypted Transmission',
                    'category': 'Data Protection', 'priority': 'CRITICAL',
                    'description': 'Encrypt transmission of cardholder data across public networks'
                },
                
                # Vulnerability Management
                {
                    'id': 'PCI_5', 'name': 'Anti-virus Software',
                    'category': 'Malware Protection', 'priority': 'HIGH',
                    'description': 'Use and regularly update anti-virus software'
                },
                {
                    'id': 'PCI_6', 'name': 'Secure Systems',
                    'category': 'System Security', 'priority': 'HIGH',
                    'description': 'Develop and maintain secure systems and applications'
                },
                
                # Access Control
                {
                    'id': 'PCI_7', 'name': 'Restrict Access by Business Need',
                    'category': 'Access Control', 'priority': 'HIGH',
                    'description': 'Restrict access to cardholder data by business need-to-know'
                },
                {
                    'id': 'PCI_8', 'name': 'Unique User IDs',
                    'category': 'Access Control', 'priority': 'CRITICAL',
                    'description': 'Assign unique ID to each person with computer access'
                },
                {
                    'id': 'PCI_9', 'name': 'Physical Access',
                    'category': 'Physical Security', 'priority': 'HIGH',
                    'description': 'Restrict physical access to cardholder data'
                },
                
                # Monitoring and Testing
                {
                    'id': 'PCI_10', 'name': 'Track and Monitor Access',
                    'category': 'Monitoring', 'priority': 'CRITICAL',
                    'description': 'Track and monitor all access to network resources and cardholder data'
                },
                {
                    'id': 'PCI_11', 'name': 'Security Testing',
                    'category': 'Testing', 'priority': 'HIGH',
                    'description': 'Regularly test security systems and processes'
                },
                
                # Information Security Policy
                {
                    'id': 'PCI_12', 'name': 'Security Policy',
                    'category': 'Policy', 'priority': 'HIGH',
                    'description': 'Maintain policy that addresses information security for all personnel'
                }
            ]
            
            for control in pci_controls:
                session.run("""
                    MATCH (f:Framework {name: 'PCI DSS'})
                    MERGE (c:Control {id: $id})
                    SET c.name = $name,
                        c.category = $category,
                        c.priority = $priority,
                        c.description = $description,
                        c.framework_type = 'PCI DSS'
                    MERGE (c)-[:BELONGS_TO]->(f)
                """, **control)
            
            logger.info(f"Added PCI DSS framework with {len(pci_controls)} requirements")
    
    def add_iso27001_framework(self):
        """Add ISO 27001:2022 Information Security Management System"""
        
        with self.driver.session() as session:
            # Create ISO 27001 framework
            session.run("""
                MERGE (f:Framework {name: 'ISO 27001:2022'})
                SET f.country = 'International',
                    f.type = 'Information Security Management',
                    f.authority = 'ISO',
                    f.description = 'International standard for information security management systems',
                    f.version = '2022'
            """)
            
            # ISO 27001:2022 Annex A Controls (Key Selection)
            iso_controls = [
                # Organizational Controls
                {
                    'id': 'ISO_5.1', 'name': 'Policies for information security',
                    'category': 'Organizational', 'control_type': 'Preventive',
                    'description': 'Information security policy and topic-specific policies'
                },
                {
                    'id': 'ISO_5.7', 'name': 'Threat intelligence',
                    'category': 'Organizational', 'control_type': 'Preventive',
                    'description': 'Information relating to information security threats'
                },
                {
                    'id': 'ISO_5.23', 'name': 'Information security in supplier relationships',
                    'category': 'Organizational', 'control_type': 'Preventive',
                    'description': 'Processes to manage security risks in supplier relationships'
                },
                
                # People Controls
                {
                    'id': 'ISO_6.1', 'name': 'Screening',
                    'category': 'People', 'control_type': 'Preventive',
                    'description': 'Background verification checks on all candidates'
                },
                {
                    'id': 'ISO_6.3', 'name': 'Information security awareness',
                    'category': 'People', 'control_type': 'Preventive',
                    'description': 'Awareness education and regular training'
                },
                
                # Physical Controls
                {
                    'id': 'ISO_7.1', 'name': 'Physical security perimeters',
                    'category': 'Physical', 'control_type': 'Preventive',
                    'description': 'Security perimeters to protect information processing facilities'
                },
                {
                    'id': 'ISO_7.4', 'name': 'Physical security monitoring',
                    'category': 'Physical', 'control_type': 'Detective',
                    'description': 'Premises monitored for unauthorized physical access'
                },
                
                # Technological Controls
                {
                    'id': 'ISO_8.1', 'name': 'User endpoint devices',
                    'category': 'Technological', 'control_type': 'Preventive',
                    'description': 'Information on endpoint devices protected'
                },
                {
                    'id': 'ISO_8.2', 'name': 'Privileged access rights',
                    'category': 'Technological', 'control_type': 'Preventive',
                    'description': 'Allocation and use of privileged access rights restricted'
                },
                {
                    'id': 'ISO_8.5', 'name': 'Secure authentication',
                    'category': 'Technological', 'control_type': 'Preventive',
                    'description': 'Secure authentication technologies and procedures'
                },
                {
                    'id': 'ISO_8.12', 'name': 'Data leakage prevention',
                    'category': 'Technological', 'control_type': 'Detective',
                    'description': 'Measures against data leakage applied'
                },
                {
                    'id': 'ISO_8.16', 'name': 'Monitoring activities',
                    'category': 'Technological', 'control_type': 'Detective',
                    'description': 'Networks, systems and applications monitored for anomalous behavior'
                },
                {
                    'id': 'ISO_8.23', 'name': 'Web filtering',
                    'category': 'Technological', 'control_type': 'Preventive',
                    'description': 'Access to external websites managed to reduce exposure'
                },
                {
                    'id': 'ISO_8.28', 'name': 'Secure coding',
                    'category': 'Technological', 'control_type': 'Preventive',
                    'description': 'Secure coding principles applied in software development'
                }
            ]
            
            for control in iso_controls:
                session.run("""
                    MATCH (f:Framework {name: 'ISO 27001:2022'})
                    MERGE (c:Control {id: $id})
                    SET c.name = $name,
                        c.category = $category,
                        c.control_type = $control_type,
                        c.description = $description,
                        c.framework_type = 'ISO 27001'
                    MERGE (c)-[:BELONGS_TO]->(f)
                """, **control)
            
            logger.info(f"Added ISO 27001:2022 with {len(iso_controls)} controls")
    
    def create_cross_framework_mappings(self):
        """Map relationships between new frameworks and existing ones"""
        
        with self.driver.session() as session:
            # Map HIPAA to Essential 8
            hipaa_e8_mappings = [
                ("HIPAA_T1", "E8_7", "MFA supports HIPAA access control"),
                ("HIPAA_T2", "E8_8", "Backups support HIPAA audit controls"),
                ("HIPAA_A3", "E8_5", "Admin privileges support HIPAA access management"),
                ("HIPAA_T4", "E8_2", "Patching supports transmission security")
            ]
            
            # Map PCI DSS to Essential 8
            pci_e8_mappings = [
                ("PCI_8", "E8_7", "MFA meets PCI unique user ID requirement"),
                ("PCI_2", "E8_5", "Admin privileges prevent default passwords"),
                ("PCI_5", "E8_1", "Application control provides anti-malware"),
                ("PCI_6", "E8_2", "Patching maintains secure systems")
            ]
            
            # Map ISO 27001 to Essential 8
            iso_e8_mappings = [
                ("ISO_8.5", "E8_7", "MFA implements secure authentication"),
                ("ISO_8.2", "E8_5", "Admin privileges align with ISO privileged access"),
                ("ISO_8.28", "E8_2", "Patching supports secure coding practices"),
                ("ISO_8.16", "E8_8", "Backups support monitoring activities")
            ]
            
            # Create all mappings
            all_mappings = [
                ("HIPAA", hipaa_e8_mappings),
                ("PCI DSS", pci_e8_mappings),
                ("ISO 27001", iso_e8_mappings)
            ]
            
            for framework_name, mappings in all_mappings:
                for new_control, e8_control, description in mappings:
                    session.run("""
                        MATCH (c1:Control {id: $new_control})
                        MATCH (c2:Control {id: $e8_control})
                        MERGE (c1)-[r:ALIGNS_WITH]->(c2)
                        SET r.description = $description,
                            r.type = 'Cross-Framework Alignment'
                    """, new_control=new_control, e8_control=e8_control, description=description)
            
            logger.info("Created cross-framework mappings")
    
    def map_to_threats(self):
        """Map new framework controls to existing threats"""
        
        with self.driver.session() as session:
            # HIPAA threat mappings
            hipaa_threat_mappings = [
                ("HIPAA_T1", ["T_DATA_BREACH", "T_INSIDER"], "Access controls prevent breaches"),
                ("HIPAA_A2", ["T_PHISHING", "T_INSIDER"], "Training reduces human threats"),
                ("HIPAA_T4", ["T_DATA_BREACH", "T_API_EXPOSURE"], "Transmission security prevents exposure")
            ]
            
            # PCI threat mappings
            pci_threat_mappings = [
                ("PCI_3", ["T_DATA_BREACH", "T_RANSOMWARE"], "Encryption protects stored card data"),
                ("PCI_1", ["T_APT_LATERAL", "T_CLOUD_CONFIG"], "Firewalls prevent lateral movement"),
                ("PCI_10", ["T_INSIDER", "T_LIVING_LAND"], "Monitoring detects malicious activity")
            ]
            
            # ISO threat mappings
            iso_threat_mappings = [
                ("ISO_5.7", ["T_APT_LATERAL", "T_SUPPLY_SOFTWARE"], "Threat intelligence prevents APTs"),
                ("ISO_8.12", ["T_DATA_BREACH", "T_API_EXPOSURE"], "DLP prevents data breaches"),
                ("ISO_8.23", ["T_PHISHING", "T_MALWARE"], "Web filtering blocks threats")
            ]
            
            all_threat_mappings = hipaa_threat_mappings + pci_threat_mappings + iso_threat_mappings
            
            for control_id, threat_ids, reasoning in all_threat_mappings:
                for threat_id in threat_ids:
                    session.run("""
                        MATCH (c:Control {id: $control_id})
                        MATCH (t:Threat {id: $threat_id})
                        MERGE (c)-[r:PREVENTS]->(t)
                        SET r.reasoning = $reasoning,
                            r.effectiveness = 'HIGH'
                    """, control_id=control_id, threat_id=threat_id, reasoning=reasoning)
            
            logger.info("Mapped new controls to existing threats")
    
    def get_expansion_statistics(self):
        """Get statistics on the expanded knowledge graph"""
        
        with self.driver.session() as session:
            stats = {}
            
            # Total frameworks
            result = session.run("MATCH (f:Framework) RETURN count(f) as count")
            stats['total_frameworks'] = result.single()['count']
            
            # Total controls
            result = session.run("MATCH (c:Control) RETURN count(c) as count")
            stats['total_controls'] = result.single()['count']
            
            # Controls by framework
            result = session.run("""
                MATCH (f:Framework)<-[:BELONGS_TO]-(c:Control)
                RETURN f.name as framework, count(c) as control_count
                ORDER BY control_count DESC
            """)
            stats['controls_by_framework'] = [dict(r) for r in result]
            
            # Cross-framework alignments
            result = session.run("MATCH ()-[r:ALIGNS_WITH]->() RETURN count(r) as count")
            stats['cross_framework_alignments'] = result.single()['count']
            
            # Threat coverage
            result = session.run("MATCH ()-[r:PREVENTS]->() RETURN count(r) as count")
            stats['threat_prevention_relationships'] = result.single()['count']
            
            return stats
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()

def expand_to_enterprise_frameworks():
    """Main function to add enterprise frameworks"""
    
    print("\nENTERPRISE FRAMEWORK EXPANSION")
    print("=" * 50)
    print("Adding HIPAA, PCI DSS, and ISO 27001...")
    
    try:
        expander = EnterpriseFrameworkExpansion()
        
        # Add frameworks
        print("\n1. Adding HIPAA framework...")
        expander.add_hipaa_framework()
        
        print("2. Adding PCI DSS framework...")
        expander.add_pci_dss_framework()
        
        print("3. Adding ISO 27001:2022 framework...")
        expander.add_iso27001_framework()
        
        # Create relationships
        print("4. Creating cross-framework mappings...")
        expander.create_cross_framework_mappings()
        
        print("5. Mapping to threat landscape...")
        expander.map_to_threats()
        
        # Get statistics
        print("\n" + "=" * 50)
        print("EXPANSION COMPLETE - STATISTICS")
        print("=" * 50)
        
        stats = expander.get_expansion_statistics()
        print(f"Total frameworks: {stats['total_frameworks']}")
        print(f"Total controls: {stats['total_controls']}")
        print(f"Cross-framework alignments: {stats['cross_framework_alignments']}")
        print(f"Threat prevention relationships: {stats['threat_prevention_relationships']}")
        
        print("\nControls by framework:")
        for fw in stats['controls_by_framework']:
            print(f"  - {fw['framework']}: {fw['control_count']} controls")
        
        expander.close()
        
        print("\nSUCCESS: Enterprise frameworks added!")
        print("You can now assess companies against:")
        print("  • HIPAA (Healthcare)")
        print("  • PCI DSS (Payment Cards)")
        print("  • ISO 27001:2022 (International Standard)")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Framework expansion failed - {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    expand_to_enterprise_frameworks()