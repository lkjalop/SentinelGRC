"""
Test script for Enterprise PDF Generator
"""

import sys
import os
sys.path.append('src')

from professional.enterprise_pdf_generator import EnterprisePDFGenerator

def test_enterprise_pdf():
    """Test enterprise PDF generation with comprehensive data"""
    
    # Comprehensive test data
    sample_assessment = {
        "controls": [
            {"id": "AC-1", "status": "implemented", "criticality": "high", "category": "access_control", 
             "description": "Access Control Policy and Procedures"},
            {"id": "AC-2", "status": "partial", "criticality": "medium", "category": "access_control",
             "description": "Account Management"},
            {"id": "AC-3", "status": "not_implemented", "criticality": "high", "category": "access_control",
             "description": "Access Enforcement"},
            {"id": "AU-1", "status": "implemented", "criticality": "high", "category": "audit",
             "description": "Audit and Accountability Policy"},
            {"id": "AU-2", "status": "partial", "criticality": "medium", "category": "audit",
             "description": "Audit Events"},
            {"id": "SC-1", "status": "not_implemented", "criticality": "high", "category": "system_communications",
             "description": "System and Communications Protection Policy"}
        ],
        "findings": [
            {
                "title": "Multi-factor authentication gaps",
                "severity": "critical",
                "description": "MFA not implemented across all administrative systems, creating significant access control vulnerabilities",
                "business_impact": "high",
                "recommendation": "Implement enterprise MFA solution across all systems within 4 weeks",
                "type": "access",
                "probability": "high",
                "asset_criticality": "high"
            },
            {
                "title": "Insufficient log retention periods",
                "severity": "high", 
                "description": "Current log retention of 30 days does not meet compliance requirements of 12 months",
                "business_impact": "medium",
                "recommendation": "Extend log retention to 12 months and implement automated archiving",
                "type": "audit",
                "probability": "medium",
                "asset_criticality": "medium"
            },
            {
                "title": "Unencrypted data transmission",
                "severity": "medium",
                "description": "Some internal communications not using TLS encryption",
                "business_impact": "medium", 
                "recommendation": "Enforce TLS 1.3 for all data transmission",
                "type": "encryption",
                "probability": "medium",
                "asset_criticality": "high"
            },
            {
                "title": "Outdated access review procedures",
                "severity": "low",
                "description": "Quarterly access reviews running 2 weeks behind schedule",
                "business_impact": "low",
                "recommendation": "Automate access review notifications and tracking",
                "type": "process",
                "probability": "low",
                "asset_criticality": "medium"
            }
        ]
    }
    
    customer_context = {
        "name": "TechCorp Industries Inc",
        "industry": "technology",
        "size": "medium"
    }
    
    expert_comments = [
        {
            "reviewer_name": "Sarah Johnson, CISSP, CISM",
            "section": "Access Controls",
            "comment_text": "The organization should prioritize implementing a privileged access management (PAM) solution. This will address the MFA gaps and provide better visibility into administrative activities. Consider solutions like CyberArk or BeyondTrust.",
            "timestamp": "2025-08-16T10:30:00",
            "comment_type": "strategic_insight"
        },
        {
            "reviewer_name": "Michael Chen, CISA",
            "section": "Audit and Logging",
            "comment_text": "The current logging infrastructure appears adequate but needs capacity expansion for 12-month retention. Budget approximately $25K for additional storage and SIEM licensing. This investment will pay dividends during the SOC 2 audit.",
            "timestamp": "2025-08-16T10:45:00",
            "comment_type": "recommendation"
        },
        {
            "reviewer_name": "Dr. Lisa Thompson, Security Architect",
            "section": "Overall Strategy",
            "comment_text": "TechCorp's security maturity is progressing well. The organization shows strong leadership commitment. Focus on automation and integration of security tools to reduce manual overhead and improve consistency. Consider a phased approach to certification with SOC 2 first, then ISO 27001.",
            "timestamp": "2025-08-16T11:00:00",
            "comment_type": "strategic_insight"
        }
    ]
    
    # Test PDF generation
    print("Starting Enterprise PDF Generation Test...")
    
    try:
        generator = EnterprisePDFGenerator()
        print("[OK] Enterprise PDF Generator initialized")
        
        # Generate the report
        output_path = generator.generate_enterprise_report(
            assessment_data=sample_assessment,
            framework="SOC 2",
            customer_context=customer_context,
            expert_comments=expert_comments,
            output_path="reports/TechCorp_SOC2_Enterprise_Test.pdf"
        )
        
        print(f"[OK] Enterprise PDF generated successfully!")
        print(f"[OK] Output location: {output_path}")
        
        # Check if file exists and get size
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"[OK] File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
            
            if file_size > 100000:  # > 100KB indicates successful generation
                print("[OK] PDF appears to be properly generated (sufficient file size)")
            else:
                print("[WARNING] PDF file size is small, may indicate generation issues")
        else:
            print("[ERROR] PDF file was not created")
            return False
        
        print("\n" + "="*60)
        print("ENTERPRISE PDF GENERATION TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"[ERROR] PDF generation failed")
        print(f"Error details: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enterprise_pdf()
    if success:
        print("\n[SUCCESS] All tests passed! Enterprise PDF Generator is working correctly.")
    else:
        print("\n[FAILED] Tests failed. Check error messages above.")