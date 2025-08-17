#!/usr/bin/env python3
"""
SentinelGRC Executive Dashboard
The GRC Head of Cerberus AI - Strategic oversight for compliance professionals
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import numpy as np
from typing import Dict, List, Any
import time

# Configure Streamlit page
st.set_page_config(
    page_title="SentinelGRC Executive Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional GRC styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .risk-critical { border-left-color: #EF4444 !important; }
    .risk-high { border-left-color: #F97316 !important; }
    .risk-medium { border-left-color: #F59E0B !important; }
    .risk-low { border-left-color: #10B981 !important; }
    
    .executive-summary {
        background: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
    }
    
    .framework-badge {
        display: inline-block;
        background: #10B981;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        margin-right: 0.5rem;
        margin-bottom: 0.25rem;
    }
    
    .human-review-alert {
        background: #FEF3C7;
        border: 1px solid #F59E0B;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .compliance-score {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
    }
    
    .score-excellent { color: #10B981; }
    .score-good { color: #059669; }
    .score-fair { color: #F59E0B; }
    .score-poor { color: #EF4444; }
</style>
""", unsafe_allow_html=True)

class GRCExecutiveDashboard:
    """Main GRC Executive Dashboard Class"""
    
    def __init__(self):
        self.initialize_session_state()
        self.load_sample_data()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'dashboard_initialized' not in st.session_state:
            st.session_state.dashboard_initialized = True
            st.session_state.selected_frameworks = ['Essential 8', 'NIST CSF', 'SOC 2']
            st.session_state.time_period = '30 days'
            st.session_state.auto_refresh = True
    
    def load_sample_data(self):
        """Load sample compliance data for demonstration"""
        
        # Overall compliance metrics
        self.compliance_summary = {
            'overall_score': 87,
            'trend': '+5%',
            'total_controls': 156,
            'compliant_controls': 136,
            'violations': 20,
            'human_reviews_pending': 8,
            'frameworks_covered': 7,
            'last_assessment': '2025-08-13 14:30:00'
        }
        
        # Framework-specific data
        self.framework_data = [
            {'framework': 'Essential 8', 'score': 92, 'controls': 45, 'compliant': 41, 'violations': 4, 'trend': '+3%', 'status': 'Excellent'},
            {'framework': 'NIST CSF', 'score': 89, 'controls': 52, 'compliant': 46, 'violations': 6, 'trend': '+7%', 'status': 'Good'},
            {'framework': 'SOC 2', 'score': 85, 'controls': 38, 'compliant': 32, 'violations': 6, 'trend': '+2%', 'status': 'Good'},
            {'framework': 'GDPR', 'score': 78, 'controls': 21, 'compliant': 16, 'violations': 5, 'trend': '-2%', 'status': 'Fair'},
            {'framework': 'ISO 27001', 'score': 82, 'controls': 35, 'compliant': 29, 'violations': 6, 'trend': '+4%', 'status': 'Good'},
            {'framework': 'PCI DSS', 'score': 91, 'controls': 28, 'compliant': 25, 'violations': 3, 'trend': '+1%', 'status': 'Excellent'},
            {'framework': 'HIPAA', 'score': 88, 'controls': 24, 'compliant': 21, 'violations': 3, 'trend': '+6%', 'status': 'Good'}
        ]
        
        # Risk register data
        self.risk_data = [
            {'id': 'RISK-001', 'title': 'Unpatched Critical Vulnerability', 'severity': 'Critical', 'framework': 'Essential 8', 'status': 'Open', 'owner': 'Security Team', 'due_date': '2025-08-15', 'human_review': True},
            {'id': 'RISK-002', 'title': 'Data Retention Policy Gap', 'severity': 'High', 'framework': 'GDPR', 'status': 'In Progress', 'owner': 'Legal Team', 'due_date': '2025-08-20', 'human_review': True},
            {'id': 'RISK-003', 'title': 'Access Control Documentation', 'severity': 'Medium', 'framework': 'SOC 2', 'status': 'Open', 'owner': 'IT Team', 'due_date': '2025-08-25', 'human_review': False},
            {'id': 'RISK-004', 'title': 'Incident Response Plan Update', 'severity': 'Medium', 'framework': 'NIST CSF', 'status': 'Open', 'owner': 'CISO', 'due_date': '2025-08-30', 'human_review': True},
            {'id': 'RISK-005', 'title': 'Vendor Risk Assessment', 'severity': 'High', 'framework': 'SOC 2', 'status': 'In Progress', 'owner': 'Procurement', 'due_date': '2025-09-01', 'human_review': True}
        ]
        
        # Audit trail data
        self.audit_data = [
            {'timestamp': '2025-08-13 14:30:00', 'event': 'Compliance Assessment Completed', 'framework': 'Essential 8', 'score': 92, 'user': 'System', 'details': 'Automated assessment via DevOps pipeline'},
            {'timestamp': '2025-08-13 13:45:00', 'event': 'Human Review Required', 'framework': 'GDPR', 'score': 78, 'user': 'AI System', 'details': 'Complex data processing scenario detected'},
            {'timestamp': '2025-08-13 12:20:00', 'event': 'Risk Accepted', 'framework': 'SOC 2', 'score': 85, 'user': 'J. Smith (GRC Manager)', 'details': 'Temporary exception approved for legacy system'},
            {'timestamp': '2025-08-13 11:15:00', 'event': 'Violation Remediated', 'framework': 'NIST CSF', 'score': 89, 'user': 'DevOps Team', 'details': 'Security control gap closed via automation'},
            {'timestamp': '2025-08-13 10:30:00', 'event': 'Framework Update', 'framework': 'ISO 27001', 'score': 82, 'user': 'System', 'details': 'Control library updated to latest version'}
        ]
        
        # DevOps integration metrics
        self.devops_metrics = {
            'pipelines_monitored': 47,
            'deployments_this_week': 156,
            'compliance_checks_passed': 142,
            'compliance_checks_failed': 14,
            'human_escalations': 8,
            'average_check_time': '23 seconds'
        }
    
    def render_header(self):
        """Render the main dashboard header"""
        st.markdown("""
        <div class="main-header">
            <h1>🛡️ SentinelGRC Executive Dashboard</h1>
            <p>AI-Powered Compliance Intelligence • Human Expertise Amplified</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_executive_summary(self):
        """Render executive summary section"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Overall compliance score
        with col1:
            score_class = self.get_score_class(self.compliance_summary['overall_score'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>Overall Compliance</h3>
                <div class="compliance-score {score_class}">
                    {self.compliance_summary['overall_score']}%
                </div>
                <p>↗️ {self.compliance_summary['trend']} vs last month</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Controls status
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Controls Status</h3>
                <h2>{self.compliance_summary['compliant_controls']}/{self.compliance_summary['total_controls']}</h2>
                <p>Controls Compliant</p>
                <small>{self.compliance_summary['violations']} violations to address</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Human reviews pending
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Expert Reviews</h3>
                <h2>{self.compliance_summary['human_reviews_pending']}</h2>
                <p>Pending Human Review</p>
                <small>Strategic decisions requiring expertise</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Framework coverage
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Framework Coverage</h3>
                <h2>{self.compliance_summary['frameworks_covered']}</h2>
                <p>Active Frameworks</p>
                <small>Last updated: {self.compliance_summary['last_assessment'][:10]}</small>
            </div>
            """, unsafe_allow_html=True)
    
    def render_framework_performance(self):
        """Render framework performance section"""
        st.markdown("## 📊 Framework Performance Overview")
        
        # Create DataFrame for easier manipulation
        df_frameworks = pd.DataFrame(self.framework_data)
        
        # Framework scores chart
        fig_scores = px.bar(
            df_frameworks, 
            x='framework', 
            y='score',
            color='score',
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981'],
            title="Compliance Scores by Framework"
        )
        fig_scores.update_layout(showlegend=False, height=400)
        fig_scores.update_coloraxes(showscale=False)
        
        st.plotly_chart(fig_scores, use_container_width=True)
        
        # Framework details table
        st.markdown("### Framework Details")
        
        # Format the data for display
        display_data = []
        for framework in self.framework_data:
            status_emoji = {"Excellent": "🟢", "Good": "🟡", "Fair": "🟠", "Poor": "🔴"}
            display_data.append({
                "Framework": f"<span class='framework-badge'>{framework['framework']}</span>",
                "Score": f"{framework['score']}%",
                "Status": f"{status_emoji.get(framework['status'], '⚪')} {framework['status']}",
                "Controls": f"{framework['compliant']}/{framework['controls']}",
                "Violations": framework['violations'],
                "Trend": framework['trend']
            })
        
        # Create DataFrame and display as HTML table
        df_display = pd.DataFrame(display_data)
        st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    def render_risk_register(self):
        """Render risk register section"""
        st.markdown("## ⚠️ Risk Register & Human Review Queue")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        with col1:
            severity_filter = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Closed"])
        with col3:
            human_review_filter = st.selectbox("Human Review Required", ["All", "Yes", "No"])
        
        # Filter data
        filtered_risks = self.risk_data.copy()
        if severity_filter != "All":
            filtered_risks = [r for r in filtered_risks if r['severity'] == severity_filter]
        if status_filter != "All":
            filtered_risks = [r for r in filtered_risks if r['status'] == status_filter]
        if human_review_filter == "Yes":
            filtered_risks = [r for r in filtered_risks if r['human_review']]
        elif human_review_filter == "No":
            filtered_risks = [r for r in filtered_risks if not r['human_review']]
        
        # Risk summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        critical_risks = len([r for r in filtered_risks if r['severity'] == 'Critical'])
        high_risks = len([r for r in filtered_risks if r['severity'] == 'High'])
        human_review_risks = len([r for r in filtered_risks if r['human_review']])
        overdue_risks = len([r for r in filtered_risks if datetime.strptime(r['due_date'], '%Y-%m-%d') < datetime.now()])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card risk-critical">
                <h3>Critical Risks</h3>
                <h2>{critical_risks}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card risk-high">
                <h3>High Risks</h3>
                <h2>{high_risks}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Require Human Review</h3>
                <h2>{human_review_risks}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card risk-high">
                <h3>Overdue</h3>
                <h2>{overdue_risks}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk details table
        st.markdown("### Risk Details")
        
        for risk in filtered_risks[:10]:  # Show top 10 risks
            severity_class = f"risk-{risk['severity'].lower()}"
            human_review_indicator = "👥 " if risk['human_review'] else ""
            
            st.markdown(f"""
            <div class="metric-card {severity_class}">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div style="flex-grow: 1;">
                        <h4>{human_review_indicator}{risk['title']}</h4>
                        <p><strong>Framework:</strong> {risk['framework']} | 
                           <strong>Severity:</strong> {risk['severity']} | 
                           <strong>Status:</strong> {risk['status']}</p>
                        <p><strong>Owner:</strong> {risk['owner']} | 
                           <strong>Due:</strong> {risk['due_date']}</p>
                    </div>
                    <div style="text-align: right;">
                        <button style="background: #10B981; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;">
                            Review
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_devops_integration(self):
        """Render DevOps integration metrics"""
        st.markdown("## 🚀 DevOps Integration Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Pipeline Monitoring")
            
            # Pipeline metrics
            metrics_data = [
                ("Monitored Pipelines", self.devops_metrics['pipelines_monitored'], "🔍"),
                ("Deployments This Week", self.devops_metrics['deployments_this_week'], "🚀"),
                ("Checks Passed", self.devops_metrics['compliance_checks_passed'], "✅"),
                ("Checks Failed", self.devops_metrics['compliance_checks_failed'], "❌"),
                ("Human Escalations", self.devops_metrics['human_escalations'], "👥"),
            ]
            
            for metric, value, icon in metrics_data:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; border-bottom: 1px solid #E2E8F0;">
                    <span>{icon} {metric}</span>
                    <strong>{value}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Performance Metrics")
            
            # Success rate calculation
            total_checks = self.devops_metrics['compliance_checks_passed'] + self.devops_metrics['compliance_checks_failed']
            success_rate = (self.devops_metrics['compliance_checks_passed'] / total_checks * 100) if total_checks > 0 else 0
            
            # Create donut chart for success rate
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Passed', 'Failed'],
                values=[self.devops_metrics['compliance_checks_passed'], self.devops_metrics['compliance_checks_failed']],
                hole=.6,
                marker_colors=['#10B981', '#EF4444']
            )])
            
            fig_donut.update_layout(
                title="Compliance Check Success Rate",
                annotations=[dict(text=f'{success_rate:.1f}%', x=0.5, y=0.5, font_size=24, showarrow=False)],
                height=300,
                showlegend=True
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
            
            st.metric("Average Check Time", self.devops_metrics['average_check_time'], "⚡")
    
    def render_human_intelligence_section(self):
        """Render human intelligence and AI collaboration section"""
        st.markdown("## 🧠 Human Intelligence & AI Collaboration")
        
        # Human review alert
        if self.compliance_summary['human_reviews_pending'] > 0:
            st.markdown(f"""
            <div class="human-review-alert">
                <h4>👥 {self.compliance_summary['human_reviews_pending']} items require your expertise</h4>
                <p>Complex compliance scenarios have been identified that require human judgment and strategic thinking. 
                Your expertise is essential for:</p>
                <ul>
                    <li>Regulatory interpretation and context</li>
                    <li>Strategic risk assessment</li>
                    <li>Stakeholder impact analysis</li>
                    <li>Business continuity decisions</li>
                </ul>
                <button style="background: #F59E0B; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 0.5rem; cursor: pointer; margin-top: 0.5rem;">
                    Review Queue →
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### AI Automation Impact")
            
            automation_stats = [
                ("Routine Checks Automated", "94%", "🤖"),
                ("Expert Time Saved Weekly", "32 hours", "⏰"),
                ("False Positive Rate", "3.2%", "🎯"),
                ("Human Review Accuracy", "97.8%", "👥"),
            ]
            
            for stat, value, icon in automation_stats:
                st.markdown(f"""
                <div style="padding: 1rem; background: #F8FAFC; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span>{icon} {stat}</span>
                        <strong style="color: #10B981;">{value}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Value-Add Activities")
            
            human_activities = [
                "Strategic risk assessment and mitigation planning",
                "Regulatory interpretation for complex scenarios", 
                "Stakeholder communication and executive reporting",
                "Cross-framework correlation and gap analysis",
                "Vendor risk evaluation and contract review",
                "Incident response coordination and lessons learned"
            ]
            
            for activity in human_activities:
                st.markdown(f"✅ {activity}")
    
    def render_audit_trail(self):
        """Render audit trail section"""
        st.markdown("## 📋 Audit Trail & Activity Log")
        
        # Convert audit data to DataFrame
        df_audit = pd.DataFrame(self.audit_data)
        df_audit['timestamp'] = pd.to_datetime(df_audit['timestamp'])
        
        # Timeline view
        for _, row in df_audit.head(10).iterrows():
            event_time = row['timestamp'].strftime('%H:%M')
            event_date = row['timestamp'].strftime('%Y-%m-%d')
            
            # Determine event icon
            event_icons = {
                'Compliance Assessment Completed': '🔍',
                'Human Review Required': '👥',
                'Risk Accepted': '✅',
                'Violation Remediated': '🔧',
                'Framework Update': '🔄'
            }
            icon = event_icons.get(row['event'], '📝')
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 1rem; border-left: 3px solid #10B981; margin-bottom: 0.5rem; background: #F8FAFC;">
                <div style="margin-right: 1rem; font-size: 1.5rem;">{icon}</div>
                <div style="flex-grow: 1;">
                    <strong>{row['event']}</strong> - {row['framework']}
                    <br>
                    <small style="color: #64748B;">{event_date} at {event_time} by {row['user']}</small>
                    <br>
                    <em>{row['details']}</em>
                </div>
                <div style="text-align: right; color: #10B981; font-weight: bold;">
                    {row.get('score', 'N/A')}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar with controls and filters"""
        with st.sidebar:
            st.markdown("## 🛡️ SentinelGRC Controls")
            
            # Auto-refresh toggle
            auto_refresh = st.toggle("Auto Refresh", value=st.session_state.auto_refresh)
            st.session_state.auto_refresh = auto_refresh
            
            if auto_refresh:
                st.success("Dashboard auto-refreshing every 30 seconds")
                time.sleep(0.1)  # Small delay for UX
                st.rerun()
            
            st.markdown("---")
            
            # Framework selection
            st.markdown("### Framework Focus")
            available_frameworks = [f['framework'] for f in self.framework_data]
            selected_frameworks = st.multiselect(
                "Select Frameworks",
                available_frameworks,
                default=st.session_state.selected_frameworks
            )
            st.session_state.selected_frameworks = selected_frameworks
            
            # Time period selection
            st.markdown("### Time Period")
            time_period = st.selectbox(
                "Analysis Period",
                ['7 days', '30 days', '90 days', '1 year'],
                index=1
            )
            st.session_state.time_period = time_period
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### Quick Actions")
            
            if st.button("📊 Generate Executive Report"):
                st.success("Executive report generated! Check your email.")
            
            if st.button("👥 Review Human Queue"):
                st.info("Redirecting to human review interface...")
            
            if st.button("🔄 Force Refresh"):
                st.experimental_rerun()
            
            st.markdown("---")
            
            # AI Intelligence Status
            st.markdown("### 🧠 AI Intelligence Status")
            st.markdown("""
            - **Core Engine**: 🟢 Operational
            - **Framework Translation**: 🟢 Active  
            - **Multi-Regional**: 🟢 Synced
            - **Token Optimization**: 🟢 67% savings
            - **Human Escalation**: 🟢 Ready
            """)
            
            # Platform info
            st.markdown("---")
            st.markdown("### Platform Info")
            st.caption(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            st.caption("**Version:** SentinelGRC v1.0")
            st.caption("**Powered by:** Cerberus AI Intelligence")
    
    def get_score_class(self, score):
        """Get CSS class based on compliance score"""
        if score >= 90:
            return "score-excellent"
        elif score >= 80:
            return "score-good"
        elif score >= 70:
            return "score-fair"
        else:
            return "score-poor"
    
    def run_dashboard(self):
        """Main dashboard execution"""
        
        # Render sidebar first
        self.render_sidebar()
        
        # Main dashboard content
        self.render_header()
        
        # Executive summary
        self.render_executive_summary()
        
        st.markdown("---")
        
        # Framework performance
        self.render_framework_performance()
        
        st.markdown("---")
        
        # Risk register
        self.render_risk_register()
        
        st.markdown("---")
        
        # DevOps integration
        self.render_devops_integration()
        
        st.markdown("---")
        
        # Human intelligence section
        self.render_human_intelligence_section()
        
        st.markdown("---")
        
        # Audit trail
        self.render_audit_trail()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #64748B; padding: 2rem;">
            <p>🔱 <strong>Powered by Cerberus AI</strong> - The Three-Headed Guardian of Enterprise Compliance</p>
            <p><em>One Intelligence. Two Interfaces. Complete Compliance.</em></p>
        </div>
        """, unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    dashboard = GRCExecutiveDashboard()
    dashboard.run_dashboard()