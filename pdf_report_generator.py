"""
PDF Report Generator for Sentinel GRC
======================================
Generates professional PDF compliance reports.
Using reportlab for PDF generation.
"""

# First install: pip install reportlab

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import json
from typing import Dict, Any, List

class PDFReportGenerator:
    """Generate professional PDF compliance reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='Executive',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
    
    def generate_compliance_report(self, 
                                  company_data: Dict,
                                  assessment_results: Dict,
                                  output_file: str = None) -> str:
        """Generate comprehensive compliance report"""
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"compliance_report_{timestamp}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        story = []
        
        # Title Page
        story.append(Paragraph("COMPLIANCE ASSESSMENT REPORT", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(company_data.get('name', 'Company'), self.styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), self.styles['Normal']))
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("EXECUTIVE SUMMARY", self.styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        compliance_score = assessment_results.get('compliance_percentage', 0)
        summary_text = f"""
        This report presents the compliance assessment results for {company_data.get('name', 'the organization')}.
        The assessment evaluated compliance against {', '.join(assessment_results.get('frameworks', ['Essential8']))}.
        
        Overall Compliance Score: {compliance_score:.1f}%
        Risk Level: {company_data.get('risk_profile', 'MEDIUM')}
        Assessment Date: {datetime.now().strftime("%Y-%m-%d")}
        """
        story.append(Paragraph(summary_text, self.styles['Executive']))
        
        # Key Findings
        story.append(Paragraph("KEY FINDINGS", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        # Create findings table
        findings_data = [
            ['Category', 'Status', 'Priority'],
            ['Controls Implemented', f"{len(assessment_results.get('implemented_controls', []))}", 'N/A'],
            ['Controls Missing', f"{len(assessment_results.get('missing_controls', []))}", 'HIGH'],
            ['Exposed Threats', f"{len(assessment_results.get('exposed_threats', []))}", 'CRITICAL'],
        ]
        
        findings_table = Table(findings_data, colWidths=[3*inch, 2*inch, 1.5*inch])
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(findings_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("RECOMMENDATIONS", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        recommendations = assessment_results.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations[:5], 1):
                rec_text = f"{i}. {rec.get('control', 'Control')} - {rec.get('effort', 'MEDIUM')} effort"
                story.append(Paragraph(rec_text, self.styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
        
        # Build PDF
        doc.build(story)
        
        return output_file
    
    def generate_executive_dashboard(self, 
                                    companies: List[Dict],
                                    output_file: str = "executive_dashboard.pdf") -> str:
        """Generate executive dashboard for multiple companies"""
        
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        story = []
        
        # Dashboard Title
        story.append(Paragraph("GRC EXECUTIVE DASHBOARD", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"Portfolio Overview - {datetime.now().strftime('%B %Y')}", self.styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Portfolio Summary Table
        portfolio_data = [['Company', 'Industry', 'Compliance', 'Risk Level']]
        
        for company in companies[:10]:  # Limit to 10 for space
            portfolio_data.append([
                company.get('name', 'Unknown')[:30],
                company.get('industry', 'N/A'),
                f"{company.get('compliance', 0):.0f}%",
                company.get('risk_profile', 'MEDIUM')
            ])
        
        portfolio_table = Table(portfolio_data, colWidths=[3*inch, 2*inch, 1.5*inch, 1.5*inch])
        portfolio_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightblue])
        ]))
        
        story.append(portfolio_table)
        
        # Build PDF
        doc.build(story)
        
        return output_file

def test_pdf_generation():
    """Test PDF report generation with demo data"""
    
    print("Testing PDF Report Generation...")
    
    # Load demo data
    try:
        with open("demo_companies.json", "r") as f:
            companies = json.load(f)
    except:
        companies = [
            {
                "name": "Test Company",
                "industry": "Healthcare",
                "risk_profile": "HIGH",
                "compliance": 75
            }
        ]
    
    # Create generator
    generator = PDFReportGenerator()
    
    # Test company report
    test_company = companies[0] if companies else {"name": "Test Corp"}
    test_results = {
        "compliance_percentage": 75.5,
        "frameworks": ["Essential8", "HIPAA", "ISO 27001"],
        "implemented_controls": ["E8_7", "E8_8", "HIPAA_A1"],
        "missing_controls": ["E8_1", "E8_2", "E8_3", "E8_4", "E8_5"],
        "exposed_threats": ["Ransomware", "Phishing", "Data Breach"],
        "recommendations": [
            {"control": "Multi-factor Authentication", "effort": "LOW"},
            {"control": "Application Control", "effort": "HIGH"},
            {"control": "Regular Backups", "effort": "MEDIUM"}
        ]
    }
    
    # Generate report
    report_file = generator.generate_compliance_report(test_company, test_results)
    print(f"Generated compliance report: {report_file}")
    
    # Generate dashboard
    dashboard_file = generator.generate_executive_dashboard(companies[:5])
    print(f"Generated executive dashboard: {dashboard_file}")
    
    print("\nPDF generation complete!")
    print("Note: Install reportlab first: pip install reportlab")

if __name__ == "__main__":
    test_pdf_generation()