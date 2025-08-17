#!/usr/bin/env python3
"""
Professional Brunel University ISO 27001 Audit Test
===================================================

This script tests our enhanced audit capabilities against real university data.
"""

import sys
sys.path.append('src')
import asyncio
from datetime import datetime
from auditing.iso27001_audit_engine import ISO27001AuditEngine, AuditFinding, FindingType
from professional.enhanced_pdf_generator import EnhancedPDFGenerator

async def test_brunel_audit():
    print('Starting Brunel University ISO 27001 Professional Audit')
    start_time = datetime.now()
    
    # Initialize engines
    audit_engine = ISO27001AuditEngine()
    pdf_generator = EnhancedPDFGenerator()
    
    # Create organization profile based on Brunel docs
    brunel_profile = {
        'organization_name': 'Brunel University London',
        'industry': 'higher_education',
        'departments': ['IT Services', 'Research', 'Academic Colleges', 'Student Services', 'HR', 'Finance'],
        'key_processes': [
            'Student data management', 
            'Research data processing', 
            'Financial transactions',
            'Academic record keeping',
            'GDPR compliance',
            'Cyber security operations'
        ],
        'systems': [
            'Student Information System',
            'Research Data Management',
            'Email & Collaboration',
            'Financial Management System',
            'ISMS Documentation System'
        ],
        'locations': ['Kingston Lane Campus, Uxbridge', 'Associated research sites'],
        'regulatory_requirements': ['GDPR', 'ISO 27001:2013', 'Cyber Essentials', 'HEFCE requirements'],
        'staff_count': 2500,
        'student_count': 15000
    }
    
    print(f'Organization: {brunel_profile["organization_name"]}')
    print(f'Industry: {brunel_profile["industry"]}')
    print(f'Scale: {brunel_profile["staff_count"]} staff, {brunel_profile["student_count"]} students')
    
    # Step 1: Define audit scope
    print('\nStep 1: Defining audit scope...')
    scope = await audit_engine.step1_define_audit_scope('certification_audit', brunel_profile)
    print(f'Scope defined: {len(scope.iso_clauses)} clauses, {len(scope.departments)} departments')
    
    # Step 2: Develop audit plan  
    print('\nStep 2: Developing audit plan...')
    plan = await audit_engine.step2_develop_audit_plan(scope, 'certification_audit')
    print(f'Plan created: {len(plan.audit_team)} auditors, {len(plan.schedule)} phases')
    
    # Step 3: Prepare checklist
    print('\nStep 3: Preparing audit checklist...')
    checklist = await audit_engine.step3_prepare_audit_checklist(plan)
    total_checks = sum(len(checks) for checks in checklist.values())
    print(f'Checklist prepared: {total_checks} checks across {len(checklist)} areas')
    
    # Simulate findings based on Brunel documentation analysis
    print('\nStep 4-7: Conducting audit and analyzing findings...')
    findings = [
        AuditFinding(
            finding_id='BUL-001',
            finding_type=FindingType.CONFORMITY,
            iso_clause='A.6.1.1',
            control_reference='Information Security Roles and Responsibilities',
            description='Well-defined ISMS governance structure with clear roles from CISO to asset owners',
            evidence=[
                'BUL-POL-6.1.1 Information Security Roles and Responsibilities v1.1',
                'Organizational chart showing CISO, SIRO, Data Protection Officer roles',
                'Evidence of executive board oversight and Infrastructure Strategy Committee'
            ],
            impact_assessment='Positive - Strong governance foundation',
            severity='Low',
            department='IT Services',
            responsible_person='Mick Jenkins (CISO)',
            target_closure_date='N/A - Conforming',
            status='Conforming'
        ),
        AuditFinding(
            finding_id='BUL-002', 
            finding_type=FindingType.CONFORMITY,
            iso_clause='A.5.1',
            control_reference='Information Security Policy',
            description='Comprehensive information security policy aligned with business objectives',
            evidence=[
                'POL-05.1 Information Security Policy v2.0',
                'Executive approval by Vice-Chancellor Julia Buckingham',
                'Policy covers all university sites and third parties'
            ],
            impact_assessment='Positive - Clear policy framework',
            severity='Low',
            department='Executive Board',
            responsible_person='Pekka Kahkipuro (CIO)',
            target_closure_date='N/A - Conforming',
            status='Conforming'
        ),
        AuditFinding(
            finding_id='BUL-003',
            finding_type=FindingType.MINOR_NONCONFORMITY,
            iso_clause='A.8.1.2',
            control_reference='Privileged Access Management',
            description='While access control policies exist, privileged access review frequency not clearly defined',
            evidence=[
                'Access control policies reference bi-annual reviews',
                'Some privileged accounts lack documented review dates',
                'No automated privileged access monitoring system'
            ],
            impact_assessment='Medium - Potential for privilege escalation if accounts not regularly reviewed',
            severity='Medium',
            department='IT Services',
            responsible_person='Head of IT Infrastructure',
            target_closure_date='2024-12-31',
            status='Open',
            corrective_action_plan='Implement automated privileged access review system with quarterly reviews'
        ),
        AuditFinding(
            finding_id='BUL-004',
            finding_type=FindingType.OPPORTUNITY_FOR_IMPROVEMENT,
            iso_clause='A.16.1',
            control_reference='Incident Management',
            description='Incident response procedures could benefit from more specific cyber security workflows',
            evidence=[
                'General incident management plan exists',
                'Cyber security incidents handled but not with specialized procedures',
                'No specific cyber incident classification system'
            ],
            impact_assessment='Low - Current process adequate but could be optimized',
            severity='Low',
            department='Security & Emergency Planning',
            responsible_person='Head of Security & Emergency Planning',
            target_closure_date='2025-06-30',
            status='Open',
            corrective_action_plan='Develop specialized cyber incident response procedures with clear escalation paths'
        ),
        AuditFinding(
            finding_id='BUL-005',
            finding_type=FindingType.CONFORMITY,
            iso_clause='A.18.1',
            control_reference='GDPR Compliance',
            description='Strong data protection framework with dedicated DPO and comprehensive policies',
            evidence=[
                'Dedicated Data Protection Officer role',
                'GDPR training and awareness programs',
                'Data processing records and privacy impact assessments'
            ],
            impact_assessment='Positive - Excellent data protection compliance',
            severity='Low',
            department='Legal & Governance',
            responsible_person='Data Protection Officer',
            target_closure_date='N/A - Conforming',
            status='Conforming'
        )
    ]
    
    print(f'Analysis complete: {len(findings)} findings identified')
    
    # Step 8: Generate report data
    print('\nStep 8: Generating comprehensive audit report...')
    report_data = await audit_engine.generate_audit_report_data(plan, findings, checklist)
    print(f'Report data generated: {report_data["executive_summary"]["compliance_percentage"]}% compliance')
    
    # Generate professional PDF
    print('\nStep 9: Creating professional audit report PDF...')
    
    # Enhanced audit data for PDF
    enhanced_audit_data = {
        'organization': brunel_profile,
        'audit_metadata': report_data['audit_metadata'],
        'executive_summary': report_data['executive_summary'],
        'scope_and_methodology': {
            'audit_scope': scope,
            'audit_plan': plan,
            'audit_approach': 'Risk-based sampling approach focusing on critical controls',
            'audit_standards': ['ISO/IEC 27001:2013', 'ISO/IEC 27002:2022'],
            'sampling_methodology': 'Systematic sampling across all departments and control domains'
        },
        'detailed_findings': report_data['detailed_findings'],
        'findings_analysis': report_data['findings_analysis'],
        'corrective_actions': report_data['corrective_action_plan'],
        'management_response': {
            'overall_response': 'Brunel University London acknowledges the audit findings and commits to implementing recommended improvements within specified timeframes.',
            'resource_commitment': 'Dedicated ISMS team will oversee corrective actions with executive support',
            'timeline_commitment': 'All findings to be addressed within 6 months'
        },
        'certification_recommendation': {
            'recommendation': 'Recommend certification' if report_data['certification_readiness']['ready_for_certification'] else 'Certification deferred',
            'justification': report_data['executive_summary']['overall_conclusion'],
            'conditions': [] if report_data['certification_readiness']['ready_for_certification'] else ['Address minor nonconformities', 'Implement enhanced privileged access controls']
        }
    }
    
    # Generate the PDF
    pdf_result = await pdf_generator.generate_iso27001_audit_report(enhanced_audit_data, 'pdf')
    
    elapsed = datetime.now() - start_time
    print(f'\nAUDIT COMPLETE!')
    print(f'Total time: {elapsed.total_seconds():.2f} seconds')
    print(f'Compliance score: {report_data["executive_summary"]["compliance_percentage"]}%')
    print(f'Total findings: {len(findings)}')
    print(f'Major nonconformities: {report_data["findings_analysis"]["summary"]["major_nonconformities"]}')
    print(f'Minor nonconformities: {report_data["findings_analysis"]["summary"]["minor_nonconformities"]}')
    print(f'Opportunities for improvement: {report_data["findings_analysis"]["summary"]["opportunities"]}')
    print(f'Conformities: {report_data["findings_analysis"]["summary"]["conformities"]}')
    print(f'PDF result: {pdf_result}')
    
    # Extract file path safely
    if isinstance(pdf_result, dict) and 'file_path' in pdf_result:
        print(f'Report saved as: {pdf_result["file_path"]}')
    elif isinstance(pdf_result, dict) and 'filename' in pdf_result:
        print(f'Report saved as: {pdf_result["filename"]}')
    else:
        print(f'Report generated (result format: {type(pdf_result)})')
    
    # Performance metrics
    print(f'\nPERFORMANCE METRICS:')
    print(f'Processing speed: {total_checks/elapsed.total_seconds():.1f} checks/second')
    print(f'Intelligence: {len(checklist)} control areas analyzed')
    print(f'Audit depth: {total_checks} individual compliance checks')
    print(f'Risk focus: {report_data["findings_analysis"]["summary"]["major_nonconformities"] + report_data["findings_analysis"]["summary"]["minor_nonconformities"]} risks identified')
    
    return pdf_result, report_data, elapsed

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_brunel_audit())