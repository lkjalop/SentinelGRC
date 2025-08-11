

"""
Neo4j Knowledge Graph for Compliance Relationships
This replaces the simple NetworkX graph with a proper graph database
"""

from neo4j import GraphDatabase
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ComplianceKnowledgeGraph:
    """
    Neo4j-powered knowledge graph for compliance relationships.
    This is like upgrading from a paper map to Google Maps.
    """
    
    def __init__(self):
        # Connect to your local Neo4j
        self.uri = "neo4j://localhost:7687"
        self.username = "neo4j"
        self.password = "Ag3nt-GRC"  # The password you set
        
        # Create driver connection
        self.driver = GraphDatabase.driver(
            self.uri, 
            auth=(self.username, self.password)
        )
        
        # Verify connection
        self.driver.verify_connectivity()
        logger.info("Connected to Neo4j successfully")
        
        # Initialize the schema
        self._initialize_schema()
        
    def _initialize_schema(self):
        """
        Create indexes and constraints for better performance.
        Like creating a table of contents for a book.
        """
        with self.driver.session() as session:
            # Create uniqueness constraints (prevents duplicates)
            queries = [
                "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Control) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Threat) REQUIRE t.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Framework) REQUIRE f.name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Asset) REQUIRE a.id IS UNIQUE",
                
                # Create indexes for faster searches
                "CREATE INDEX IF NOT EXISTS FOR (c:Control) ON (c.name)",
                "CREATE INDEX IF NOT EXISTS FOR (t:Threat) ON (t.severity)",
                "CREATE INDEX IF NOT EXISTS FOR (c:Company) ON (c.name)",
            ]
            
            for query in queries:
                session.run(query)
                
            logger.info("Neo4j schema initialized")
    
    def close(self):
        """Always close the driver when done"""
        self.driver.close()