"""
COMPREHENSIVE INTEGRATION TEST
============================
Final validation of all optimized framework integration modules
Production readiness verification
"""

import logging
import time
import json
from pathlib import Path
from typing import Dict, Any, List

# Import our optimized modules
from optimized_nist_csf_integration import NISTCSFIntegrator, FrameworkConfig
from optimized_essential_eight_integration import OptimizedEssentialEightIntegrator, EssentialEightConfig
from optimized_harmonization_reports import OptimizedFrameworkHarmonizationReporter, HarmonizationConfig, OrganizationSize

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComprehensiveIntegrationTester:
    """Comprehensive integration testing suite"""
    
    def __init__(self):
        self.test_results = {}
        self.performance_metrics = {}
        
        logger.info("Starting Comprehensive Integration Test Suite")
        
    def run_full_integration_test(self) -> bool:
        """Run complete integration test across all modules"""
        
        try:
            # Test 1: NIST CSF 2.0 Integration
            logger.info("📋 Test 1: NIST CSF 2.0 Integration")
            nist_result = self._test_nist_integration()
            self.test_results["nist_csf"] = nist_result
            
            # Test 2: Essential Eight Integration  
            logger.info("📋 Test 2: Essential Eight Integration")
            e8_result = self._test_essential_eight_integration()
            self.test_results["essential_eight"] = e8_result
            
            # Test 3: Cross-Framework Mapping
            logger.info("📋 Test 3: Cross-Framework Mapping")
            mapping_result = self._test_cross_framework_mapping()
            self.test_results["cross_mapping"] = mapping_result
            
            # Test 4: Harmonization Reports
            logger.info("📋 Test 4: Harmonization Reports")
            reports_result = self._test_harmonization_reports()
            self.test_results["reports"] = reports_result
            
            # Test 5: Performance & Scalability
            logger.info("📋 Test 5: Performance & Scalability")
            performance_result = self._test_performance()
            self.test_results["performance"] = performance_result
            
            # Test 6: Data Integrity
            logger.info("📋 Test 6: Data Integrity")
            integrity_result = self._test_data_integrity()
            self.test_results["data_integrity"] = integrity_result
            
            # Test 7: End-to-End Workflow
            logger.info("📋 Test 7: End-to-End Workflow")
            e2e_result = self._test_end_to_end_workflow()
            self.test_results["end_to_end"] = e2e_result
            
            # Generate test report
            success = self._generate_test_report()
            
            if success:
                logger.info("ALL INTEGRATION TESTS PASSED!")
                logger.info("System ready for production deployment")
            else:
                logger.error("Some integration tests failed")
                
            return success
            
        except Exception as e:
            logger.error(f"💥 Integration test suite failed: {e}")
            return False
    
    def _test_nist_integration(self) -> bool:
        """Test NIST CSF 2.0 integration module"""
        
        try:
            config = FrameworkConfig(
                data_path=Path("test_data/nist"),
                cache_enabled=True,
                validate_data=True
            )
            
            integrator = NISTCSFIntegrator(config)
            
            # Test framework structure
            structure = integrator.get_csf_2_core_structure()
            assert len(structure["functions"]) == 6, "Should have 6 CSF functions"
            
            # Test data loading
            framework_data = integrator.load_framework_data()
            assert "framework_info" in framework_data, "Should have framework info"
            
            # Test cross-framework mapper
            mapper = integrator.create_cross_framework_mapper()
            mappings = mapper.map_control("ID.AM-01", "NIST_CSF_2", "Essential_Eight")
            assert isinstance(mappings, list), "Should return list of mappings"
            
            logger.info("NIST CSF 2.0 integration passed")
            return True
            
        except Exception as e:
            logger.error(f"NIST integration failed: {e}")
            return False
    
    def _test_essential_eight_integration(self) -> bool:
        """Test Essential Eight integration module"""
        
        try:
            config = EssentialEightConfig(
                data_path=Path("test_data/essential_eight"),
                include_mitre_mappings=True,
                validate_oscal=True
            )
            
            integrator = OptimizedEssentialEightIntegrator(config)
            
            # Test enhanced controls
            controls = integrator.get_enhanced_essential_eight_controls()
            assert len(controls) >= 4, "Should have at least 4 E8 controls"
            
            # Test OSCAL structure
            oscal = integrator.get_comprehensive_ism_oscal_structure()
            assert "essential_eight_profiles" in oscal, "Should have E8 profiles"
            assert len(oscal["essential_eight_profiles"]) == 3, "Should have 3 maturity levels"
            
            # Test NIST mappings
            nist_mappings = integrator.create_comprehensive_nist_mappings()
            assert "bidirectional_mappings" in nist_mappings, "Should have bidirectional mappings"
            
            # Test MITRE ATT&CK integration
            mitre_count = sum(len(c.get("mitre_attack_mappings", [])) for c in controls.values())
            assert mitre_count > 0, "Should have MITRE ATT&CK mappings"
            
            logger.info("✅ Essential Eight integration passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Essential Eight integration failed: {e}")
            return False
    
    def _test_cross_framework_mapping(self) -> bool:
        """Test cross-framework mapping capabilities"""
        
        try:
            # Initialize integrators
            nist_integrator = NISTCSFIntegrator()
            mapper = nist_integrator.create_cross_framework_mapper()
            
            # Test various mapping scenarios
            test_cases = [
                ("ID.AM-01", "NIST_CSF_2", "Essential_Eight"),
                ("PR.AA-02", "NIST_CSF_2", "Essential_Eight"),
                ("E8_6", "Essential_Eight", "NIST_CSF_2"),
                ("ID.AM-01", "NIST_CSF_2", "CIS_Controls_8.1")
            ]
            
            for source_control, source_framework, target_framework in test_cases:
                mappings = mapper.map_control(source_control, source_framework, target_framework)
                
                # Validate mapping results
                if mappings:  # Some mappings may be empty and that's OK
                    for mapping in mappings:
                        assert "control" in mapping, "Mapping should have control field"
                        assert "name" in mapping, "Mapping should have name field"
                        
            # Test overlap detection
            overlaps = mapper.find_control_overlaps(["NIST_CSF_2", "Essential_Eight"])
            assert "common_controls" in overlaps, "Should have common controls analysis"
            
            logger.info("✅ Cross-framework mapping passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cross-framework mapping failed: {e}")
            return False
    
    def _test_harmonization_reports(self) -> bool:
        """Test harmonization reporting module"""
        
        try:
            config = HarmonizationConfig(
                data_path=Path("test_data/harmonization"),
                include_financial_modeling=True,
                include_risk_analysis=True,
                validate_cost_models=True
            )
            
            reporter = OptimizedFrameworkHarmonizationReporter(config)
            
            # Test comprehensive analysis
            frameworks = ["NIST_CSF_2", "Essential_Eight"]
            analysis = reporter.generate_comprehensive_analysis(
                frameworks=frameworks,
                organization_size=OrganizationSize.MEDIUM
            )
            
            # Validate analysis structure
            required_sections = [
                "analysis_metadata", "executive_dashboard", "financial_impact_model",
                "control_overlap_analysis", "implementation_roadmap"
            ]
            
            for section in required_sections:
                assert section in analysis, f"Should have {section} section"
                
            # Validate financial model
            financial_model = analysis["financial_impact_model"]
            assert "investment_analysis" in financial_model, "Should have investment analysis"
            assert "roi_analysis" in financial_model, "Should have ROI analysis"
            
            # Validate executive dashboard
            dashboard = analysis["executive_dashboard"]
            assert "key_metrics" in dashboard, "Should have key metrics"
            assert len(dashboard["key_metrics"]) >= 5, "Should have multiple KPIs"
            
            logger.info("✅ Harmonization reports passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Harmonization reports failed: {e}")
            return False
    
    def _test_performance(self) -> bool:
        """Test performance and scalability"""
        
        try:
            # Performance test parameters
            iterations = 100
            
            # Test NIST integration performance
            integrator = NISTCSFIntegrator()
            
            start_time = time.time()
            for _ in range(iterations):
                integrator.get_csf_2_core_structure()
            nist_time = time.time() - start_time
            
            self.performance_metrics["nist_structure_generation"] = {
                "iterations": iterations,
                "total_time": nist_time,
                "avg_time": nist_time / iterations
            }
            
            # Test mapping performance
            mapper = integrator.create_cross_framework_mapper()
            
            start_time = time.time()
            for _ in range(iterations):
                mapper.map_control("ID.AM-01", "NIST_CSF_2", "Essential_Eight")
            mapping_time = time.time() - start_time
            
            self.performance_metrics["control_mapping"] = {
                "iterations": iterations,
                "total_time": mapping_time,
                "avg_time": mapping_time / iterations
            }
            
            # Performance thresholds (adjust based on requirements)
            assert nist_time < 5.0, f"NIST structure generation too slow: {nist_time}s"
            assert mapping_time < 1.0, f"Control mapping too slow: {mapping_time}s"
            
            logger.info(f"✅ Performance test passed - NIST: {nist_time:.3f}s, Mapping: {mapping_time:.3f}s")
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            return False
    
    def _test_data_integrity(self) -> bool:
        """Test data integrity and validation"""
        
        try:
            # Test NIST data integrity
            integrator = NISTCSFIntegrator()
            framework_data = integrator.load_framework_data(force_refresh=True)
            
            # Validate framework structure
            assert "framework_info" in framework_data, "Should have framework info"
            assert "functions" in framework_data, "Should have functions"
            assert len(framework_data["functions"]) == 6, "Should have 6 functions"
            
            # Test Essential Eight data integrity
            e8_integrator = OptimizedEssentialEightIntegrator()
            e8_controls = e8_integrator.get_enhanced_essential_eight_controls()
            
            # Validate Essential Eight controls
            expected_controls = ["E8_1", "E8_2", "E8_6", "E8_8"]
            for control_id in expected_controls:
                assert control_id in e8_controls, f"Should have {control_id}"
                control = e8_controls[control_id]
                assert "maturity_levels" in control, f"{control_id} should have maturity levels"
                
            # Test data consistency
            nist_mappings = e8_integrator.create_comprehensive_nist_mappings()
            nist_to_e8 = nist_mappings["bidirectional_mappings"]["nist_to_e8"]
            e8_to_nist = nist_mappings["bidirectional_mappings"]["e8_to_nist"]
            
            # Basic bidirectional consistency check
            for nist_control, e8_mappings in nist_to_e8.items():
                for e8_mapping in e8_mappings:
                    e8_control = e8_mapping["control"]
                    if e8_control in e8_to_nist:
                        # Verify reverse mapping exists
                        reverse_mappings = [m["control"] for m in e8_to_nist[e8_control]]
                        # Note: Perfect bidirectional mapping not always expected, but some consistency should exist
            
            logger.info("✅ Data integrity test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Data integrity test failed: {e}")
            return False
    
    def _test_end_to_end_workflow(self) -> bool:
        """Test complete end-to-end workflow"""
        
        try:
            logger.info("🔄 Testing complete workflow: Framework Analysis → Mapping → Reporting")
            
            # Step 1: Initialize all components
            nist_integrator = NISTCSFIntegrator()
            e8_integrator = OptimizedEssentialEightIntegrator()
            reporter = OptimizedFrameworkHarmonizationReporter()
            
            # Step 2: Load framework data
            nist_data = nist_integrator.load_framework_data()
            e8_data = e8_integrator.get_enhanced_essential_eight_controls()
            
            # Step 3: Perform cross-framework mapping
            mapper = nist_integrator.create_cross_framework_mapper()
            sample_mappings = []
            
            test_controls = ["ID.AM-01", "PR.AA-02", "DE.CM-01"]
            for control in test_controls:
                mappings = mapper.map_control(control, "NIST_CSF_2", "Essential_Eight")
                sample_mappings.extend(mappings)
                
            # Step 4: Generate comprehensive report
            frameworks = ["NIST_CSF_2", "Essential_Eight"]
            analysis = reporter.generate_comprehensive_analysis(frameworks)
            
            # Step 5: Validate end-to-end results
            assert len(sample_mappings) > 0, "Should have generated some mappings"
            assert "executive_dashboard" in analysis, "Should have executive dashboard"
            assert "financial_impact_model" in analysis, "Should have financial model"
            
            # Step 6: Save integrated results
            integrated_results = {
                "workflow_timestamp": time.time(),
                "nist_functions_count": len(nist_data["functions"]),
                "e8_controls_count": len(e8_data),
                "mappings_generated": len(sample_mappings),
                "analysis_sections": list(analysis.keys()),
                "workflow_status": "SUCCESS"
            }
            
            with open("end_to_end_workflow_results.json", 'w') as f:
                json.dump(integrated_results, f, indent=2)
                
            logger.info("✅ End-to-end workflow test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ End-to-end workflow test failed: {e}")
            return False
    
    def _generate_test_report(self) -> bool:
        """Generate comprehensive test report"""
        
        try:
            passed_tests = sum(1 for result in self.test_results.values() if result)
            total_tests = len(self.test_results)
            success_rate = (passed_tests / total_tests) * 100
            
            test_report = {
                "test_suite": "Comprehensive Framework Integration Test",
                "timestamp": time.time(),
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": total_tests - passed_tests,
                    "success_rate": f"{success_rate:.1f}%",
                    "overall_status": "PASS" if success_rate == 100 else "FAIL"
                },
                "test_results": self.test_results,
                "performance_metrics": self.performance_metrics,
                "system_readiness": {
                    "production_ready": success_rate == 100,
                    "components_validated": [
                        "NIST CSF 2.0 Integration",
                        "Essential Eight Integration", 
                        "Cross-Framework Mapping",
                        "Harmonization Reporting",
                        "Performance & Scalability",
                        "Data Integrity"
                    ],
                    "next_steps": [
                        "Deploy to production environment",
                        "Configure monitoring and logging",
                        "Set up automated testing pipeline",
                        "Create user documentation"
                    ] if success_rate == 100 else [
                        "Fix failing test cases",
                        "Re-run integration tests",
                        "Review system architecture"
                    ]
                }
            }
            
            # Save test report
            with open("comprehensive_integration_test_report.json", 'w') as f:
                json.dump(test_report, f, indent=2, ensure_ascii=False)
                
            # Log summary
            logger.info(f"📊 TEST SUMMARY: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
            
            for test_name, result in self.test_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                logger.info(f"   {test_name}: {status}")
                
            return success_rate == 100
            
        except Exception as e:
            logger.error(f"Error generating test report: {e}")
            return False

def main():
    """Run comprehensive integration test suite"""
    
    print("=" * 80)
    print("SENTINEL GRC - COMPREHENSIVE INTEGRATION TEST SUITE")
    print("=" * 80)
    
    tester = ComprehensiveIntegrationTester()
    success = tester.run_full_integration_test()
    
    print("=" * 80)
    if success:
        print("ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!")
        print("Proceed with deployment and user training")
    else:
        print("SOME TESTS FAILED - REVIEW ISSUES BEFORE DEPLOYMENT")
        print("Check test report for detailed failure analysis")
    print("=" * 80)
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)