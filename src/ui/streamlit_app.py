"""
SentinelGRC - Unified Multi-Regional Compliance Platform
======================================================
Entry point for the unified platform with geographic routing.
Supports Australian, US, and EU compliance frameworks.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main application entry point"""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="SentinelGRC - Global Compliance Platform",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add demo disclaimer for international usage
    show_demo_disclaimer()
    
    # Initialize the geographic routing system
    from src.config.geographic_router import ComplianceRouter
    
    # Check if we have a router in session state
    if 'router' not in st.session_state:
        st.session_state.router = ComplianceRouter()
    
    # Check if region is already selected
    if 'selected_region' not in st.session_state:
        # Show region selection interface
        st.session_state.router.create_selection_interface()
        return
    
    # Region is selected, show the main application
    run_regional_application()

def show_demo_disclaimer():
    """Show important disclaimer for demo usage"""
    
    # Only show if not already acknowledged
    if 'disclaimer_acknowledged' not in st.session_state:
        st.warning("""
        **🚨 DEMO VERSION - IMPORTANT DISCLAIMERS**
        
        • **Sanitized Data Only**: Use only non-sensitive, sanitized data for testing
        • **Demo Purposes**: This is a proof-of-concept, not production-ready
        • **No Real Compliance**: Results are for demonstration only
        • **Data Privacy**: No real company data should be entered
        • **US Colleagues**: This demo uses Australian compliance baselines adapted for US frameworks
        
        **For Production Use**: Contact your compliance team before using with real data.
        """)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("✅ I Understand - Continue to Demo", type="primary", use_container_width=True):
                st.session_state.disclaimer_acknowledged = True
                st.rerun()
        return

def run_regional_application():
    """Run the main application based on selected region"""
    
    # Get current region configuration
    region = st.session_state.selected_region
    config = st.session_state.region_config
    
    # Show region header with change option
    create_region_header()
    
    st.markdown("---")
    
    # Create main application tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Assessment", 
        "📊 Dashboard", 
        "📈 Analytics", 
        "⚙️ Settings"
    ])
    
    with tab1:
        show_assessment_interface(region, config)
    
    with tab2:
        show_dashboard_interface(region, config)
    
    with tab3:
        show_analytics_interface(region, config)
    
    with tab4:
        show_settings_interface(region, config)

def create_region_header():
    """Create header showing current region with change option"""
    
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        if st.session_state.region_config:
            config = st.session_state.region_config
            st.markdown(f"### {config.flag_emoji} {config.region_name}")
    
    with col2:
        # Show key regional info
        if st.session_state.region_config:
            config = st.session_state.region_config
            st.caption(f"Currency: {config.currency} | Privacy: {config.privacy_law}")
    
    with col3:
        if st.button("🔄 Change Region", key="change_region"):
            # Clear region selection
            keys_to_clear = [
                'selected_region', 'region_config', 'compliance_agents', 
                'assessment_results', 'framework_selection'
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def show_assessment_interface(region: str, config):
    """Show the assessment interface for the selected region"""
    
    st.header(f"Compliance Assessment - {config.region_name}")
    
    # Framework selection
    st.subheader("Available Frameworks")
    
    # Create framework selection grid
    framework_cols = st.columns(min(len(config.frameworks), 4))
    selected_frameworks = []
    
    for idx, framework in enumerate(config.frameworks):
        col_idx = idx % len(framework_cols)
        with framework_cols[col_idx]:
            if st.checkbox(framework, key=f"fw_{framework}_{region}"):
                selected_frameworks.append(framework)
    
    # Company profile form
    st.subheader("Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", key="company_name")
        industry = st.selectbox("Industry", [
            "Technology", "Healthcare", "Financial Services",
            "Manufacturing", "Retail", "Government", "Other"
        ], key="industry")
    
    with col2:
        revenue = st.number_input(
            f"Annual Revenue ({config.currency})", 
            min_value=0, 
            format="%d",
            key="revenue"
        )
        employees = st.number_input(
            "Number of Employees", 
            min_value=1, 
            format="%d",
            key="employees"
        )
    
    # Region-specific fields
    show_regional_fields(region, config)
    
    # Assessment button
    if st.button("🚀 Run Assessment", type="primary", use_container_width=True):
        if not selected_frameworks:
            st.error("Please select at least one framework")
        elif not company_name:
            st.error("Please enter company name")
        else:
            run_assessment(region, selected_frameworks, {
                "name": company_name,
                "industry": industry,
                "revenue": revenue,
                "employees": employees,
                "region": region
            })

def show_regional_fields(region: str, config):
    """Show region-specific form fields"""
    
    st.subheader(f"{config.region_name} Specific Requirements")
    
    if region == "australia":
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Critical Infrastructure Entity?", key="au_critical_infra")
            st.checkbox("APRA Regulated Entity?", key="au_apra_regulated")
        with col2:
            st.checkbox("Handle Government Data?", key="au_govt_data")
            st.checkbox("ASX Listed Company?", key="au_asx_listed")
            
    elif region == "united_states":
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Process California Resident Data?", key="us_ca_data")
            st.checkbox("Federal Contractor?", key="us_federal_contractor")
        with col2:
            st.checkbox("Handle Protected Health Info (PHI)?", key="us_phi_data")
            st.number_input("California Consumers (if applicable)", min_value=0, key="us_ca_consumers")
            
    elif region == "european_union":
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Data Controller?", key="eu_data_controller")
            st.checkbox("Data Processor?", key="eu_data_processor")
        with col2:
            st.checkbox("Cross-border Data Transfers?", key="eu_cross_border")
            st.selectbox("Primary EU Country", [
                "Germany", "France", "Netherlands", "Ireland", "Spain", "Italy", "Other"
            ], key="eu_primary_country")

def run_assessment(region: str, frameworks: list, company_profile: dict):
    """Run the compliance assessment"""
    
    with st.spinner(f"Running {region.title()} compliance assessment..."):
        # This would integrate with your existing agents
        if region == "australia":
            from australian_compliance_agents import load_australian_agents
            agents = load_australian_agents()
        elif region == "united_states":
            from us_adaptation_config import load_us_agents
            agents = load_us_agents()
            st.success(f"✅ US agents loaded: {list(agents.keys())}")
        else:
            st.info(f"{region.title()} agents not yet implemented")
            agents = {}
        
        # Mock results for demo
        results = generate_demo_results(frameworks, company_profile)
        
        # Display results
        display_assessment_results(results)

def generate_demo_results(frameworks: list, company_profile: dict):
    """Generate realistic demo results"""
    import random
    
    results = {}
    for framework in frameworks:
        # Generate realistic demo scores
        base_score = random.uniform(65, 85)
        results[framework] = {
            "compliance_score": round(base_score, 1),
            "maturity_level": "Developing" if base_score < 70 else "Managed" if base_score < 80 else "Optimized",
            "critical_gaps_count": random.randint(1, 5),
            "findings": [
                f"Demo finding 1 for {framework}",
                f"Demo finding 2 for {framework}",
                f"Demo finding 3 for {framework}"
            ]
        }
    
    return results

def display_assessment_results(results: dict):
    """Display assessment results"""
    
    st.subheader("🎯 Assessment Results")
    
    for framework, result in results.items():
        with st.expander(f"📊 {framework} Results", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Compliance Score",
                    f"{result['compliance_score']}%",
                    delta=f"+{random.randint(1, 8)}.{random.randint(0, 9)}%"
                )
            
            with col2:
                st.metric("Maturity Level", result['maturity_level'])
            
            with col3:
                st.metric("Critical Gaps", result['critical_gaps_count'])
            
            # Show findings
            st.subheader("Key Findings")
            for finding in result['findings']:
                st.write(f"• {finding}")

def show_dashboard_interface(region: str, config):
    """Show dashboard for selected region"""
    st.header(f"Compliance Dashboard - {config.region_name}")
    st.info(f"Dashboard configured for {config.region_name} regulatory environment")
    
    # Mock dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Primary Framework", config.cybersecurity_baseline)
    with col2:
        st.metric("Privacy Regulation", config.privacy_law)
    with col3:
        st.metric("Financial Regulation", config.financial_regulation)
    with col4:
        data_residency = "Required" if config.data_residency_requirements else "Flexible"
        st.metric("Data Residency", data_residency)

def show_analytics_interface(region: str, config):
    """Show analytics for selected region"""
    st.header(f"Regional Analytics - {config.region_name}")
    st.info(f"Compliance trends and insights for {config.region_name}")
    
    # Mock analytics
    import numpy as np
    chart_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Compliance Score": [65, 68, 72, 75, 78]
    }
    
    st.line_chart(chart_data, x="Month", y="Compliance Score")

def show_settings_interface(region: str, config):
    """Show settings for selected region"""
    st.header(f"Regional Settings - {config.region_name}")
    
    # Regional preferences  
    st.subheader("Regional Configuration")
    st.text_input("Currency", value=config.currency, disabled=True)
    
    # Notifications
    st.subheader("Regulatory Update Notifications")
    st.checkbox(f"Subscribe to {config.privacy_law} updates")
    st.checkbox(f"Subscribe to {config.cybersecurity_baseline} updates")
    
    # Export preferences
    st.subheader("Export Preferences")
    if region == "australia":
        st.selectbox("Report Format", ["ACSC Format", "Board Report", "Audit Package"])
    elif region == "united_states":
        st.selectbox("Report Format", ["Vanta Format", "SOC 2 Package", "Board Slides"])
    else:
        st.selectbox("Report Format", ["Standard PDF", "Executive Summary", "Technical Report"])

if __name__ == "__main__":
    main()