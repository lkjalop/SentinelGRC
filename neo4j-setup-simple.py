"""
NEO4J SETUP FOR SENTINEL GRC
============================
Complete Neo4j integration for compliance knowledge graph
Uses secure configuration management - no hardcoded credentials.
Set NEO4J_PASSWORD environment variable or use .env file.
"""

# First, install Neo4j driver in your terminal:
# pip install neo4j

from neo4j import GraphDatabase
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplianceKnowledgeGraph:
    """
    Neo4j Knowledge Graph for GRC Compliance
    Connects controls, threats, and companies
    """
    
    def __init__(self):
        # Use secure configuration instead of hardcoded credentials
        from secure_neo4j_config import get_secure_neo4j_config
        config = get_secure_neo4j_config()
        
        self.uri = config.uri
        self.username = config.username
        self.password = config.password
        
        try:
            # Connect to Neo4j
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.username, self.password)
            )
            # Test connection
            self.driver.verify_connectivity()
            logger.info("✓ Connected to Neo4j successfully")
        except Exception as e:
            logger.error(f"✗ Failed to connect to Neo4j: {e}")
            logger.info("Make sure Neo4j Desktop is running with password: Ag3nt-GRC")
            raise
    
    def setup_database(self):
        """
        Create indexes and constraints for better performance
        Run this once when setting up
        """
        with self.driver.session() as session:
            # Create constraints (prevents duplicates)
            constraints = [
                "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Control) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Threat) REQUIRE t.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (company:Company) REQUIRE company.name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Framework) REQUIRE f.name IS UNIQUE",
            ]
            
            for constraint in constraints:
                session.run(constraint)
                logger.info(f"✓ Created: {constraint[:50]}...")
            
            logger.info("✓ Database setup complete")
    
    def load_essential8(self):
        """
        Load Essential 8 controls into Neo4j
        """
        with self.driver.session() as session:
            # Create Essential 8 Framework
            session.run("""
                MERGE (f:Framework {name: 'Essential8'})
                SET f.country = 'Australia',
                    f.description = 'Australian Cyber Security Centre Essential Eight'
            """)
            
            # Essential 8 Controls
            controls = [
                {
                    'id': 'E8_1',
                    'name': 'Application Control',
                    'description': 'Prevent execution of unapproved/malicious programs',
                    'effort': 'HIGH',
                    'impact': 'CRITICAL'
                },
                {
                    'id': 'E8_2',
                    'name': 'Patch Applications',
                    'description': 'Patch applications within 48 hours to 1 month',
                    'effort': 'MEDIUM',
                    'impact': 'HIGH'
                },
                {
                    'id': 'E8_3',
                    'name': 'Configure Microsoft Office Macro Settings',
                    'description': 'Block macros from the internet and untrusted sources',
                    'effort': 'LOW',
                    'impact': 'MEDIUM'
                },
                {
                    'id': 'E8_4',
                    'name': 'User Application Hardening',
                    'description': 'Configure web browsers to block Flash, ads and Java',
                    'effort': 'MEDIUM',
                    'impact': 'MEDIUM'
                },
                {
                    'id': 'E8_5',
                    'name': 'Restrict Administrative Privileges',
                    'description': 'Limit admin rights based on duties',
                    'effort': 'MEDIUM',
                    'impact': 'HIGH'
                },
                {
                    'id': 'E8_6',
                    'name': 'Patch Operating Systems',
                    'description': 'Patch OS vulnerabilities within 48 hours to 1 month',
                    'effort': 'MEDIUM',
                    'impact': 'HIGH'
                },
                {
                    'id': 'E8_7',
                    'name': 'Multi-factor Authentication',
                    'description': 'MFA for all users accessing sensitive data',
                    'effort': 'LOW',
                    'impact': 'CRITICAL'
                },
                {
                    'id': 'E8_8',
                    'name': 'Regular Backups',
                    'description': 'Daily backups with regular restoration tests',
                    'effort': 'MEDIUM',
                    'impact': 'CRITICAL'
                }
            ]
            
            # Create each control
            for control in controls:
                session.run("""
                    MATCH (f:Framework {name: 'Essential8'})
                    MERGE (c:Control {id: $id})
                    SET c.name = $name,
                        c.description = $description,
                        c.effort = $effort,
                        c.impact = $impact
                    MERGE (c)-[:BELONGS_TO]->(f)
                """, **control)
                logger.info(f"✓ Created control: {control['name']}")
            
            logger.info("✓ Essential 8 controls loaded")
    
    def load_threats(self):
        """
        Load threat data and connect to controls
        """
        with self.driver.session() as session:
            # Define threats and which controls prevent them
            threat_mappings = [
                {
                    'threat_id': 'T_RANSOMWARE',
                    'threat_name': 'Ransomware',
                    'severity': 'CRITICAL',
                    'prevented_by': ['E8_1', 'E8_2', 'E8_6', 'E8_8']  # App control, patching, backups
                },
                {
                    'threat_id': 'T_PHISHING',
                    'threat_name': 'Phishing',
                    'severity': 'HIGH',
                    'prevented_by': ['E8_3', 'E8_7', 'E8_4']  # Macros, MFA, hardening
                },
                {
                    'threat_id': 'T_INSIDER',
                    'threat_name': 'Insider Threat',
                    'severity': 'MEDIUM',
                    'prevented_by': ['E8_5', 'E8_7']  # Admin privileges, MFA
                },
                {
                    'threat_id': 'T_MALWARE',
                    'threat_name': 'Malware',
                    'severity': 'HIGH',
                    'prevented_by': ['E8_1', 'E8_2', 'E8_4', 'E8_6']  # App control, patching
                },
                {
                    'threat_id': 'T_DATA_BREACH',
                    'threat_name': 'Data Breach',
                    'severity': 'CRITICAL',
                    'prevented_by': ['E8_7', 'E8_5', 'E8_8']  # MFA, privileges, backups
                }
            ]
            
            for mapping in threat_mappings:
                # Create threat
                session.run("""
                    MERGE (t:Threat {id: $threat_id})
                    SET t.name = $threat_name,
                        t.severity = $severity
                """, 
                threat_id=mapping['threat_id'],
                threat_name=mapping['threat_name'],
                severity=mapping['severity'])
                
                # Connect controls to threats
                for control_id in mapping['prevented_by']:
                    session.run("""
                        MATCH (c:Control {id: $control_id})
                        MATCH (t:Threat {id: $threat_id})
                        MERGE (c)-[:PREVENTS]->(t)
                    """, control_id=control_id, threat_id=mapping['threat_id'])
                
                logger.info(f"✓ Created threat: {mapping['threat_name']} with {len(mapping['prevented_by'])} controls")
            
            logger.info("✓ Threats loaded and connected")
    
    def assess_company(self, company_name: str, implemented_controls: List[str]) -> Dict[str, Any]:
        """
        Assess a company's compliance and risk
        
        Args:
            company_name: Name of the company
            implemented_controls: List of control IDs they have (e.g., ['E8_7', 'E8_8'])
        
        Returns:
            Assessment with threats, gaps, and recommendations
        """
        with self.driver.session() as session:
            # Create or update company
            session.run("""
                MERGE (c:Company {name: $name})
                SET c.assessed_date = datetime()
            """, name=company_name)
            
            # Connect company to implemented controls
            for control_id in implemented_controls:
                session.run("""
                    MATCH (company:Company {name: $name})
                    MATCH (control:Control {id: $control_id})
                    MERGE (company)-[:HAS_IMPLEMENTED]->(control)
                """, name=company_name, control_id=control_id)
            
            # Find missing controls
            missing = session.run("""
                MATCH (c:Control)
                WHERE NOT c.id IN $implemented
                RETURN c.id as id, c.name as name, c.effort as effort, c.impact as impact
                ORDER BY c.impact DESC, c.effort ASC
            """, implemented=implemented_controls)
            
            missing_controls = [dict(record) for record in missing]
            
            # Find exposed threats (threats not prevented due to missing controls)
            exposed = session.run("""
                MATCH (t:Threat)
                WHERE NOT EXISTS {
                    MATCH (c:Control)-[:PREVENTS]->(t)
                    WHERE c.id IN $implemented
                }
                RETURN t.name as threat, t.severity as severity
                ORDER BY t.severity DESC
            """, implemented=implemented_controls)
            
            exposed_threats = [dict(record) for record in exposed]
            
            # Get recommendations (quick wins - low effort, high impact)
            recommendations = session.run("""
                MATCH (c:Control)-[:PREVENTS]->(t:Threat)
                WHERE NOT c.id IN $implemented
                WITH c, count(t) as threats_prevented
                RETURN c.name as control, 
                       c.effort as effort,
                       c.impact as impact,
                       threats_prevented
                ORDER BY c.effort ASC, threats_prevented DESC
                LIMIT 3
            """, implemented=implemented_controls)
            
            top_recommendations = [dict(record) for record in recommendations]
            
            return {
                'company': company_name,
                'implemented_controls': implemented_controls,
                'missing_controls': missing_controls,
                'exposed_threats': exposed_threats,
                'recommendations': top_recommendations,
                'compliance_percentage': (len(implemented_controls) / 8) * 100
            }
    
    def get_implementation_path(self, current_controls: List[str]) -> List[Dict]:
        """
        Get optimal order to implement missing controls
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Control)
                WHERE NOT c.id IN $current
                OPTIONAL MATCH (c)-[:PREVENTS]->(t:Threat)
                WITH c, collect(t.name) as threats_prevented, count(t) as threat_count
                RETURN c.name as control,
                       c.effort as effort,
                       c.impact as impact,
                       threats_prevented,
                       threat_count
                ORDER BY 
                    CASE c.effort 
                        WHEN 'LOW' THEN 1 
                        WHEN 'MEDIUM' THEN 2 
                        WHEN 'HIGH' THEN 3 
                    END ASC,
                    threat_count DESC
            """, current=current_controls)
            
            return [dict(record) for record in result]
    
    def close(self):
        """Close the Neo4j connection"""
        self.driver.close()
        logger.info("✓ Neo4j connection closed")

