"""
Sentinel GRC - Streamlit Demo Interface
======================================
Simple UI for demonstrating the unified GRC assessment system.
Zero-cost implementation using free tiers only.
"""

import streamlit as st
import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any

# Import the unified system
try:
    from unified_orchestrator import SentinelGRC
    from sentinel_grc_complete import CompanyProfile
    from supabase_integration import (
        save_assessment_to_db, get_assessment_history, 
        get_dashboard_metrics, is_database_available
    )
except ImportError as e:
    st.error(f"Missing dependencies: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Sentinel GRC Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        margin-bottom: 1rem;
        text-align: center;
    }
    .framework-badge {
        background-color: #e8f4f8;
        color: #1f4e79;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        margin: 0.125rem;
        font-size: 0.8rem;
        display: inline-block;
    }
    .confidence-high { background-color: #d4edda; color: #155724; }
    .confidence-medium { background-color: #fff3cd; color: #856404; }
    .confidence-low { background-color: #f8d7da; color: #721c24; }
    .gap-high { border-left: 4px solid #dc3545; padding-left: 1rem; }
    .gap-medium { border-left: 4px solid #ffc107; padding-left: 1rem; }
    .gap-low { border-left: 4px solid #17a2b8; padding-left: 1rem; }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'assessment_result' not in st.session_state:
        st.session_state.assessment_result = None
    if 'sidecar_requests' not in st.session_state:
        st.session_state.sidecar_requests = {}
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False
    if 'sentinel_system' not in st.session_state:
        st.session_state.sentinel_system = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Assessment"
    if 'assessment_saved' not in st.session_state:
        st.session_state.assessment_saved = False

@st.cache_resource
def initialize_sentinel_system():
    """Initialize the Sentinel GRC system (cached)"""
    try:
        return SentinelGRC(enable_sidecars=True, enable_groq=True)
    except Exception as e:
        st.error(f"Failed to initialize Sentinel GRC: {e}")
        return None

def run_async_function(coro):
    """Run async function in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)
    except RuntimeError:
        # Create new event loop if none exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

def render_main_header():
    """Render the main application header"""
    st.markdown('<h1 class="main-header">🛡️ Sentinel GRC Assessment Platform</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #6c757d; margin-bottom: 2rem;">
        <strong>Australian Compliance Assessment System</strong><br>
        Essential 8 • Privacy Act • APRA CPS 234 • SOCI Act
    </div>
    """, unsafe_allow_html=True)

def render_company_input_form():
    """Render company information input form"""
    
    with st.form("company_assessment_form"):
        st.subheader("📋 Company Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g., HealthTech Solutions Pty Ltd"
            )
            
            industry = st.selectbox(
                "Industry *",
                options=[
                    "Healthcare", "Finance", "Banking", "Insurance", "Superannuation",
                    "Technology", "Education", "Government", "Energy", "Telecommunications",
                    "Transport", "Water", "Defence", "Manufacturing", "Retail", "Other"
                ],
                index=0
            )
            
            employee_count = st.number_input(
                "Number of Employees *",
                min_value=1,
                max_value=50000,
                value=50,
                step=1
            )
            
        with col2:
            annual_revenue = st.number_input(
                "Annual Revenue (AUD, optional)",
                min_value=0,
                value=0,
                step=100000,
                format="%d"
            )
            
            has_govt_contracts = st.checkbox(
                "Has Government Contracts",
                help="Does your organization have contracts with government agencies?"
            )
            
            country = st.selectbox(
                "Country",
                options=["Australia", "New Zealand", "Other"],
                index=0
            )
        
        st.subheader("🔐 Current Security Controls")
        current_controls = st.multiselect(
            "Select existing security controls",
            options=[
                "Application Control", "Patch Applications", "Configure MS Office Macro Settings",
                "User Application Hardening", "Restrict Admin Privileges", "Patch Operating Systems",
                "Multi-Factor Authentication", "Regular Backups", "Network Segmentation",
                "Access Control", "Monitoring & Logging", "Incident Response Plan",
                "Security Awareness Training", "Data Encryption"
            ],
            default=["Multi-Factor Authentication", "Regular Backups"]
        )
        
        st.subheader("⚠️ Previous Security Incidents (Optional)")
        previous_incidents = st.text_area(
            "Describe any previous security incidents",
            placeholder="e.g., Phishing attack in 2023, Data breach incident, etc.",
            height=80
        )
        
        # Assessment options
        st.subheader("🎯 Assessment Options")
        col3, col4 = st.columns(2)
        
        with col3:
            enable_sidecars = st.checkbox(
                "Enable Background Analysis",
                value=True,
                help="Enhanced legal and threat modeling analysis"
            )
        
        with col4:
            enable_groq = st.checkbox(
                "Enable AI Enhancement",
                value=True,
                help="AI-powered compliance analysis using Groq"
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "🔍 Start Compliance Assessment",
            type="primary",
            use_container_width=True
        )
        
        return submitted, {
            "company_name": company_name,
            "industry": industry,
            "employee_count": employee_count,
            "annual_revenue": annual_revenue if annual_revenue > 0 else None,
            "has_government_contracts": has_govt_contracts,
            "country": country,
            "current_controls": current_controls,
            "previous_incidents": [previous_incidents] if previous_incidents.strip() else [],
            "enable_sidecars": enable_sidecars,
            "enable_groq": enable_groq
        }

def render_navigation():
    """Render navigation menu"""
    
    st.sidebar.markdown("### 🧭 Navigation")
    
    pages = ["Assessment", "Dashboard", "History"]
    
    for page in pages:
        if st.sidebar.button(f"📊 {page}" if page == "Dashboard" else f"🔍 {page}" if page == "Assessment" else f"📈 {page}", 
                           use_container_width=True,
                           type="primary" if st.session_state.current_page == page else "secondary"):
            st.session_state.current_page = page
            st.rerun()

def render_system_status():
    """Render system status in sidebar"""
    
    st.sidebar.markdown("### 🏥 System Status")
    
    # Database status
    if is_database_available():
        st.sidebar.success("✅ Database Connected")
    else:
        st.sidebar.warning("⚠️ Database Offline")
    
    if st.session_state.sentinel_system:
        status = st.session_state.sentinel_system.get_status()
        
        # Core agents
        st.sidebar.success(f"✅ Core Agents: {len(status.get('core_agents', []))}")
        
        # ML Enhancement
        if status.get('ml_enhanced'):
            st.sidebar.success("✅ ML Enhanced")
        else:
            st.sidebar.warning("⚠️ ML Not Available")
        
        # Sidecars
        if status.get('sidecars_enabled'):
            st.sidebar.success("✅ Background Analysis")
        else:
            st.sidebar.info("ℹ️ Background Analysis Disabled")
        
        # Groq
        if status.get('groq_enhanced'):
            st.sidebar.success("✅ AI Enhancement Available")
        else:
            st.sidebar.warning("⚠️ AI Enhancement Not Available")
        
        # Neo4j
        if status.get('neo4j_enhanced') and status.get('neo4j_available'):
            st.sidebar.success("✅ Graph Analytics Available")
            graph_features = status.get('graph_features', [])
            with st.sidebar.expander("Graph Features"):
                for feature in graph_features:
                    st.sidebar.text(f"• {feature}")
        else:
            st.sidebar.warning("⚠️ Graph Analytics Not Available")
        
        # Knowledge sources
        sources = status.get('knowledge_sources', [])
        st.sidebar.markdown(f"📚 **Knowledge Sources**: {len(sources)}")
        
        with st.sidebar.expander("View Sources"):
            for source in sources:
                st.sidebar.text(f"• {source}")
    
    else:
        st.sidebar.error("❌ System Not Initialized")

def render_assessment_results(result: Dict[str, Any]):
    """Render assessment results"""
    
    assessment = result['assessment_result']
    
    # Main metrics
    st.subheader("📊 Assessment Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        confidence_class = get_confidence_class(assessment.confidence_score)
        st.markdown(f"""
        <div class="metric-card">
            <h4>Confidence Score</h4>
            <span class="framework-badge {confidence_class}">
                {assessment.confidence_score:.1%}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Overall Maturity</h4>
            <span class="framework-badge">
                {assessment.overall_maturity:.1%}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Gaps Identified</h4>
            <span class="framework-badge">
                {len(assessment.gaps_identified)}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        escalation_color = "confidence-low" if assessment.escalation_required.value != "NONE" else "confidence-high"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Escalation Status</h4>
            <span class="framework-badge {escalation_color}">
                {assessment.escalation_required.value}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Frameworks assessed
    st.subheader("🎯 Frameworks Assessed")
    frameworks_html = ""
    for framework in result['frameworks_assessed']:
        frameworks_html += f'<span class="framework-badge">{framework}</span>'
    st.markdown(frameworks_html, unsafe_allow_html=True)
    
    # Processing info
    st.info(f"⏱️ Processing completed in {result['processing_time']:.2f} seconds")
    
    # Show Neo4j enhancement status
    if result.get('neo4j_enhanced'):
        st.info("🌐 Assessment enhanced with Neo4j knowledge graph analysis")
    
    # Tabs for detailed results
    tabs = ["🚨 Gaps & Risks", "💡 Recommendations", "📋 Controls", "🔍 Framework Details"]
    
    # Add Graph Insights tab if Neo4j is enabled
    if result.get('neo4j_enhanced') and result.get('graph_insights'):
        tabs.append("📊 Graph Insights")
    
    # Create tabs
    if len(tabs) == 4:
        tab1, tab2, tab3, tab4 = st.tabs(tabs)
        render_tabs = [tab1, tab2, tab3, tab4]
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)
        render_tabs = [tab1, tab2, tab3, tab4, tab5]
    
    with render_tabs[0]:
        render_gaps_and_risks(assessment.gaps_identified)
    
    with render_tabs[1]:
        render_recommendations(assessment.recommendations)
    
    with render_tabs[2]:
        render_controls_assessed(assessment.controls_assessed)
    
    with render_tabs[3]:
        if hasattr(assessment, 'framework_results'):
            render_framework_details(assessment.framework_results)
        else:
            st.info("Framework-specific details not available")
    
    # Render Graph Insights tab if available
    if len(render_tabs) == 5:
        with render_tabs[4]:
            render_graph_insights(result.get('graph_insights', {}))

def get_confidence_class(confidence: float) -> str:
    """Get CSS class for confidence level"""
    if confidence >= 0.8:
        return "confidence-high"
    elif confidence >= 0.6:
        return "confidence-medium"
    else:
        return "confidence-low"

def render_gaps_and_risks(gaps: list):
    """Render gaps and risks"""
    
    if not gaps:
        st.success("🎉 No critical compliance gaps identified!")
        return
    
    # Group gaps by risk level
    high_risk = [g for g in gaps if g.get('risk_level') == 'HIGH']
    medium_risk = [g for g in gaps if g.get('risk_level') == 'MEDIUM'] 
    low_risk = [g for g in gaps if g.get('risk_level') == 'LOW']
    
    if high_risk:
        st.markdown("### 🚨 High Risk Gaps")
        for gap in high_risk:
            render_gap_item(gap, "gap-high")
    
    if medium_risk:
        st.markdown("### ⚠️ Medium Risk Gaps")
        for gap in medium_risk:
            render_gap_item(gap, "gap-medium")
    
    if low_risk:
        st.markdown("### ℹ️ Low Risk Gaps")
        for gap in low_risk:
            render_gap_item(gap, "gap-low")

def render_gap_item(gap: Dict[str, Any], css_class: str):
    """Render individual gap item"""
    
    framework = gap.get('source_framework', 'Unknown')
    control = gap.get('control', 'Unknown Control')
    description = gap.get('gap_description', gap.get('description', 'No description available'))
    
    st.markdown(f"""
    <div class="{css_class}">
        <strong>{control}</strong> ({framework})<br>
        {description}
    </div>
    """, unsafe_allow_html=True)

def render_recommendations(recommendations: list):
    """Render recommendations"""
    
    if not recommendations:
        st.info("No specific recommendations available")
        return
    
    for i, rec in enumerate(recommendations, 1):
        framework = rec.get('source_framework', 'General')
        priority = rec.get('priority', 'Medium')
        description = rec.get('description', rec.get('recommendation', 'No description available'))
        
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "🔵")
        
        st.markdown(f"""
        **{i}. {priority_emoji} {rec.get('title', f'Recommendation {i}')}** ({framework})
        
        {description}
        """)

def render_controls_assessed(controls: list):
    """Render assessed controls"""
    
    if not controls:
        st.info("No controls assessment data available")
        return
    
    # Group by framework
    frameworks = {}
    for control in controls:
        fw = control.get('source_framework', 'Unknown')
        if fw not in frameworks:
            frameworks[fw] = []
        frameworks[fw].append(control)
    
    for framework, fw_controls in frameworks.items():
        st.markdown(f"### {framework}")
        
        for control in fw_controls:
            name = control.get('control_name', control.get('name', 'Unknown'))
            status = control.get('status', 'Unknown')
            maturity = control.get('maturity_level', 'N/A')
            
            status_emoji = {
                "COMPLIANT": "✅",
                "PARTIAL": "🟡", 
                "NON_COMPLIANT": "❌",
                "NOT_APPLICABLE": "⚪"
            }.get(status, "❓")
            
            st.markdown(f"- {status_emoji} **{name}** (Maturity: {maturity})")

def render_framework_details(framework_results: Dict[str, Any]):
    """Render framework-specific details"""
    
    for framework, result in framework_results.items():
        if isinstance(result, dict) and not result.get('error'):
            st.markdown(f"### {framework}")
            
            # Framework-specific metrics
            col1, col2 = st.columns(2)
            
            with col1:
                confidence = result.get('confidence', 0)
                st.metric("Confidence", f"{confidence:.1%}")
            
            with col2:
                maturity = result.get('overall_maturity', result.get('compliance_score', 0))
                st.metric("Maturity", f"{maturity:.1%}")
            
            # Framework-specific details
            if framework == "Essential8":
                render_essential8_details(result)
            elif framework == "PrivacyAct":
                render_privacy_act_details(result)
            elif framework == "APRACPS234":
                render_apra_details(result)
            elif framework == "SOCIAct":
                render_soci_details(result)

def render_essential8_details(result: Dict[str, Any]):
    """Render Essential 8 specific details"""
    strategies = result.get('strategy_scores', {})
    
    if strategies:
        st.markdown("**Strategy Maturity Levels:**")
        for strategy, score in strategies.items():
            st.progress(score, text=f"{strategy}: {score:.1%}")

def render_privacy_act_details(result: Dict[str, Any]):
    """Render Privacy Act specific details"""
    principles = result.get('principle_scores', {})
    
    if principles:
        st.markdown("**Privacy Principles Assessment:**")
        for principle, score in list(principles.items())[:5]:  # Show first 5
            st.progress(score, text=f"{principle}: {score:.1%}")

def render_apra_details(result: Dict[str, Any]):
    """Render APRA CPS 234 specific details"""
    requirements = result.get('requirement_scores', {})
    
    if requirements:
        st.markdown("**APRA Requirements Assessment:**")
        for req, score in list(requirements.items())[:5]:
            st.progress(score, text=f"{req}: {score:.1%}")

def render_soci_details(result: Dict[str, Any]):
    """Render SOCI Act specific details"""
    obligations = result.get('obligation_scores', {})
    
    if obligations:
        st.markdown("**SOCI Obligations Assessment:**")
        for obligation, score in list(obligations.items())[:5]:
            st.progress(score, text=f"{obligation}: {score:.1%}")

def render_graph_insights(graph_insights: Dict[str, Any]):
    """Render Neo4j graph insights"""
    
    if not graph_insights:
        st.info("No graph insights available")
        return
    
    st.subheader("📊 Knowledge Graph Analysis")
    st.markdown("*Advanced relationship analysis powered by Neo4j*")
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        compliance_pct = graph_insights.get('compliance_percentage', 0)
        st.metric("Graph Compliance Score", f"{compliance_pct:.1f}%")
    
    with col2:
        exposed_threats = len(graph_insights.get('exposed_threats', []))
        st.metric("Exposed Threats", exposed_threats)
    
    with col3:
        impl_steps = len(graph_insights.get('implementation_path', []))
        st.metric("Implementation Steps", impl_steps)
    
    # Exposed Threats Analysis
    exposed_threats = graph_insights.get('exposed_threats', [])
    if exposed_threats:
        st.markdown("### 🎯 Threat Exposure Analysis")
        
        for threat in exposed_threats[:5]:  # Show top 5 threats
            threat_name = threat.get('threat', 'Unknown Threat')
            severity = threat.get('severity', 'MEDIUM')
            
            # Color code by severity
            if severity == 'CRITICAL':
                st.error(f"🚨 **{threat_name}** - Critical Risk")
            elif severity == 'HIGH':
                st.warning(f"⚠️ **{threat_name}** - High Risk")
            else:
                st.info(f"ℹ️ **{threat_name}** - Medium Risk")
    
    # Implementation Path
    impl_path = graph_insights.get('implementation_path', [])
    if impl_path:
        st.markdown("### 🛤️ Optimal Implementation Path")
        st.markdown("*Neo4j-recommended order based on threat prevention and effort analysis*")
        
        for i, step in enumerate(impl_path[:5], 1):
            control = step.get('control', 'Unknown Control')
            effort = step.get('effort', 'UNKNOWN')
            threats_prevented = step.get('threats_prevented', [])
            
            # Format effort level
            effort_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(effort, "⚪")
            
            with st.expander(f"Step {i}: {control} {effort_emoji}"):
                st.write(f"**Effort Level:** {effort}")
                st.write(f"**Threats Prevented:** {len(threats_prevented)}")
                if threats_prevented:
                    threats_list = ", ".join(threats_prevented[:3])
                    if len(threats_prevented) > 3:
                        threats_list += f" and {len(threats_prevented) - 3} more"
                    st.write(f"**Protects Against:** {threats_list}")
    
    # Priority Recommendations from Graph
    priority_recs = graph_insights.get('priority_recommendations', [])
    if priority_recs:
        st.markdown("### 💡 Graph-Driven Recommendations")
        
        for rec in priority_recs[:3]:  # Top 3 recommendations
            control = rec.get('control', 'Unknown')
            effort = rec.get('effort', 'UNKNOWN')
            threats_prevented = rec.get('threats_prevented', 0)
            
            effort_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(effort, "⚪")
            
            st.markdown(f"""
            **{control}** {effort_color}
            - Effort: {effort}
            - Prevents: {threats_prevented} threat(s)
            """)
    
    # Relationship Analysis
    relationship_analysis = graph_insights.get('relationship_analysis', {})
    if relationship_analysis:
        st.markdown("### 🔗 Control Relationship Analysis")
        
        # Coverage analysis
        threat_coverage = relationship_analysis.get('threat_coverage_analysis', [])
        if threat_coverage:
            st.markdown("**Threat Coverage Status:**")
            
            protected_count = len([t for t in threat_coverage if t.get('status') == 'Protected'])
            exposed_count = len([t for t in threat_coverage if t.get('status') == 'Exposed'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Protected Threats", protected_count, delta=None)
            with col2:
                st.metric("Exposed Threats", exposed_count, delta=None)
            
            # Show threat details
            if st.checkbox("Show detailed threat analysis"):
                for threat in threat_coverage[:8]:  # Show up to 8 threats
                    threat_name = threat.get('threat', 'Unknown')
                    status = threat.get('status', 'Unknown')
                    severity = threat.get('severity', 'MEDIUM')
                    protecting_controls = threat.get('protecting_controls', 0)
                    
                    status_icon = "✅" if status == "Protected" else "❌"
                    severity_color = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🔵"}.get(severity, "⚪")
                    
                    st.markdown(f"{status_icon} **{threat_name}** {severity_color} - {protecting_controls} control(s)")
    
    # Neo4j Query Insights
    if st.checkbox("Show advanced graph metrics"):
        st.markdown("### 🔍 Advanced Graph Metrics")
        
        # Calculate some derived metrics
        total_controls = 8  # Essential 8
        implemented_controls = relationship_analysis.get('implemented_control_count', 0)
        coverage_pct = relationship_analysis.get('coverage_percentage', 0)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Control Implementation", 
                f"{implemented_controls}/{total_controls}",
                delta=f"{coverage_pct:.1f}% coverage"
            )
        
        with col2:
            # Calculate threat reduction potential
            missing_controls = total_controls - implemented_controls
            potential_reduction = missing_controls * 12.5  # Rough estimate
            st.metric(
                "Risk Reduction Potential",
                f"{potential_reduction:.1f}%",
                delta=f"{missing_controls} controls to implement"
            )
        
        with col3:
            # Relationship density
            related_gaps = len(relationship_analysis.get('related_control_gaps', []))
            st.metric(
                "Control Relationships",
                related_gaps,
                delta="gaps with shared threats"
            )

def render_sidecar_status(sidecar_requests: Dict[str, str]):
    """Render sidecar analysis status"""
    
    if not sidecar_requests:
        return
    
    st.subheader("🔄 Background Analysis Status")
    
    sentinel = st.session_state.sentinel_system
    if not sentinel:
        return
    
    try:
        # Get latest sidecar results
        sidecar_results = run_async_function(
            sentinel.get_enhanced_results(sidecar_requests)
        )
        
        for analysis_type, result in sidecar_results.items():
            status = result.get('status', 'unknown')
            
            if status == 'processing':
                st.info(f"🔄 {analysis_type.replace('_', ' ').title()}: In Progress...")
            else:
                confidence = result.get('confidence', 0)
                processing_time = result.get('processing_time', 0)
                
                st.success(f"✅ {analysis_type.replace('_', ' ').title()}: Completed in {processing_time:.1f}s (Confidence: {confidence:.1%})")
                
                # Show enhanced analysis results
                with st.expander(f"View {analysis_type.replace('_', ' ').title()} Results"):
                    analysis_content = result.get('analysis', {})
                    if isinstance(analysis_content, dict):
                        for key, value in analysis_content.items():
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
                    else:
                        st.text(str(analysis_content))
    
    except Exception as e:
        st.warning(f"Could not retrieve sidecar results: {e}")

def render_assessment_page():
    """Render the main assessment page"""
    
    if st.session_state.assessment_result is None:
        # Show input form
        submitted, form_data = render_company_input_form()
        
        if submitted:
            # Validate required fields
            if not form_data['company_name'].strip():
                st.error("Company name is required")
                return
                
            if not form_data['industry']:
                st.error("Industry selection is required")
                return
            
            # Run assessment
            with st.spinner("🔍 Running comprehensive compliance assessment..."):
                try:
                    # Build company profile (mock for demo)
                    sentinel = st.session_state.sentinel_system
                    
                    # Run assessment
                    result = run_async_function(
                        sentinel.assess_company(
                            company_name=form_data['company_name'],
                            industry=form_data['industry'],
                            employee_count=form_data['employee_count'],
                            annual_revenue=form_data['annual_revenue'],
                            has_government_contracts=form_data['has_government_contracts'],
                            current_controls=form_data['current_controls'],
                            previous_incidents=form_data['previous_incidents']
                        )
                    )
                    
                    # Store results
                    st.session_state.assessment_result = result
                    st.session_state.sidecar_requests = result.get('sidecar_requests', {})
                    
                    st.success("✅ Assessment completed successfully!")
                    
                    # Save to database if available
                    if is_database_available() and not st.session_state.assessment_saved:
                        try:
                            assessment_id = run_async_function(save_assessment_to_db(result))
                            if assessment_id:
                                st.info(f"💾 Assessment saved to database (ID: {assessment_id[:8]}...)")
                                st.session_state.assessment_saved = True
                        except Exception as e:
                            st.warning(f"Could not save to database: {e}")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Assessment failed: {e}")
                    st.exception(e)
    else:
        # Show results
        render_assessment_results(st.session_state.assessment_result)
        
        # Show sidecar status if available
        if st.session_state.sidecar_requests:
            render_sidecar_status(st.session_state.sidecar_requests)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Start New Assessment", type="primary"):
                st.session_state.assessment_result = None
                st.session_state.sidecar_requests = {}
                st.session_state.assessment_saved = False
                st.rerun()
        
        with col2:
            if st.button("📊 View Dashboard", type="secondary"):
                st.session_state.current_page = "Dashboard"
                st.rerun()
        
        with col3:
            if st.button("📈 View History", type="secondary"):
                st.session_state.current_page = "History"
                st.rerun()

def main():
    """Main application"""
    
    init_session_state()
    render_main_header()
    
    # Initialize system
    if not st.session_state.system_initialized:
        with st.spinner("Initializing Sentinel GRC system..."):
            st.session_state.sentinel_system = initialize_sentinel_system()
            st.session_state.system_initialized = True
            
        if st.session_state.sentinel_system:
            st.success("✅ Sentinel GRC system initialized successfully!")
        else:
            st.error("❌ Failed to initialize system")
            return
    
    # Render navigation and sidebar
    render_navigation()
    render_system_status()
    
    # Main content based on current page
    if st.session_state.current_page == "Assessment":
        render_assessment_page()
    elif st.session_state.current_page == "Dashboard":
        render_dashboard()
    elif st.session_state.current_page == "History":
        render_history()

def render_dashboard():
    """Render analytics dashboard"""
    
    st.subheader("📊 GRC Analytics Dashboard")
    
    # Get dashboard metrics
    with st.spinner("Loading dashboard metrics..."):
        try:
            metrics = run_async_function(get_dashboard_metrics())
            
            if "error" in metrics:
                st.error(f"Dashboard error: {metrics['error']}")
                return
            
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Assessments", metrics.get('total_assessments', 0))
            
            with col2:
                st.metric("Recent Assessments", metrics.get('recent_assessments', 0))
            
            with col3:
                avg_confidence = metrics.get('average_confidence', 0)
                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
            
            with col4:
                avg_maturity = metrics.get('average_maturity', 0)
                st.metric("Avg Maturity", f"{avg_maturity:.1%}")
            
            # Industry breakdown
            st.subheader("🏭 Industry Breakdown")
            industry_data = metrics.get('industry_breakdown', {})
            
            if industry_data:
                import pandas as pd
                
                df = pd.DataFrame(list(industry_data.items()), columns=['Industry', 'Count'])
                st.bar_chart(df.set_index('Industry'))
            else:
                st.info("No industry data available yet")
                
        except Exception as e:
            st.error(f"Failed to load dashboard: {e}")

def render_history():
    """Render assessment history"""
    
    st.subheader("📈 Assessment History")
    
    # Company filter
    company_filter = st.text_input("Filter by company name (optional)", placeholder="Enter company name")
    
    # Load history
    with st.spinner("Loading assessment history..."):
        try:
            history = run_async_function(get_assessment_history(company_filter if company_filter else None))
            
            if not history:
                st.info("No assessment history found")
                return
            
            # Display history table
            import pandas as pd
            
            # Convert to DataFrame for better display
            df_data = []
            for record in history:
                df_data.append({
                    'Date': record['created_at'][:10] if record['created_at'] else 'Unknown',
                    'Company': record['company_name'],
                    'Industry': record['industry'],
                    'Employees': record['employee_count'],
                    'Confidence': f"{record['overall_confidence']:.1%}" if record['overall_confidence'] else 'N/A',
                    'Maturity': f"{record['overall_maturity']:.1%}" if record['overall_maturity'] else 'N/A',
                    'Gaps': record['gaps_count'],
                    'Escalation': '❗' if record['escalation_required'] else '✅'
                })
            
            df = pd.DataFrame(df_data)
            
            # Display with formatting
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # Export option
            if st.button("📥 Export History (CSV)", type="secondary"):
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "grc_assessment_history.csv",
                    "text/csv"
                )
                
        except Exception as e:
            st.error(f"Failed to load history: {e}")

if __name__ == "__main__":
    main()