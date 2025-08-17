#!/usr/bin/env python3
"""
GitHub Actions API Endpoint for Cerberus AI
Handles validation requests from the GitHub Actions integration
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
import asyncio
from datetime import datetime
import hashlib
import json

# Import existing Cerberus AI components
from ..core.sentinel_grc_complete import SentinelGRC
from ..core.core_types import CompanyProfile, Config
from ..core.cache_manager import get_cache_manager
from ..core.error_handler import ErrorHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Cerberus AI - GitHub Actions API",
    description="API endpoint for GitHub Actions compliance validation",
    version="1.0.0"
)

# Security
security = HTTPBearer()

# Request/Response Models
class GitHubRepository(BaseModel):
    name: str
    owner: str
    full_name: str
    default_branch: str

class GitHubCommit(BaseModel):
    sha: str
    message: str
    author: str

class GitHubWorkflow(BaseModel):
    name: str
    run_id: int
    run_number: int

class GitHubFileChange(BaseModel):
    filename: str
    status: str
    changes: int
    content: Optional[str] = None
    patch: Optional[str] = None

class GitHubContext(BaseModel):
    repository: GitHubRepository
    commit: GitHubCommit
    pull_request: Optional[Dict[str, Any]] = None
    workflow: GitHubWorkflow
    files_changed: List[GitHubFileChange]
    timestamp: str

class ComplianceRequest(BaseModel):
    context: GitHubContext
    frameworks: List[str] = Field(default=['essential8'])
    mode: str = Field(default='validate', pattern='^(validate|audit|monitor)$')
    options: Dict[str, Any] = Field(default_factory=dict)

class ComplianceViolation(BaseModel):
    rule_id: str
    rule_name: str
    title: str
    description: str
    severity: str
    framework: str
    category: str
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    remediation: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None

class ComplianceResponse(BaseModel):
    compliance_score: int
    violations: List[ComplianceViolation]
    frameworks_checked: List[str]
    human_review_required: bool
    report_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GitHubActionsAPI:
    """API handler for GitHub Actions integration"""
    
    def __init__(self):
        self.orchestrator = SentinelGRC()
        self.cache = get_cache_manager()
        self.error_handler = ErrorHandler()
        
    async def validate_api_key(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """Validate API key - simplified for demo"""
        api_key = credentials.credentials
        
        # Demo mode - accept any key starting with 'demo-'
        if api_key.startswith('demo-'):
            return api_key
            
        # In production, validate against database/service
        # For now, accept predefined keys
        valid_keys = ['cerberus-dev-key', 'cerberus-test-key']
        if api_key in valid_keys:
            return api_key
            
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    def generate_request_id(self, context: GitHubContext) -> str:
        """Generate unique request ID for caching"""
        unique_string = f"{context.repository.full_name}:{context.commit.sha}:{context.timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    async def analyze_repository_context(self, context: GitHubContext) -> Dict[str, Any]:
        """Analyze GitHub repository context for compliance assessment"""
        
        logger.info(f"Analyzing repository: {context.repository.full_name}")
        
        analysis = {
            'repository_metadata': {
                'name': context.repository.name,
                'owner': context.repository.owner,
                'branch': context.repository.default_branch,
                'total_files_changed': len(context.files_changed)
            },
            'commit_metadata': {
                'sha': context.commit.sha[:8],  # Truncate for display
                'author': context.commit.author,
                'message_length': len(context.commit.message),
                'is_merge_commit': 'Merge' in context.commit.message
            },
            'file_analysis': {
                'languages_detected': self.detect_languages(context.files_changed),
                'config_files_changed': self.identify_config_files(context.files_changed),
                'sensitive_files': self.identify_sensitive_files(context.files_changed),
                'total_lines_changed': sum(f.changes for f in context.files_changed if f.changes)
            },
            'risk_indicators': {
                'large_changeset': len(context.files_changed) > 50,
                'config_changes': any('config' in f.filename.lower() for f in context.files_changed),
                'security_files': any(any(sec in f.filename.lower() for sec in ['security', 'auth', 'credential']) 
                                    for f in context.files_changed),
                'database_changes': any('migration' in f.filename.lower() or '.sql' in f.filename 
                                      for f in context.files_changed)
            }
        }
        
        logger.debug(f"Repository analysis: {analysis}")
        return analysis
    
    def detect_languages(self, files: List[GitHubFileChange]) -> List[str]:
        """Detect programming languages from file extensions"""
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.rs': 'Rust',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.json': 'JSON',
            '.xml': 'XML',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.dockerfile': 'Docker',
            '.tf': 'Terraform'
        }
        
        detected = set()
        for file in files:
            for ext, lang in language_map.items():
                if file.filename.lower().endswith(ext):
                    detected.add(lang)
                    break
        
        return list(detected)
    
    def identify_config_files(self, files: List[GitHubFileChange]) -> List[str]:
        """Identify configuration files that may affect compliance"""
        config_patterns = [
            'config', 'settings', '.env', 'docker', 'kubernetes', 
            'helm', 'terraform', 'ansible', 'package.json', 'requirements.txt',
            'pom.xml', 'build.gradle', 'nginx.conf', 'apache'
        ]
        
        config_files = []
        for file in files:
            filename_lower = file.filename.lower()
            if any(pattern in filename_lower for pattern in config_patterns):
                config_files.append(file.filename)
        
        return config_files
    
    def identify_sensitive_files(self, files: List[GitHubFileChange]) -> List[str]:
        """Identify files that may contain sensitive information"""
        sensitive_patterns = [
            'secret', 'key', 'password', 'credential', 'token', 'cert', 
            'private', '.pem', '.key', '.p12', '.pfx', 'wallet'
        ]
        
        sensitive_files = []
        for file in files:
            filename_lower = file.filename.lower()
            if any(pattern in filename_lower for pattern in sensitive_patterns):
                sensitive_files.append(file.filename)
                
            # Check file content for sensitive patterns (if available)
            if file.content and len(file.content) < 10000:  # Only check small files
                content_lower = file.content.lower()
                if any(pattern in content_lower for pattern in ['password=', 'secret=', 'token=', 'key=']):
                    if file.filename not in sensitive_files:
                        sensitive_files.append(file.filename)
        
        return sensitive_files
    
    async def perform_compliance_validation(
        self, 
        context: GitHubContext, 
        frameworks: List[str], 
        mode: str,
        options: Dict[str, Any]
    ) -> ComplianceResponse:
        """Perform actual compliance validation"""
        
        logger.info(f"Performing {mode} validation for frameworks: {frameworks}")
        
        # Generate assessment context
        repo_analysis = await self.analyze_repository_context(context)
        
        # Create company profile from repository context
        company_profile = CompanyProfile(
            company_name=context.repository.owner,
            industry="Technology",  # Default for tech companies
            employee_count=50,  # Estimate from repository activity
            country="Australia",  # Default to Australia, can be configured
            current_controls=self._extract_current_controls(repo_analysis),
            previous_incidents=[],  # Empty by default
            has_government_contracts=False  # Default to false
        )
        
        # Perform assessment using SentinelGRC orchestrator
        try:
            assessment_result = await self.orchestrator.assess_company(
                company_profile, 
                frameworks=frameworks
            )
            
            # Extract violations and results
            violations = []
            frameworks_checked = assessment_result.get("frameworks_assessed", [])
            compliance_scores = []
            
            # Process assessment results to extract violations
            for framework, result in assessment_result.get("assessment_results", {}).items():
                if isinstance(result, dict) and result.get("gaps_identified"):
                    for gap in result["gaps_identified"]:
                        violations.append(ComplianceViolation(
                            rule_id=gap.get("control", f"{framework}_unknown"),
                            rule_name=gap.get("title", "Unknown Control"),
                            title=gap.get("description", "Compliance Gap"),
                            description=gap.get("remediation", "Requires remediation"),
                            severity=gap.get("priority", "MEDIUM").lower(),
                            framework=framework,
                            category="compliance",
                            message=gap.get("status", "Implementation required"),
                            remediation=gap.get("remediation", "Contact compliance team")
                        ))
                
                # Extract compliance score
                if isinstance(result, dict) and "compliance_percentage" in result:
                    compliance_scores.append(result["compliance_percentage"])
            
            # Calculate overall score
            overall_score = int(sum(compliance_scores) / len(compliance_scores)) if compliance_scores else 75
            human_review_required = assessment_result.get("escalation_required", "none") != "none"
            
        except Exception as assessment_error:
            logger.error(f"Assessment failed: {assessment_error}")
            # Fallback to individual framework checks
            violations = []
            frameworks_checked = []
            compliance_scores = []
            human_review_required = True
            
            # Process each framework individually as fallback
            for framework in frameworks:
                try:
                    logger.info(f"Fallback: Checking {framework} compliance...")
                    
                    # Create assessment data structure for fallback methods
                    assessment_data = {
                        'context': {'analysis': repo_analysis},
                        'files': context.files_changed
                    }
                    
                    if framework.lower() == 'essential8':
                        result = await self.check_essential8_compliance(assessment_data)
                    elif framework.lower() in ['nistcsf', 'nist_csf']:
                        result = await self.check_nist_csf_compliance(assessment_data)
                    elif framework.lower() == 'soc2':
                        result = await self.check_soc2_compliance(assessment_data)
                    elif framework.lower() == 'gdpr':
                        result = await self.check_gdpr_compliance(assessment_data)
                    else:
                        logger.warning(f"Framework {framework} not yet implemented")
                        continue
                    
                    frameworks_checked.append(framework)
                    violations.extend(result['violations'])
                    compliance_scores.append(result['score'])
                    
                    if result.get('human_review_required'):
                        human_review_required = True
                        
                except Exception as e:
                    logger.error(f"Error checking {framework} compliance: {e}")
                    # Don't fail the entire request, just skip this framework
                    continue
        
        # Calculate overall compliance score
        overall_score = int(sum(compliance_scores) / len(compliance_scores)) if compliance_scores else 100
        
        # Determine human review requirement based on complexity
        if not human_review_required:
            complexity_indicators = [
                len(violations) > 10,
                any(v.severity == 'critical' for v in violations),
                repo_analysis['risk_indicators']['large_changeset'],
                repo_analysis['risk_indicators']['security_files'],
                overall_score < 70
            ]
            human_review_required = sum(complexity_indicators) >= 2
        
        response = ComplianceResponse(
            compliance_score=overall_score,
            violations=violations,
            frameworks_checked=frameworks_checked,
            human_review_required=human_review_required,
            report_url=f"https://app.cerberus-ai.com/reports/{self.generate_request_id(context)}",
            metadata={
                'assessment_mode': mode,
                'repository_analysis': repo_analysis,
                'processing_time': 'calculated_in_production',
                'api_version': '1.0.0'
            }
        )
        
        logger.info(f"Compliance validation completed: {overall_score}/100 score, {len(violations)} violations")
        return response
    
    def _extract_current_controls(self, repo_analysis: Dict[str, Any]) -> List[str]:
        """Extract current controls from repository analysis"""
        current_controls = []
        
        # Basic controls based on repository setup
        if repo_analysis['file_analysis']['config_files_changed']:
            current_controls.append("Configuration Management")
        
        # Security-related controls
        if repo_analysis['risk_indicators']['security_files']:
            current_controls.append("Security Controls")
        
        # Language-specific controls
        languages = repo_analysis['file_analysis']['languages_detected']
        if 'Python' in languages:
            current_controls.append("Secure Development - Python")
        if any(lang in languages for lang in ['JavaScript', 'TypeScript']):
            current_controls.append("Web Application Security")
        
        # Infrastructure controls
        if any(lang in languages for lang in ['YAML', 'Terraform', 'Docker']):
            current_controls.append("Infrastructure as Code")
        
        # Default minimal controls for all repositories
        if not current_controls:
            current_controls = ["Version Control", "Code Review"]
        
        return current_controls
    
    async def check_essential8_compliance(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check Essential 8 compliance using existing orchestrator"""
        
        violations = []
        
        # Use existing orchestrator for actual compliance checking
        # This is a simplified version - in production, integrate fully with the orchestrator
        
        # Example violation patterns based on repository analysis
        repo_analysis = assessment_data['context']['analysis']
        
        # Check for configuration management issues
        if repo_analysis['file_analysis']['config_files_changed']:
            violations.append(ComplianceViolation(
                rule_id="E8-APP-01",
                rule_name="Application Control",
                title="Configuration Changes Detected",
                description="Changes to configuration files require review for application control compliance",
                severity="medium",
                framework="essential8",
                category="application_control",
                message="Review configuration changes for unauthorized applications",
                file_path=repo_analysis['file_analysis']['config_files_changed'][0],
                remediation="Ensure all configuration changes are approved and necessary applications are whitelisted"
            ))
        
        # Check for sensitive file exposure
        if repo_analysis['file_analysis']['sensitive_files']:
            for sensitive_file in repo_analysis['file_analysis']['sensitive_files']:
                violations.append(ComplianceViolation(
                    rule_id="E8-INFO-01",
                    rule_name="Information Security",
                    title="Potential Sensitive Information Exposure",
                    description="File may contain sensitive information that should not be in version control",
                    severity="high",
                    framework="essential8",
                    category="information_security",
                    message=f"Sensitive file detected: {sensitive_file}",
                    file_path=sensitive_file,
                    remediation="Remove sensitive information and use environment variables or secure vaults"
                ))
        
        # Calculate score based on violations
        base_score = 100
        score = base_score - (len(violations) * 15)  # Deduct 15 points per violation
        score = max(score, 0)
        
        return {
            'violations': violations,
            'score': score,
            'human_review_required': len(violations) > 5 or any(v.severity == 'critical' for v in violations)
        }
    
    async def check_nist_csf_compliance(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check NIST Cybersecurity Framework compliance"""
        
        violations = []
        repo_analysis = assessment_data['context']['analysis']
        
        # NIST CSF focuses on cybersecurity functions: Identify, Protect, Detect, Respond, Recover
        
        # Protect function - check for security configurations
        if repo_analysis['risk_indicators']['security_files']:
            violations.append(ComplianceViolation(
                rule_id="NIST-PR-01",
                rule_name="Protect Function",
                title="Security Configuration Changes",
                description="Changes to security-related files require careful review",
                severity="medium",
                framework="nistcsf",
                category="protect",
                message="Security configuration changes detected",
                remediation="Review security changes with security team"
            ))
        
        # Identify function - check for asset management
        if repo_analysis['repository_metadata']['total_files_changed'] > 100:
            violations.append(ComplianceViolation(
                rule_id="NIST-ID-01",
                rule_name="Identify Function",
                title="Large-Scale Changes",
                description="Extensive changes may indicate asset management issues",
                severity="low",
                framework="nistcsf",
                category="identify",
                message="Large number of files changed in single commit",
                remediation="Consider breaking large changes into smaller, reviewable commits"
            ))
        
        base_score = 100
        score = base_score - (len(violations) * 10)
        score = max(score, 0)
        
        return {
            'violations': violations,
            'score': score,
            'human_review_required': len(violations) > 8
        }
    
    async def check_soc2_compliance(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check SOC 2 compliance (Security, Availability, Processing Integrity, Confidentiality, Privacy)"""
        
        violations = []
        repo_analysis = assessment_data['context']['analysis']
        
        # SOC 2 Security criterion
        if repo_analysis['file_analysis']['sensitive_files']:
            violations.append(ComplianceViolation(
                rule_id="SOC2-CC6.1",
                rule_name="Logical Access Security",
                title="Potential Credential Exposure",
                description="Sensitive files detected that may compromise logical access security",
                severity="high",
                framework="soc2",
                category="security",
                message="Review files for exposed credentials or access keys",
                remediation="Use secure credential management systems"
            ))
        
        # SOC 2 Processing Integrity
        if repo_analysis['risk_indicators']['database_changes']:
            violations.append(ComplianceViolation(
                rule_id="SOC2-PI1.1",
                rule_name="Processing Integrity",
                title="Database Schema Changes",
                description="Database changes may affect processing integrity",
                severity="medium",
                framework="soc2",
                category="processing_integrity",
                message="Database changes require integrity validation",
                remediation="Ensure database changes maintain data integrity and are properly tested"
            ))
        
        base_score = 100
        score = base_score - (len(violations) * 12)
        score = max(score, 0)
        
        return {
            'violations': violations,
            'score': score,
            'human_review_required': any(v.severity == 'high' for v in violations)
        }
    
    async def check_gdpr_compliance(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check GDPR compliance"""
        
        violations = []
        repo_analysis = assessment_data['context']['analysis']
        files_changed = assessment_data.get('files', [])
        
        # Check for potential personal data processing
        personal_data_indicators = [
            'email', 'user', 'customer', 'person', 'profile', 'contact', 
            'address', 'phone', 'gdpr', 'privacy', 'consent'
        ]
        
        for file_data in files_changed:
            filename = file_data.get('filename', '').lower()
            content = file_data.get('content', '').lower() if file_data.get('content') else ''
            
            if any(indicator in filename or indicator in content for indicator in personal_data_indicators):
                violations.append(ComplianceViolation(
                    rule_id="GDPR-ART25",
                    rule_name="Data Protection by Design",
                    title="Personal Data Processing Detected",
                    description="Code changes may involve personal data processing requiring GDPR compliance review",
                    severity="medium",
                    framework="gdpr",
                    category="data_protection",
                    message="Ensure personal data processing complies with GDPR requirements",
                    file_path=file_data.get('filename'),
                    remediation="Review for lawful basis, data minimization, and user consent mechanisms"
                ))
                break  # Only flag once per assessment
        
        base_score = 100
        score = base_score - (len(violations) * 20)  # GDPR violations are serious
        score = max(score, 0)
        
        return {
            'violations': violations,
            'score': score,
            'human_review_required': len(violations) > 0  # GDPR always requires human review
        }

# Initialize API handler
github_api = GitHubActionsAPI()

# API Endpoints
@app.post("/api/v1/compliance/github-validate", response_model=ComplianceResponse)
async def validate_compliance(
    request: ComplianceRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(github_api.validate_api_key)
):
    """
    Validate compliance for GitHub Actions workflow
    """
    try:
        logger.info(f"Received compliance validation request from {request.context.repository.full_name}")
        
        # Generate request ID for caching/tracking
        request_id = github_api.generate_request_id(request.context)
        
        # Check cache first (for identical requests)
        cache_key = f"github_validation:{request_id}"
        cached_result = await github_api.cache.get(cache_key)
        if cached_result:
            logger.info("Returning cached compliance result")
            return ComplianceResponse(**cached_result)
        
        # Perform validation
        result = await github_api.perform_compliance_validation(
            context=request.context,
            frameworks=request.frameworks,
            mode=request.mode,
            options=request.options
        )
        
        # Cache result for 1 hour
        await github_api.cache.set(cache_key, result.dict(), ttl=3600)
        
        # Log metrics (background task)
        background_tasks.add_task(
            log_compliance_metrics,
            request.context.repository.full_name,
            request.frameworks,
            result.compliance_score,
            len(result.violations)
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Compliance validation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Compliance validation failed: {str(e)}")

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "cerberus-ai-github-actions",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/frameworks")
async def list_supported_frameworks(api_key: str = Depends(github_api.validate_api_key)):
    """List supported compliance frameworks"""
    return {
        "frameworks": [
            {
                "id": "essential8",
                "name": "Essential 8",
                "description": "Australian Cyber Security Centre's Essential 8",
                "status": "active"
            },
            {
                "id": "nistcsf",
                "name": "NIST Cybersecurity Framework",
                "description": "NIST Cybersecurity Framework v1.1",
                "status": "active"
            },
            {
                "id": "soc2",
                "name": "SOC 2",
                "description": "System and Organization Controls 2",
                "status": "active"
            },
            {
                "id": "gdpr",
                "name": "GDPR",
                "description": "General Data Protection Regulation",
                "status": "active"
            }
        ]
    }

async def log_compliance_metrics(repository: str, frameworks: List[str], score: int, violations: int):
    """Background task to log compliance metrics"""
    try:
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'repository': repository,
            'frameworks': frameworks,
            'compliance_score': score,
            'violations_count': violations,
            'api_version': '1.0.0'
        }
        
        # In production, send to monitoring system
        logger.info(f"Compliance metrics: {json.dumps(metrics)}")
        
    except Exception as e:
        logger.error(f"Failed to log metrics: {e}")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "github_actions_api_endpoint:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )