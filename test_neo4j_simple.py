"""
Simple Neo4j Integration Test (Windows Compatible)
================================================
Tests Neo4j integration without Unicode issues.
"""

import asyncio
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_neo4j_connection():
    """Check if Neo4j is running and accessible"""
    
    print("\n=== Testing Neo4j Connection ===")
    
    try:
        from neo4j import GraphDatabase
        
        # Your Neo4j connection details
        uri = "bolt://localhost:7687"
        username = "neo4j"  
        password = "Ag3nt-GRC"  # From your neo4j-setup-simple.py
        
        print(f"Connecting to: {uri}")
        print(f"Username: {username}")
        print("Password: [PROTECTED]")
        
        # Try to connect
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        
        print("SUCCESS: Neo4j connection established")
        
        # Test a simple query
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' as message")
            record = result.single()
            print(f"Test query result: {record['message']}")
        
        driver.close()
        return True
        
    except ImportError:
        print("ERROR: Neo4j driver not installed")
        print("Install with: pip install neo4j")
        return False
    except Exception as e:
        print(f"ERROR: Neo4j connection failed - {e}")
        print("\nTroubleshooting:")
        print("1. Is Neo4j Desktop running?")
        print("2. Is the database started?") 
        print("3. Is the password 'Ag3nt-GRC' correct?")
        print("4. Is it running on bolt://localhost:7687?")
        return False

def test_essential8_data():
    """Test if Essential 8 data is loaded"""
    
    print("\n=== Testing Essential 8 Data ===")
    
    try:
        # Import with hyphenated filename
        import importlib.util
        spec = importlib.util.spec_from_file_location("neo4j_setup_simple", "neo4j-setup-simple.py")
        neo4j_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(neo4j_module)
        
        ComplianceKnowledgeGraph = neo4j_module.ComplianceKnowledgeGraph
        
        # Initialize knowledge graph
        kg = ComplianceKnowledgeGraph()
        
        print("SUCCESS: Knowledge graph initialized")
        
        # Test basic query
        with kg.driver.session() as session:
            # Check if Essential 8 controls exist
            result = session.run("""
                MATCH (c:Control)
                RETURN count(c) as control_count
            """)
            
            record = result.single()
            control_count = record['control_count'] if record else 0
            
            print(f"Essential 8 controls in database: {control_count}")
            
            if control_count == 0:
                print("WARNING: No controls found - need to run setup")
                return False
            elif control_count < 8:
                print("WARNING: Incomplete Essential 8 data")
                return False
            else:
                print("SUCCESS: Essential 8 data complete")
                
            # Test threats
            result = session.run("""
                MATCH (t:Threat)
                RETURN count(t) as threat_count
            """)
            
            record = result.single()
            threat_count = record['threat_count'] if record else 0
            print(f"Threats in database: {threat_count}")
        
        kg.close()
        return True
        
    except Exception as e:
        print(f"ERROR: Essential 8 data test failed - {e}")
        return False

def setup_neo4j_data():
    """Setup Neo4j with Essential 8 data"""
    
    print("\n=== Setting Up Neo4j Data ===")
    
    try:
        # Import setup function
        import importlib.util
        spec = importlib.util.spec_from_file_location("neo4j_setup_simple", "neo4j-setup-simple.py")
        neo4j_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(neo4j_module)
        
        setup_neo4j = neo4j_module.setup_neo4j
        
        print("Running Neo4j setup...")
        setup_neo4j()
        
        print("SUCCESS: Neo4j setup completed")
        return True
        
    except Exception as e:
        print(f"ERROR: Neo4j setup failed - {e}")
        return False

