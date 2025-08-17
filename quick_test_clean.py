"""
Quick Test of New Features
=========================

Test the new ISO 27001 agent and enhanced PDF generation.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from src.core.core_types import CompanyProfile
from src.core.sentinel_grc_complete import SentinelGRC

async def test_new_features():
    """Test new ISO 27001 agent and enhanced features"""
    
    print("=" * 60)
    print("TESTING NEW FEATURES")
    print("=" * 60)
    
    # Test 1: Platform initialization
    print("\n1. Testing platform initialization...")
    try:
        platform = SentinelGRC()
        print(f"   Platform loaded: {platform.platform_name} v{platform.version}")
        print(f"   Agents loaded: {len(platform.agents)}")
        
        # List all loaded agents
        for agent_name in platform.agents.keys():
            print(f"   - {agent_name}")
        
        # Check if ISO 27001 agent is loaded
        if 'iso_27001' in platform.agents:
            print("    ISO 27001 agent successfully loaded!")
        else:
            print("    ISO 27001 agent not found")
        
    except Exception as e:
        print(f"    Platform initialization failed: {str(e)}")
        return
    
    # Test 2: Create test company
    print("\n2. Creating test company profile...")
    try:
        test_company = CompanyProfile(
            company_name="TechFlow Solutions",
            industry="Technology", 
            employee_count=85,
            country="Australia",
            has_government_contracts=False,
            annual_revenue=15000000.0,
            current_controls=["Firewall", "Antivirus", "Backup"],
            regulatory_requirements=["Privacy Act", "SOC 2"]
        )
        print(f"   Test company created: {test_company.company_name}")
        
    except Exception as e:
        print(f"   Failed to create test company: {str(e)}")
        return
    
    # Test 3: Test ISO 27001 assessment
    print("\n3. Testing ISO 27001 assessment...")
    try:
        iso_agent = platform.agents.get('iso_27001')
        if iso_agent:
            result = await iso_agent.assess_company(test_company)
            
            print(f"    Assessment completed")
            print(f"   - Overall Score: {getattr(result, 'overall_score', 'N/A')}")
            print(f"   - Risk Level: {getattr(result, 'risk_level', 'N/A')}")
            print(f"   - Recommendations: {len(getattr(result, 'recommendations', []))}")
            
            # Check for AI integration
            detailed_findings = getattr(result, 'detailed_findings', {})
            if 'ai_integration' in detailed_findings:
                ai_data = detailed_findings['ai_integration']
                if ai_data.get('applicable'):
                    print(f"    AI integration assessment included")
                    print(f"   - AI Score: {ai_data.get('overall_ai_score', 'N/A')}")
                else:
                    print(f"   - AI integration not applicable for this company")
            
        else:
            print("    ISO 27001 agent not available")
            
    except Exception as e:
        print(f"    ISO 27001 assessment failed: {str(e)}")
    
    # Test 4: Test a few other frameworks
    print("\n4. Testing other framework agents...")
    
    test_frameworks = ['privacy_act', 'soc2', 'essential_eight']
    
    for framework_name in test_frameworks:
        try:
            agent = platform.agents.get(framework_name)
            if agent:
                if hasattr(agent, 'assess_company'):
                    result = await agent.assess_company(test_company)
                    score = getattr(result, 'overall_score', getattr(result, 'compliance_percentage', 0))
                    print(f"    {framework_name}: {score:.1f}%")
                else:
                    print(f"   ? {framework_name}: No assess_company method")
            else:
                print(f"    {framework_name}: Agent not found")
                
        except Exception as e:
            print(f"    {framework_name}: Error - {str(e)}")
    
    # Test 5: Framework count verification
    print(f"\n5. Framework Summary:")
    print(f"   Total frameworks loaded: {len(platform.agents)}")
    print(f"   Expected minimum: 6 (Privacy Act, APRA, SOCI, SOC 2, ISO 27001, NIST)")
    
    if len(platform.agents) >= 6:
        print("    Sufficient frameworks loaded for enterprise platform")
    else:
        print("   ? Fewer frameworks than expected")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_new_features())