# ============================================
# USAGE EXAMPLES
# ============================================

def setup_neo4j():
    """
    One-time setup to initialize Neo4j with Essential 8 data
    """
    print("\n" + "="*50)
    print("SETTING UP NEO4J FOR SENTINEL GRC")
    print("="*50)
    
    # Initialize connection
    kg = ComplianceKnowledgeGraph()
    
    # Setup database structure
    kg.setup_database()
    
    # Load Essential 8 framework
    kg.load_essential8()
    
    # Load threats and relationships
    kg.load_threats()
    
    print("\n✓ Neo4j setup complete!")
    print("✓ You can now view your graph at http://localhost:7474")
    print("✓ Username: neo4j")
    print("✓ Password: Ag3nt-GRC")
    
    # Close connection
    kg.close()

def test_assessment():
    """
    Test company assessment
    """
    print("\n" + "="*50)
    print("TESTING COMPANY ASSESSMENT")
    print("="*50)
    
    kg = ComplianceKnowledgeGraph()
    
    # Assess a company that only has MFA and Backups
    result = kg.assess_company(
        company_name="TechCorp Pty Ltd",
        implemented_controls=["E8_7", "E8_8"]  # Only MFA and Backups
    )
    
    print(f"\nCompany: {result['company']}")
    print(f"Compliance: {result['compliance_percentage']:.0f}%")
    
    print("\n🚨 EXPOSED THREATS:")
    for threat in result['exposed_threats'][:3]:
        print(f"   - {threat['threat']} ({threat['severity']})")
    
    print("\n📋 TOP RECOMMENDATIONS:")
    for rec in result['recommendations']:
        print(f"   - {rec['control']} (Effort: {rec['effort']}, Prevents {rec['threats_prevented']} threats)")
    
    print("\n🛤️ IMPLEMENTATION PATH:")
    path = kg.get_implementation_path(["E8_7", "E8_8"])
    for i, step in enumerate(path[:3], 1):
        print(f"   {i}. {step['control']} - {step['effort']} effort - Prevents: {', '.join(step['threats_prevented'])}")
    
    kg.close()

