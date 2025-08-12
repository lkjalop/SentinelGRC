"""
Direct Neo4j Test - Check if data loaded correctly
"""

from neo4j import GraphDatabase

def test_neo4j_data():
    """Test if Neo4j has the Essential 8 data"""
    
    print("Testing Neo4j data directly...")
    
    try:
        # Connect to Neo4j
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Ag3nt-GRC"))
        
        with driver.session() as session:
            # Check controls
            result = session.run("MATCH (c:Control) RETURN count(c) as count")
            control_count = result.single()["count"]
            print(f"Controls in database: {control_count}")
            
            # Check threats
            result = session.run("MATCH (t:Threat) RETURN count(t) as count")
            threat_count = result.single()["count"]
            print(f"Threats in database: {threat_count}")
            
            # Check relationships
            result = session.run("MATCH ()-[r:PREVENTS]->() RETURN count(r) as count")
            rel_count = result.single()["count"]
            print(f"PREVENTS relationships: {rel_count}")
            
            # Show sample data
            if control_count > 0:
                print("\nSample controls:")
                result = session.run("MATCH (c:Control) RETURN c.id, c.name LIMIT 3")
                for record in result:
                    print(f"  {record['c.id']}: {record['c.name']}")
            
            if threat_count > 0:
                print("\nSample threats:")
                result = session.run("MATCH (t:Threat) RETURN t.id, t.name LIMIT 3") 
                for record in result:
                    print(f"  {record['t.id']}: {record['t.name']}")
        
        driver.close()
        
        # Summary
        if control_count >= 8 and threat_count >= 5 and rel_count >= 10:
            print("\nSUCCESS: Neo4j has all required data")
            return True
        else:
            print(f"\nWARNING: Data incomplete - Controls:{control_count}, Threats:{threat_count}, Relations:{rel_count}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_neo4j_data()