def test_graph_enhancer():
    """Test the graph enhancement functionality"""
    
    print("\n=== Testing Graph Enhancement ===")
    
    try:
        from neo4j_sentinel_integration import GraphEnhancedAssessment
        
        # Initialize enhancer
        enhancer = GraphEnhancedAssessment()
        
        if not enhancer.is_available():
            print("ERROR: Graph enhancer not available")
            return False
        
        print("SUCCESS: Graph enhancer initialized")
        
        # Create test data
        from sentinel_grc_complete import CompanyProfile, AssessmentResult, ConfidenceLevel
        
        test_company = CompanyProfile(
            company_name="Test Corp",
            industry="Healthcare", 
            employee_count=150,
            current_controls=["MFA", "Backups"]
        )
        
        mock_assessment = AssessmentResult(
            framework="Essential8",
            company_profile=test_company,
            controls_assessed=[
                {"control_id": "E8_7", "status": "COMPLIANT"},
                {"control_id": "E8_8", "status": "COMPLIANT"}
            ],
            gaps_identified=[],
            recommendations=[],
            overall_maturity=0.6,
            confidence_score=0.8,
            confidence_level=ConfidenceLevel.HIGH,
            timestamp=datetime.now()
        )
        
        test_data = {
            'assessment_result': mock_assessment,
            'company_profile': test_company,
            'frameworks_assessed': ['Essential8']
        }
        
        print("Testing graph enhancement...")
        enhanced_data = enhancer.enhance_assessment_with_graph(test_data, test_company)
        
        # Check results
        graph_insights = enhanced_data.get('graph_insights', {})
        
        if graph_insights:
            print("SUCCESS: Graph insights generated")
            print(f"  Compliance: {graph_insights.get('compliance_percentage', 0):.1f}%")
            print(f"  Exposed threats: {len(graph_insights.get('exposed_threats', []))}")
            print(f"  Implementation steps: {len(graph_insights.get('implementation_path', []))}")
        else:
            print("WARNING: No graph insights generated")
            return False
        
        enhancer.close()
        return True
        
    except Exception as e:
        print(f"ERROR: Graph enhancement test failed - {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_unified_orchestrator():
    """Test unified orchestrator with Neo4j"""
    
    print("\n=== Testing Unified Orchestrator ===")
    
    try:
        from unified_orchestrator import SentinelGRC
        
        # Initialize with Neo4j enabled
        print("Initializing Sentinel GRC...")
        sentinel = SentinelGRC(enable_neo4j=True, enable_sidecars=False, enable_groq=False)
        
        # Check status
        status = sentinel.get_status()
        print(f"Neo4j enhanced: {status.get('neo4j_enhanced', False)}")
        print(f"Neo4j available: {status.get('neo4j_available', False)}")
        
        if not status.get('neo4j_enhanced'):
            print("ERROR: Neo4j not enabled in orchestrator")
            return False
        
        print("Running test assessment...")
        
        # Run assessment
        result = await sentinel.assess_company(
            company_name="Neo4j Test Corp",
            industry="Healthcare",
            employee_count=150,
            current_controls=["MFA", "Backups"]
        )
        
        print("SUCCESS: Assessment completed")
        print(f"  Processing time: {result['processing_time']:.2f}s")
        print(f"  Neo4j enhanced: {result.get('neo4j_enhanced', False)}")
        print(f"  Graph insights: {bool(result.get('graph_insights'))}")
        
        # Check graph insights
        graph_insights = result.get('graph_insights', {})
        if graph_insights:
            print(f"  Graph compliance: {graph_insights.get('compliance_percentage', 0):.1f}%")
            print(f"  Exposed threats: {len(graph_insights.get('exposed_threats', []))}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Unified orchestrator test failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    
    print("SENTINEL GRC - Neo4j Integration Test")
    print("=" * 45)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = []
    
    # Test 1: Basic connection
    tests.append(("Neo4j Connection", check_neo4j_connection()))
    
    if not tests[-1][1]:
        print("\nERROR: Neo4j not accessible - stopping tests")
        return False
    
    # Test 2: Check data or setup if needed
    if not test_essential8_data():
        print("Setting up Essential 8 data...")
        tests.append(("Neo4j Data Setup", setup_neo4j_data()))
        if not tests[-1][1]:
            print("ERROR: Could not setup Neo4j data")
            return False
    else:
        tests.append(("Essential 8 Data", True))
    
    # Test 3: Graph enhancer
    tests.append(("Graph Enhancement", test_graph_enhancer()))
    
    # Test 4: Unified orchestrator
    print("Running async test...")
    orchestrator_result = asyncio.run(test_unified_orchestrator())
    tests.append(("Unified Orchestrator", orchestrator_result))
    
    # Summary
    print("\n=== TEST RESULTS ===")
    passed = 0
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\nSUCCESS: All tests passed!")
        print("Neo4j integration is working correctly")
        print("\nNext step: streamlit run streamlit_demo.py")
        return True
    else:
        print(f"\nERROR: {len(tests) - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)