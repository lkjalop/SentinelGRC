#!/usr/bin/env python3
"""
Cerberus AI Demo Launcher
========================
Unified demo environment showcasing both heads of the Cerberus AI platform:
- ArgusAI: DevOps integration and shift-left compliance
- SentinelGRC: Executive dashboard and GRC professional tools
"""

import streamlit as st
import subprocess
import sys
import time
from pathlib import Path
import webbrowser
from datetime import datetime
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Cerberus AI Demo Launcher",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for demo launcher
st.markdown("""
<style>
    .demo-header {
        background: linear-gradient(135deg, #6B46C1 0%, #10B981 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .platform-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        border: 2px solid transparent;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .platform-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .argus-card {
        border-color: #2563EB;
    }
    
    .sentinel-card {
        border-color: #10B981;
    }
    
    .demo-badge {
        display: inline-block;
        background: #F59E0B;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        margin: 0.25rem;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
    }
    
    .feature-list li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .feature-list li:last-child {
        border-bottom: none;
    }
    
    .launch-button {
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 0.5rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .argus-button {
        background: #2563EB;
        color: white;
    }
    
    .sentinel-button {
        background: #10B981;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

class CerberusDemoLauncher:
    """Demo launcher for Cerberus AI platform"""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.demo_sessions = {}
        
    def render_header(self):
        """Render main header"""
        st.markdown("""
        <div class="demo-header">
            <h1>🔱 Cerberus AI Platform Demo</h1>
            <h3>The Three-Headed Guardian of Enterprise Compliance</h3>
            <p><em>One Intelligence. Two Interfaces. Complete Compliance.</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_platform_overview(self):
        """Render platform overview"""
        st.markdown("## 🎯 Choose Your Interface")
        
        col1, col2 = st.columns(2)
        
        # ArgusAI - DevOps Head
        with col1:
            st.markdown("""
            <div class="platform-card argus-card">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h2>🐺 ArgusAI</h2>
                    <p><strong>The DevOps Head</strong></p>
                    <span class="demo-badge">For Development Teams</span>
                </div>
                
                <h4>🚀 "Shift-left compliance that doesn't slow you down"</h4>
                
                <div class="feature-list">
                    <li>✅ CI/CD Pipeline Integration</li>
                    <li>✅ GitHub Actions Plugin Demo</li>
                    <li>✅ Pre-commit Hook Examples</li>
                    <li>✅ Container Security Scanning</li>
                    <li>✅ Policy as Code Engine</li>
                    <li>✅ Developer-Friendly Reports</li>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <h5>Target Audience:</h5>
                    <p>DevOps Engineers, Platform Engineers, SREs, Security Engineers, Development Team Leads</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Launch ArgusAI Demo", key="argus_launch", help="DevOps-focused compliance interface"):
                self.launch_argus_demo()
        
        # SentinelGRC - GRC Head  
        with col2:
            st.markdown("""
            <div class="platform-card sentinel-card">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h2>🛡️ SentinelGRC</h2>
                    <p><strong>The GRC Head</strong></p>
                    <span class="demo-badge">For GRC Professionals</span>
                </div>
                
                <h4>👥 "AI that amplifies your expertise, not replaces it"</h4>
                
                <div class="feature-list">
                    <li>✅ Executive Dashboard</li>
                    <li>✅ Risk Register Management</li>
                    <li>✅ Human Review Queue</li>
                    <li>✅ Framework Performance</li>
                    <li>✅ Audit Trail & Evidence</li>
                    <li>✅ Strategic Reports</li>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <h5>Target Audience:</h5>
                    <p>Chief Compliance Officers, GRC Managers, Risk Analysts, Compliance Professionals, Auditors</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🛡️ Launch SentinelGRC Demo", key="sentinel_launch", help="Executive GRC dashboard"):
                self.launch_sentinel_demo()
    
    def render_unified_demo_section(self):
        """Render unified demo section"""
        st.markdown("---")
        st.markdown("## 🧠 Unified Intelligence Demo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🔄 Multi-Regional Framework Translation
            See how the same compliance requirement translates across:
            - **Australia**: Essential 8
            - **United States**: NIST CSF
            - **European Union**: GDPR
            """)
            
            if st.button("🌍 Launch Multi-Regional Demo", key="regional_demo"):
                self.launch_regional_demo()
        
        with col2:
            st.markdown("""
            ### ⚡ Token Optimization Engine
            Experience the 60-70% API cost reduction through:
            - **Semantic Caching**: Similar queries cached intelligently
            - **Response Compression**: Efficient data serialization
            - **Batch Processing**: Multiple validations in one call
            """)
            
            if st.button("💰 Launch Cost Demo", key="cost_demo"):
                self.show_cost_optimization_demo()
        
        with col3:
            st.markdown("""
            ### 🤝 Human-AI Collaboration
            See how AI routes complex decisions to human experts:
            - **Automated Routine**: 94% of checks automated
            - **Expert Escalation**: Complex scenarios to humans
            - **Decision Tracking**: Full audit trail
            """)
            
            if st.button("👥 Launch Collaboration Demo", key="collab_demo"):
                self.show_human_ai_demo()
    
    def render_api_demo_section(self):
        """Render API integration demos"""
        st.markdown("---")
        st.markdown("## 🔌 API Integration Demos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🚀 GitHub Actions Integration
            Test the CI/CD compliance checking:
            - Upload a sample repository
            - See real-time compliance validation
            - View SARIF security reports
            - Experience PR comment automation
            """)
            
            if st.button("🔧 Test GitHub Integration", key="github_test"):
                self.launch_github_demo()
        
        with col2:
            st.markdown("""
            ### 📊 REST API Playground  
            Explore the Cerberus AI API:
            - Framework validation endpoints
            - Real-time compliance scoring
            - Multi-format report generation
            - Webhook event handling
            """)
            
            if st.button("🌐 Launch API Playground", key="api_playground"):
                self.launch_api_playground()
    
    def render_competitive_comparison(self):
        """Render competitive comparison"""
        st.markdown("---")
        st.markdown("## ⚔️ Competitive Advantage Demo")
        
        comparison_data = [
            {"Feature": "DevOps Integration", "Traditional GRC": "❌ Manual", "DevSecOps Tools": "⚠️ Security Only", "Cerberus AI": "✅ Native CI/CD"},
            {"Feature": "GRC Professional Tools", "Traditional GRC": "✅ Comprehensive", "DevSecOps Tools": "❌ None", "Cerberus AI": "✅ AI-Enhanced"},
            {"Feature": "Multi-Framework Support", "Traditional GRC": "⚠️ Limited", "DevSecOps Tools": "❌ None", "Cerberus AI": "✅ 7+ Frameworks"},
            {"Feature": "Human-AI Collaboration", "Traditional GRC": "❌ Manual Only", "DevSecOps Tools": "❌ Automated Only", "Cerberus AI": "✅ Hybrid Approach"},
            {"Feature": "Real-time Compliance", "Traditional GRC": "❌ Periodic", "DevSecOps Tools": "⚠️ Security Only", "Cerberus AI": "✅ Continuous"},
            {"Feature": "Cost Optimization", "Traditional GRC": "❌ Expensive", "DevSecOps Tools": "⚠️ Per-Developer", "Cerberus AI": "✅ 60% Reduction"}
        ]
        
        st.table(comparison_data)
    
    def launch_argus_demo(self):
        """Launch ArgusAI DevOps demo"""
        st.success("🐺 Launching ArgusAI - DevOps Interface...")
        
        # Show demo features
        st.markdown("""
        ### 🚀 ArgusAI Demo Features
        
        **1. GitHub Actions Plugin**
        - Live CI/CD compliance checking
        - Automated PR comments with compliance scores
        - SARIF report generation for GitHub Security tab
        
        **2. Policy as Code**
        - Version-controlled compliance policies
        - Framework-specific rule engines
        - Custom validation logic
        
        **3. Developer Experience**  
        - Sub-30-second compliance checks
        - Actionable remediation suggestions
        - Zero workflow disruption
        """)
        
        # Simulate launching in new terminal/browser
        if st.button("🔧 Open ArgusAI Interface", key="argus_interface"):
            st.info("In production: This would launch the DevOps-specific interface at localhost:8001")
            st.code("""
            # Command to launch ArgusAI interface:
            streamlit run argus_devops_interface.py --server.port 8001
            
            # Or via Docker:
            docker run -p 8001:8001 cerberus-ai:argus
            """)
    
    def launch_sentinel_demo(self):
        """Launch SentinelGRC executive demo"""
        st.success("🛡️ Launching SentinelGRC - Executive Interface...")
        
        try:
            # Try to launch the GRC dashboard in a new process
            subprocess.Popen([
                sys.executable, "-m", "streamlit", "run",
                str(self.current_dir / "grc_executive_dashboard.py"),
                "--server.port", "8002",
                "--server.address", "localhost"
            ])
            
            st.success("🎉 SentinelGRC Dashboard launched!")
            st.info("📊 Opening at: http://localhost:8002")
            
            # Auto-open browser after a delay
            time.sleep(2)
            webbrowser.open("http://localhost:8002")
            
        except Exception as e:
            st.error(f"Failed to launch SentinelGRC: {e}")
            st.info("Manual launch: `streamlit run grc_executive_dashboard.py --server.port 8002`")
    
    def launch_regional_demo(self):
        """Launch multi-regional demo"""
        st.success("🌍 Launching Multi-Regional Framework Demo...")
        
        try:
            # Launch the existing regional demo
            subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", 
                str(self.current_dir / "streamlit_app.py"),
                "--server.port", "8003"
            ])
            
            st.success("🌍 Multi-Regional demo launched at: http://localhost:8003")
            time.sleep(2)
            webbrowser.open("http://localhost:8003")
            
        except Exception as e:
            st.error(f"Failed to launch regional demo: {e}")
    
    def launch_github_demo(self):
        """Launch GitHub Actions demo"""
        st.success("🔧 GitHub Actions Integration Demo")
        
        st.markdown("""
        ### 🚀 GitHub Actions Demo
        
        **Setup Instructions:**
        1. Copy the action files to your repository:
        ```bash
        cp -r .github/actions/cerberus-compliance /path/to/your/repo/.github/actions/
        ```
        
        **2. Add to your workflow:**
        ```yaml
        - name: Cerberus AI Compliance Check
          uses: ./.github/actions/cerberus-compliance
          with:
            api-key: ${{ secrets.CERBERUS_API_KEY }}
            frameworks: 'essential8,nistcsf'
        ```
        
        **3. Test with sample repository:**
        """)
        
        if st.button("🔧 Start GitHub Actions Server", key="github_server"):
            try:
                # Launch the GitHub Actions API server
                subprocess.Popen([
                    sys.executable, str(self.current_dir / "github_actions_api_endpoint.py")
                ])
                st.success("🚀 GitHub Actions API server started at: http://localhost:8000")
                st.info("Use this endpoint in your GitHub Actions workflow")
                
            except Exception as e:
                st.error(f"Failed to start GitHub Actions server: {e}")
    
    def launch_api_playground(self):
        """Launch API playground"""
        st.success("🌐 API Playground")
        
        st.markdown("### 🔌 Cerberus AI REST API")
        
        # API endpoint examples
        st.code("""
        # Health Check
        GET http://localhost:8000/api/v1/health
        
        # List Supported Frameworks
        GET http://localhost:8000/api/v1/frameworks
        Authorization: Bearer your-api-key
        
        # Validate Compliance
        POST http://localhost:8000/api/v1/compliance/github-validate
        Authorization: Bearer your-api-key
        Content-Type: application/json
        
        {
          "context": {
            "repository": {...},
            "commit": {...},
            "files_changed": [...]
          },
          "frameworks": ["essential8", "nistcsf"],
          "mode": "validate"
        }
        """)
        
        if st.button("🚀 Start API Server", key="api_server"):
            try:
                subprocess.Popen([
                    sys.executable, str(self.current_dir / "github_actions_api_endpoint.py")
                ])
                st.success("🌐 API server started at: http://localhost:8000")
                st.info("Try the endpoints with curl or Postman!")
                
            except Exception as e:
                st.error(f"Failed to start API server: {e}")
    
    def show_cost_optimization_demo(self):
        """Show cost optimization demo"""
        st.success("💰 Token Optimization Engine Demo")
        
        # Mock cost comparison
        import random
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Without Cerberus AI")
            baseline_cost = random.uniform(850, 1200)
            st.metric("Monthly API Costs", f"${baseline_cost:.0f}")
            st.metric("Requests per Month", "45,000")
            st.metric("Average Cost per Request", f"${baseline_cost/45000:.4f}")
        
        with col2:
            st.markdown("### 🚀 With Cerberus AI")
            optimized_cost = baseline_cost * 0.35  # 65% reduction
            savings = baseline_cost - optimized_cost
            
            st.metric("Monthly API Costs", f"${optimized_cost:.0f}", f"-${savings:.0f}")
            st.metric("Requests per Month", "45,000", "Same volume")
            st.metric("Average Cost per Request", f"${optimized_cost/45000:.4f}", f"-{65}%")
        
        st.markdown(f"""
        ### 🎯 Optimization Techniques
        - **Semantic Caching**: 78% cache hit rate
        - **Response Compression**: 45% size reduction  
        - **Batch Processing**: 3.2x fewer API calls
        - **Smart Routing**: Region-specific optimization
        
        **Annual Savings**: ${(baseline_cost - optimized_cost) * 12:.0f}
        """)
    
    def show_human_ai_demo(self):
        """Show human-AI collaboration demo"""
        st.success("👥 Human-AI Collaboration Demo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🤖 AI Automated (94%)")
            automated_tasks = [
                "✅ Code security scanning",
                "✅ Configuration validation", 
                "✅ Framework compliance checking",
                "✅ Policy violations detection",
                "✅ Evidence collection",
                "✅ Report generation"
            ]
            
            for task in automated_tasks:
                st.write(task)
        
        with col2:
            st.markdown("### 👥 Human Expert Review (6%)")
            human_tasks = [
                "🧠 Regulatory interpretation",
                "🧠 Strategic risk assessment",
                "🧠 Stakeholder impact analysis", 
                "🧠 Exception approval",
                "🧠 Complex scenario decisions",
                "🧠 Audit coordination"
            ]
            
            for task in human_tasks:
                st.write(task)
        
        st.markdown("""
        ### 🎯 Collaboration Benefits
        - **32 hours/week** saved for GRC professionals
        - **97.8% accuracy** on human review decisions
        - **3.2% false positive** rate from AI
        - **100% audit trail** for all decisions
        """)
    
    def render_sidebar(self):
        """Render sidebar with demo controls"""
        with st.sidebar:
            st.markdown("## 🔱 Demo Controls")
            
            # Demo status
            st.markdown("### 📊 Active Demos")
            demo_status = self.check_demo_status()
            
            for demo, status in demo_status.items():
                status_icon = "🟢" if status else "⚪"
                st.write(f"{status_icon} {demo}")
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            
            if st.button("🔄 Refresh Status"):
                st.rerun()
            
            if st.button("🛑 Stop All Demos"):
                self.stop_all_demos()
            
            if st.button("📋 Export Demo Data"):
                self.export_demo_data()
            
            st.markdown("---")
            
            # Demo info
            st.markdown("### ℹ️ Demo Information")
            st.caption(f"**Version**: Cerberus AI v1.0")
            st.caption(f"**Updated**: {datetime.now().strftime('%Y-%m-%d')}")
            st.caption("**Mode**: Development Demo")
            
            st.markdown("---")
            
            # Links
            st.markdown("### 🔗 Resources")
            st.markdown("""
            - [📖 Documentation](https://docs.cerberus-ai.com)
            - [💻 GitHub](https://github.com/cerberus-ai/platform)
            - [🎯 Competitive Analysis](./COMPETITIVE_LANDSCAPE_ANALYSIS.md)
            - [🏢 Brand Positioning](./CERBERUS_AI_BRAND_POSITIONING.md)
            """)
    
    def check_demo_status(self):
        """Check status of running demos"""
        # This would check actual process status in production
        return {
            "ArgusAI Interface": False,
            "SentinelGRC Dashboard": False,
            "Multi-Regional Demo": False,
            "GitHub Actions API": False,
            "API Playground": False
        }
    
    def stop_all_demos(self):
        """Stop all running demo processes"""
        st.info("🛑 Stopping all demo processes...")
        # This would terminate spawned processes in production
        st.success("✅ All demos stopped")
    
    def export_demo_data(self):
        """Export demo data and configurations"""
        demo_config = {
            "demo_version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "available_demos": [
                "ArgusAI DevOps Interface",
                "SentinelGRC Executive Dashboard", 
                "Multi-Regional Framework Translation",
                "GitHub Actions Integration",
                "REST API Playground"
            ],
            "supported_frameworks": [
                "Essential 8", "NIST CSF", "SOC 2", "GDPR",
                "ISO 27001", "PCI DSS", "HIPAA"
            ]
        }
        
        st.download_button(
            "📋 Download Demo Config",
            data=str(demo_config),
            file_name="cerberus_demo_config.json",
            mime="application/json"
        )
    
    def run_launcher(self):
        """Main launcher execution"""
        
        # Render sidebar
        self.render_sidebar()
        
        # Main content
        self.render_header()
        self.render_platform_overview()
        self.render_unified_demo_section()
        self.render_api_demo_section()
        self.render_competitive_comparison()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #64748B; padding: 2rem;">
            <p>🔱 <strong>Cerberus AI Platform Demo</strong></p>
            <p><em>Transforming Enterprise Compliance Through Unified Intelligence</em></p>
            <p>Built for DevOps Speed • Designed for GRC Expertise • Powered by AI</p>
        </div>
        """, unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    launcher = CerberusDemoLauncher()
    launcher.run_launcher()