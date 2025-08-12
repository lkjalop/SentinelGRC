"""
Neo4j Integration for Sentinel GRC
==================================
Integrates the existing Neo4j knowledge graph with the unified orchestrator.
Provides enhanced relationship analysis and implementation guidance.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import Neo4j setup
from neo4j_setup_simple import ComplianceKnowledgeGraph

logger = logging.getLogger(__name__)

class GraphEnhancedAssessment:
    """
    Enhances standard compliance assessment with Neo4j graph insights.
    Provides relationship analysis, implementation paths, and risk chains.
    """
    
    def __init__(self):
        self.graph = None
        self.graph_available = False
        
        try:
            # Initialize Neo4j connection
            self.graph = ComplianceKnowledgeGraph()
            self.graph_available = True
            logger.info("✅ Neo4j graph database connected")
        except Exception as e:
            logger.warning(f"⚠️ Neo4j not available: {e}")
            logger.info("Falling back to standard assessment without graph insights")
    
    def is_available(self) -> bool:
        """Check if Neo4j graph is available"""
        return self.graph_available
    
    def enhance_assessment_with_graph(self, 
                                     assessment_data: Dict[str, Any], 
                                     company_profile) -> Dict[str, Any]:
        """
        Enhance standard assessment with Neo4j graph insights.
        
        Args:
            assessment_data: Standard assessment results
            company_profile: Company information
            
        Returns:
            Enhanced assessment with graph insights
        """
        
        if not self.graph_available:
            logger.info("Neo4j not available - returning standard assessment")
            return assessment_data
        
        try:
            # Extract implemented controls from assessment
            implemented_controls = self._extract_implemented_controls(assessment_data)
            
            # Get graph-based company assessment
            graph_assessment = self.graph.assess_company(
                company_name=company_profile.company_name,
                implemented_controls=implemented_controls
            )
            
            # Get implementation path recommendations
            implementation_path = self.graph.get_implementation_path(implemented_controls)
            
            # Enhance the assessment data
            enhanced_data = assessment_data.copy()
            enhanced_data['graph_insights'] = {
                'compliance_percentage': graph_assessment['compliance_percentage'],
                'exposed_threats': graph_assessment['exposed_threats'],
                'missing_controls': graph_assessment['missing_controls'],
                'priority_recommendations': graph_assessment['recommendations'],
                'implementation_path': implementation_path[:5],  # Top 5 next steps
                'relationship_analysis': self._analyze_control_relationships(implemented_controls)
            }
            
            # Update confidence based on graph consistency
            if 'assessment_result' in enhanced_data:
                enhanced_data['assessment_result'] = self._adjust_confidence_with_graph(
                    enhanced_data['assessment_result'], 
                    graph_assessment
                )
            
            logger.info(f"✅ Enhanced assessment with graph insights for {company_profile.company_name}")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Failed to enhance assessment with graph: {e}")
            return assessment_data
    
    def _extract_implemented_controls(self, assessment_data: Dict[str, Any]) -> List[str]:
        """Extract list of implemented controls from assessment"""
        
        implemented = []
        
        # Check if assessment_result exists
        assessment_result = assessment_data.get('assessment_result')
        if not assessment_result:
            return implemented
        
        # Extract from controls_assessed
        controls_assessed = getattr(assessment_result, 'controls_assessed', [])
        
        for control in controls_assessed:
            if isinstance(control, dict):
                status = control.get('status')
                control_id = control.get('control_id') or control.get('name', '').replace(' ', '_').upper()
                
                # Map control names to Essential 8 IDs
                control_mapping = {
                    'APPLICATION_CONTROL': 'E8_1',
                    'PATCH_APPLICATIONS': 'E8_2', 
                    'CONFIGURE_MICROSOFT_OFFICE_MACRO_SETTINGS': 'E8_3',
                    'USER_APPLICATION_HARDENING': 'E8_4',
                    'RESTRICT_ADMINISTRATIVE_PRIVILEGES': 'E8_5',
                    'PATCH_OPERATING_SYSTEMS': 'E8_6',
                    'MULTI-FACTOR_AUTHENTICATION': 'E8_7',
                    'REGULAR_BACKUPS': 'E8_8'
                }
                
                mapped_id = control_mapping.get(control_id, control_id)
                
                if status in ['COMPLIANT', 'PARTIAL']:
                    implemented.append(mapped_id)
        
        # Also check company profile current controls
        company_controls = assessment_data.get('company_profile')
        if hasattr(company_controls, 'current_controls'):
            for control_name in company_controls.current_controls:
                # Map common control names to E8 IDs
                name_mapping = {
                    'MFA': 'E8_7',
                    'Multi-Factor Authentication': 'E8_7',
                    'Backups': 'E8_8',
                    'Regular Backups': 'E8_8',
                    'Application Control': 'E8_1',
                    'Patch Applications': 'E8_2',
                    'Patch Operating Systems': 'E8_6',
                    'Admin Privileges': 'E8_5'
                }
                
                if control_name in name_mapping:
                    implemented.append(name_mapping[control_name])
        
        # Remove duplicates
        return list(set(implemented))
    
    def _analyze_control_relationships(self, implemented_controls: List[str]) -> Dict[str, Any]:
        """Analyze relationships between implemented and missing controls"""
        
        if not self.graph_available:
            return {}
        
        try:
            with self.graph.driver.session() as session:
                # Find control clusters (controls that prevent the same threats)
                result = session.run("""
                    MATCH (c1:Control)-[:PREVENTS]->(t:Threat)<-[:PREVENTS]-(c2:Control)
                    WHERE c1.id IN $implemented AND NOT c2.id IN $implemented
                    WITH c2, collect(DISTINCT t.name) as shared_threats, count(DISTINCT t) as threat_count
                    RETURN c2.name as missing_control,
                           c2.id as control_id,
                           shared_threats,
                           threat_count
                    ORDER BY threat_count DESC
                    LIMIT 5
                """, implemented=implemented_controls)
                
                related_gaps = [dict(record) for record in result]
                
                # Find threat coverage analysis
                coverage_result = session.run("""
                    MATCH (t:Threat)
                    OPTIONAL MATCH (c:Control)-[:PREVENTS]->(t)
                    WHERE c.id IN $implemented
                    WITH t, count(c) as protecting_controls
                    RETURN t.name as threat,
                           t.severity as severity,
                           protecting_controls,
                           CASE WHEN protecting_controls > 0 THEN 'Protected' ELSE 'Exposed' END as status
                    ORDER BY 
                        CASE t.severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 ELSE 3 END,
                        protecting_controls ASC
                """, implemented=implemented_controls)
                
                threat_coverage = [dict(record) for record in coverage_result]
                
                return {
                    'related_control_gaps': related_gaps,
                    'threat_coverage_analysis': threat_coverage,
                    'implemented_control_count': len(implemented_controls),
                    'total_controls': 8,
                    'coverage_percentage': (len(implemented_controls) / 8) * 100
                }
                
        except Exception as e:
            logger.error(f"Failed to analyze control relationships: {e}")
            return {}
    
    def _adjust_confidence_with_graph(self, assessment_result, graph_assessment: Dict[str, Any]):
        """Adjust assessment confidence based on graph consistency"""
        
        try:
            # Compare graph assessment with standard assessment
            graph_compliance = graph_assessment.get('compliance_percentage', 0) / 100
            standard_maturity = getattr(assessment_result, 'overall_maturity', 0)
            
            # Calculate consistency score
            consistency = 1 - abs(graph_compliance - standard_maturity)
            
            # Adjust confidence based on consistency
            original_confidence = getattr(assessment_result, 'confidence_score', 0.7)
            
            if consistency > 0.9:
                # High consistency - boost confidence
                adjusted_confidence = min(original_confidence * 1.1, 1.0)
            elif consistency < 0.7:
                # Low consistency - reduce confidence  
                adjusted_confidence = original_confidence * 0.9
            else:
                adjusted_confidence = original_confidence
            
            # Update assessment result
            assessment_result.confidence_score = adjusted_confidence
            
            # Add graph validation metadata
            if hasattr(assessment_result, '__dict__'):
                assessment_result.graph_validation = {
                    'consistency_score': consistency,
                    'graph_compliance': graph_compliance,
                    'confidence_adjustment': adjusted_confidence - original_confidence
                }
            
            logger.info(f"Adjusted confidence from {original_confidence:.3f} to {adjusted_confidence:.3f} based on graph consistency")
            
            return assessment_result
            
        except Exception as e:
            logger.error(f"Failed to adjust confidence with graph: {e}")
            return assessment_result
    
    def get_risk_chain_analysis(self, company_name: str, threat_name: str) -> Dict[str, Any]:
        """Get detailed risk chain analysis for a specific threat"""
        
        if not self.graph_available:
            return {'error': 'Neo4j not available'}
        
        try:
            with self.graph.driver.session() as session:
                result = session.run("""
                    MATCH (company:Company {name: $company_name})
                    MATCH (threat:Threat {name: $threat_name})
                    MATCH (control:Control)-[:PREVENTS]->(threat)
                    
                    OPTIONAL MATCH (company)-[:HAS_IMPLEMENTED]->(control)
                    
                    WITH threat, control, 
                         CASE WHEN (company)-[:HAS_IMPLEMENTED]->(control) 
                              THEN 'Implemented' 
                              ELSE 'Missing' 
                         END as control_status
                    
                    RETURN threat.name as threat,
                           threat.severity as severity,
                           collect({
                               control: control.name,
                               control_id: control.id,
                               effort: control.effort,
                               impact: control.impact,
                               status: control_status
                           }) as protective_controls
                """, company_name=company_name, threat_name=threat_name)
                
                record = result.single()
                if record:
                    return dict(record)
                else:
                    return {'error': f'No data found for threat: {threat_name}'}
                    
        except Exception as e:
            logger.error(f"Failed to get risk chain analysis: {e}")
            return {'error': str(e)}
    
    def close(self):
        """Close Neo4j connection"""
        if self.graph:
            self.graph.close()


# Integration utility functions
def setup_neo4j_for_sentinel():
    """Setup Neo4j database with Essential 8 data for Sentinel GRC"""
    
    print("🛡️ Setting up Neo4j for Sentinel GRC")
    print("=" * 40)
    
    try:
        # Run the existing setup
        from neo4j_setup_simple import setup_neo4j
        setup_neo4j()
        
        print("\n✅ Neo4j setup complete for Sentinel GRC!")
        print("🌐 View graph at: http://localhost:7474")
        print("🔐 Username: neo4j")
        print("🔐 Password: Ag3nt-GRC")
        
        return True
        
    except Exception as e:
        print(f"❌ Neo4j setup failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Ensure Neo4j Desktop is running")
        print("2. Create database with password: Ag3nt-GRC")
        print("3. Check that URI bolt://localhost:7687 is accessible")
        return False

def test_neo4j_integration():
    """Test Neo4j integration with sample assessment"""
    
    print("\n🧪 Testing Neo4j integration...")
    
    try:
        # Create test assessment data
        from sentinel_grc_complete import CompanyProfile, AssessmentResult, ConfidenceLevel
        from datetime import datetime
        
        # Mock company profile
        test_company = CompanyProfile(
            company_name="Test Corp Pty Ltd",
            industry="Healthcare",
            employee_count=150,
            current_controls=["MFA", "Backups"],
            previous_incidents=[]
        )
        
        # Mock assessment result
        test_assessment = AssessmentResult(
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
        
        test_data = {
            'assessment_result': test_assessment,
            'company_profile': test_company,
            'frameworks_assessed': ['Essential8']
        }
        
        # Test enhancement
        enhancer = GraphEnhancedAssessment()
        
        if not enhancer.is_available():
            print("⚠️ Neo4j not available - ensure database is running")
            return False
        
        enhanced_data = enhancer.enhance_assessment_with_graph(test_data, test_company)
        
        # Print results
        graph_insights = enhanced_data.get('graph_insights', {})
        
        print(f"✅ Graph insights generated:")
        print(f"   Compliance: {graph_insights.get('compliance_percentage', 0):.1f}%")
        print(f"   Exposed threats: {len(graph_insights.get('exposed_threats', []))}")
        print(f"   Implementation steps: {len(graph_insights.get('implementation_path', []))}")
        
        enhancer.close()
        return True
        
    except Exception as e:
        print(f"❌ Neo4j integration test failed: {e}")
        return False

if __name__ == "__main__":
    # Setup and test
    if setup_neo4j_for_sentinel():
        test_neo4j_integration()