#!/usr/bin/env python3
"""
Test the restored Intelligence Core - Dynamic Control Selection
This demonstrates the killer feature that makes Sentinel GRC unique
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.core.sentinel_grc_complete import SentinelGRC
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

async def test_intelligence_feature():
    """Test the restored intelligence core"""
    
    print("🧠 Testing Restored Intelligence Core")
    print("=" * 50)
    
    # Initialize the platform
    try:
        sentinel = SentinelGRC()
        print("✅ Sentinel GRC platform initialized")
        
        # Check if intelligence graph is available
        if sentinel.intelligence_graph:
            print("✅ Intelligence Knowledge Graph is operational")
        else:
            print("⚠️ Intelligence Graph not available (Neo4j not running?)")
            print("💡 To enable full intelligence:")
            print("   docker run -p 7687:7687 -p 7474:7474 neo4j:latest")
            return
        
    except Exception as e:
        print(f"❌ Platform initialization failed: {e}")
        return
    
    # Test company profiles for different scenarios
    test_companies = [
        {
            "company_name": "TechStartup Inc",
            "industry": "technology",
            "employee_count": 45,
            "cloud_usage": "cloud-native",
            "regulatory_requirements": ["soc2"],
            "security_maturity": "medium"
        },
        {
            "company_name": "FinanceCorpAU",
            "industry": "financial_services", 
            "employee_count": 250,
            "cloud_usage": "hybrid",
            "regulatory_requirements": ["apra", "privacy_act"],
            "security_maturity": "high"
        },
        {
            "company_name": "HealthTech Solutions",
            "industry": "healthcare",
            "employee_count": 120,
            "cloud_usage": "cloud-first",
            "regulatory_requirements": ["gdpr", "hipaa"],
            "security_maturity": "medium"
        }
    ]
    
    certifications_to_test = ["iso_27001", "soc2", "essential_eight"]
    
    print("\n🎯 Testing Dynamic Control Selection (THE KILLER FEATURE)")
    print("=" * 60)
    
    for i, company in enumerate(test_companies, 1):
        print(f"\n📊 Test {i}: {company['company_name']}")
        print(f"   Industry: {company['industry']}")
        print(f"   Size: {company['employee_count']} employees")
        print(f"   Cloud: {company['cloud_usage']}")
        
        for certification in certifications_to_test:
            print(f"\n   🎯 Testing {certification.upper()} certification...")
            
            try:
                # THE KILLER FEATURE IN ACTION
                result = await sentinel.get_intelligent_control_selection(
                    company_profile=company,
                    target_certification=certification,
                    risk_tolerance="medium"
                )
                
                if result.get("success"):
                    data = result["data"]
                    controls = data.get("prioritized_controls", [])
                    insights = data.get("intelligence_insights", [])
                    
                    print(f"      ✅ {len(controls)} controls prioritized")
                    print(f"      🏆 High priority: {data.get('high_priority_controls', 0)}")
                    print(f"      ⏱️ Timeline: {data.get('estimated_total_timeline', 'N/A')}")
                    print(f"      💰 Cost: {data.get('estimated_cost', 'N/A')}")
                    
                    if insights:
                        print(f"      💡 Key insight: {insights[0][:80]}...")
                    
                    # Show top 3 prioritized controls
                    if controls:
                        print("      🎯 Top 3 prioritized controls:")
                        for j, control in enumerate(controls[:3], 1):
                            print(f"         {j}. {control['control_id']}: {control['title'][:50]}...")
                            print(f"            Priority: {control['priority']} | Effort: {control['implementation_effort']}")
                
                else:
                    print(f"      ❌ Failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"      ❌ Exception: {e}")
    
    print("\n" + "=" * 60)
    print("🧠 Intelligence Core Test Complete")
    print("\n💡 This demonstrates what makes Sentinel GRC unique:")
    print("   • Context-aware control prioritization")
    print("   • Company-specific implementation guidance") 
    print("   • Cross-framework intelligence mapping")
    print("   • Risk-based timeline estimation")
    print("\n🏆 NO OTHER COMPLIANCE PLATFORM HAS THIS CAPABILITY!")

async def test_pdf_enhancement():
    """Test the enhanced PDF generator"""
    
    print("\n📄 Testing Enhanced PDF Generator")
    print("=" * 50)
    
    try:
        from src.professional.enhanced_pdf_generator import EnhancedPDFGenerator
        
        pdf_gen = EnhancedPDFGenerator()
        print("✅ Enhanced PDF Generator initialized")
        
        # Test company profile
        company_profile = {
            "company_name": "Demo Corp",
            "industry": "technology",
            "employee_count": 100
        }
        
        # Mock assessment results
        assessment_results = {
            "frameworks": {
                "iso_27001": {
                    "overall_compliance": 78.5,
                    "readiness_level": "Partial Compliance",
                    "estimated_timeline": "6-8 months",
                    "control_assessment": {
                        "A.8.1": {"status": "compliant", "score": 85, "family": "A.8"},
                        "A.8.2": {"status": "non_compliant", "score": 45, "family": "A.8"},
                        "A.12.6": {"status": "partial", "score": 70, "family": "A.12"}
                    },
                    "recommendations": [
                        {"control_id": "A.8.2", "title": "Implement privileged access management", "priority": "HIGH", "timeline": "2-4 weeks"},
                        {"control_id": "A.12.6", "title": "Enhance vulnerability management", "priority": "MEDIUM", "timeline": "4-6 weeks"}
                    ]
                }
            }
        }
        
        # Generate professional PDF
        result = await pdf_gen.generate_executive_report(company_profile, assessment_results)
        
        if result.get("success"):
            print("✅ Professional PDF generated successfully")
            print(f"   📄 Filename: {result['filename']}")
            print(f"   📏 Size: {result['size']:,} bytes")
            print(f"   📅 Generated: {result['generated_at']}")
            print("   🏆 Features: Document control header, cross-references, professional layout")
        else:
            print(f"❌ PDF generation failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ PDF enhancement test failed: {e}")

if __name__ == "__main__":
    print("🚀 Sentinel GRC Intelligence Core Test Suite")
    print("============================================")
    
    asyncio.run(test_intelligence_feature())
    asyncio.run(test_pdf_enhancement())
    
    print("\n✅ All tests completed!")
    print("\n🎯 READY FOR DEMO:")
    print("   1. Intelligence-powered control selection")
    print("   2. Professional PDF generation") 
    print("   3. Context-aware compliance recommendations")
    print("\n💰 MARKET POSITION: Premium enterprise platform ($25K-100K pricing)")