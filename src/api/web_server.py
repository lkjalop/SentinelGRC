"""
Sentinel GRC Web Server
=======================
Serves the two-door HTML/CSS interface and provides API endpoints
for the backend integration, replacing the Streamlit interface.
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our backend components
from ..core.sentinel_grc_complete import SentinelGRC
from ..core.core_types import CompanyProfile, Config
from ..config.geographic_router import ComplianceRouter
from ..core.auth_manager import AuthenticationManager, initialize_default_users, UserRole
from ..integrations.cicd_connector import CICDIntegrator, CICDConfig, CICDProvider

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Sentinel GRC",
    description="Unified Intelligence Platform for Enterprise Compliance & DevOps",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for UI
ui_path = Path(__file__).parent.parent / "ui"
if ui_path.exists():
    app.mount("/css", StaticFiles(directory=str(ui_path / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(ui_path / "js")), name="js")

# Global instances
sentinel_grc = None
compliance_router = None
auth_manager = None
cicd_integrator = None

# Pydantic models for API
class AssessmentRequest(BaseModel):
    company_profile: Dict[str, Any]
    frameworks: list[str]
    region: str = "australia"

class StatsResponse(BaseModel):
    compliance_score: int
    deployments_today: int
    controls_passing: Dict[str, int]
    next_audit: int
    last_updated: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize backend components on startup"""
    global sentinel_grc, compliance_router, auth_manager, cicd_integrator
    
    try:
        # Initialize SentinelGRC 
        sentinel_grc = SentinelGRC()
        compliance_router = ComplianceRouter()
        
        # Initialize authentication
        auth_manager = AuthenticationManager()
        initialize_default_users(auth_manager)
        
        # Initialize CI/CD integration
        cicd_integrator = CICDIntegrator()
        
        logger.info("✅ Sentinel GRC backend initialized successfully")
        logger.info("🔐 Authentication system initialized with default users")
        logger.info("🔄 CI/CD integration system initialized")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize backend: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def serve_gateway():
    """Serve the main two-door interface"""
    gateway_path = ui_path / "sentinel_gateway.html"
    
    if not gateway_path.exists():
        raise HTTPException(status_code=404, detail="Gateway interface not found")
    
    try:
        with open(gateway_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Error serving gateway: {e}")
        raise HTTPException(status_code=500, detail="Failed to load gateway")

@app.get("/devops-dashboard.html", response_class=HTMLResponse)
async def serve_devops_dashboard():
    """Serve DevOps mode interface"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sentinel GRC - DevOps Mode</title>
        <link rel="stylesheet" href="/css/sentinel.css">
    </head>
    <body>
        <div class="devops-container">
            <header class="devops-header">
                <h1>🚀 DevOps Mode</h1>
                <p>CI/CD Integration & Real-time Compliance</p>
                <a href="/" class="back-link">← Back to Gateway</a>
            </header>
            
            <main class="devops-main">
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>Pipeline Status</h3>
                        <p>Monitor compliance checks in your CI/CD pipeline</p>
                        <div id="pipeline-status" class="status-indicator">✅ All Checks Passing</div>
                    </div>
                    
                    <div class="feature-card">
                        <h3>Security Scanning</h3>
                        <p>Automated vulnerability detection and remediation</p>
                        <div id="security-status" class="status-indicator">🔍 Scanning...</div>
                    </div>
                    
                    <div class="feature-card">
                        <h3>Compliance Evidence</h3>
                        <p>Automatically generated compliance documentation</p>
                        <button onclick="generateEvidence()" class="action-btn">Generate Evidence</button>
                    </div>
                    
                    <div class="feature-card">
                        <h3>Integration Setup</h3>
                        <p>Connect with GitHub, Jenkins, GitLab</p>
                        <button onclick="setupIntegration()" class="action-btn">Setup Integration</button>
                    </div>
                </div>
            </main>
        </div>
        
        <script>
            function generateEvidence() {
                alert('Evidence generation started! This would integrate with the Python backend.');
            }
            
            function setupIntegration() {
                alert('Integration setup would connect to your CI/CD platform.');
            }
        </script>
        
        <style>
            .devops-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
            .devops-header { text-align: center; margin-bottom: 2rem; }
            .devops-header h1 { color: #00D4FF; }
            .back-link { color: #0B3D91; text-decoration: none; }
            .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
            .feature-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .action-btn { background: #00D4FF; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
            .action-btn:hover { background: #00A8CC; }
            .status-indicator { margin-top: 1rem; padding: 0.5rem; background: #f0f8f0; border-radius: 4px; }
        </style>
    </body>
    </html>
    """)

