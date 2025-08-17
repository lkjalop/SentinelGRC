"""
Secure Neo4j Configuration Manager
Handles credentials and connection settings securely using environment variables
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class Neo4jConfig:
    """Neo4j connection configuration"""
    uri: str
    username: str
    password: str
    database: str = "neo4j"
    encrypted: bool = True
    trust: str = "TRUST_SYSTEM_CA_SIGNED_CERTIFICATES"

def get_secure_neo4j_config() -> Neo4jConfig:
    """
    Get Neo4j configuration from environment variables
    Falls back to secure defaults for development
    """
    
    # Try environment variables first (production)
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_username = os.getenv('NEO4J_USERNAME') 
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    neo4j_database = os.getenv('NEO4J_DATABASE', 'neo4j')
    
    # If environment variables not set, use secure development defaults
    if not all([neo4j_uri, neo4j_username, neo4j_password]):
        logger.warning("⚠️ Neo4j environment variables not found. Using development configuration.")
        
        # Check for local .env file
        env_file = Path('.env')
        if env_file.exists():
            logger.info("📄 Loading configuration from .env file")
            load_env_file(env_file)
            
            neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            neo4j_username = os.getenv('NEO4J_USERNAME', 'neo4j')
            neo4j_password = os.getenv('NEO4J_PASSWORD', 'sentinel-grc-2025')
        else:
            # Secure development defaults
            neo4j_uri = 'bolt://localhost:7687'
            neo4j_username = 'neo4j'
            neo4j_password = 'sentinel-grc-2025'  # Default for local development
            
            logger.info("🔧 Using development defaults. Create .env file for custom config.")
    
    config = Neo4jConfig(
        uri=neo4j_uri,
        username=neo4j_username,
        password=neo4j_password,
        database=neo4j_database
    )
    
    logger.info(f"📡 Neo4j configuration loaded: {config.uri} (database: {config.database})")
    return config

def load_env_file(env_file: Path):
    """Load environment variables from .env file"""
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        logger.error(f"❌ Error loading .env file: {e}")

def test_neo4j_connection(config: Optional[Neo4jConfig] = None) -> bool:
    """Test Neo4j connection with given or default configuration"""
    
    if config is None:
        config = get_secure_neo4j_config()
    
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            config.uri,
            auth=(config.username, config.password)
        )
        
        # Test connection
        driver.verify_connectivity()
        
        # Test basic query
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            test_value = result.single()["test"]
            
        driver.close()
        
        logger.info("✅ Neo4j connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Neo4j connection test failed: {e}")
        return False

def create_development_env_template():
    """Create a template .env file for development"""
    
    env_template = """# Sentinel GRC Neo4j Configuration
# Copy this file to .env and update with your settings

# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-secure-password-here
NEO4J_DATABASE=sentinel_grc

# Alternative: Neo4j Aura (Cloud)
# NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=your-aura-password

# API Configuration  
API_SECRET_KEY=your-secret-key-here
DEBUG=false

# External Integrations
GITHUB_TOKEN=your-github-token
SLACK_WEBHOOK=your-slack-webhook-url
"""
    
    env_file = Path('.env.template')
    with open(env_file, 'w') as f:
        f.write(env_template)
    
    logger.info(f"📄 Created environment template: {env_file}")
    logger.info("📝 Copy .env.template to .env and update with your credentials")

if __name__ == "__main__":
    # Test the configuration
    logging.basicConfig(level=logging.INFO)
    
    print("🔧 Testing Neo4j configuration...")
    config = get_secure_neo4j_config()
    print(f"📡 URI: {config.uri}")
    print(f"👤 Username: {config.username}")
    print(f"🔒 Password: {'*' * len(config.password)}")
    
    print("\n🧪 Testing connection...")
    if test_neo4j_connection(config):
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        print("\n📝 Creating .env template...")
        create_development_env_template()