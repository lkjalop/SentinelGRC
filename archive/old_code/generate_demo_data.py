"""
Generate Synthetic Demo Data for Sentinel GRC
==============================================
Creates realistic demo scenarios for different industries to showcase capabilities.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import asyncio

class DemoDataGenerator:
    """Generate realistic demo data for different industries"""
    
    def __init__(self):
        self.demo_companies = self.create_demo_companies()
        self.demo_scenarios = self.create_demo_scenarios()
    
    def create_demo_companies(self) -> List[Dict[str, Any]]:
        """Create realistic demo companies across industries"""
        
        companies = [
            # Healthcare
            {
                "name": "MediCare Plus Hospital",
                "industry": "Healthcare",
                "size": "Large",
                "employee_count": 2500,
                "location": "Sydney, NSW",
                "frameworks": ["Essential8", "HIPAA", "Privacy Act 1988"],
                "current_controls": ["E8_7", "E8_8", "HIPAA_A1", "APP11"],
                "risk_profile": "HIGH",
                "description": "Major metropolitan hospital handling sensitive patient data",
                "challenges": ["Legacy systems", "24/7 operations", "Complex supply chain"],
                "annual_revenue": "$450M",
                "it_budget": "$22M"
            },
            {
                "name": "HealthTech Innovations",
                "industry": "Healthcare Technology",
                "size": "Medium",
                "employee_count": 350,
                "location": "Melbourne, VIC",
                "frameworks": ["Essential8", "HIPAA", "ISO 27001:2022"],
                "current_controls": ["E8_7", "E8_2", "ISO_8.5"],
                "risk_profile": "MEDIUM",
                "description": "Digital health platform provider",
                "challenges": ["Rapid growth", "Multi-cloud architecture", "API security"],
                "annual_revenue": "$45M",
                "it_budget": "$4.5M"
            },
            
            # Financial Services
            {
                "name": "SecureBank Australia",
                "industry": "Banking",
                "size": "Large",
                "employee_count": 8000,
                "location": "Sydney, NSW",
                "frameworks": ["Essential8", "APRA CPS 234", "PCI DSS"],
                "current_controls": ["E8_7", "E8_5", "E8_8", "CPS234_12", "PCI_8"],
                "risk_profile": "CRITICAL",
                "description": "Regional bank with digital transformation initiative",
                "challenges": ["Legacy core banking", "Open banking compliance", "Fraud prevention"],
                "annual_revenue": "$2.1B",
                "it_budget": "$180M"
            },
            {
                "name": "PayFlow Solutions",
                "industry": "Payment Processing",
                "size": "Medium",
                "employee_count": 450,
                "location": "Brisbane, QLD",
                "frameworks": ["PCI DSS", "Essential8", "ISO 27001:2022"],
                "current_controls": ["PCI_3", "PCI_4", "E8_7"],
                "risk_profile": "HIGH",
                "description": "Payment gateway and merchant services provider",
                "challenges": ["PCI compliance", "Real-time processing", "Fraud detection"],
                "annual_revenue": "$120M",
                "it_budget": "$15M"
            },
            
            # Critical Infrastructure
            {
                "name": "PowerGrid NSW",
                "industry": "Energy",
                "size": "Large",
                "employee_count": 3500,
                "location": "Newcastle, NSW",
                "frameworks": ["SOCI Act", "Essential8", "ISO 27001:2022"],
                "current_controls": ["SOCI_RMP", "E8_1", "E8_8", "ISO_7.1"],
                "risk_profile": "CRITICAL",
                "description": "State electricity distribution network operator",
                "challenges": ["OT/IT convergence", "Nation-state threats", "Physical security"],
                "annual_revenue": "$3.5B",
                "it_budget": "$140M"
            },
            {
                "name": "AquaFlow Water Services",
                "industry": "Water Utilities",
                "size": "Medium",
                "employee_count": 850,
                "location": "Perth, WA",
                "frameworks": ["SOCI Act", "Essential8"],
                "current_controls": ["SOCI_ACCESS", "E8_5"],
                "risk_profile": "HIGH",
                "description": "Regional water treatment and distribution",
                "challenges": ["SCADA security", "Remote facilities", "Supply chain risks"],
                "annual_revenue": "$280M",
                "it_budget": "$18M"
            },
            
            # Retail & E-commerce
            {
                "name": "OzMart Retail Group",
                "industry": "Retail",
                "size": "Large",
                "employee_count": 5000,
                "location": "Melbourne, VIC",
                "frameworks": ["PCI DSS", "Privacy Act 1988", "Essential8"],
                "current_controls": ["PCI_1", "APP6", "E8_7"],
                "risk_profile": "MEDIUM",
                "description": "National retail chain with e-commerce platform",
                "challenges": ["Omnichannel security", "Customer data protection", "Supply chain"],
                "annual_revenue": "$850M",
                "it_budget": "$42M"
            },
            
            # Government
            {
                "name": "Department of Digital Services",
                "industry": "Government",
                "size": "Large",
                "employee_count": 1200,
                "location": "Canberra, ACT",
                "frameworks": ["Essential8", "Privacy Act 1988", "ISO 27001:2022"],
                "current_controls": ["E8_1", "E8_7", "E8_5", "E8_8", "APP11"],
                "risk_profile": "HIGH",
                "description": "Federal government digital transformation agency",
                "challenges": ["Legacy systems", "Citizen data protection", "Service availability"],
                "annual_revenue": "N/A",
                "it_budget": "$95M"
            },
            
            # Technology
            {
                "name": "CloudNative Solutions",
                "industry": "Technology",
                "size": "Small",
                "employee_count": 120,
                "location": "Sydney, NSW",
                "frameworks": ["ISO 27001:2022", "Essential8"],
                "current_controls": ["ISO_8.28", "E8_2", "E8_7"],
                "risk_profile": "MEDIUM",
                "description": "SaaS platform for enterprise automation",
                "challenges": ["Multi-tenant security", "API security", "DevSecOps"],
                "annual_revenue": "$18M",
                "it_budget": "$3M"
            },
            
            # Education
            {
                "name": "Metro University Sydney",
                "industry": "Education",
                "size": "Large",
                "employee_count": 3000,
                "location": "Sydney, NSW",
                "frameworks": ["Essential8", "Privacy Act 1988"],
                "current_controls": ["E8_7", "APP5"],
                "risk_profile": "MEDIUM",
                "description": "Major university with 45,000 students",
                "challenges": ["BYOD security", "Research data protection", "Student privacy"],
                "annual_revenue": "$680M",
                "it_budget": "$34M"
            }
        ]
        
        return companies
    
    def create_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Create realistic compliance scenarios"""
        
        scenarios = [
            {
                "id": "BREACH_RESPONSE",
                "name": "Data Breach Response Scenario",
                "description": "Suspected data breach requiring immediate assessment and response",
                "urgency": "CRITICAL",
                "timeline": "24 hours",
                "key_questions": [
                    "What controls failed?",
                    "What is our exposure?",
                    "What are notification requirements?",
                    "How do we prevent recurrence?"
                ]
            },
            {
                "id": "AUDIT_PREP",
                "name": "Regulatory Audit Preparation",
                "description": "Upcoming APRA audit requiring compliance validation",
                "urgency": "HIGH",
                "timeline": "2 weeks",
                "key_questions": [
                    "Are we compliant with CPS 234?",
                    "What gaps exist?",
                    "What evidence do we need?",
                    "What's our remediation timeline?"
                ]
            },
            {
                "id": "M&A_DUE_DILIGENCE",
                "name": "Merger & Acquisition Due Diligence",
                "description": "Security assessment for potential acquisition target",
                "urgency": "MEDIUM",
                "timeline": "30 days",
                "key_questions": [
                    "What's their security posture?",
                    "What risks are we inheriting?",
                    "Integration challenges?",
                    "Compliance gaps?"
                ]
            },
            {
                "id": "BOARD_REPORTING",
                "name": "Board Risk Reporting",
                "description": "Quarterly security posture report for board meeting",
                "urgency": "MEDIUM",
                "timeline": "1 week",
                "key_questions": [
                    "Current risk level?",
                    "Improvement trends?",
                    "Peer comparison?",
                    "Investment priorities?"
                ]
            },
            {
                "id": "INCIDENT_POSTMORTEM",
                "name": "Ransomware Attack Post-Mortem",
                "description": "Analysis after ransomware incident to improve defenses",
                "urgency": "HIGH",
                "timeline": "3 days",
                "key_questions": [
                    "How did they get in?",
                    "What controls would have prevented this?",
                    "Recovery time objective met?",
                    "Lessons learned?"
                ]
            }
        ]
        
        return scenarios
    
    def generate_assessment_history(self, company: Dict) -> List[Dict]:
        """Generate historical assessment data for trending"""
        
        history = []
        current_date = datetime.now()
        
        # Generate 12 months of history
        for months_ago in range(12, 0, -1):
            assessment_date = current_date - timedelta(days=months_ago * 30)
            
            # Gradually improve compliance over time
            base_compliance = 45 + (12 - months_ago) * 3
            compliance = min(95, base_compliance + random.randint(-5, 10))
            
            history.append({
                "date": assessment_date.isoformat(),
                "compliance_score": compliance,
                "controls_implemented": len(company["current_controls"]) - (months_ago // 3),
                "high_risks": max(1, 8 - (12 - months_ago) // 2),
                "medium_risks": random.randint(5, 15),
                "low_risks": random.randint(10, 25)
            })
        
        return history
    
    def generate_risk_scenarios(self, company: Dict) -> List[Dict]:
        """Generate specific risk scenarios for a company"""
        
        industry_risks = {
            "Healthcare": [
                {"risk": "Patient data breach", "likelihood": "MEDIUM", "impact": "CRITICAL"},
                {"risk": "Medical device vulnerabilities", "likelihood": "HIGH", "impact": "HIGH"},
                {"risk": "Ransomware disrupting operations", "likelihood": "HIGH", "impact": "CRITICAL"}
            ],
            "Banking": [
                {"risk": "Financial fraud", "likelihood": "HIGH", "impact": "CRITICAL"},
                {"risk": "Core banking system failure", "likelihood": "LOW", "impact": "CRITICAL"},
                {"risk": "Open banking API compromise", "likelihood": "MEDIUM", "impact": "HIGH"}
            ],
            "Energy": [
                {"risk": "OT system compromise", "likelihood": "MEDIUM", "impact": "CRITICAL"},
                {"risk": "Nation-state attack", "likelihood": "LOW", "impact": "CRITICAL"},
                {"risk": "Physical infrastructure attack", "likelihood": "LOW", "impact": "HIGH"}
            ],
            "Retail": [
                {"risk": "POS malware", "likelihood": "MEDIUM", "impact": "HIGH"},
                {"risk": "E-commerce platform breach", "likelihood": "HIGH", "impact": "HIGH"},
                {"risk": "Supply chain attack", "likelihood": "MEDIUM", "impact": "MEDIUM"}
            ],
            "Government": [
                {"risk": "Citizen data exposure", "likelihood": "MEDIUM", "impact": "CRITICAL"},
                {"risk": "Service availability attack", "likelihood": "HIGH", "impact": "HIGH"},
                {"risk": "Insider threat", "likelihood": "MEDIUM", "impact": "HIGH"}
            ],
            "Technology": [
                {"risk": "Source code theft", "likelihood": "MEDIUM", "impact": "HIGH"},
                {"risk": "API security breach", "likelihood": "HIGH", "impact": "HIGH"},
                {"risk": "Multi-tenant data leak", "likelihood": "LOW", "impact": "CRITICAL"}
            ]
        }
        
        base_industry = company["industry"].split()[0]  # Get first word for matching
        risks = industry_risks.get(base_industry, industry_risks["Technology"])
        
        # Add common risks
        risks.extend([
            {"risk": "Phishing attack success", "likelihood": "HIGH", "impact": "MEDIUM"},
            {"risk": "Third-party breach", "likelihood": "MEDIUM", "impact": "MEDIUM"},
            {"risk": "Cloud misconfiguration", "likelihood": "MEDIUM", "impact": "HIGH"}
        ])
        
        return risks
    
    def save_demo_data(self):
        """Save demo data to JSON files"""
        
        # Save companies
        with open("demo_companies.json", "w") as f:
            json.dump(self.demo_companies, f, indent=2)
        
        # Save scenarios
        with open("demo_scenarios.json", "w") as f:
            json.dump(self.demo_scenarios, f, indent=2)
        
        # Generate and save full demo package
        full_demo = {
            "companies": self.demo_companies,
            "scenarios": self.demo_scenarios,
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_companies": len(self.demo_companies),
                "industries": list(set(c["industry"] for c in self.demo_companies)),
                "total_scenarios": len(self.demo_scenarios)
            }
        }
        
        with open("sentinel_grc_demo_data.json", "w") as f:
            json.dump(full_demo, f, indent=2)
        
        print(f"Demo data saved to:")
        print("  - demo_companies.json")
        print("  - demo_scenarios.json")
        print("  - sentinel_grc_demo_data.json")

async def run_demo_assessment(company: Dict):
    """Run a demo assessment for a company"""
    
    from unified_orchestrator import UnifiedSentinelGRC
    
    print(f"\n{'='*60}")
    print(f"DEMO ASSESSMENT: {company['name']}")
    print(f"{'='*60}")
    print(f"Industry: {company['industry']}")
    print(f"Size: {company['size']} ({company['employee_count']} employees)")
    print(f"Frameworks: {', '.join(company['frameworks'])}")
    print(f"Risk Profile: {company['risk_profile']}")
    
    # Initialize Sentinel GRC
    sentinel = UnifiedSentinelGRC(enable_neo4j=True, enable_sidecars=False, enable_groq=False)
    
    # Run assessment
    result = await sentinel.assess_company(
        company_name=company['name'],
        industry=company['industry'],
        employee_count=company['employee_count'],
        current_controls=company['current_controls']
    )
    
    # Display results
    print(f"\nASSESSMENT RESULTS:")
    print(f"Processing Time: {result['processing_time']:.2f}s")
    
    if result.get('graph_insights'):
        insights = result['graph_insights']
        print(f"Compliance: {insights.get('compliance_percentage', 0):.1f}%")
        print(f"Exposed Threats: {len(insights.get('exposed_threats', []))}")
        
        if insights.get('exposed_threats'):
            print("\nTop Threats:")
            for threat in insights['exposed_threats'][:3]:
                print(f"  - {threat.get('threat', 'Unknown')}")
    
    return result

def main():
    """Generate and test demo data"""
    
    print("SENTINEL GRC - DEMO DATA GENERATOR")
    print("=" * 50)
    
    # Generate demo data
    generator = DemoDataGenerator()
    
    print(f"\nGenerated {len(generator.demo_companies)} demo companies:")
    for company in generator.demo_companies:
        print(f"  - {company['name']} ({company['industry']})")
    
    print(f"\nGenerated {len(generator.demo_scenarios)} demo scenarios:")
    for scenario in generator.demo_scenarios:
        print(f"  - {scenario['name']}")
    
    # Save demo data
    generator.save_demo_data()
    
    # Test with one company
    print("\n" + "="*50)
    print("TESTING WITH SAMPLE COMPANY")
    print("="*50)
    
    test_company = generator.demo_companies[0]  # MediCare Plus Hospital
    asyncio.run(run_demo_assessment(test_company))
    
    print("\nDEMO DATA GENERATION COMPLETE!")
    print("You can now use this data to demonstrate Sentinel GRC capabilities")

if __name__ == "__main__":
    main()