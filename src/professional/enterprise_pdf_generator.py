"""
Enterprise PDF Generator - Big 4 Consulting Quality Reports
==========================================================

Generates enterprise-grade PDF reports that match Big 4 consulting standards.
Integrates executive summary, risk analysis, and professional visualization.

Author: Sentinel GRC Platform  
Version: 1.0.0-enterprise
"""

import os
import io
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, 
    Image, KeepTogether, NextPageTemplate, Frame
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.colors import HexColor

# Import our enterprise engines
from .executive_summary_engine import ExecutiveSummaryEngine, ExecutiveSummary
from .risk_analysis_engine import RiskAnalysisEngine, RiskAnalysisReport

logger = logging.getLogger(__name__)

class EnterprisePDFGenerator:
    """
    Enterprise-grade PDF generator matching Big 4 consulting quality standards
    """
    
    def __init__(self):
        self.executive_engine = ExecutiveSummaryEngine()
        self.risk_engine = RiskAnalysisEngine()
        self.styles = getSampleStyleSheet()
        self.setup_enterprise_styles()
        self.setup_color_scheme()
        
        # Professional templates by framework
        self.framework_templates = self._initialize_framework_templates()
        
        # Ensure temp directory for visualizations
        self.temp_dir = "temp/visualizations"
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def generate_enterprise_report(self,
                                 assessment_data: Dict[str, Any],
                                 framework: str,
                                 customer_context: Dict[str, Any],
                                 expert_comments: Optional[List[Dict[str, Any]]] = None,
                                 output_path: Optional[str] = None) -> str:
        """
        Generate complete enterprise-grade PDF report
        
        Args:
            assessment_data: Assessment results and findings
            framework: Compliance framework (SOC 2, ISO 27001, etc.)
            customer_context: Customer/organization context
            expert_comments: Human expert review comments
            output_path: Optional output file path
            
        Returns:
            str: Path to generated PDF file
        """
        logger.info(f"Generating enterprise PDF report for {framework}")
        
        try:
            # Generate core analysis components
            executive_summary = self.executive_engine.generate_executive_summary(
                assessment_data, framework, customer_context
            )
            risk_analysis = self.risk_engine.generate_risk_analysis(
                assessment_data, framework, customer_context
            )
            
            # Generate visualizations
            viz_paths = self._generate_visualizations(risk_analysis, executive_summary, framework)
            
            # Set output path
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                customer_name = customer_context.get('name', 'Organization').replace(' ', '_')
                output_path = f"reports/{customer_name}_{framework}_{timestamp}_enterprise.pdf"
            
            # Ensure output directory
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Build PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=1*inch,
                bottomMargin=1*inch
            )
            
            # Build story (content)
            story = []
            
            # 1. Title page
            story.extend(self._build_title_page(customer_context, framework, executive_summary, risk_analysis))
            story.append(PageBreak())
            
            # 2. Executive summary (1-2 pages)
            story.extend(self._build_executive_summary_section(executive_summary, risk_analysis))
            story.append(PageBreak())
            
            # 3. Risk analysis with visualizations
            story.extend(self._build_risk_analysis_section(risk_analysis, viz_paths))
            story.append(PageBreak())
            
            # 4. Detailed findings
            story.extend(self._build_detailed_findings_section(assessment_data, framework))
            story.append(PageBreak())
            
            # 5. Compliance matrix
            story.extend(self._build_compliance_matrix_section(risk_analysis, framework))
            story.append(PageBreak())
            
            # 6. Remediation roadmap
            story.extend(self._build_remediation_roadmap_section(executive_summary, risk_analysis))
            story.append(PageBreak())
            
            # 7. Expert comments (if provided)
            if expert_comments:
                story.extend(self._build_expert_comments_section(expert_comments))
                story.append(PageBreak())
            
            # 8. Appendices
            story.extend(self._build_appendices_section(assessment_data, framework))
            
            # Build PDF
            doc.build(story)
            
            # Cleanup temp files
            self._cleanup_temp_files(viz_paths)
            
            logger.info(f"Enterprise PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating enterprise PDF: {e}")
            raise
    
    def setup_enterprise_styles(self):
        """Setup professional Big 4 consulting styles"""
        
        # Corporate title - matches consulting firm style
        self.styles.add(ParagraphStyle(
            name='CorporateTitle',
            parent=self.styles['Title'],
            fontSize=32,
            textColor=HexColor('#0B3D91'),  # Deep professional blue
            alignment=TA_CENTER,
            spaceAfter=36,
            spaceBefore=24,
            fontName='Helvetica-Bold',
            letterSpacing=1
        ))
        
        # Framework subtitle
        self.styles.add(ParagraphStyle(
            name='FrameworkSubtitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#1565C0'),
            alignment=TA_CENTER,
            spaceAfter=24,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Executive summary style - critical for C-suite
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_JUSTIFY,
            spaceAfter=14,
            spaceBefore=8,
            leftIndent=0,
            rightIndent=0,
            lineSpacing=1.3,
            fontName='Helvetica'
        ))
        
        # Professional section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#0B3D91'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            keepWithNext=1
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#1565C0'),
            spaceAfter=8,
            spaceBefore=16,
            fontName='Helvetica-Bold',
            keepWithNext=1
        ))
        
        # Key finding style
        self.styles.add(ParagraphStyle(
            name='KeyFinding',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=4,
            leftIndent=20,
            bulletIndent=12,
            fontName='Helvetica',
            textColor=HexColor('#2E2E2E')
        ))
        
        # Risk finding - critical
        self.styles.add(ParagraphStyle(
            name='CriticalFinding',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=4,
            leftIndent=20,
            fontName='Helvetica-Bold',
            textColor=HexColor('#C62828')
        ))
        
        # Recommendation style
        self.styles.add(ParagraphStyle(
            name='Recommendation',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            spaceBefore=6,
            leftIndent=16,
            fontName='Helvetica',
            textColor=HexColor('#2E7D32')
        ))
        
        # Business impact highlight
        self.styles.add(ParagraphStyle(
            name='BusinessImpact',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            spaceBefore=8,
            leftIndent=24,
            rightIndent=24,
            fontName='Helvetica-Bold',
            textColor=HexColor('#1565C0'),
            backColor=HexColor('#F5F9FF'),
            borderPadding=8
        ))
        
        # Expert comment style
        self.styles.add(ParagraphStyle(
            name='ExpertComment',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            spaceBefore=4,
            leftIndent=12,
            rightIndent=12,
            fontName='Helvetica-Oblique',
            textColor=HexColor('#424242'),
            backColor=HexColor('#FAFAFA'),
            borderPadding=6
        ))
    
    def setup_color_scheme(self):
        """Setup professional color scheme"""
        self.colors = {
            # Primary brand colors
            'primary_blue': HexColor('#0B3D91'),
            'secondary_blue': HexColor('#1565C0'),
            'accent_blue': HexColor('#2196F3'),
            
            # Status colors
            'success_green': HexColor('#2E7D32'),
            'warning_orange': HexColor('#F57C00'),
            'critical_red': HexColor('#C62828'),
            'info_blue': HexColor('#1976D2'),
            
            # Neutral colors
            'dark_gray': HexColor('#424242'),
            'medium_gray': HexColor('#757575'),
            'light_gray': HexColor('#E0E0E0'),
            'background_gray': HexColor('#FAFAFA'),
            
            # Risk matrix colors
            'risk_low': HexColor('#4CAF50'),
            'risk_medium': HexColor('#FF9800'),
            'risk_high': HexColor('#F44336'),
            'risk_critical': HexColor('#B71C1C')
        }
    
    def _build_title_page(self, customer_context: Dict[str, Any], 
                         framework: str, executive_summary: ExecutiveSummary,
                         risk_analysis: RiskAnalysisReport) -> List:
        """Build professional title page"""
        content = []
        
        # Main title
        title_text = f"{framework} Compliance Assessment Report"
        content.append(Paragraph(title_text, self.styles['CorporateTitle']))
        content.append(Spacer(1, 0.5*inch))
        
        # Customer name
        customer_name = customer_context.get('name', 'Organization')
        content.append(Paragraph(customer_name, self.styles['FrameworkSubtitle']))
        content.append(Spacer(1, 0.3*inch))
        
        # Assessment summary box
        summary_data = [
            ['Assessment Date', datetime.now().strftime('%B %d, %Y')],
            ['Framework Standard', framework],
            ['Compliance Score', f"{executive_summary.compliance_score}%"],
            ['Overall Risk Level', risk_analysis.risk_level.value.title()],
            ['Industry Sector', customer_context.get('industry', 'Technology')],
            ['Report Version', '1.0']
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['background_gray']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['dark_gray']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['light_gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        content.append(Spacer(1, 0.5*inch))
        content.append(summary_table)
        content.append(Spacer(1, 0.5*inch))
        
        # Professional disclaimer
        disclaimer = """
        <b>CONFIDENTIAL</b><br/>
        This report contains confidential and proprietary information. It is intended solely for the use of 
        the organization named above and should not be distributed to unauthorized parties. The assessment 
        was conducted using industry-standard methodologies and represents the security posture at the time 
        of evaluation. This report is designed to support management decision-making and compliance 
        certification efforts.
        """
        content.append(Paragraph(disclaimer, self.styles['Normal']))
        
        # Footer with branding
        content.append(Spacer(1, 1*inch))
        footer_text = """
        <b>Generated by Sentinel GRC Enterprise Platform</b><br/>
        Professional Compliance Assessment and Risk Management<br/>
        Report ID: {report_id}
        """.format(report_id=f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        
        content.append(Paragraph(footer_text, self.styles['Normal']))
        
        return content
    
    def _build_executive_summary_section(self, executive_summary: ExecutiveSummary, 
                                       risk_analysis: RiskAnalysisReport) -> List:
        """Build executive summary section"""
        content = []
        
        # Section header
        content.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        # Assessment overview
        content.append(Paragraph("Assessment Overview", self.styles['SubsectionHeading']))
        content.append(Paragraph(executive_summary.assessment_overview, self.styles['ExecutiveSummary']))
        content.append(Spacer(1, 0.15*inch))
        
        # Key metrics table
        metrics_data = [
            ['Metric', 'Current State', 'Target State', 'Gap Analysis'],
            ['Overall Compliance', f"{executive_summary.compliance_score}%", "95%", 
             f"{95 - executive_summary.compliance_score}% gap"],
            ['Risk Score', f"{risk_analysis.overall_risk_score:.1f}/10", "≤3.0/10", 
             f"{max(0, risk_analysis.overall_risk_score - 3.0):.1f} excess risk"],
            ['Critical Findings', str(len([f for f in executive_summary.key_findings if 'critical' in f.lower()])), 
             "0", "Immediate attention required"],
            ['Estimated Timeline', executive_summary.business_impact.certification_timeline, 
             "Target timeline", "Based on current resources"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 2*inch])
        metrics_table.setStyle(self._get_professional_table_style())
        content.append(metrics_table)
        content.append(Spacer(1, 0.2*inch))
        
        # Key findings
        content.append(Paragraph("Key Findings", self.styles['SubsectionHeading']))
        for i, finding in enumerate(executive_summary.key_findings, 1):
            finding_text = f"{i}. {finding}"
            style = self.styles['CriticalFinding'] if 'critical' in finding.lower() else self.styles['KeyFinding']
            content.append(Paragraph(finding_text, style))
        content.append(Spacer(1, 0.15*inch))
        
        # Business impact highlight
        content.append(Paragraph("Business Impact Analysis", self.styles['SubsectionHeading']))
        
        impact_text = f"""
        <b>Financial Impact:</b> {executive_summary.business_impact.current_risk_exposure}<br/>
        <b>Investment Required:</b> {executive_summary.business_impact.remediation_investment}<br/>
        <b>ROI Timeline:</b> {executive_summary.business_impact.roi_timeline}<br/>
        <b>Competitive Advantage:</b> {executive_summary.business_impact.competitive_advantage}
        """
        content.append(Paragraph(impact_text, self.styles['BusinessImpact']))
        content.append(Spacer(1, 0.2*inch))
        
        # Strategic recommendations
        content.append(Paragraph("Strategic Recommendations", self.styles['SubsectionHeading']))
        for i, rec in enumerate(executive_summary.strategic_recommendations[:3], 1):  # Top 3
            rec_text = f"""
            <b>{i}. {rec.title}</b><br/>
            {rec.description}<br/>
            <i>Business Rationale:</i> {rec.business_rationale}<br/>
            <i>Timeline:</i> {rec.timeline} | <i>Investment:</i> {rec.investment}
            """
            content.append(Paragraph(rec_text, self.styles['Recommendation']))
            content.append(Spacer(1, 0.1*inch))
        
        # Critical actions
        content.append(Paragraph("Immediate Actions Required", self.styles['SubsectionHeading']))
        for action in executive_summary.critical_actions:
            content.append(Paragraph(f"• {action}", self.styles['CriticalFinding']))
        
        return content
    
    def _build_risk_analysis_section(self, risk_analysis: RiskAnalysisReport, 
                                   viz_paths: Dict[str, str]) -> List:
        """Build risk analysis section with visualizations"""
        content = []
        
        # Section header
        content.append(Paragraph("Risk Analysis", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        # Overall risk assessment
        content.append(Paragraph("Overall Risk Assessment", self.styles['SubsectionHeading']))
        
        risk_text = f"""
        The organization's overall risk score is <b>{risk_analysis.overall_risk_score:.1f}/10</b>, 
        indicating a <b>{risk_analysis.risk_level.value.upper()}</b> risk level. This assessment is based on 
        comprehensive analysis of {len(risk_analysis.risk_metrics)} risk categories using industry-standard 
        methodologies. The residual risk after planned mitigations is projected to be 
        <b>{risk_analysis.residual_risk_assessment['residual_risk']:.1f}/10</b>.
        """
        content.append(Paragraph(risk_text, self.styles['ExecutiveSummary']))
        content.append(Spacer(1, 0.15*inch))
        
        # Risk heat map
        if 'heat_map' in viz_paths:
            content.append(Paragraph("Risk Heat Map", self.styles['SubsectionHeading']))
            try:
                heat_map = Image(viz_paths['heat_map'], width=6*inch, height=4*inch)
                content.append(heat_map)
                content.append(Spacer(1, 0.1*inch))
            except Exception as e:
                logger.warning(f"Could not include heat map: {e}")
        
        # Risk metrics by category
        content.append(Paragraph("Risk Metrics by Category", self.styles['SubsectionHeading']))
        
        risk_data = [['Category', 'Current Risk', 'Target Risk', 'Priority', 'Investment', 'Timeline']]
        for metric in risk_analysis.risk_metrics:
            risk_data.append([
                metric.category,
                f"{metric.current_score:.1f}/10",
                f"{metric.target_score:.1f}/10", 
                str(metric.mitigation_priority),
                f"${metric.cost_to_remediate:,}",
                f"{metric.timeline_weeks} weeks"
            ])
        
        risk_table = Table(risk_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 0.6*inch, 1*inch, 0.8*inch])
        risk_table.setStyle(self._get_professional_table_style())
        content.append(risk_table)
        content.append(Spacer(1, 0.2*inch))
        
        # Industry benchmarking
        if risk_analysis.benchmarking_data:
            content.append(Paragraph("Industry Benchmarking", self.styles['SubsectionHeading']))
            
            bench_data = risk_analysis.benchmarking_data
            benchmark_text = f"""
            Compared to the <b>{bench_data['industry']}</b> industry average:
            • Compliance: <b>{bench_data['current_compliance']}%</b> vs industry average <b>{bench_data['industry_avg_compliance']}%</b>
            • Risk Score: <b>{bench_data['current_risk']:.1f}</b> vs industry average <b>{bench_data['industry_avg_risk']:.1f}</b>
            • Industry Percentile: <b>{bench_data['percentile_ranking']}th percentile</b>
            """
            content.append(Paragraph(benchmark_text, self.styles['ExecutiveSummary']))
        
        return content
    
    def _build_detailed_findings_section(self, assessment_data: Dict[str, Any], framework: str) -> List:
        """Build detailed findings section"""
        content = []
        
        # Section header
        content.append(Paragraph("Detailed Findings", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        findings = assessment_data.get('findings', [])
        if not findings:
            content.append(Paragraph("No specific findings documented in assessment data.", 
                                   self.styles['Normal']))
            return content
        
        # Group findings by severity
        severity_groups = {}
        for finding in findings:
            severity = finding.get('severity', 'medium').lower()
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(finding)
        
        # Display findings by severity (critical first)
        severity_order = ['critical', 'high', 'medium', 'low']
        
        for severity in severity_order:
            if severity in severity_groups:
                # Severity section
                severity_title = f"{severity.title()} Risk Findings"
                content.append(Paragraph(severity_title, self.styles['SubsectionHeading']))
                
                findings_data = [['Finding', 'Description', 'Impact', 'Recommendation']]
                
                for finding in severity_groups[severity]:
                    findings_data.append([
                        finding.get('title', 'Security Finding'),
                        finding.get('description', 'Security vulnerability identified'),
                        finding.get('business_impact', 'Operational risk'),
                        finding.get('recommendation', 'Implement security controls')
                    ])
                
                findings_table = Table(findings_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
                findings_table.setStyle(self._get_professional_table_style())
                content.append(findings_table)
                content.append(Spacer(1, 0.15*inch))
        
        return content
    
    def _build_compliance_matrix_section(self, risk_analysis: RiskAnalysisReport, framework: str) -> List:
        """Build compliance matrix section"""
        content = []
        
        # Section header
        content.append(Paragraph("Compliance Matrix", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        matrix = risk_analysis.compliance_matrix
        
        # Build compliance matrix table
        matrix_data = [['Control Category'] + matrix.frameworks]
        
        for i, category in enumerate(matrix.control_categories):
            row = [category]
            if i < len(matrix.compliance_scores):
                for score_list in matrix.compliance_scores[i]:
                    row.append(f"{score_list}%")
            else:
                row.extend(['N/A'] * len(matrix.frameworks))
            matrix_data.append(row)
        
        compliance_table = Table(matrix_data, colWidths=[2.5*inch] + [1.5*inch] * len(matrix.frameworks))
        
        # Color code the compliance scores
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary_blue']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['light_gray']),
        ]
        
        # Add color coding for compliance scores
        for i in range(1, len(matrix_data)):
            for j in range(1, len(matrix_data[i])):
                try:
                    score = int(matrix_data[i][j].replace('%', ''))
                    if score >= 90:
                        bg_color = self.colors['success_green']
                    elif score >= 70:
                        bg_color = self.colors['warning_orange']
                    else:
                        bg_color = self.colors['critical_red']
                    
                    table_style.append(('BACKGROUND', (j, i), (j, i), bg_color))
                    table_style.append(('TEXTCOLOR', (j, i), (j, i), colors.white))
                except (ValueError, AttributeError):
                    pass
        
        compliance_table.setStyle(TableStyle(table_style))
        content.append(compliance_table)
        content.append(Spacer(1, 0.2*inch))
        
        # Legend
        legend_text = """
        <b>Compliance Score Legend:</b><br/>
        • 90-100%: Compliant (Green) - Minor gaps, certification ready<br/>
        • 70-89%: Partially Compliant (Orange) - Moderate gaps, remediation needed<br/>
        • 0-69%: Non-Compliant (Red) - Significant gaps, major remediation required
        """
        content.append(Paragraph(legend_text, self.styles['Normal']))
        
        return content
    
    def _build_remediation_roadmap_section(self, executive_summary: ExecutiveSummary, 
                                         risk_analysis: RiskAnalysisReport) -> List:
        """Build remediation roadmap section"""
        content = []
        
        # Section header
        content.append(Paragraph("Remediation Roadmap", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        # Prioritized recommendations
        content.append(Paragraph("Implementation Priority Matrix", self.styles['SubsectionHeading']))
        
        # Create roadmap table from strategic recommendations
        roadmap_data = [['Phase', 'Initiative', 'Timeline', 'Investment', 'Expected Outcome']]
        
        for i, rec in enumerate(executive_summary.strategic_recommendations, 1):
            phase = f"Phase {i}"
            roadmap_data.append([
                phase,
                rec.title,
                rec.timeline,
                rec.investment,
                rec.expected_outcome
            ])
        
        roadmap_table = Table(roadmap_data, colWidths=[0.8*inch, 2*inch, 1*inch, 1*inch, 2.2*inch])
        roadmap_table.setStyle(self._get_professional_table_style())
        content.append(roadmap_table)
        content.append(Spacer(1, 0.2*inch))
        
        # Timeline visualization would go here (if implemented)
        
        # Next steps
        content.append(Paragraph("Immediate Next Steps", self.styles['SubsectionHeading']))
        for i, step in enumerate(executive_summary.next_steps, 1):
            content.append(Paragraph(f"{i}. {step}", self.styles['Normal']))
        
        return content
    
    def _build_expert_comments_section(self, expert_comments: List[Dict[str, Any]]) -> List:
        """Build expert comments section"""
        content = []
        
        # Section header
        content.append(Paragraph("Expert Review Comments", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        for comment in expert_comments:
            # Comment header
            reviewer = comment.get('reviewer_name', 'Expert Reviewer')
            section = comment.get('section', 'General')
            timestamp = comment.get('timestamp', datetime.now().isoformat())
            
            header_text = f"<b>{reviewer}</b> - {section} ({timestamp})"
            content.append(Paragraph(header_text, self.styles['SubsectionHeading']))
            
            # Comment text
            comment_text = comment.get('comment_text', 'No comment provided')
            content.append(Paragraph(comment_text, self.styles['ExpertComment']))
            content.append(Spacer(1, 0.1*inch))
        
        return content
    
    def _build_appendices_section(self, assessment_data: Dict[str, Any], framework: str) -> List:
        """Build appendices section"""
        content = []
        
        # Section header
        content.append(Paragraph("Appendices", self.styles['SectionHeading']))
        content.append(Spacer(1, 0.2*inch))
        
        # Appendix A: Methodology
        content.append(Paragraph("Appendix A: Assessment Methodology", self.styles['SubsectionHeading']))
        methodology_text = f"""
        This assessment was conducted using industry-standard methodologies aligned with {framework} requirements.
        The evaluation included:
        • Document review and policy analysis
        • Technical control testing and validation
        • Interview with key personnel
        • Risk assessment and gap analysis
        • Industry benchmarking and best practice comparison
        
        The assessment scope covered all applicable {framework} controls and requirements relevant to the 
        organization's environment and business objectives.
        """
        content.append(Paragraph(methodology_text, self.styles['Normal']))
        content.append(Spacer(1, 0.15*inch))
        
        # Appendix B: Control details (sample)
        content.append(Paragraph("Appendix B: Control Assessment Summary", self.styles['SubsectionHeading']))
        
        controls = assessment_data.get('controls', [])
        if controls:
            control_data = [['Control ID', 'Description', 'Status', 'Criticality']]
            for control in controls[:10]:  # Limit to first 10 for space
                control_data.append([
                    control.get('id', 'N/A'),
                    control.get('description', 'Control description'),
                    control.get('status', 'Unknown'),
                    control.get('criticality', 'Medium')
                ])
            
            control_table = Table(control_data, colWidths=[1*inch, 3*inch, 1*inch, 1*inch])
            control_table.setStyle(self._get_professional_table_style())
            content.append(control_table)
        
        return content
    
    def _generate_visualizations(self, risk_analysis: RiskAnalysisReport, 
                               executive_summary: ExecutiveSummary, framework: str) -> Dict[str, str]:
        """Generate all visualization files"""
        viz_paths = {}
        
        try:
            # Risk heat map
            heat_map_path = os.path.join(self.temp_dir, f"risk_heatmap_{framework}.png")
            self._create_risk_heat_map(risk_analysis.heat_map_data, heat_map_path)
            viz_paths['heat_map'] = heat_map_path
            
            # Compliance trend chart
            trend_path = os.path.join(self.temp_dir, f"compliance_trend_{framework}.png")
            self._create_compliance_trend_chart(risk_analysis.trend_analysis, trend_path)
            viz_paths['trend'] = trend_path
            
            # Risk metrics chart
            metrics_path = os.path.join(self.temp_dir, f"risk_metrics_{framework}.png")
            self._create_risk_metrics_chart(risk_analysis.risk_metrics, metrics_path)
            viz_paths['metrics'] = metrics_path
            
        except Exception as e:
            logger.warning(f"Error generating visualizations: {e}")
        
        return viz_paths
    
    def _create_risk_heat_map(self, heat_map_data, output_path: str):
        """Create risk heat map visualization"""
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Create 5x5 risk matrix
            risk_matrix = np.zeros((5, 5))
            
            # Populate matrix with risk items
            for item in heat_map_data.risk_items:
                likelihood = item.get('likelihood', 3) - 1  # Convert to 0-4
                impact = item.get('impact', 3) - 1
                risk_matrix[4-impact, likelihood] += 1  # Flip impact axis
            
            # Create heat map
            sns.heatmap(risk_matrix, 
                       annot=True, 
                       fmt='g',
                       xticklabels=heat_map_data.likelihood_axis,
                       yticklabels=list(reversed(heat_map_data.impact_axis)),
                       cmap='RdYlGn_r',
                       cbar_kws={'label': 'Number of Risk Items'})
            
            plt.title('Risk Heat Map - Likelihood vs Impact')
            plt.xlabel('Likelihood')
            plt.ylabel('Impact')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Error creating risk heat map: {e}")
    
    def _create_compliance_trend_chart(self, trend_data: Dict[str, Any], output_path: str):
        """Create compliance trend chart"""
        try:
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Sample trend data
            months = ['Current', '3 Months', '6 Months', '12 Months']
            compliance_scores = [
                60,  # Current
                trend_data.get('projected_compliance', {}).get('3_months', 75),
                trend_data.get('projected_compliance', {}).get('6_months', 85),
                trend_data.get('projected_compliance', {}).get('12_months', 95)
            ]
            
            plt.plot(months, compliance_scores, marker='o', linewidth=3, markersize=8)
            plt.axhline(y=95, color='green', linestyle='--', label='Certification Target')
            plt.axhline(y=70, color='orange', linestyle='--', label='Baseline Compliance')
            
            plt.title('Projected Compliance Improvement Timeline')
            plt.ylabel('Compliance Score (%)')
            plt.xlabel('Timeline')
            plt.ylim(0, 100)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Error creating compliance trend chart: {e}")
    
    def _create_risk_metrics_chart(self, risk_metrics: List, output_path: str):
        """Create risk metrics comparison chart"""
        try:
            if not risk_metrics:
                return
                
            fig, ax = plt.subplots(figsize=(10, 6))
            
            categories = [m.category for m in risk_metrics]
            current_scores = [m.current_score for m in risk_metrics]
            target_scores = [m.target_score for m in risk_metrics]
            
            x = np.arange(len(categories))
            width = 0.35
            
            plt.bar(x - width/2, current_scores, width, label='Current Risk', color='lightcoral')
            plt.bar(x + width/2, target_scores, width, label='Target Risk', color='lightgreen')
            
            plt.xlabel('Risk Categories')
            plt.ylabel('Risk Score (1-10)')
            plt.title('Risk Metrics by Category - Current vs Target')
            plt.xticks(x, categories, rotation=45)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Error creating risk metrics chart: {e}")
    
    def _get_professional_table_style(self) -> TableStyle:
        """Get professional table styling"""
        return TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary_blue']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Body styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.colors['dark_gray']),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['light_gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
    
    def _cleanup_temp_files(self, viz_paths: Dict[str, str]):
        """Clean up temporary visualization files"""
        for path in viz_paths.values():
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                logger.warning(f"Could not clean up temp file {path}: {e}")
    
    def _initialize_framework_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize framework-specific templates"""
        return {
            "SOC 2": {
                "title_suffix": "Type II Examination Report",
                "focus_areas": ["Security", "Availability", "Confidentiality"],
                "certification_body": "AICPA SOC 2 Standards"
            },
            "ISO 27001": {
                "title_suffix": "ISMS Assessment Report", 
                "focus_areas": ["Information Security Management", "Risk Management", "Continuous Improvement"],
                "certification_body": "ISO/IEC 27001:2022"
            },
            "NIST CSF": {
                "title_suffix": "Cybersecurity Framework Assessment",
                "focus_areas": ["Identify", "Protect", "Detect", "Respond", "Recover"],
                "certification_body": "NIST Cybersecurity Framework 2.0"
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Sample data for testing
    sample_assessment = {
        "controls": [
            {"id": "AC-1", "status": "implemented", "criticality": "high", "category": "access_control"},
            {"id": "AC-2", "status": "partial", "criticality": "medium", "category": "access_control"},
            {"id": "AU-1", "status": "not_implemented", "criticality": "high", "category": "audit"}
        ],
        "findings": [
            {"title": "Multi-factor authentication gaps", "severity": "critical", 
             "description": "MFA not implemented across all systems", "business_impact": "high"},
            {"title": "Log retention policy", "severity": "medium",
             "description": "Insufficient log retention periods", "business_impact": "medium"}
        ]
    }
    
    customer_context = {
        "name": "TechCorp Inc",
        "industry": "technology",
        "size": "medium"
    }
    
    expert_comments = [
        {
            "reviewer_name": "John Smith, CISSP",
            "section": "Access Controls",
            "comment_text": "Recommend implementing privileged access management solution for enhanced security.",
            "timestamp": "2025-08-16T10:30:00"
        }
    ]
    
    # Generate enterprise report
    generator = EnterprisePDFGenerator()
    
    try:
        output_path = generator.generate_enterprise_report(
            assessment_data=sample_assessment,
            framework="SOC 2",
            customer_context=customer_context,
            expert_comments=expert_comments
        )
        print(f"Enterprise PDF generated: {output_path}")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()