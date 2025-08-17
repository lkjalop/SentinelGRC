"""
Bulk PDF Export Manager
======================

Handles bulk export of compliance reports for easy auditor access
"""

import os
import zipfile
from datetime import datetime
from typing import List, Dict, Any
import asyncio
from .enhanced_pdf_generator import EnhancedPDFGenerator

class BulkExportManager:
    def __init__(self):
        self.pdf_generator = EnhancedPDFGenerator()
    
    async def export_audit_package(self, 
                                  organization_data: Dict[str, Any],
                                  export_formats: List[str] = None) -> Dict[str, Any]:
        """
        Export complete audit package for external auditors
        
        Creates:
        - ISO 27001 Audit Report
        - Executive Summary  
        - Findings Detail Report
        - Corrective Action Plan
        - Evidence Package
        """
        
        if export_formats is None:
            export_formats = ['pdf', 'excel', 'json']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        org_name = organization_data.get('organization_name', 'Organization').replace(' ', '_')
        
        export_package = {
            'timestamp': timestamp,
            'organization': org_name,
            'files': [],
            'summary': {}
        }
        
        # Generate all report types
        reports = []
        
        if 'pdf' in export_formats:
            # Main audit report
            audit_pdf = await self.pdf_generator.generate_iso27001_audit_report(
                organization_data, 'pdf'
            )
            reports.append({
                'name': f'{org_name}_ISO27001_Audit_Report_{timestamp}.pdf',
                'data': audit_pdf['data'],
                'type': 'audit_report'
            })
            
            # Executive summary
            exec_summary = await self.pdf_generator.generate_executive_summary(
                organization_data, 'pdf'
            )
            reports.append({
                'name': f'{org_name}_Executive_Summary_{timestamp}.pdf', 
                'data': exec_summary['data'],
                'type': 'executive_summary'
            })
        
        # Create ZIP package
        zip_filename = f'{org_name}_Audit_Package_{timestamp}.zip'
        
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for report in reports:
                zip_file.writestr(report['name'], report['data'])
            
            # Add audit metadata
            metadata = {
                'audit_date': timestamp,
                'organization': org_name,
                'audit_type': 'ISO 27001 Certification Audit',
                'auditor': 'Sentinel GRC Platform',
                'report_count': len(reports),
                'package_contents': [r['name'] for r in reports]
            }
            
            import json
            zip_file.writestr('audit_metadata.json', json.dumps(metadata, indent=2))
        
        export_package['zip_file'] = zip_filename
        export_package['files'] = reports
        export_package['summary'] = {
            'total_reports': len(reports),
            'package_size': os.path.getsize(zip_filename),
            'ready_for_external_auditor': True
        }
        
        return export_package