# ============================================
# CYPHER QUERIES FOR NEO4J BROWSER
# ============================================

"""
USEFUL CYPHER QUERIES TO RUN IN NEO4J BROWSER:

1. See all Essential 8 controls and their relationships:
MATCH (c:Control)-[r]->(t:Threat)
RETURN c, r, t

2. Find which controls prevent ransomware:
MATCH (c:Control)-[:PREVENTS]->(t:Threat {name: 'Ransomware'})
RETURN c.name as Control, c.effort as Effort

3. See a company's compliance posture:
MATCH (company:Company {name: 'TechCorp Pty Ltd'})-[:HAS_IMPLEMENTED]->(control:Control)
RETURN company, control

4. Find critical gaps for a company:
MATCH (t:Threat {severity: 'CRITICAL'})
WHERE NOT EXISTS {
    MATCH (c:Control)-[:PREVENTS]->(t)
    MATCH (:Company {name: 'TechCorp Pty Ltd'})-[:HAS_IMPLEMENTED]->(c)
}
RETURN t.name as UnprotectedThreat

5. Get implementation statistics:
MATCH (c:Control)
OPTIONAL MATCH (c)-[:PREVENTS]->(t:Threat)
RETURN c.name as Control, 
       c.effort as Effort,
       count(t) as ThreatsPrevented
ORDER BY ThreatsPrevented DESC
"""

if __name__ == "__main__":
    # Run this to set up Neo4j
    setup_neo4j()
    
    # Then test with a sample company
    test_assessment()
