"""
Neo4j Cloud Setup for International Demo Access
===============================================
Solves the "Neo4j not on laptop" problem for US colleagues.
Uses Neo4j Aura free tier - always accessible, zero local dependencies.
"""

import os
import logging
from typing import Dict, Any, Optional
import streamlit as st

logger = logging.getLogger(__name__)

class CloudNeo4jDemo:
    """
    Cloud-based Neo4j setup for international demo access.
    Eliminates laptop dependency issues for US colleagues.
    """
    
    def __init__(self):
        self.setup_instructions = self._create_setup_guide()
        self.fallback_available = True
        
    def _create_setup_guide(self) -> str:
        return """
# Neo4j Cloud Setup for US Colleagues 🇺🇸

## Option 1: Neo4j Aura (Recommended) ⭐
**Setup Time:** 10 minutes
**Cost:** FREE (up to 1GB)
**Always accessible:** ✅

### Steps:
1. Go to: https://neo4j.com/cloud/aura-free/
2. Sign up with your email
3. Create a new instance:
   - Instance name: "SentinelGRC-Demo"  
   - Region: "US East" (for US colleagues)
   - Database: Leave default
4. Save your credentials:
   - URI: neo4j+s://xxxxx.databases.neo4j.io
   - Username: neo4j
   - Password: [generated password]
5. Update your .env file:
   ```
   NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_aura_password
   ```

## Option 2: Mock Database (Quick Demo) 🚀
If you need immediate access without setup:
- Uses pre-populated demo data
- No external dependencies
- Perfect for presentations

## Option 3: Streamlit Cloud Deployment 🌐
We can deploy the entire platform to Streamlit Cloud:
- URL: https://sentinelgrc-demo.streamlit.app
- Always accessible to anyone
- Uses cloud Neo4j automatically
        """
    
    def check_neo4j_availability(self) -> Dict[str, Any]:
        """Check if Neo4j is available and what options we have"""
        
        try:
            # Try to import Neo4j and connect
            from secure_neo4j_config import get_secure_neo4j_config
            config = get_secure_neo4j_config()
            
            # Test connection
            from neo4j import GraphDatabase
            driver = GraphDatabase.driver(
                config.uri, 
                auth=(config.username, config.password)
            )
            driver.verify_connectivity()
            driver.close()
            
            return {
                "status": "connected",
                "type": "cloud" if "neo4j.io" in config.uri else "local",
                "uri": config.uri,
                "message": "✅ Neo4j connection successful"
            }
            
        except ImportError:
            return {
                "status": "no_driver",
                "message": "❌ Neo4j driver not installed. Run: pip install neo4j",
                "fix": "pip install neo4j"
            }
            
        except Exception as e:
            return {
                "status": "connection_failed", 
                "message": f"❌ Cannot connect to Neo4j: {str(e)}",
                "solutions": [
                    "1. Use Neo4j Aura Cloud (recommended)",
                    "2. Use mock database mode",  
                    "3. Install local Neo4j"
                ]
            }
    
    def create_streamlit_setup_interface(self):
        """Create Streamlit interface for Neo4j setup"""
        
        st.header("🔧 Neo4j Setup for Demo")
        
        # Check current status
        status = self.check_neo4j_availability()
        
        if status["status"] == "connected":
            st.success(status["message"])
            if "cloud" in status.get("type", ""):
                st.info("🌍 Using Neo4j Cloud - perfect for international demo access!")
            return True
            
        else:
            st.warning(status["message"])
            
            # Show setup options
            st.subheader("Setup Options for US Colleagues")
            
            tab1, tab2, tab3 = st.tabs([
                "☁️ Neo4j Cloud (Best)", 
                "🚀 Mock Mode (Quick)", 
                "📋 Setup Guide"
            ])
            
            with tab1:
                st.markdown("""
                ### Neo4j Aura Cloud Setup
                **Perfect for US colleagues - no laptop installation needed!**
                
                1. **Sign up**: [Neo4j Aura Free](https://neo4j.com/cloud/aura-free/)
                2. **Create instance** in US region  
                3. **Copy credentials** to .env file
                4. **Restart this app** - should work immediately!
                
                **Benefits:**
                - ✅ Always accessible from anywhere
                - ✅ No local installation 
                - ✅ Professional appearance
                - ✅ Free tier sufficient for demos
                """)
                
                if st.button("🔄 Test Connection Again"):
                    st.rerun()
                    
            with tab2:
                st.markdown("""
                ### Mock Database Mode
                **For immediate demo access without any setup**
                
                - Uses pre-populated demo data
                - No external dependencies
                - Perfect for presentations
                """)
                
                if st.button("🚀 Use Mock Mode"):
                    st.session_state.use_mock_neo4j = True
                    st.success("Mock mode enabled! Assessment will use demo data.")
                    
            with tab3:
                st.markdown(self.setup_instructions)
                
        return False

def enable_mock_mode():
    """Enable mock mode for demos without Neo4j"""
    
    class MockNeo4jGraph:
        """Mock Neo4j for demos"""
        
        def __init__(self):
            self.demo_data = {
                "frameworks": ["Essential 8", "Privacy Act", "APRA CPS 234", "SOC 2"],
                "controls": 72,
                "relationships": 155
            }
        
        def query(self, cypher_query: str):
            """Return mock data based on query patterns"""
            
            if "MATCH (f:Framework)" in cypher_query:
                return [{"name": fw} for fw in self.demo_data["frameworks"]]
            elif "MATCH (c:Control)" in cypher_query:
                return [{"id": f"CTRL_{i}", "name": f"Demo Control {i}"} 
                       for i in range(1, 11)]
            else:
                return []
        
        def close(self):
            pass
    
    return MockNeo4jGraph()

# Streamlit demo interface
if __name__ == "__main__":
    st.title("Neo4j Setup for International Demo")
    
    demo = CloudNeo4jDemo()
    demo.create_streamlit_setup_interface()