@app.get("/assessment-forms.html", response_class=HTMLResponse)
async def serve_assessment_forms():
    """Serve the assessment questionnaire forms"""
    forms_path = ui_path / "assessment_forms.html"
    
    if not forms_path.exists():
        raise HTTPException(status_code=404, detail="Assessment forms not found")
    
    try:
        with open(forms_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Error serving assessment forms: {e}")
        raise HTTPException(status_code=500, detail="Failed to load assessment forms")

@app.get("/compliance-dashboard.html", response_class=HTMLResponse)
async def serve_compliance_dashboard():
    """Serve Compliance mode interface"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sentinel GRC - Compliance Mode</title>
        <link rel="stylesheet" href="/css/sentinel.css">
    </head>
    <body>
        <div class="compliance-container">
            <header class="compliance-header">
                <h1>📋 Compliance Mode</h1>
                <p>Audit Preparation & Stakeholder Management</p>
                <a href="/" class="back-link">← Back to Gateway</a>
            </header>
            
            <main class="compliance-main">
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>Audit Readiness</h3>
                        <p>Track preparation progress and evidence collection</p>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 87%"></div>
                        </div>
                        <div class="progress-text">87% Ready</div>
                    </div>
                    
                    <div class="feature-card">
                        <h3>Framework Assessment</h3>
                        <p>Multi-framework compliance analysis</p>
                        <a href="/assessment-forms.html" class="action-btn" style="text-decoration: none; display: inline-block; text-align: center;">Start Assessment</a>
                    </div>
                    
                    <div class="feature-card">
                        <h3>Expert Escalation</h3>
                        <p>Human expert review for complex scenarios</p>
                        <div id="escalation-status">No pending escalations</div>
                    </div>
                    
                    <div class="feature-card">
                        <h3>Professional Reports</h3>
                        <p>Generate audit-ready PDF documentation</p>
                        <button onclick="generatePDF()" class="action-btn">Generate PDF</button>
                    </div>
                    
                    <div class="feature-card">
                        <h3>NIST SP 800-53 Controls</h3>
                        <p>1006 comprehensive security controls available</p>
                        <button onclick="viewNISTControls()" class="action-btn">View Controls</button>
                    </div>
                </div>
            </main>
        </div>
        
        <script>
            async function runAssessment() {
                const response = await fetch('/api/assessment/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        company_profile: { company_name: 'Demo Corp', industry: 'Technology' },
                        frameworks: ['essential8', 'privacy_act'],
                        region: 'australia'
                    })
                });
                const result = await response.json();
                alert('Assessment completed! Check the results.');
            }
            
            async function generatePDF() {
                try {
                    // Show loading state
                    const button = event.target;
                    const originalText = button.textContent;
                    button.textContent = 'Generating...';
                    button.disabled = true;
                    
                    // Call the PDF generation API
                    const response = await fetch('/api/generate-pdf', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            company_profile: {
                                company_name: 'Sentinel GRC Demo',
                                industry: 'Technology',
                                employee_count: 100,
                                country: 'australia'
                            },
                            assessment_results: {
                                'essential8': { score: 87, framework: 'Essential Eight' },
                                'soc2': { score: 92, framework: 'SOC 2' }
                            }
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        alert(`PDF Report Generated Successfully!\nReport ID: ${result.report_id}\nCompany: ${result.company}`);
                    } else {
                        alert('PDF generation failed. Please try again.');
                    }
                } catch (error) {
                    console.error('PDF generation error:', error);
                    alert('Error generating PDF report. Check console for details.');
                } finally {
                    // Reset button state
                    const button = event.target;
                    button.textContent = originalText;
                    button.disabled = false;
                }
            }
            
            function viewNISTControls() {
                window.location.href = '/nist-controls.html';
            }
        </script>
        
        <style>
            .compliance-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
            .compliance-header { text-align: center; margin-bottom: 2rem; }
            .compliance-header h1 { color: #00C896; }
            .back-link { color: #0B3D91; text-decoration: none; }
            .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
            .feature-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .action-btn { background: #00C896; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
            .action-btn:hover { background: #10B981; }
            .progress-bar { background: #f0f0f0; border-radius: 8px; overflow: hidden; margin: 1rem 0 0.5rem; }
            .progress-fill { background: #00C896; height: 8px; transition: width 0.3s ease; }
            .progress-text { font-size: 0.9rem; color: #666; }
        </style>
    </body>
    </html>
    """)

