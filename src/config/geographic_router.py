# geographic_router.py
# Intelligent geographic routing for compliance frameworks
# This demonstrates understanding of global compliance complexity

import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class GeographicConfig:
    """Configuration for a geographic region's compliance requirements"""
    region_name: str
    flag_emoji: str
    frameworks: List[str]
    currency: str
    privacy_law: str
    financial_regulation: str
    cybersecurity_baseline: str
    data_residency_requirements: bool
    
class ComplianceRouter:
    """
    Routes users to appropriate compliance frameworks based on geography
    This demonstrates Vanta-level thinking about market differences
    """
    
    def __init__(self):
        self.regions = self._initialize_regions()
        self.current_region = None
        
    def _initialize_regions(self) -> Dict:
        """Define compliance requirements by region"""
        return {
            "australia": GeographicConfig(
                region_name="Australia",
                flag_emoji="🇦🇺",
                frameworks=["Essential 8", "Privacy Act", "APRA CPS 234", "SOCI Act"],
                currency="AUD",
                privacy_law="Privacy Act 1988",
                financial_regulation="APRA CPS 234",
                cybersecurity_baseline="Essential 8",
                data_residency_requirements=True
            ),
            "united_states": GeographicConfig(
                region_name="United States",
                flag_emoji="🇺🇸",
                frameworks=["SOC 2", "HIPAA", "NIST CSF", "CCPA/CPRA", "PCI DSS"],
                currency="USD",
                privacy_law="State-specific (CCPA, VCDPA, etc.)",
                financial_regulation="GLBA / NYDFS",
                cybersecurity_baseline="NIST CSF",
                data_residency_requirements=False  # Generally more flexible
            ),
            "european_union": GeographicConfig(
                region_name="European Union",
                flag_emoji="🇪🇺",
                frameworks=["GDPR", "NIS2", "DORA", "ISO 27001"],
                currency="EUR",
                privacy_law="GDPR",
                financial_regulation="DORA",
                cybersecurity_baseline="NIS2 Directive",
                data_residency_requirements=True
            ),
            "united_kingdom": GeographicConfig(
                region_name="United Kingdom",
                flag_emoji="🇬🇧",
                frameworks=["UK GDPR", "ISO 27001", "Cyber Essentials", "FCA Rules"],
                currency="GBP",
                privacy_law="UK GDPR",
                financial_regulation="FCA Operational Resilience",
                cybersecurity_baseline="Cyber Essentials",
                data_residency_requirements=True
            ),
            "canada": GeographicConfig(
                region_name="Canada",
                flag_emoji="🇨🇦",
                frameworks=["PIPEDA", "Provincial Privacy Laws", "OSFI", "ISO 27001"],
                currency="CAD",
                privacy_law="PIPEDA",
                financial_regulation="OSFI Cyber Security",
                cybersecurity_baseline="CCCS Baseline Controls",
                data_residency_requirements=True
            )
        }
    
    def create_selection_interface(self):
        """
        Creates the Streamlit interface for region selection
        This is what users see when they first arrive
        """
        st.markdown("""
        <style>
        .region-card {
            border: 2px solid #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .region-card:hover {
            border-color: #4CAF50;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .region-selected {
            border-color: #4CAF50;
            background-color: #f0f8f0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.title("🌍 Select Your Compliance Region")
        st.markdown("Choose your geographic region to load the appropriate compliance frameworks")
        
        # Create columns for region selection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"🇦🇺 Australia", key="aus_btn", use_container_width=True):
                self._set_region("australia")
                st.rerun()
                
            if st.button(f"🇪🇺 European Union", key="eu_btn", use_container_width=True):
                self._set_region("european_union")
                st.rerun()
        
        with col2:
            if st.button(f"🇺🇸 United States", key="us_btn", use_container_width=True):
                self._set_region("united_states")
                st.rerun()
                
            if st.button(f"🇬🇧 United Kingdom", key="uk_btn", use_container_width=True):
                self._set_region("united_kingdom")
                st.rerun()
        
        with col3:
            if st.button(f"🇨🇦 Canada", key="ca_btn", use_container_width=True):
                self._set_region("canada")
                st.rerun()
                
            if st.button(f"🌐 Global/Multi-Region", key="global_btn", use_container_width=True):
                self._set_region("global")
                st.rerun()
        
        # Show comparison table
        with st.expander("📊 Compare Regional Requirements"):
            self._show_region_comparison()
    
    def _set_region(self, region: str):
        """Set the selected region and store in session state"""
        st.session_state.selected_region = region
        st.session_state.region_config = self.regions.get(region)
        
        # Load appropriate compliance agents
        if region == "australia":
            from ..agents.australian_compliance_agents import PrivacyActAgent, APRACPSAgent, SOCIActAgent
            st.session_state.compliance_agents = {
                'privacy_act': PrivacyActAgent(),
                'apra_cps234': APRACPSAgent(),
                'soci_act': SOCIActAgent()
            }
        elif region == "united_states":
            from ..config.us_adaptation_config import NISTCSFAgent
            st.session_state.compliance_agents = {
                'nist_csf': NISTCSFAgent(),
                'soc2': None,  # Placeholder - implement when needed
                'hipaa': None   # Placeholder - implement when needed
            }
        elif region == "global":
            # Load all frameworks for multi-national companies
            st.session_state.compliance_agents = self._load_global_agents()
    
    def _load_global_agents(self) -> Dict:
        """Load agents for global/multi-regional compliance"""
        from ..agents.australian_compliance_agents import PrivacyActAgent, APRACPSAgent, SOCIActAgent
        from ..config.us_adaptation_config import NISTCSFAgent
        
        return {
            # Australian frameworks
            'privacy_act': PrivacyActAgent(),
            'apra_cps234': APRACPSAgent(),
            'soci_act': SOCIActAgent(),
            # US frameworks
            'nist_csf': NISTCSFAgent(),
            # European frameworks (placeholder)
            'gdpr': None,
            # Global standards
            'iso27001': None
        }
    
    def _show_region_comparison(self):
        """Display a comparison table of regional requirements"""
        comparison_data = []
        
        for region_key, config in self.regions.items():
            comparison_data.append({
                "Region": f"{config.flag_emoji} {config.region_name}",
                "Privacy Law": config.privacy_law,
                "Cybersecurity": config.cybersecurity_baseline,
                "Financial": config.financial_regulation,
                "Data Residency": "Required" if config.data_residency_requirements else "Flexible"
            })
        
        st.table(comparison_data)


# streamlit_app_with_router.py
# Main application file with geographic routing

import streamlit as st
from typing import Optional

def initialize_app():
    """Initialize the application with geographic routing"""
    
    # Set page configuration
    st.set_page_config(
        page_title="SentinelGRC - Global Compliance Platform",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize router if not already done
    if 'router' not in st.session_state:
        st.session_state.router = ComplianceRouter()
    
    # Check if region is selected
    if 'selected_region' not in st.session_state:
        # Show region selection interface
        st.session_state.router.create_selection_interface()
        return False  # Region not yet selected
    
    return True  # Region selected, proceed with main app

def create_region_header():
    """Create a header showing current region with option to change"""
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        if st.session_state.region_config:
            st.markdown(f"### {st.session_state.region_config.flag_emoji} {st.session_state.region_config.region_name}")
    
    with col3:
        if st.button("🔄 Change Region", key="change_region"):
            # Clear region selection and restart
            del st.session_state.selected_region
            del st.session_state.region_config
            st.rerun()

def run_main_application():
    """Run the main compliance assessment application"""
    
    # Show current region header
    create_region_header()
    
    # Display region-specific information
    st.markdown("---")
    
    config = st.session_state.region_config
    
    # Create tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Assessment", "📊 Dashboard", "📈 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.header(f"Compliance Assessment - {config.region_name}")
        
        # Show applicable frameworks for this region
        st.subheader("Available Frameworks")
        
        framework_cols = st.columns(len(config.frameworks))
        selected_frameworks = []
        
        for idx, framework in enumerate(config.frameworks):
            with framework_cols[idx]:
                if st.checkbox(framework, key=f"fw_{framework}"):
                    selected_frameworks.append(framework)
        
        # Company profile form adapted to region
        st.subheader("Company Information")
        
        company_name = st.text_input("Company Name")
        industry = st.selectbox("Industry", 
                               ["Technology", "Healthcare", "Financial Services", 
                                "Manufacturing", "Retail", "Government"])
        
        # Region-specific fields
        if config.region_name == "United States":
            # US-specific fields
            col1, col2 = st.columns(2)
            with col1:
                handles_ca_data = st.checkbox("Process California resident data?")
                federal_contractor = st.checkbox("Federal contractor?")
            with col2:
                revenue = st.number_input(f"Annual Revenue ({config.currency})", 
                                         min_value=0, 
                                         format="%d")
                if handles_ca_data:
                    ca_consumers = st.number_input("California consumers (count)", 
                                                  min_value=0)
        
        elif config.region_name == "Australia":
            # Australian-specific fields
            col1, col2 = st.columns(2)
            with col1:
                is_critical_infrastructure = st.checkbox("Critical Infrastructure Entity?")
                apra_regulated = st.checkbox("APRA Regulated?")
            with col2:
                handles_government_data = st.checkbox("Handle government data?")
                revenue = st.number_input(f"Annual Revenue ({config.currency})", 
                                         min_value=0, 
                                         format="%d")
        
        elif config.region_name == "European Union":
            # EU-specific fields
            col1, col2 = st.columns(2)
            with col1:
                is_data_controller = st.checkbox("Data Controller?")
                is_data_processor = st.checkbox("Data Processor?")
            with col2:
                cross_border_transfers = st.checkbox("Cross-border data transfers?")
                employees = st.number_input("Number of employees", min_value=0)
        
        # Run assessment button
        if st.button("🚀 Run Assessment", type="primary", use_container_width=True):
            if not selected_frameworks:
                st.error("Please select at least one framework")
            elif not company_name:
                st.error("Please enter company name")
            else:
                with st.spinner(f"Running {config.region_name} compliance assessment..."):
                    # This is where you'd call your actual assessment logic
                    assessment_results = run_regional_assessment(
                        region=st.session_state.selected_region,
                        frameworks=selected_frameworks,
                        company_profile={
                            "name": company_name,
                            "industry": industry,
                            "revenue": revenue if 'revenue' in locals() else None,
                            # Add other collected fields
                        }
                    )
                    
                    # Display results
                    display_assessment_results(assessment_results)
    
    with tab2:
        st.header("Compliance Dashboard")
        # Regional dashboard content
        show_regional_dashboard(config)
    
    with tab3:
        st.header("Analytics & Trends")
        # Regional analytics
        show_regional_analytics(config)
    
    with tab4:
        st.header("Regional Settings")
        show_regional_settings(config)

def run_regional_assessment(region: str, frameworks: List[str], company_profile: Dict) -> Dict:
    """
    Run assessment using region-appropriate agents
    This demonstrates the power of the routing architecture
    """
    agents = st.session_state.compliance_agents
    results = {}
    
    # Use region-specific assessment logic
    if region == "australia":
        # Australian assessment logic using Essential 8, Privacy Act, etc.
        for framework in frameworks:
            if framework == "Essential 8":
                results[framework] = agents['essential8'].assess(company_profile)
            elif framework == "Privacy Act":
                results[framework] = agents['privacy_act'].assess(company_profile)
            # ... etc
    
    elif region == "united_states":
        # US assessment logic using SOC 2, HIPAA, etc.
        for framework in frameworks:
            if framework == "SOC 2":
                results[framework] = agents['soc2'].assess(company_profile)
            elif framework == "NIST CSF":
                results[framework] = agents['nist_csf'].assess(company_profile)
            # ... etc
    
    return results

def display_assessment_results(results: Dict):
    """Display assessment results in a region-appropriate format"""
    for framework, result in results.items():
        with st.expander(f"📊 {framework} Results", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Compliance Score", 
                         f"{result.get('compliance_score', 0):.1f}%",
                         delta=f"+{result.get('improvement', 0):.1f}%")
            
            with col2:
                st.metric("Maturity Level", 
                         result.get('maturity_level', 'Unknown'))
            
            with col3:
                st.metric("Critical Gaps", 
                         result.get('critical_gaps_count', 0))
            
            # Show detailed findings
            st.subheader("Key Findings")
            for finding in result.get('findings', [])[:5]:
                st.write(f"• {finding}")

def show_regional_dashboard(config: GeographicConfig):
    """Show dashboard tailored to regional requirements"""
    st.info(f"Dashboard configured for {config.region_name} compliance requirements")
    
    # Regional metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Primary Framework", config.cybersecurity_baseline)
    with col2:
        st.metric("Privacy Law", config.privacy_law)
    with col3:
        st.metric("Financial Reg", config.financial_regulation)
    with col4:
        st.metric("Data Residency", "Required" if config.data_residency_requirements else "Flexible")

def show_regional_analytics(config: GeographicConfig):
    """Show analytics relevant to the selected region"""
    st.info(f"Analytics and trends for {config.region_name} compliance landscape")
    
    # You could show region-specific trends here
    st.subheader("Regional Compliance Trends")
    st.line_chart({"Compliance Maturity": [60, 65, 70, 75, 80]})

def show_regional_settings(config: GeographicConfig):
    """Region-specific settings and configurations"""
    st.subheader("Regional Configuration")
    
    # Currency settings
    st.text_input("Currency", value=config.currency, disabled=True)
    
    # Notification preferences
    st.subheader("Regulatory Update Notifications")
    st.checkbox(f"Subscribe to {config.privacy_law} updates")
    st.checkbox(f"Subscribe to {config.cybersecurity_baseline} updates")
    
    # Language preferences (for future)
    if config.region_name == "European Union":
        st.selectbox("Preferred Language", 
                    ["English", "French", "German", "Spanish", "Italian"])

# Main execution
if __name__ == "__main__":
    # Initialize the app with routing
    if initialize_app():
        # Region is selected, run main application
        run_main_application()
    # If initialize_app returns False, region selection is shown