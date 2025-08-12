"""
Neo4j Community Edition Integration for Sentinel GRC
=====================================================
Connects your existing system to local Neo4j database (FREE)
"""

from neo4j import GraphDatabase
import json
import logging
from typing import Dict, List, Any
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class Neo4jKnowledgeGraph:
    """
    Local Neo4j Community Edition integration.
    Replaces the in-memory NetworkX graph with persistent storage.
    """
    
    def __init__(self, uri=None, user=None, password=None):
        # Use secure configuration if parameters not provided
        if not all([uri, user, password]):
            from secure_neo4j_config import get_secure_neo4j_config
            config = get_secure_neo4j_config()
            uri = uri or config.uri
            user = user or config.username
            password = password or config.password
            
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        """Close the driver connection"""
        self.driver.close()
    
    def initialize_essential8_knowledge(self):
        """Initialize Essential 8 knowledge in Neo4j"""
        
        with self.driver.session() as session:
            # Create constraints
            session.run("""
                CREATE CONSTRAINT control_id_unique IF NOT EXISTS
                FOR (c:ComplianceControl) REQUIRE c.id IS UNIQUE
            """)
            
            session.run("""
                CREATE CONSTRAINT threat_id_unique IF NOT EXISTS  
                FOR (t:ThreatVector) REQUIRE t.id IS UNIQUE
            """)
            
            # Clear existing data (for fresh start)
            session.run("MATCH (n) DETACH DELETE n")
            
            # Create Essential 8 controls
            essential8_controls = [
                {
                    "id": "E8_1",
                    "name": "Application Control", 
                    "description": "Prevent execution of unapproved programs",
                    "maturity_levels": [
                        "Basic whitelisting on workstations",
                        "Whitelisting on servers", 
                        "Centralized management with logging"
                    ],
                    "implementation_effort": "HIGH",
                    "business_impact": "MEDIUM"
                },
                {
                    "id": "E8_2",
                    "name": "Patch Applications",
                    "description": "Patch applications within timeframes", 
                    "maturity_levels": [
                        "Patch within 1 month",
                        "Patch within 2 weeks for internet-facing",
                        "Patch within 48 hours for critical"
                    ],
                    "implementation_effort": "MEDIUM",
                    "business_impact": "LOW"
                },
                {
                    "id": "E8_3", 
                    "name": "Configure Microsoft Office Macro Settings",
                    "description": "Control macro execution",
                    "maturity_levels": [
                        "Block macros from internet",
                        "Block macros except from trusted locations",
                        "Only signed macros with limited access"
                    ],
                    "implementation_effort": "LOW",
                    "business_impact": "LOW"
                },
                {
                    "id": "E8_4",
                    "name": "User Application Hardening", 
                    "description": "Harden user applications",
                    "maturity_levels": [
                        "Basic browser hardening",
                        "ASLR for all applications",
                        "Additional hardening with logging"
                    ],
                    "implementation_effort": "MEDIUM", 
                    "business_impact": "LOW"
                },
                {
                    "id": "E8_5",
                    "name": "Restrict Administrative Privileges",
                    "description": "Limit admin access based on duties",
                    "maturity_levels": [
                        "Restrict and review annually",
                        "Just-in-time admin, review 6-monthly", 
                        "Privileged access management with monitoring"
                    ],
                    "implementation_effort": "MEDIUM",
                    "business_impact": "HIGH"
                },
                {
                    "id": "E8_6",
                    "name": "Patch Operating Systems",
                    "description": "Patch OS vulnerabilities",
                    "maturity_levels": [
                        "Patch within 1 month",
                        "Patch within 2 weeks for internet-facing",
                        "Patch within 48 hours with automation"
                    ],
                    "implementation_effort": "MEDIUM",
                    "business_impact": "LOW"
                },
                {
                    "id": "E8_7",
                    "name": "Multi-factor Authentication", 
                    "description": "MFA for users and privileged actions",
                    "maturity_levels": [
                        "MFA for remote access",
                        "MFA for privileged users and sensitive data",
                        "MFA for all users with phishing-resistant methods"
                    ],
                    "implementation_effort": "LOW",
                    "business_impact": "HIGH"
                },
                {
                    "id": "E8_8",
                    "name": "Regular Backups",
                    "description": "Daily backups with testing", 
                    "maturity_levels": [
                        "Daily backups, quarterly testing",
                        "Automated backups, monthly testing, offsite",
                        "Immutable backups, weekly testing, automated recovery"
                    ],
                    "implementation_effort": "MEDIUM",
                    "business_impact": "HIGH"
                }
            ]
            
            # Create control nodes
            for control in essential8_controls:
                session.run("""
                    CREATE (c:ComplianceControl {
                        id: $id,
                        name: $name,
                        description: $description,
                        maturity_levels: $maturity_levels,
                        implementation_effort: $implementation_effort,
                        business_impact: $business_impact,
                        framework: 'Essential8'
                    })
                """, **control)
            
            # Create threat vectors
            threats = [
                {"id": "T1", "name": "Ransomware", "severity": "CRITICAL"},
                {"id": "T2", "name": "Phishing", "severity": "HIGH"}, 
                {"id": "T3", "name": "Insider Threat", "severity": "MEDIUM"},
                {"id": "T4", "name": "Supply Chain Attack", "severity": "HIGH"},
                {"id": "T5", "name": "Zero-Day Exploit", "severity": "CRITICAL"}
            ]
            
            for threat in threats:
                session.run("""
                    CREATE (t:ThreatVector {
                        id: $id,
                        name: $name, 
                        severity: $severity
                    })
                """, **threat)
            
            # Create relationships
            relationships = [
                ("E8_1", "T1", "prevents"),  # App control prevents ransomware
                ("E8_1", "T4", "prevents"),  # App control prevents supply chain
                ("E8_2", "T5", "mitigates"), # Patching mitigates zero-days
                ("E8_3", "T2", "prevents"),  # Macro settings prevent phishing
                ("E8_5", "T3", "mitigates"), # Privilege restriction mitigates insider
                ("E8_7", "T2", "prevents"),  # MFA prevents phishing
                ("E8_8", "T1", "recovers"),  # Backups recover from ransomware
            ]
            
            for control_id, threat_id, relationship in relationships:
                session.run("""
                    MATCH (c:ComplianceControl {id: $control_id})
                    MATCH (t:ThreatVector {id: $threat_id})
                    CREATE (c)-[r:RELATIONSHIP {type: $relationship}]->(t)
                """, control_id=control_id, threat_id=threat_id, relationship=relationship)
            
            logger.info("Essential 8 knowledge graph initialized successfully")
    
    def get_control_importance(self, control_id: str, company_profile) -> float:
        """Calculate control importance for specific company"""
        
        with self.driver.session() as session:
            # Get control and its relationships
            result = session.run("""
                MATCH (c:ComplianceControl {id: $control_id})
                OPTIONAL MATCH (c)-[r]->(t:ThreatVector)
                RETURN c, collect({threat: t, relationship: r.type}) as relationships
            """, control_id=control_id)
            
            record = result.single()
            if not record:
                return 0.5
            
            control = record["c"]
            relationships = record["relationships"]
            
            base_importance = 0.5
            
            # Adjust based on business impact
            if control.get("business_impact") == "HIGH":
                base_importance += 0.2
            
            # Adjust based on threats mitigated
            critical_threats = [r for r in relationships 
                              if r["threat"] and r["threat"].get("severity") == "CRITICAL"]
            base_importance += len(critical_threats) * 0.1
            
            # Industry-specific adjustments
            if hasattr(company_profile, 'industry'):
                if company_profile.industry in ["Healthcare", "Finance", "Government"]:
                    base_importance += 0.15
            
            return min(base_importance, 1.0)
    
    def get_implementation_sequence(self, gaps: List[str]) -> List[tuple]:
        """Determine optimal implementation sequence"""
        
        with self.driver.session() as session:
            sequence = []
            
            for gap in gaps:
                result = session.run("""
                    MATCH (c:ComplianceControl {id: $gap})
                    OPTIONAL MATCH (c)-[r]->(t:ThreatVector)
                    RETURN c, count(t) as threat_count,
                           size([rel in collect(r) WHERE rel.type = 'prevents']) as prevents_count
                """, gap=gap)
                
                record = result.single()
                if record:
                    control = record["c"]
                    threat_count = record["threat_count"]
                    prevents_count = record["prevents_count"]
                    
                    # Calculate priority score
                    priority = 0.0
                    
                    # Low effort, high impact first
                    if control.get("implementation_effort") == "LOW":
                        priority += 0.3
                    if control.get("business_impact") == "HIGH":
                        priority += 0.3
                    
                    # Threat mitigation value
                    priority += threat_count * 0.1
                    priority += prevents_count * 0.15  # Prevention worth more than mitigation
                    
                    sequence.append((gap, priority))
            
            # Sort by priority descending
            sequence.sort(key=lambda x: x[1], reverse=True)
            return sequence
    
    def store_assessment_result(self, assessment_result):
        """Store assessment results in graph"""
        
        with self.driver.session() as session:
            # Create assessment node
            session.run("""
                CREATE (a:Assessment {
                    id: randomUUID(),
                    company_name: $company_name,
                    framework: $framework,
                    overall_maturity: $overall_maturity,
                    confidence_score: $confidence_score,
                    timestamp: datetime()
                })
            """, 
            company_name=assessment_result.company_profile.company_name,
            framework=assessment_result.framework, 
            overall_maturity=assessment_result.overall_maturity,
            confidence_score=assessment_result.confidence_score)
    
    def query_similar_assessments(self, company_profile) -> List[Dict]:
        """Find similar company assessments for benchmarking"""
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Assessment)
                WHERE a.company_name <> $company_name
                RETURN a.company_name as company,
                       a.framework as framework,
                       a.overall_maturity as maturity,
                       a.confidence_score as confidence
                ORDER BY a.timestamp DESC
                LIMIT 10
            """, company_name=company_profile.company_name)
            
            return [dict(record) for record in result]


# Integration with your existing system
class Enhanced_ComplianceKnowledgeGraph:
    """
    Enhanced version of your existing ComplianceKnowledgeGraph
    that uses Neo4j instead of NetworkX
    """
    
    def __init__(self):
        # Try to connect to Neo4j, fall back to NetworkX if not available
        try:
            self.neo4j_graph = Neo4jKnowledgeGraph()
            self.neo4j_graph.initialize_essential8_knowledge()
            self.use_neo4j = True
            logger.info("Connected to Neo4j Community Edition")
        except Exception as e:
            logger.warning(f"Neo4j not available: {e}. Falling back to NetworkX")
            # Import your existing NetworkX implementation
            from sentinel_grc_complete import ComplianceKnowledgeGraph
            self.networkx_graph = ComplianceKnowledgeGraph()
            self.use_neo4j = False
    
    def get_control_importance(self, control_id: str, company_profile) -> float:
        """Delegate to appropriate graph implementation"""
        if self.use_neo4j:
            return self.neo4j_graph.get_control_importance(control_id, company_profile)
        else:
            return self.networkx_graph.get_control_importance(control_id, company_profile)
    
    def get_implementation_sequence(self, gaps: List[str]) -> List[tuple]:
        """Delegate to appropriate graph implementation"""
        if self.use_neo4j:
            return self.neo4j_graph.get_implementation_sequence(gaps)
        else:
            return self.networkx_graph.get_implementation_sequence(gaps)
    
    def close(self):
        """Clean up connections"""
        if self.use_neo4j:
            self.neo4j_graph.close()


# Quick setup script
def setup_neo4j_locally():
    """
    Setup script for Neo4j Community Edition
    Run this after installing Neo4j CE
    """
    print("Setting up Neo4j Community Edition for Sentinel GRC...")
    
    try:
        # Test connection using secure configuration
        graph = Neo4jKnowledgeGraph()  # Uses secure config manager
        
        # Initialize knowledge
        graph.initialize_essential8_knowledge()
        
        # Test query
        with graph.driver.session() as session:
            result = session.run("MATCH (c:ComplianceControl) RETURN count(c) as control_count")
            count = result.single()["control_count"]
            print(f"Successfully created {count} compliance controls")
        
        graph.close()
        print("Neo4j setup completed successfully!")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        print("Make sure Neo4j Community Edition is running on localhost:7687")
        print("And update the password in the script")


if __name__ == "__main__":
    setup_neo4j_locally()