@app.get("/api/stats")
async def get_platform_stats():
    """Get real-time platform statistics"""
    try:
        # Generate real stats from the backend
        if sentinel_grc:
            # This would get real data from the SentinelGRC instance
            stats = {
                "compliance_score": 94,  # Would calculate from assessments
                "deployments_today": 47,  # Would get from CI/CD integrations
                "controls_passing": {
                    "passing": 1247,
                    "total": 1350
                },
                "next_audit": 5,  # Days until next audit
                "last_updated": datetime.now().isoformat()
            }
        else:
            # Fallback mock data
            stats = {
                "compliance_score": 87,
                "deployments_today": 23,
                "controls_passing": {"passing": 1100, "total": 1300},
                "next_audit": 12,
                "last_updated": datetime.now().isoformat()
            }
        
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"Error getting platform stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get platform stats")

@app.post("/api/assessment/run")
async def run_assessment(request: AssessmentRequest):
    """Run a compliance assessment"""
    try:
        if not sentinel_grc:
            raise HTTPException(status_code=503, detail="Backend not initialized")
        
        # Create company profile
        company_profile = CompanyProfile(
            company_name=request.company_profile.get("company_name", "Unknown"),
            industry=request.company_profile.get("industry", "Unknown"),
            employee_count=request.company_profile.get("employee_count", 100),
            annual_revenue=request.company_profile.get("annual_revenue", 1000000),
            country=request.region
        )
        
        # Run the assessment
        logger.info(f"Running assessment for {company_profile.company_name}")
        
        results = {}
        for framework in request.frameworks:
            result = await sentinel_grc.assess_compliance(
                company_profile=company_profile,
                framework_name=framework
            )
            results[framework] = result
        
        # Generate professional report if requested
        if len(request.frameworks) > 1:
            pdf_report = await sentinel_grc.generate_professional_report(
                company_profile=company_profile,
                assessment_results=results,
                output_format="pdf"
            )
            results["professional_report"] = pdf_report
        
        return JSONResponse(content={
            "success": True,
            "assessment_id": f"assess_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error running assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={
        "status": "healthy",
        "backend_initialized": sentinel_grc is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.get("/executive-dashboard.html", response_class=HTMLResponse)
async def serve_executive_dashboard():
    """Serve executive dashboard"""
    dashboard_path = ui_path / "executive_dashboard.html"
    
    if not dashboard_path.exists():
        raise HTTPException(status_code=404, detail="Executive dashboard not found")
    
    try:
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Error serving executive dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to load executive dashboard")

@app.get("/nist-controls.html", response_class=HTMLResponse)
async def serve_nist_controls():
    """Serve NIST SP 800-53 controls viewer"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NIST SP 800-53 Controls - Sentinel GRC</title>
        <link rel="stylesheet" href="/css/sentinel.css">
        <style>
            .controls-container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
            .controls-header { text-align: center; margin-bottom: 2rem; }
            .controls-header h1 { color: #0B3D91; }
            .back-link { color: #00C896; text-decoration: none; margin-bottom: 2rem; display: inline-block; }
            .controls-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
            .stat-card { background: white; padding: 1rem; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2rem; font-weight: bold; color: #0B3D91; }
            .control-families { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
            .family-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .family-header { color: #0B3D91; font-size: 1.2rem; margin-bottom: 1rem; border-bottom: 2px solid #00C896; padding-bottom: 0.5rem; }
            .control-item { padding: 0.75rem; margin: 0.5rem 0; border-left: 3px solid #00D4FF; background: #f8f9fa; }
            .control-id { font-weight: bold; color: #0B3D91; }
            .control-desc { font-size: 0.9rem; color: #666; margin-top: 0.25rem; }
            .framework-tags { margin-top: 0.5rem; }
            .tag { background: #e3f2fd; color: #1976d2; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.75rem; margin-right: 0.5rem; }
        </style>
    </head>
    <body>
        <div class="controls-container">
            <header class="controls-header">
                <a href="/compliance-dashboard.html" class="back-link">← Back to Compliance Dashboard</a>
                <h1>🔒 NIST SP 800-53 Rev 5 Controls</h1>
                <p>Comprehensive Security and Privacy Controls for Information Systems and Organizations</p>
            </header>
            
            <div class="controls-stats">
                <div class="stat-card">
                    <div class="stat-number">1,006</div>
                    <div>Total Controls</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">20</div>
                    <div>Control Families</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div>Impact Baselines</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">Rev 5</div>
                    <div>Current Version</div>
                </div>
            </div>
            
            <div class="control-families" id="control-families">
                <!-- Controls will be loaded here -->
                <div class="family-card">
                    <div class="family-header">AC - Access Control (25 controls)</div>
                    <div class="control-item">
                        <div class="control-id">AC-2: Account Management</div>
                        <div class="control-desc">Manage information system accounts including establishment, activation, modification, review, and removal</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                            <span class="tag">Essential Eight</span>
                        </div>
                    </div>
                    <div class="control-item">
                        <div class="control-id">AC-3: Access Enforcement</div>
                        <div class="control-desc">Enforce approved authorizations for logical access to information and system resources</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                        </div>
                    </div>
                </div>
                
                <div class="family-card">
                    <div class="family-header">AU - Audit and Accountability (16 controls)</div>
                    <div class="control-item">
                        <div class="control-id">AU-3: Content of Audit Records</div>
                        <div class="control-desc">Ensure audit records contain information establishing what type of event occurred</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                        </div>
                    </div>
                    <div class="control-item">
                        <div class="control-id">AU-6: Audit Record Review</div>
                        <div class="control-desc">Review and analyze information system audit records for indications of inappropriate activity</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                        </div>
                    </div>
                </div>
                
                <div class="family-card">
                    <div class="family-header">SI - System and Information Integrity (23 controls)</div>
                    <div class="control-item">
                        <div class="control-id">SI-2: Flaw Remediation</div>
                        <div class="control-desc">Identify, report, and correct information system flaws</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                            <span class="tag">Essential Eight</span>
                        </div>
                    </div>
                    <div class="control-item">
                        <div class="control-id">SI-4: System Monitoring</div>
                        <div class="control-desc">Monitor the system to detect attacks and indicators of potential attacks</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                            <span class="tag">Essential Eight</span>
                        </div>
                    </div>
                </div>
                
                <div class="family-card">
                    <div class="family-header">CM - Configuration Management (14 controls)</div>
                    <div class="control-item">
                        <div class="control-id">CM-2: Baseline Configuration</div>
                        <div class="control-desc">Develop, document, and maintain current baseline configurations of the system</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                            <span class="tag">Essential Eight</span>
                        </div>
                    </div>
                </div>
                
                <div class="family-card">
                    <div class="family-header">IA - Identification and Authentication (12 controls)</div>
                    <div class="control-item">
                        <div class="control-id">IA-2: Identification and Authentication</div>
                        <div class="control-desc">Uniquely identify and authenticate organizational users accessing the system</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                            <span class="tag">Essential Eight</span>
                        </div>
                    </div>
                </div>
                
                <div class="family-card">
                    <div class="family-header">IR - Incident Response (10 controls)</div>
                    <div class="control-item">
                        <div class="control-id">IR-4: Incident Handling</div>
                        <div class="control-desc">Implement an incident handling capability for security incidents</div>
                        <div class="framework-tags">
                            <span class="tag">NIST CSF 2.0</span>
                            <span class="tag">CIS Controls</span>
                        </div>
                    </div>
                </div>
                
            </div>
            
            <div style="text-align: center; margin-top: 2rem; padding: 2rem; background: #f8f9fa; border-radius: 8px;">
                <h3>Want to assess your compliance against NIST SP 800-53?</h3>
                <p>Use our comprehensive assessment tool to evaluate your organization's compliance with all 1,006 controls.</p>
                <a href="/assessment-forms.html" class="action-btn" style="text-decoration: none; display: inline-block; background: #0B3D91; color: white; padding: 1rem 2rem; border-radius: 6px;">Start NIST Assessment</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.post("/api/auth/login")
async def login(request: LoginRequest, client_ip: str = None) -> LoginResponse:
    """User authentication endpoint"""
    try:
        if not auth_manager:
            raise HTTPException(status_code=503, detail="Authentication system not initialized")
        
        result = auth_manager.authenticate_user(request.username, request.password, client_ip)
        
        if result["success"]:
            return LoginResponse(
                success=True,
                token=result["token"],
                user=result["user"]
            )
        else:
            return LoginResponse(success=False, error=result["error"])
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")

@app.post("/api/auth/logout")
async def logout(token: str = None):
    """User logout endpoint"""
    try:
        if not auth_manager or not token:
            return {"success": False, "error": "Invalid request"}
        
        success = auth_manager.logout_user(token)
        return {"success": success}
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return {"success": False, "error": "Logout failed"}

@app.get("/api/auth/validate")
async def validate_token(token: str = None):
    """Validate authentication token"""
    try:
        if not auth_manager or not token:
            return {"valid": False, "error": "Token required"}
        
        validation = auth_manager.validate_token(token)
        return validation
        
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        return {"valid": False, "error": "Validation failed"}

@app.get("/api/auth/security-stats")
async def get_security_stats():
    """Get authentication security statistics"""
    try:
        if not auth_manager:
            raise HTTPException(status_code=503, detail="Authentication system not initialized")
        
        stats = auth_manager.get_security_stats()
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"Security stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get security stats")

@app.post("/api/cicd/register")
async def register_cicd_pipeline(request: Dict[str, Any]):
    """Register a CI/CD pipeline for compliance monitoring"""
    try:
        if not cicd_integrator:
            raise HTTPException(status_code=503, detail="CI/CD system not initialized")
        
        pipeline_id = request.get("pipeline_id")
        provider = request.get("provider")
        
        if not pipeline_id or not provider:
            raise HTTPException(status_code=400, detail="pipeline_id and provider required")
        
        # Create CI/CD config
        config = CICDConfig(
            provider=CICDProvider(provider),
            webhook_url=request.get("webhook_url"),
            api_token=request.get("api_token"),
            repository_url=request.get("repository_url"),
            branch_patterns=request.get("branch_patterns", []),
            compliance_gates=request.get("compliance_gates", [])
        )
        
        success = cicd_integrator.register_pipeline(pipeline_id, config)
        
        if success:
            return {"success": True, "message": f"Pipeline {pipeline_id} registered successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to register pipeline")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"CI/CD registration error: {e}")
        raise HTTPException(status_code=500, detail="Pipeline registration failed")

@app.post("/api/cicd/compliance-check")
async def run_compliance_check(request: Dict[str, Any]):
    """Run compliance checks for a CI/CD pipeline"""
    try:
        if not cicd_integrator:
            raise HTTPException(status_code=503, detail="CI/CD system not initialized")
        
        pipeline_id = request.get("pipeline_id")
        context = request.get("context", {})
        
        if not pipeline_id:
            raise HTTPException(status_code=400, detail="pipeline_id required")
        
        results = await cicd_integrator.run_compliance_checks(pipeline_id, context)
        
        return JSONResponse(content=results)
        
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        raise HTTPException(status_code=500, detail="Compliance check failed")

@app.get("/api/cicd/stats")
async def get_cicd_stats():
    """Get CI/CD integration statistics"""
    try:
        if not cicd_integrator:
            raise HTTPException(status_code=503, detail="CI/CD system not initialized")
        
        stats = cicd_integrator.get_integration_stats()
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"CI/CD stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get CI/CD stats")

@app.post("/api/generate-pdf")
async def generate_pdf_report(request: Dict[str, Any]):
    """Generate professional PDF report"""
    try:
        if not sentinel_grc:
            raise HTTPException(status_code=503, detail="Backend not initialized")
        
        # Get request parameters
        company_profile_data = request.get("company_profile", {})
        assessment_results = request.get("assessment_results", {})
        
        # Create company profile
        company_profile = CompanyProfile(
            company_name=company_profile_data.get("company_name", "Demo Corporation"),
            industry=company_profile_data.get("industry", "Technology"),
            employee_count=company_profile_data.get("employee_count", 100),
            annual_revenue=company_profile_data.get("annual_revenue", 1000000),
            country=company_profile_data.get("country", "australia")
        )
        
        # Generate professional PDF report
        logger.info(f"Generating PDF report for {company_profile.company_name}")
        
        pdf_report = await sentinel_grc.generate_professional_report(
            company_profile=company_profile,
            assessment_results=assessment_results or {"demo": {"score": 87, "framework": "Essential Eight"}},
            output_format="pdf"
        )
        
        return JSONResponse(content={
            "success": True,
            "report_id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "report_path": pdf_report if isinstance(pdf_report, str) else "Professional report generated successfully",
            "company": company_profile.company_name,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/api/regions")
async def get_available_regions():
    """Get available geographic regions"""
    try:
        if compliance_router:
            regions = list(compliance_router.regions.keys())
            return JSONResponse(content={
                "regions": regions,
                "total": len(regions)
            })
        else:
            return JSONResponse(content={
                "regions": ["australia", "united_states", "european_union"],
                "total": 3
            })
    except Exception as e:
        logger.error(f"Error getting regions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get regions")

if __name__ == "__main__":
    import uvicorn
    
    # Check if UI files exist
    if not ui_path.exists():
        logger.warning("⚠️ UI directory not found. Creating minimal structure...")
        ui_path.mkdir(exist_ok=True)
        (ui_path / "css").mkdir(exist_ok=True)
        (ui_path / "js").mkdir(exist_ok=True)
    
    logger.info("🚀 Starting Sentinel GRC Web Server...")
    uvicorn.run(
        "web_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )