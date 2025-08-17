"""
Enhanced Framework-Specific PDF Report Generator
==============================================

Professional-grade PDF reports with framework-specific templates and cross-framework analysis.
Includes certification roadmaps and compliance comparison matrices.

Author: Sentinel GRC Platform
Version: 1.0.0-production
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime, timedelta
import json
import os
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class FrameworkSpecificPDFGenerator:
    """
    Advanced PDF generator with framework-specific templates and cross-framework analysis
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        self.framework_templates = self._initialize_framework_templates()
        self.certification_roadmaps = self._initialize_certification_roadmaps()
        self.color_scheme = self._initialize_color_scheme()
    
    def setup_custom_styles(self):
        """Create custom paragraph styles for professional reports"""
        
        # Corporate title style
        self.styles.add(ParagraphStyle(
            name='CorporateTitle',
            parent=self.styles['Title'],
            fontSize=28,
            textColor=colors.HexColor('#0B3D91'),  # Deep Ocean Blue
            alignment=TA_CENTER,
            spaceAfter=24,
            fontName='Helvetica-Bold'
        ))
        
        # Framework subtitle
        self.styles.add(ParagraphStyle(
            name='FrameworkSubtitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1565C0'),
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            spaceBefore=6,
            leftIndent=12,
            rightIndent=12
        ))
        
        # Professional heading
        self.styles.add(ParagraphStyle(
            name='ProfessionalHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1565C0'),
            spaceAfter=8,
            spaceBefore=16,
            fontName='Helvetica-Bold'
        ))
        
        # Finding style
        self.styles.add(ParagraphStyle(
            name='Finding',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20,
            bulletIndent=12
        ))
        
        # Recommendation style
        self.styles.add(ParagraphStyle(
            name='Recommendation',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=16,
            textColor=colors.HexColor('#2E7D32')
        ))
        
        # Critical finding style
        self.styles.add(ParagraphStyle(
            name='CriticalFinding',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20,
            textColor=colors.HexColor('#C62828'),
            fontName='Helvetica-Bold'
        ))
    
    def _initialize_color_scheme(self) -> Dict[str, Any]:
        """Initialize professional color scheme"""
        return {
            "primary": colors.HexColor('#0B3D91'),      # Deep Ocean Blue
            "secondary": colors.HexColor('#1565C0'),    # Medium Blue
            "success": colors.HexColor('#2E7D32'),      # Success Green
            "warning": colors.HexColor('#F57C00'),      # Warning Orange
            "critical": colors.HexColor('#C62828'),     # Critical Red
            "light_gray": colors.HexColor('#F5F5F5'),   # Light Background
            "medium_gray": colors.HexColor('#E0E0E0'),  # Medium Background
            "dark_gray": colors.HexColor('#424242'),    # Dark Text
            "white": colors.white,
            "black": colors.black
        }
    
    def _initialize_framework_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize framework-specific report templates"""
        return {
            "iso_27001": {
                "title": "ISO 27001:2022 Information Security Management System Assessment",
                "subtitle": "ISMS Maturity Assessment with AI Integration",
                "executive_summary_template": """
                This report presents a comprehensive assessment of the Information Security Management System (ISMS) 
                against ISO/IEC 27001:2022 requirements. The assessment includes evaluation of all 93 Annex A controls 
                and integration with AI risk management standards (ISO 42001 and ISO 23894) where applicable.
                
                The assessment methodology follows industry best practices and provides a maturity-based evaluation 
                of the organization's information security posture, certification readiness, and strategic recommendations 
                for continuous improvement.
                """,
                "key_sections": [
                    "ISMS Context and Scope (Clause 4)",
                    "Leadership and Policy Framework (Clause 5)", 
                    "Risk Management Process (Clause 6)",
                    "Support and Resources (Clause 7)",
                    "Operational Controls (Clause 8)",
                    "Performance Monitoring (Clause 9)",
                    "Continuous Improvement (Clause 10)",
                    "Annex A Control Assessment",
                    "AI Risk Management Integration",
                    "Certification Readiness"
                ],
                "certification_focus": "ISO 27001:2022 certification readiness with AI considerations"
            },
            
            "soc2": {
                "title": "SOC 2 Type II Readiness Assessment",
                "subtitle": "Trust Service Criteria Evaluation",
                "executive_summary_template": """
                This report evaluates the organization's readiness for a SOC 2 Type II examination based on the 
                Trust Service Criteria (TSC). The assessment covers Security (Common Criteria) and applicable 
                additional criteria: Availability, Processing Integrity, Confidentiality, and Privacy.
                
                The evaluation methodology assesses both the design and operational effectiveness of controls 
                over a specified period, providing insights into SOC 2 audit readiness and areas requiring 
                attention before engaging with a CPA firm.
                """,
                "key_sections": [
                    "Security (Common Criteria)",
                    "Availability Criteria", 
                    "Processing Integrity Criteria",
                    "Confidentiality Criteria",
                    "Privacy Criteria",
                    "Control Environment Assessment",
                    "Risk Assessment Process",
                    "Information and Communication",
                    "Monitoring Activities",
                    "SOC 2 Audit Readiness"
                ],
                "certification_focus": "SOC 2 Type II examination readiness"
            },
            
            "nist_sp_800_53": {
                "title": "NIST SP 800-53 Rev 5 Security Controls Assessment",
                "subtitle": "Federal Risk and Authorization Management Program (FedRAMP) Alignment",
                "executive_summary_template": """
                This assessment evaluates security controls implementation against NIST SP 800-53 Rev 5 
                requirements. The evaluation covers all relevant control families and provides assessment 
                of control implementation status, effectiveness, and alignment with federal security requirements.
                
                The assessment methodology considers control inheritance, hybrid implementations, and 
                customer responsibilities in cloud environments, providing a comprehensive view of 
                the security control posture for federal compliance requirements.
                """,
                "key_sections": [
                    "Access Control (AC)",
                    "Awareness and Training (AT)",
                    "Audit and Accountability (AU)",
                    "Configuration Management (CM)",
                    "Contingency Planning (CP)",
                    "Identification and Authentication (IA)",
                    "Incident Response (IR)",
                    "Risk Assessment (RA)",
                    "System and Communications Protection (SC)",
                    "FedRAMP Compliance Status"
                ],
                "certification_focus": "FedRAMP authorization readiness"
            },
            
            "privacy_act": {
                "title": "Privacy Act 1988 (Cth) Compliance Assessment",
                "subtitle": "Australian Privacy Principles Evaluation", 
                "executive_summary_template": """
                This report assesses compliance with the Privacy Act 1988 (Commonwealth) and the 
                13 Australian Privacy Principles (APPs). The assessment evaluates personal information 
                handling practices, privacy policies, consent mechanisms, and breach response procedures.
                
                The evaluation methodology considers the organization's personal information lifecycle, 
                cross-border data transfers, and obligations under the Notifiable Data Breaches scheme, 
                providing recommendations for privacy compliance and risk mitigation.
                """,
                "key_sections": [
                    "APP 1 - Open and Transparent Management",
                    "APP 2 - Anonymity and Pseudonymity",
                    "APP 3 - Collection of Personal Information",
                    "APP 4 - Dealing with Unsolicited Personal Information",
                    "APP 5 - Notification of Collection",
                    "APP 6 - Use or Disclosure",
                    "APP 7 - Direct Marketing",
                    "APP 8 - Cross-Border Disclosure",
                    "APP 9 - Government Related Identifiers",
                    "APP 10 - Quality of Personal Information",
                    "APP 11 - Security",
                    "APP 12 - Access to Personal Information",
                    "APP 13 - Correction",
                    "Notifiable Data Breaches Compliance"
                ],
                "certification_focus": "Privacy Act compliance and OAIC audit readiness"
            },
            
            "essential_eight": {
                "title": "ACSC Essential Eight Maturity Assessment",
                "subtitle": "Cyber Security Maturity Evaluation",
                "executive_summary_template": """
                This assessment evaluates the organization's implementation of the Australian Cyber Security Centre's 
                Essential Eight mitigation strategies. The evaluation covers all eight strategies across 
                Maturity Levels 1, 2, and 3, providing a comprehensive view of cyber security posture.
                
                The assessment methodology aligns with ACSC guidance and provides specific recommendations 
                for progressing through maturity levels, with particular attention to the effectiveness 
                of implemented strategies in mitigating common attack vectors.
                """,
                "key_sections": [
                    "Application Control",
                    "Patch Applications", 
                    "Configure Microsoft Office Macro Settings",
                    "User Application Hardening",
                    "Restrict Administrative Privileges",
                    "Patch Operating Systems",
                    "Multi-factor Authentication",
                    "Regular Backups",
                    "Maturity Level Assessment",
                    "Threat Mitigation Effectiveness"
                ],
                "certification_focus": "ACSC Essential Eight maturity progression"
            }
        }
    
    def _initialize_certification_roadmaps(self) -> Dict[str, Dict[str, Any]]:
        """Initialize certification roadmaps and cross-framework recommendations"""
        return {
            "iso_27001": {
                "prerequisites": [],
                "typical_timeline": "12-18 months",
                "complementary_frameworks": ["SOC 2", "NIST SP 800-53", "Essential Eight"],
                "certification_body": "Accredited ISO 27001 certification body",
                "annual_cost_estimate": "$15,000 - $50,000",
                "cross_framework_benefits": {
                    "SOC 2": "ISO 27001 ISMS provides strong foundation for SOC 2 Security criteria",
                    "NIST SP 800-53": "Many ISO 27001 controls map directly to NIST controls",
                    "Essential Eight": "Technical controls complement ISO 27001 Annex A requirements"
                }
            },
            "soc2": {
                "prerequisites": ["Established internal controls", "Documentation systems"],
                "typical_timeline": "6-12 months",
                "complementary_frameworks": ["ISO 27001", "NIST CSF"],
                "certification_body": "Licensed CPA firm",
                "annual_cost_estimate": "$25,000 - $100,000",
                "cross_framework_benefits": {
                    "ISO 27001": "SOC 2 Type II provides evidence for ISO 27001 management system",
                    "NIST CSF": "SOC 2 security controls align with NIST CSF implementation"
                }
            },
            "privacy_act": {
                "prerequisites": ["Privacy policy", "Data mapping"],
                "typical_timeline": "3-6 months",
                "complementary_frameworks": ["ISO 27001", "SOC 2"],
                "certification_body": "Self-certification with OAIC compliance",
                "annual_cost_estimate": "$5,000 - $25,000",
                "cross_framework_benefits": {
                    "ISO 27001": "Privacy controls strengthen A.18 Compliance requirements",
                    "SOC 2": "Privacy criteria directly supports SOC 2 Privacy TSC"
                }
            }
        }
    
    def generate_framework_specific_report(self, 
                                         framework_name: str,
                                         company_profile: Dict[str, Any],
                                         assessment_result: Dict[str, Any],
                                         output_path: str = None) -> str:
        """Generate framework-specific professional report"""
        
        if framework_name not in self.framework_templates:
            raise ValueError(f"Framework template not found: {framework_name}")
        
        template = self.framework_templates[framework_name]
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_company = "".join(c for c in company_profile.get('name', 'Company') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = f"{safe_company}_{framework_name}_Assessment_{timestamp}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        story = []
        
        # Generate report sections
        story.extend(self._create_title_page(template, company_profile, assessment_result))
        story.extend(self._create_executive_summary(template, company_profile, assessment_result))
        story.extend(self._create_assessment_methodology(framework_name))
        story.extend(self._create_detailed_findings(framework_name, assessment_result))
        story.extend(self._create_maturity_assessment(assessment_result))
        story.extend(self._create_recommendations(framework_name, assessment_result))
        story.extend(self._create_certification_roadmap(framework_name))
        story.extend(self._create_cross_framework_analysis(framework_name, company_profile))
        story.extend(self._create_appendices(framework_name, assessment_result))
        
        # Build PDF
        doc.build(story)
        logger.info(f"Generated framework-specific report: {output_path}")
        
        return output_path
    
    def _create_title_page(self, template: Dict[str, Any], company_profile: Dict[str, Any], 
                          assessment_result: Dict[str, Any]) -> List[Any]:
        """Create professional title page"""
        elements = []
        
        # Company logo space (placeholder)
        elements.append(Spacer(1, 0.5*inch))
        
        # Main title
        elements.append(Paragraph(template["title"], self.styles['CorporateTitle']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        elements.append(Paragraph(template["subtitle"], self.styles['FrameworkSubtitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Company information
        elements.append(Paragraph(f"<b>Organization:</b> {company_profile.get('name', 'N/A')}", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>Industry:</b> {company_profile.get('industry', 'N/A')}", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>Assessment Date:</b> {assessment_result.get('assessment_date', datetime.now().strftime('%Y-%m-%d'))}", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Assessment summary box
        overall_score = assessment_result.get('overall_score', 0)
        risk_level = assessment_result.get('risk_level', 'Unknown')
        
        summary_data = [
            ['Assessment Summary', ''],
            ['Overall Score', f"{overall_score:.1f}%"],
            ['Risk Level', risk_level],
            ['Compliance Status', assessment_result.get('compliance_status', 'Unknown')],
            ['Next Review Date', assessment_result.get('next_review_date', 'TBD')]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["primary"]),
            ('BACKGROUND', (0, 1), (-1, -1), self.color_scheme["light_gray"]),
        ]))
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Professional disclaimer
        disclaimer = """
        <b>CONFIDENTIAL</b><br/>
        This report contains confidential and proprietary information. It is intended solely for the use of the organization 
        named above and should not be distributed without prior written consent. The assessment is based on information 
        provided at the time of evaluation and represents a point-in-time analysis.
        """
        elements.append(Paragraph(disclaimer, self.styles['Normal']))
        
        # Prepared by
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph("<b>Prepared by:</b> Sentinel GRC Platform", self.styles['Normal']))
        elements.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.styles['Normal']))
        
        elements.append(PageBreak())
        return elements
    
    def _create_executive_summary(self, template: Dict[str, Any], company_profile: Dict[str, Any],
                                assessment_result: Dict[str, Any]) -> List[Any]:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Framework-specific introduction
        elements.append(Paragraph(template["executive_summary_template"], self.styles['ExecutiveSummary']))
        
        # Key metrics
        overall_score = assessment_result.get('overall_score', 0)
        confidence = assessment_result.get('confidence_level', 'Unknown')
        
        key_metrics_text = f"""
        <b>Assessment Overview:</b><br/>
        Overall Compliance Score: {overall_score:.1f}%<br/>
        Assessment Confidence: {confidence}<br/>
        Risk Level: {assessment_result.get('risk_level', 'Unknown')}<br/>
        Number of Recommendations: {len(assessment_result.get('recommendations', []))}<br/>
        """
        elements.append(Paragraph(key_metrics_text, self.styles['ExecutiveSummary']))
        
        # Key findings summary
        elements.append(Paragraph("<b>Key Findings:</b>", self.styles['Normal']))
        
        recommendations = assessment_result.get('recommendations', [])
        critical_recs = [r for r in recommendations if r.get('priority') == 'Critical']
        high_recs = [r for r in recommendations if r.get('priority') == 'High']
        
        findings_text = f"""
        • {len(critical_recs)} critical issues requiring immediate attention<br/>
        • {len(high_recs)} high-priority recommendations for compliance improvement<br/>
        • {max(0, len(recommendations) - len(critical_recs) - len(high_recs))} medium/low priority enhancement opportunities<br/>
        """
        
        if assessment_result.get('detailed_findings', {}).get('maturity_assessment'):
            maturity = assessment_result['detailed_findings']['maturity_assessment']
            findings_text += f"• Current maturity level: {maturity.get('overall_level', 'Unknown')}<br/>"
        
        elements.append(Paragraph(findings_text, self.styles['Finding']))
        
        # Business impact statement
        business_impact = self._generate_business_impact_statement(assessment_result, template)
        elements.append(Paragraph("<b>Business Impact:</b>", self.styles['Normal']))
        elements.append(Paragraph(business_impact, self.styles['ExecutiveSummary']))
        
        elements.append(PageBreak())
        return elements
    
    def _generate_business_impact_statement(self, assessment_result: Dict[str, Any], 
                                          template: Dict[str, Any]) -> str:
        """Generate business impact statement based on assessment results"""
        
        overall_score = assessment_result.get('overall_score', 0)
        
        if overall_score >= 80:
            return """
            The organization demonstrates strong compliance posture and is well-positioned for certification. 
            The current implementation provides solid risk mitigation and supports business objectives. 
            Recommended actions focus on optimization and continuous improvement rather than critical gaps.
            """
        elif overall_score >= 60:
            return """
            The organization has established foundational compliance practices but requires targeted improvements 
            to achieve full compliance. The identified gaps present moderate business risk that should be 
            addressed to support certification objectives and reduce operational risks.
            """
        else:
            return """
            Significant compliance gaps present elevated business and operational risks. Immediate action is 
            required to establish fundamental controls and processes. The organization should prioritize 
            critical recommendations to reduce risk exposure and establish a foundation for systematic improvement.
            """
    
    def _create_assessment_methodology(self, framework_name: str) -> List[Any]:
        """Create assessment methodology section"""
        elements = []
        
        elements.append(Paragraph("ASSESSMENT METHODOLOGY", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        methodology_text = f"""
        This assessment was conducted using industry-standard methodologies and best practices specific to {framework_name}. 
        The evaluation process included:
        
        <b>1. Documentation Review:</b> Analysis of policies, procedures, and supporting documentation to assess 
        design effectiveness of controls and processes.
        
        <b>2. Technical Assessment:</b> Evaluation of implemented technical controls, configurations, and 
        security measures where applicable.
        
        <b>3. Process Evaluation:</b> Assessment of operational processes, workflows, and management practices 
        to determine operational effectiveness.
        
        <b>4. Maturity Assessment:</b> Evaluation of implementation maturity using industry-standard maturity models 
        to provide developmental guidance.
        
        <b>5. Gap Analysis:</b> Identification of gaps between current state and framework requirements, 
        with prioritized recommendations for improvement.
        """
        
        elements.append(Paragraph(methodology_text, self.styles['ExecutiveSummary']))
        
        # Assessment limitations
        limitations_text = """
        <b>Assessment Limitations:</b><br/>
        This assessment is based on information provided at the time of evaluation and represents a point-in-time analysis. 
        The assessment does not constitute a guarantee of security or compliance and should be supplemented with 
        ongoing monitoring and regular reassessment.
        """
        
        elements.append(Paragraph(limitations_text, self.styles['Normal']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_detailed_findings(self, framework_name: str, assessment_result: Dict[str, Any]) -> List[Any]:
        """Create detailed findings section"""
        elements = []
        
        elements.append(Paragraph("DETAILED FINDINGS", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        detailed_findings = assessment_result.get('detailed_findings', {})
        
        if framework_name == "iso_27001":
            elements.extend(self._create_iso27001_findings(detailed_findings))
        elif framework_name == "soc2":
            elements.extend(self._create_soc2_findings(detailed_findings))
        elif framework_name == "privacy_act":
            elements.extend(self._create_privacy_findings(detailed_findings))
        else:
            # Generic findings format
            elements.extend(self._create_generic_findings(detailed_findings))
        
        return elements
    
    def _create_iso27001_findings(self, detailed_findings: Dict[str, Any]) -> List[Any]:
        """Create ISO 27001 specific findings section"""
        elements = []
        
        # ISMS Clause Assessment
        if 'isms_clauses' in detailed_findings:
            elements.append(Paragraph("ISO 27001 Clause Assessment (4-10)", self.styles['Heading3']))
            
            clauses_data = [['Clause', 'Title', 'Score', 'Status']]
            for clause_id, clause_info in detailed_findings['isms_clauses'].items():
                clauses_data.append([
                    clause_id,
                    clause_info.get('title', 'N/A'),
                    f"{clause_info.get('overall_score', 0):.1f}%",
                    clause_info.get('status', 'Unknown')
                ])
            
            clauses_table = Table(clauses_data, colWidths=[0.8*inch, 3*inch, 1*inch, 1.2*inch])
            clauses_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["primary"]),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["medium_gray"]),
            ]))
            
            elements.append(clauses_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Annex A Controls Assessment
        if 'annex_a_controls' in detailed_findings:
            elements.append(Paragraph("Annex A Controls Assessment", self.styles['Heading3']))
            
            controls = detailed_findings['annex_a_controls']
            if 'section_scores' in controls:
                sections_data = [['Section', 'Controls Area', 'Score', 'Status']]
                for section_id, score in controls['section_scores'].items():
                    status = "Compliant" if score >= 70 else "Non-Compliant"
                    sections_data.append([
                        section_id,
                        self._get_annex_section_title(section_id),
                        f"{score:.1f}%",
                        status
                    ])
                
                sections_table = Table(sections_data, colWidths=[0.8*inch, 2.5*inch, 1*inch, 1.2*inch])
                sections_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["secondary"]),
                    ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["medium_gray"]),
                ]))
                
                elements.append(sections_table)
                elements.append(Spacer(1, 0.2*inch))
        
        # AI Integration Assessment
        if 'ai_integration' in detailed_findings:
            ai_assessment = detailed_findings['ai_integration']
            if ai_assessment.get('applicable', False):
                elements.append(Paragraph("AI Risk Management Integration", self.styles['Heading3']))
                
                ai_text = f"""
                <b>AI Integration Status:</b> {ai_assessment.get('overall_maturity', 'Basic')}<br/>
                <b>ISO 42001 Readiness:</b> {ai_assessment.get('iso_42001_integration', {}).get('overall_readiness', 'Developing')}<br/>
                <b>AI Risk Score:</b> {ai_assessment.get('overall_ai_score', 0):.1f}%<br/>
                """
                elements.append(Paragraph(ai_text, self.styles['Finding']))
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _get_annex_section_title(self, section_id: str) -> str:
        """Get human-readable title for Annex A sections"""
        section_titles = {
            "A.5": "Information Security Policies",
            "A.6": "People",
            "A.7": "Physical and Environmental Security",
            "A.8": "Technology",
            "A.9": "Access Control",
            "A.10": "Cryptography",
            "A.11": "Operations Security",
            "A.12": "Communications Security",
            "A.13": "System Acquisition, Development and Maintenance",
            "A.14": "Supplier Relationships",
            "A.15": "Information Security Incident Management",
            "A.16": "Information Security in Business Continuity",
            "A.17": "Information Security Aspects of Business Continuity Management",
            "A.18": "Compliance"
        }
        return section_titles.get(section_id, section_id)
    
    def _create_soc2_findings(self, detailed_findings: Dict[str, Any]) -> List[Any]:
        """Create SOC 2 specific findings section"""
        elements = []
        
        elements.append(Paragraph("SOC 2 Trust Service Criteria Assessment", self.styles['Heading3']))
        
        # Trust Service Criteria table
        tsc_data = [['Criteria', 'Description', 'Score', 'Readiness']]
        
        # Add Security (Common Criteria)
        security_score = detailed_findings.get('security_score', 0)
        tsc_data.append(['Security', 'Common Criteria - Foundational Security', f"{security_score:.1f}%", 
                        "Ready" if security_score >= 75 else "Needs Work"])
        
        # Add other criteria if present
        criteria_map = {
            'availability': 'Availability',
            'processing_integrity': 'Processing Integrity', 
            'confidentiality': 'Confidentiality',
            'privacy': 'Privacy'
        }
        
        for key, title in criteria_map.items():
            if key in detailed_findings:
                score = detailed_findings[key]
                tsc_data.append([title, f"{title} Trust Service Criteria", f"{score:.1f}%",
                               "Ready" if score >= 75 else "Needs Work"])
        
        tsc_table = Table(tsc_data, colWidths=[1.2*inch, 2.8*inch, 1*inch, 1*inch])
        tsc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["medium_gray"]),
        ]))
        
        elements.append(tsc_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_privacy_findings(self, detailed_findings: Dict[str, Any]) -> List[Any]:
        """Create Privacy Act specific findings section"""
        elements = []
        
        elements.append(Paragraph("Australian Privacy Principles Assessment", self.styles['Heading3']))
        
        # APP assessment if available
        if 'app_assessment' in detailed_findings:
            app_data = [['APP', 'Principle', 'Score', 'Status']]
            
            for app_id, app_info in detailed_findings['app_assessment'].items():
                app_data.append([
                    app_id,
                    app_info.get('title', 'N/A'),
                    f"{app_info.get('score', 0):.1f}%",
                    app_info.get('status', 'Unknown')
                ])
            
            app_table = Table(app_data, colWidths=[0.8*inch, 3*inch, 1*inch, 1.2*inch])
            app_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["primary"]),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["medium_gray"]),
            ]))
            
            elements.append(app_table)
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_generic_findings(self, detailed_findings: Dict[str, Any]) -> List[Any]:
        """Create generic findings section for other frameworks"""
        elements = []
        
        for section_name, section_data in detailed_findings.items():
            if isinstance(section_data, dict) and 'score' in section_data:
                elements.append(Paragraph(f"{section_name.replace('_', ' ').title()}", self.styles['Heading3']))
                elements.append(Paragraph(f"Score: {section_data['score']:.1f}%", self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_maturity_assessment(self, assessment_result: Dict[str, Any]) -> List[Any]:
        """Create maturity assessment section"""
        elements = []
        
        elements.append(Paragraph("MATURITY ASSESSMENT", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        maturity_data = assessment_result.get('detailed_findings', {}).get('maturity_assessment', {})
        
        if maturity_data:
            overall_level = maturity_data.get('overall_level', 1)
            overall_score = maturity_data.get('overall_score', 0)
            
            maturity_text = f"""
            <b>Current Maturity Level:</b> {overall_level} - {self._get_maturity_name(overall_level)}<br/>
            <b>Maturity Score:</b> {overall_score:.1f}%<br/>
            <b>Assessment:</b> {self._get_maturity_description(overall_level)}
            """
            
            elements.append(Paragraph(maturity_text, self.styles['ExecutiveSummary']))
            
            # Maturity progression recommendations
            next_level = min(5, overall_level + 1)
            progression_text = f"""
            <b>Next Maturity Level ({next_level}):</b><br/>
            {self._get_maturity_progression_guidance(overall_level, next_level)}
            """
            
            elements.append(Paragraph(progression_text, self.styles['Finding']))
        
        elements.append(PageBreak())
        return elements
    
    def _get_maturity_name(self, level: int) -> str:
        """Get maturity level name"""
        names = {1: "Ad Hoc", 2: "Developing", 3: "Defined", 4: "Managed", 5: "Optimized"}
        return names.get(level, "Unknown")
    
    def _get_maturity_description(self, level: int) -> str:
        """Get maturity level description"""
        descriptions = {
            1: "Processes are ad hoc and reactive. Limited formal documentation exists.",
            2: "Basic processes are developing but inconsistently applied across the organization.",
            3: "Formal processes are defined, documented, and consistently implemented.",
            4: "Processes are quantitatively managed with metrics and continuous monitoring.",
            5: "Processes are optimized through innovation and continuous improvement."
        }
        return descriptions.get(level, "Maturity level not assessed")
    
    def _get_maturity_progression_guidance(self, current_level: int, next_level: int) -> str:
        """Get guidance for progressing to next maturity level"""
        if current_level == 1:
            return "Focus on establishing basic documented processes and formal policies. Implement systematic approaches to key controls."
        elif current_level == 2:
            return "Standardize processes across the organization. Ensure consistent implementation and regular reviews."
        elif current_level == 3:
            return "Implement metrics and monitoring to measure process effectiveness. Establish quantitative management approaches."
        elif current_level == 4:
            return "Focus on optimization and innovation. Implement predictive analytics and automation where appropriate."
        else:
            return "Continue innovation and industry leadership in security practices."
    
    def _create_recommendations(self, framework_name: str, assessment_result: Dict[str, Any]) -> List[Any]:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("RECOMMENDATIONS", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        recommendations = assessment_result.get('recommendations', [])
        
        if not recommendations:
            elements.append(Paragraph("No specific recommendations generated.", self.styles['Normal']))
            elements.append(PageBreak())
            return elements
        
        # Group recommendations by priority
        priority_groups = {}
        for rec in recommendations:
            priority = rec.get('priority', 'Medium')
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(rec)
        
        # Display recommendations by priority
        priority_order = ['Critical', 'High', 'Medium', 'Low']
        
        for priority in priority_order:
            if priority in priority_groups:
                elements.append(Paragraph(f"{priority} Priority Recommendations", self.styles['Heading3']))
                
                for i, rec in enumerate(priority_groups[priority], 1):
                    rec_text = f"""
                    <b>{i}. {rec.get('title', 'Untitled Recommendation')}</b><br/>
                    {rec.get('description', 'No description available.')}<br/>
                    <b>Timeline:</b> {rec.get('timeline', 'Not specified')}<br/>
                    <b>Effort:</b> {rec.get('effort', 'Not specified')}<br/>
                    """
                    
                    if rec.get('business_impact'):
                        rec_text += f"<b>Business Impact:</b> {rec['business_impact']}<br/>"
                    
                    if priority == 'Critical':
                        elements.append(Paragraph(rec_text, self.styles['CriticalFinding']))
                    else:
                        elements.append(Paragraph(rec_text, self.styles['Recommendation']))
                    
                    elements.append(Spacer(1, 0.1*inch))
                
                elements.append(Spacer(1, 0.2*inch))
        
        elements.append(PageBreak())
        return elements
    
    def _create_certification_roadmap(self, framework_name: str) -> List[Any]:
        """Create certification roadmap section"""
        elements = []
        
        elements.append(Paragraph("CERTIFICATION ROADMAP", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        roadmap = self.certification_roadmaps.get(framework_name, {})
        
        if roadmap:
            roadmap_text = f"""
            <b>Certification Timeline:</b> {roadmap.get('typical_timeline', 'Not specified')}<br/>
            <b>Certification Body:</b> {roadmap.get('certification_body', 'Not specified')}<br/>
            <b>Estimated Annual Cost:</b> {roadmap.get('annual_cost_estimate', 'Varies')}<br/>
            """
            
            elements.append(Paragraph(roadmap_text, self.styles['ExecutiveSummary']))
            
            # Prerequisites
            prerequisites = roadmap.get('prerequisites', [])
            if prerequisites:
                elements.append(Paragraph("<b>Prerequisites:</b>", self.styles['Normal']))
                for prereq in prerequisites:
                    elements.append(Paragraph(f"• {prereq}", self.styles['Finding']))
                elements.append(Spacer(1, 0.1*inch))
        
        elements.append(PageBreak())
        return elements
    
    def _create_cross_framework_analysis(self, framework_name: str, company_profile: Dict[str, Any]) -> List[Any]:
        """Create cross-framework analysis and recommendations"""
        elements = []
        
        elements.append(Paragraph("CROSS-FRAMEWORK ANALYSIS", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        roadmap = self.certification_roadmaps.get(framework_name, {})
        complementary = roadmap.get('complementary_frameworks', [])
        
        if complementary:
            elements.append(Paragraph("Complementary Frameworks", self.styles['Heading3']))
            
            analysis_text = f"""
            Based on your {framework_name} assessment, the following frameworks would provide 
            complementary value and leverage existing investments:
            """
            elements.append(Paragraph(analysis_text, self.styles['ExecutiveSummary']))
            
            # Create framework comparison table
            comparison_data = [['Framework', 'Synergy Benefit', 'Estimated Timeline', 'Strategic Value']]
            
            for comp_framework in complementary:
                comp_roadmap = self.certification_roadmaps.get(comp_framework.lower().replace(' ', '_'), {})
                benefit = roadmap.get('cross_framework_benefits', {}).get(comp_framework, 'Complementary controls')
                timeline = comp_roadmap.get('typical_timeline', 'Varies')
                
                # Determine strategic value based on company profile
                strategic_value = self._assess_strategic_value(comp_framework, company_profile)
                
                comparison_data.append([
                    comp_framework,
                    benefit,
                    timeline,
                    strategic_value
                ])
            
            comparison_table = Table(comparison_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1*inch])
            comparison_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["secondary"]),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["medium_gray"]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elements.append(comparison_table)
            elements.append(Spacer(1, 0.2*inch))
            
            # Certification pathway recommendations
            pathway_text = """
            <b>Recommended Certification Pathway:</b><br/>
            Based on your current implementation and business requirements, consider pursuing 
            certifications in the following order to maximize return on investment and minimize 
            overlapping effort.
            """
            elements.append(Paragraph(pathway_text, self.styles['ExecutiveSummary']))
        
        elements.append(PageBreak())
        return elements
    
    def _assess_strategic_value(self, framework: str, company_profile: Dict[str, Any]) -> str:
        """Assess strategic value of framework for company"""
        industry = company_profile.get('industry', '').lower()
        
        if framework == "SOC 2":
            if industry in ['technology', 'software', 'saas']:
                return "High"
            else:
                return "Medium"
        elif framework == "ISO 27001":
            if industry in ['financial services', 'healthcare', 'government']:
                return "High"
            else:
                return "Medium"
        elif framework == "Privacy Act":
            if company_profile.get('location', '').lower() in ['australia', 'australian']:
                return "High"
            else:
                return "Low"
        else:
            return "Medium"
    
    def _create_appendices(self, framework_name: str, assessment_result: Dict[str, Any]) -> List[Any]:
        """Create appendices section"""
        elements = []
        
        elements.append(Paragraph("APPENDICES", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Appendix A: Assessment Methodology
        elements.append(Paragraph("Appendix A: Assessment Methodology", self.styles['Heading3']))
        methodology_text = """
        This assessment utilized automated analysis combined with industry best practices to evaluate 
        compliance posture. The methodology included document analysis, configuration review, and 
        gap identification against framework requirements.
        """
        elements.append(Paragraph(methodology_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Appendix B: Definitions and Acronyms
        elements.append(Paragraph("Appendix B: Definitions and Acronyms", self.styles['Heading3']))
        definitions = self._get_framework_definitions(framework_name)
        for term, definition in definitions.items():
            elements.append(Paragraph(f"<b>{term}:</b> {definition}", self.styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
        
        return elements
    
    def _get_framework_definitions(self, framework_name: str) -> Dict[str, str]:
        """Get framework-specific definitions"""
        common_definitions = {
            "ISMS": "Information Security Management System",
            "TSC": "Trust Service Criteria", 
            "APP": "Australian Privacy Principle",
            "NIST": "National Institute of Standards and Technology",
            "ISO": "International Organization for Standardization"
        }
        
        framework_specific = {
            "iso_27001": {
                "CIA": "Confidentiality, Integrity, Availability",
                "PDCA": "Plan-Do-Check-Act cycle",
                "SoA": "Statement of Applicability"
            },
            "soc2": {
                "Type I": "Report on design of controls at a point in time",
                "Type II": "Report on design and operating effectiveness over a period",
                "Service Organization": "Entity that provides services to user entities"
            }
        }
        
        definitions = common_definitions.copy()
        definitions.update(framework_specific.get(framework_name, {}))
        return definitions

    def generate_multi_framework_comparison_report(self, 
                                                 company_profile: Dict[str, Any],
                                                 assessment_results: Dict[str, Dict[str, Any]],
                                                 output_path: str = None) -> str:
        """Generate comprehensive multi-framework comparison report"""
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_company = "".join(c for c in company_profile.get('name', 'Company') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = f"{safe_company}_Multi_Framework_Comparison_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        story = []
        
        # Title page
        story.extend(self._create_comparison_title_page(company_profile, assessment_results))
        
        # Executive summary
        story.extend(self._create_comparison_executive_summary(company_profile, assessment_results))
        
        # Framework comparison matrix
        story.extend(self._create_framework_comparison_matrix(assessment_results))
        
        # Certification roadmap
        story.extend(self._create_integrated_certification_roadmap(assessment_results))
        
        # Investment analysis
        story.extend(self._create_investment_analysis(assessment_results))
        
        doc.build(story)
        logger.info(f"Generated multi-framework comparison report: {output_path}")
        
        return output_path
    
    def _create_comparison_title_page(self, company_profile: Dict[str, Any], 
                                    assessment_results: Dict[str, Dict[str, Any]]) -> List[Any]:
        """Create title page for multi-framework comparison"""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("MULTI-FRAMEWORK COMPLIANCE ANALYSIS", self.styles['CorporateTitle']))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Strategic Certification Roadmap & Investment Analysis", self.styles['FrameworkSubtitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Company and assessment info
        elements.append(Paragraph(f"<b>Organization:</b> {company_profile.get('name', 'N/A')}", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>Frameworks Assessed:</b> {', '.join(assessment_results.keys())}", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>Assessment Date:</b> {datetime.now().strftime('%Y-%m-%d')}", self.styles['Normal']))
        
        elements.append(PageBreak())
        return elements
    
    def _create_comparison_executive_summary(self, company_profile: Dict[str, Any],
                                           assessment_results: Dict[str, Dict[str, Any]]) -> List[Any]:
        """Create executive summary for multi-framework comparison"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Calculate overall metrics
        total_frameworks = len(assessment_results)
        avg_score = sum(result.get('overall_score', 0) for result in assessment_results.values()) / total_frameworks
        ready_frameworks = sum(1 for result in assessment_results.values() if result.get('overall_score', 0) >= 75)
        
        summary_text = f"""
        This report provides a comprehensive analysis of compliance posture across {total_frameworks} frameworks, 
        offering strategic guidance for certification prioritization and investment planning.
        
        <b>Key Findings:</b><br/>
        • Average compliance score across all frameworks: {avg_score:.1f}%<br/>
        • Frameworks ready for certification: {ready_frameworks} of {total_frameworks}<br/>
        • Estimated total certification investment: {self._calculate_total_investment(assessment_results)}<br/>
        • Recommended certification timeline: {self._calculate_optimal_timeline(assessment_results)}<br/>
        """
        
        elements.append(Paragraph(summary_text, self.styles['ExecutiveSummary']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_framework_comparison_matrix(self, assessment_results: Dict[str, Dict[str, Any]]) -> List[Any]:
        """Create framework comparison matrix"""
        elements = []
        
        elements.append(Paragraph("FRAMEWORK COMPARISON MATRIX", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Create comparison table
        matrix_data = [['Framework', 'Current Score', 'Cert Readiness', 'Timeline', 'Est. Cost', 'Priority']]
        
        for framework_name, result in assessment_results.items():
            score = result.get('overall_score', 0)
            readiness = "Ready" if score >= 75 else "Developing" if score >= 60 else "Not Ready"
            roadmap = self.certification_roadmaps.get(framework_name, {})
            timeline = roadmap.get('typical_timeline', 'TBD')
            cost = roadmap.get('annual_cost_estimate', 'Varies')
            priority = self._calculate_framework_priority(framework_name, result)
            
            matrix_data.append([
                framework_name.replace('_', ' ').title(),
                f"{score:.1f}%",
                readiness,
                timeline,
                cost,
                priority
            ])
        
        matrix_table = Table(matrix_data, colWidths=[1.2*inch, 0.8*inch, 1*inch, 1*inch, 1.2*inch, 0.8*inch])
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.color_scheme["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.color_scheme["white"]),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, self.color_scheme["medium_gray"]),
        ]))
        
        elements.append(matrix_table)
        elements.append(PageBreak())
        
        return elements
    
    def _calculate_framework_priority(self, framework_name: str, result: Dict[str, Any]) -> str:
        """Calculate framework certification priority"""
        score = result.get('overall_score', 0)
        
        if score >= 75:
            return "High"
        elif score >= 60:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_total_investment(self, assessment_results: Dict[str, Dict[str, Any]]) -> str:
        """Calculate total certification investment estimate"""
        total_min = 0
        total_max = 0
        
        for framework_name in assessment_results.keys():
            roadmap = self.certification_roadmaps.get(framework_name, {})
            cost_range = roadmap.get('annual_cost_estimate', '$0 - $0')
            
            # Parse cost range (simplified)
            if '$' in cost_range and '-' in cost_range:
                try:
                    parts = cost_range.replace('$', '').replace(',', '').split(' - ')
                    min_cost = int(parts[0])
                    max_cost = int(parts[1])
                    total_min += min_cost
                    total_max += max_cost
                except:
                    pass
        
        if total_min > 0 and total_max > 0:
            return f"${total_min:,} - ${total_max:,} annually"
        else:
            return "Varies by framework selection"
    
    def _calculate_optimal_timeline(self, assessment_results: Dict[str, Dict[str, Any]]) -> str:
        """Calculate optimal certification timeline"""
        ready_count = sum(1 for result in assessment_results.values() if result.get('overall_score', 0) >= 75)
        developing_count = sum(1 for result in assessment_results.values() if 60 <= result.get('overall_score', 0) < 75)
        
        if ready_count >= 2:
            return "12-18 months for multiple certifications"
        elif ready_count >= 1:
            return "6-12 months for initial certification, 18-24 months for full suite"
        else:
            return "18-36 months for comprehensive certification program"
    
    def _create_integrated_certification_roadmap(self, assessment_results: Dict[str, Dict[str, Any]]) -> List[Any]:
        """Create integrated certification roadmap"""
        elements = []
        
        elements.append(Paragraph("INTEGRATED CERTIFICATION ROADMAP", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Sort frameworks by readiness
        sorted_frameworks = sorted(
            assessment_results.items(),
            key=lambda x: x[1].get('overall_score', 0),
            reverse=True
        )
        
        roadmap_text = """
        <b>Recommended Certification Sequence:</b><br/>
        Based on current readiness levels and strategic value, pursue certifications in the following order:
        """
        elements.append(Paragraph(roadmap_text, self.styles['ExecutiveSummary']))
        
        for i, (framework_name, result) in enumerate(sorted_frameworks, 1):
            score = result.get('overall_score', 0)
            readiness = "Ready" if score >= 75 else "Developing" if score >= 60 else "Foundational work required"
            
            phase_text = f"""
            <b>Phase {i}: {framework_name.replace('_', ' ').title()}</b><br/>
            Current Score: {score:.1f}% - {readiness}<br/>
            Strategic Value: {self._get_strategic_value_description(framework_name)}<br/>
            """
            
            elements.append(Paragraph(phase_text, self.styles['Finding']))
            elements.append(Spacer(1, 0.1*inch))
        
        elements.append(PageBreak())
        return elements
    
    def _get_strategic_value_description(self, framework_name: str) -> str:
        """Get strategic value description for framework"""
        descriptions = {
            "iso_27001": "Global recognition, comprehensive security management",
            "soc2": "Market requirement for SaaS/cloud services",
            "privacy_act": "Legal compliance requirement in Australia",
            "nist_sp_800_53": "Federal government and contractor requirements",
            "essential_eight": "Australian government and critical infrastructure"
        }
        return descriptions.get(framework_name, "Specialized compliance requirement")
    
    def _create_investment_analysis(self, assessment_results: Dict[str, Dict[str, Any]]) -> List[Any]:
        """Create investment analysis section"""
        elements = []
        
        elements.append(Paragraph("INVESTMENT ANALYSIS", self.styles['ProfessionalHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        analysis_text = """
        <b>Return on Investment Considerations:</b><br/>
        Certification investments provide multiple value streams including risk reduction, 
        market access, competitive differentiation, and operational efficiency improvements.
        
        <b>Key Benefits:</b><br/>
        • Enhanced customer trust and market credibility<br/>
        • Reduced insurance premiums and liability exposure<br/>
        • Streamlined vendor assessments and procurement processes<br/>
        • Improved operational efficiency through standardized processes<br/>
        • Competitive advantage in regulated markets<br/>
        """
        
        elements.append(Paragraph(analysis_text, self.styles['ExecutiveSummary']))
        
        return elements