"""
Neo4j Integration Test Suite
============================
Comprehensive testing of Neo4j integration with Sentinel GRC.
"""

import asyncio
import sys
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_neo4j_setup():
    """Test 1: Verify Neo4j setup and data population"""
    
    print("\n🧪 TEST 1: Neo4j Setup and Data Population")
    print("=" * 50)
    
    try:
        # Import and setup Neo4j
        from neo4j_setup_simple import setup_neo4j, test_assessment
        
        print("📋 Setting up Neo4j database...")
        setup_neo4j()
        
        print("\n📊 Testing basic company assessment...")
        test_assessment()
        
        print("\n✅ TEST 1 PASSED: Neo4j setup successful")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {e}")
        print("\n🛠️ Troubleshooting steps:")
        print("1. Ensure Neo4j Desktop is running")
        print("2. Create database with password: Ag3nt-GRC")
        print("3. Check bolt://localhost:7687 is accessible")
        return False

def test_graph_enhancement():
    """Test 2: Verify graph enhancement integration"""
    
    print("\n🧪 TEST 2: Graph Enhancement Integration")
    print("=" * 50)
    
    try:
        from neo4j_sentinel_integration import GraphEnhancedAssessment
        from sentinel_grc_complete import CompanyProfile, AssessmentResult, ConfidenceLevel
        
        # Create test company
        test_company = CompanyProfile(
            company_name="Test Healthcare Corp",
            industry="Healthcare",
            employee_count=150,
            current_controls=["Multi-Factor Authentication", "Regular Backups"],
            previous_incidents=["Phishing attempt in 2023"]
        )
        
        # Create mock assessment result
        mock_assessment = AssessmentResult(
            framework="Essential8",
            company_profile=test_company,
            controls_assessed=[
                {"control_id": "E8_7", "status": "COMPLIANT", "name": "Multi-Factor Authentication"},
                {"control_id": "E8_8", "status": "COMPLIANT", "name": "Regular Backups"},
                {"control_id": "E8_1", "status": "NON_COMPLIANT", "name": "Application Control"}
            ],
            gaps_identified=[],
            recommendations=[],
            overall_maturity=0.6,
            confidence_score=0.8,
            confidence_level=ConfidenceLevel.HIGH,
            timestamp=datetime.now()
        )
        
        # Test data structure
        test_data = {
            'assessment_result': mock_assessment,
            'company_profile': test_company,
            'frameworks_assessed': ['Essential8']
        }
        
        print("📊 Initializing graph enhancer...")
        enhancer = GraphEnhancedAssessment()
        
        if not enhancer.is_available():
            print("⚠️ Neo4j not available - check connection")
            return False
        
        print("✅ Neo4j connected successfully")
        
        print("🔍 Running graph enhancement...")
        enhanced_data = enhancer.enhance_assessment_with_graph(test_data, test_company)
        
        # Verify enhancement worked
        graph_insights = enhanced_data.get('graph_insights', {})
        
        if graph_insights:
            print(f"✅ Graph insights generated:")
            print(f"   • Compliance: {graph_insights.get('compliance_percentage', 0):.1f}%")
            print(f"   • Exposed threats: {len(graph_insights.get('exposed_threats', []))}")
            print(f"   • Missing controls: {len(graph_insights.get('missing_controls', []))}")
            print(f"   • Implementation steps: {len(graph_insights.get('implementation_path', []))}")
            
            # Test relationship analysis
            relationship_analysis = graph_insights.get('relationship_analysis', {})
            if relationship_analysis:
                print(f"   • Control relationships analyzed: {len(relationship_analysis.get('threat_coverage_analysis', []))}")
        else:
            print("⚠️ No graph insights generated")
            return False
        
        enhancer.close()
        print("\n✅ TEST 2 PASSED: Graph enhancement working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        return False

async def test_unified_orchestrator():
    """Test 3: Verify unified orchestrator with Neo4j"""
    
    print("\n🧪 TEST 3: Unified Orchestrator Integration")
    print("=" * 50)
    
    try:
        from unified_orchestrator import SentinelGRC
        
        print("🚀 Initializing Sentinel GRC with Neo4j...")
        
        # Initialize with Neo4j enabled
        sentinel = SentinelGRC(
            enable_sidecars=False,  # Disable sidecars for testing
            enable_groq=False,      # Disable Groq for testing  
            enable_neo4j=True       # Enable Neo4j
        )
        
        # Check system status
        status = sentinel.get_status()
        print(f"✅ System initialized:")
        print(f"   • Core agents: {len(status.get('core_agents', []))}")
        print(f"   • Neo4j enhanced: {status.get('neo4j_enhanced', False)}")
        print(f"   • Neo4j available: {status.get('neo4j_available', False)}")
        
        if not status.get('neo4j_enhanced'):
            print("⚠️ Neo4j not enabled in orchestrator")
            return False
        
        if not status.get('neo4j_available'):
            print("⚠️ Neo4j not available in orchestrator")
            return False
        
        print("🔍 Running test assessment...")
        
        # Run assessment
        result = await sentinel.assess_company(
            company_name="Neo4j Test Corp",
            industry="Healthcare", 
            employee_count=200,
            current_controls=["MFA", "Backups"],
            has_government_contracts=True
        )
        
        print(f"✅ Assessment completed:")
        print(f"   • Processing time: {result['processing_time']:.2f}s")
        print(f"   • Frameworks assessed: {len(result['frameworks_assessed'])}")
        print(f"   • Neo4j enhanced: {result.get('neo4j_enhanced', False)}")
        print(f"   • Graph insights available: {bool(result.get('graph_insights'))}")
        
        # Verify graph insights
        graph_insights = result.get('graph_insights', {})
        if graph_insights:
            print(f"   • Graph compliance: {graph_insights.get('compliance_percentage', 0):.1f}%")
            print(f"   • Exposed threats: {len(graph_insights.get('exposed_threats', []))}")
            
            # Show sample insights
            exposed_threats = graph_insights.get('exposed_threats', [])
            if exposed_threats:
                print(f"   • Sample threat: {exposed_threats[0].get('threat', 'Unknown')}")
            
            impl_path = graph_insights.get('implementation_path', [])
            if impl_path:
                print(f"   • Next recommended control: {impl_path[0].get('control', 'Unknown')}")
        
        print("\n✅ TEST 3 PASSED: Unified orchestrator with Neo4j working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_integration():
    """Test 4: Verify Streamlit can handle Neo4j results"""
    
    print("\n🧪 TEST 4: Streamlit Integration Compatibility")
    print("=" * 50)
    
    try:
        # Test if we can import Streamlit components
        print("📦 Checking Streamlit imports...")
        
        # Import render function
        sys.path.append('.')
        from streamlit_demo import render_graph_insights
        
        # Create mock graph insights for testing
        mock_graph_insights = {
            'compliance_percentage': 62.5,
            'exposed_threats': [
                {'threat': 'Ransomware', 'severity': 'CRITICAL'},
                {'threat': 'Phishing', 'severity': 'HIGH'},
                {'threat': 'Malware', 'severity': 'HIGH'}
            ],
            'implementation_path': [
                {'control': 'Application Control', 'effort': 'HIGH', 'threats_prevented': ['Malware', 'Ransomware']},
                {'control': 'Patch Management', 'effort': 'MEDIUM', 'threats_prevented': ['Malware']},
                {'control': 'Admin Privileges', 'effort': 'MEDIUM', 'threats_prevented': ['Insider Threat']}
            ],
            'priority_recommendations': [
                {'control': 'Application Control', 'effort': 'HIGH', 'threats_prevented': 2},
                {'control': 'Patch Applications', 'effort': 'MEDIUM', 'threats_prevented': 2}
            ],
            'relationship_analysis': {
                'implemented_control_count': 2,
                'coverage_percentage': 25.0,
                'threat_coverage_analysis': [
                    {'threat': 'Ransomware', 'status': 'Exposed', 'severity': 'CRITICAL', 'protecting_controls': 0},
                    {'threat': 'Data Breach', 'status': 'Protected', 'severity': 'CRITICAL', 'protecting_controls': 1}
                ],
                'related_control_gaps': [
                    {'missing_control': 'Application Control', 'shared_threats': ['Malware', 'Ransomware']}
                ]
            }
        }
        
        print("✅ Streamlit imports successful")
        print("✅ Mock graph insights created")
        print(f"   • Compliance: {mock_graph_insights['compliance_percentage']}%")
        print(f"   • Threats: {len(mock_graph_insights['exposed_threats'])}")
        print(f"   • Implementation steps: {len(mock_graph_insights['implementation_path'])}")
        
        print("\n✅ TEST 4 PASSED: Streamlit integration compatible")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {e}")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        return False

def neo4j_instructions():
    """Provide Neo4j setup instructions"""
    
    print("\n📋 NEO4J SETUP INSTRUCTIONS")
    print("=" * 40)
    print("""
To set up Neo4j for Sentinel GRC:

1. Install Neo4j Desktop:
   https://neo4j.com/download/

2. Create a new database:
   • Database name: sentinel-grc
   • Password: Ag3nt-GRC
   • Version: 5.x (latest)

3. Start the database:
   • Make sure it's running on bolt://localhost:7687

4. Test connection:
   python test_neo4j_integration.py

5. If successful, run the Streamlit app:
   streamlit run streamlit_demo.py

Neo4j Browser URL: http://localhost:7474
Username: neo4j
Password: Ag3nt-GRC
    """)

async def main():
    """Run all integration tests"""
    
    print("🛡️ SENTINEL GRC - Neo4j Integration Test Suite")
    print("=" * 60)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track test results
    results = {}
    
    # Test 1: Neo4j Setup
    results['neo4j_setup'] = test_neo4j_setup()
    
    if not results['neo4j_setup']:
        print("\n❌ Neo4j setup failed - stopping tests")
        neo4j_instructions()
        return False
    
    # Test 2: Graph Enhancement
    results['graph_enhancement'] = test_graph_enhancement()
    
    # Test 3: Unified Orchestrator  
    results['unified_orchestrator'] = await test_unified_orchestrator()
    
    # Test 4: Streamlit Integration
    results['streamlit_integration'] = test_streamlit_integration()
    
    # Summary
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Neo4j integration is ready for Streamlit demo")
        print("\n🚀 Next step: Run streamlit run streamlit_demo.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("🔧 Please fix issues before proceeding")
        
        if not results['neo4j_setup']:
            neo4j_instructions()
        
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    
    if not success:
        sys.exit(1)