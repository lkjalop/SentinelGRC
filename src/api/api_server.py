"""
Enterprise REST API Server for SentinelGRC
Production-ready API endpoints for compliance platform integration
"""

from fastapi import FastAPI, HTTPException, Depends, Security, status, BackgroundTasks
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uvicorn
import asyncio
import logging
import json
from enum import Enum

from config_manager import config
from async_compliance_orchestrator import AsyncComplianceOrchestrator
from database_pool import db_pool
from cache_manager import CacheManager
from enterprise_liability_framework import EnterpriseComplianceLiabilityManager
from token_optimization_engine import TokenOptimizationEngine

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SentinelGRC Enterprise API",
    description="Multi-regional compliance intelligence platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.security.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)

# Global instances
orchestrator = None
cache = CacheManager()
liability_manager = EnterpriseComplianceLiabilityManager()
token_optimizer = TokenOptimizationEngine()


# ============================================
# Pydantic Models
# ============================================

class Region(str, Enum):
    AU = "AU"
    US = "US"
    EU = "EU"
    GLOBAL = "GLOBAL"


class CompanySize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class CompanyProfile(BaseModel):
    """Company profile for compliance assessment"""
    name: str = Field(..., min_length=1, max_length=200)
    region: Region
    industry: str = Field(..., min_length=1, max_length=100)
    size: CompanySize
    employees: Optional[int] = Field(None, ge=1)
    annual_revenue: Optional[float] = Field(None, ge=0)
    security_controls: Optional[List[str]] = []
    previous_incidents: Optional[List[str]] = []
    compliance_history: Optional[Dict[str, Any]] = {}
    
    @validator('industry')
    def validate_industry(cls, v):
        valid_industries = [
            'finance', 'healthcare', 'technology', 'retail', 'manufacturing',
            'government', 'education', 'energy', 'telecommunications', 'transportation'
        ]
        if v.lower() not in valid_industries:
            logger.warning(f"Non-standard industry provided: {v}")
        return v


class AssessmentRequest(BaseModel):
    """Request model for compliance assessment"""
    company_profile: CompanyProfile
    frameworks: Optional[List[str]] = None
    include_recommendations: bool = True
    include_liability_assessment: bool = True
    parallel_execution: bool = True
    cache_enabled: bool = True


class AssessmentResponse(BaseModel):
    """Response model for compliance assessment"""
    assessment_id: str
    timestamp: str
    company_name: str
    overall_compliance_score: float
    frameworks_assessed: List[str]
    framework_results: Dict[str, Any]
    recommendations: Optional[List[Dict[str, Any]]]
    liability_assessment: Optional[Dict[str, Any]]
    processing_time_seconds: float


class FrameworkStatusResponse(BaseModel):
    """Response model for framework status"""
    framework: str
    enabled: bool
    region: str
    description: str
    controls_count: int
    last_updated: str


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str
    environment: str
    database_connected: bool
    cache_available: bool
    api_keys_configured: bool


class MetricsResponse(BaseModel):
    """API metrics response"""
    total_assessments: int
    average_processing_time: float
    cache_hit_rate: float
    framework_usage: Dict[str, int]
    database_pool_status: Dict[str, Any]
    error_rate: float


# ============================================
# Security & Authentication
# ============================================

async def verify_api_key(api_key: str = Depends(api_key_header)) -> bool:
    """Verify API key for authentication"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    
    # In production, validate against database or key management service
    valid_keys = ["demo_api_key_12345"]  # This should come from secure storage
    
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return True


async def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> str:
    """Verify bearer token for authentication"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required"
        )
    
    # In production, validate JWT token
    # For now, return a demo user
    return "authenticated_user"


# ============================================
# API Endpoints
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global orchestrator
    orchestrator = AsyncComplianceOrchestrator()
    await orchestrator.__aenter__()
    logger.info("API server started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if orchestrator:
        await orchestrator.__aexit__(None, None, None)
    await db_pool.close_all_pools()
    logger.info("API server shut down successfully")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": "SentinelGRC Enterprise API",
        "version": "1.0.0",
        "documentation": "/api/docs"
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    
    # Check database connection
    db_connected = False
    try:
        await db_pool.execute_query("SELECT 1")
        db_connected = True
    except:
        pass
    
    # Check API keys configuration
    api_keys_configured = bool(
        config.api.groq_api_key or 
        config.api.openai_api_key or 
        config.api.anthropic_api_key
    )
    
    return HealthCheckResponse(
        status="healthy" if db_connected else "degraded",
        timestamp=datetime.now().isoformat(),
        version=config.application.app_version,
        environment=config.application.environment.value,
        database_connected=db_connected,
        cache_available=True,
        api_keys_configured=api_keys_configured
    )


@app.post("/api/v1/assess", response_model=AssessmentResponse, tags=["Assessment"])
async def assess_compliance(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Perform comprehensive compliance assessment
    
    This endpoint performs a multi-framework compliance assessment for the provided
    company profile. It supports parallel execution, caching, and liability assessment.
    """
    start_time = datetime.now()
    
    try:
        # Convert request to dict for orchestrator
        company_profile = request.company_profile.dict()
        
        # Perform assessment
        results = await orchestrator.assess_compliance(
            company_profile=company_profile,
            frameworks=request.frameworks,
            parallel=request.parallel_execution
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Prepare response
        response = AssessmentResponse(
            assessment_id=results['assessment_id'],
            timestamp=results['timestamp'],
            company_name=company_profile['name'],
            overall_compliance_score=results['overall_compliance_score'],
            frameworks_assessed=results['frameworks_assessed'],
            framework_results=results['framework_results'],
            recommendations=results.get('recommendations') if request.include_recommendations else None,
            liability_assessment=results.get('liability_assessment') if request.include_liability_assessment else None,
            processing_time_seconds=processing_time
        )
        
        # Schedule background task for analytics
        background_tasks.add_task(record_assessment_analytics, results)
        
        return response
    
    except Exception as e:
        logger.error(f"Assessment failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment failed: {str(e)}"
        )


@app.get("/api/v1/frameworks", response_model=List[FrameworkStatusResponse], tags=["Frameworks"])
async def list_frameworks(
    region: Optional[Region] = None,
    authenticated: bool = Depends(verify_api_key)
):
    """List available compliance frameworks"""
    
    frameworks = [
        FrameworkStatusResponse(
            framework="essential_8",
            enabled=True,
            region="AU",
            description="Australian Essential 8 maturity model",
            controls_count=8,
            last_updated="2024-01-01"
        ),
        FrameworkStatusResponse(
            framework="privacy_act",
            enabled=True,
            region="AU",
            description="Australian Privacy Act 1988 (13 APPs)",
            controls_count=13,
            last_updated="2024-01-01"
        ),
        FrameworkStatusResponse(
            framework="soc2",
            enabled=True,
            region="US",
            description="SOC 2 Trust Service Criteria",
            controls_count=5,
            last_updated="2024-01-01"
        ),
        FrameworkStatusResponse(
            framework="nist_csf",
            enabled=True,
            region="US",
            description="NIST Cybersecurity Framework",
            controls_count=5,
            last_updated="2024-01-01"
        ),
        FrameworkStatusResponse(
            framework="gdpr",
            enabled=True,
            region="EU",
            description="General Data Protection Regulation",
            controls_count=7,
            last_updated="2024-01-01"
        ),
        FrameworkStatusResponse(
            framework="iso27001",
            enabled=True,
            region="GLOBAL",
            description="ISO 27001 Information Security",
            controls_count=14,
            last_updated="2024-01-01"
        )
    ]
    
    if region:
        frameworks = [f for f in frameworks if f.region == region or f.region == "GLOBAL"]
    
    return frameworks


@app.get("/api/v1/assessment/{assessment_id}", tags=["Assessment"])
async def get_assessment(
    assessment_id: str,
    authenticated: bool = Depends(verify_api_key)
):
    """Retrieve specific assessment results"""
    
    try:
        # Query database for assessment
        query = """
            SELECT assessment_id, company_name, timestamp, overall_score, results_json
            FROM compliance_assessments
            WHERE assessment_id = $1
        """
        
        results = await db_pool.execute_query(query, (assessment_id,))
        
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assessment {assessment_id} not found"
            )
        
        assessment = results[0]
        return json.loads(assessment['results_json'])
    
    except Exception as e:
        logger.error(f"Failed to retrieve assessment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve assessment: {str(e)}"
        )


@app.get("/api/v1/metrics", response_model=MetricsResponse, tags=["Metrics"])
async def get_metrics(
    authenticated: bool = Depends(verify_api_key)
):
    """Get API performance metrics"""
    
    # Get orchestrator metrics
    orchestrator_metrics = orchestrator.get_metrics()
    
    # Get database pool status
    pool_status = db_pool.get_pool_status()
    
    return MetricsResponse(
        total_assessments=orchestrator_metrics.get('completed_tasks', 0),
        average_processing_time=orchestrator_metrics.get('total_time', 0) / max(orchestrator_metrics.get('completed_tasks', 1), 1),
        cache_hit_rate=orchestrator_metrics.get('cache_hit_rate', 0),
        framework_usage=orchestrator_metrics.get('framework_times', {}),
        database_pool_status=pool_status,
        error_rate=orchestrator_metrics.get('failed_tasks', 0) / max(orchestrator_metrics.get('total_tasks', 1), 1)
    )


@app.post("/api/v1/optimize", tags=["Optimization"])
async def optimize_query(
    query: str,
    framework: str,
    industry: str,
    authenticated: bool = Depends(verify_api_key)
):
    """Optimize compliance query for token efficiency"""
    
    result = token_optimizer.optimize_compliance_query(query, framework, industry)
    
    return {
        "original_query": query,
        "optimized_query": result['optimized_query'],
        "original_tokens": result['original_tokens'],
        "optimized_tokens": result['optimized_tokens'],
        "savings_percentage": result['savings_percentage']
    }


@app.post("/api/v1/liability/assess", tags=["Liability"])
async def assess_liability(
    assessment_context: Dict[str, Any],
    authenticated: bool = Depends(verify_api_key)
):
    """Assess liability and risk for compliance recommendations"""
    
    result = liability_manager.assess_liability_risk(assessment_context)
    
    return result


@app.get("/api/v1/cache/status", tags=["Cache"])
async def cache_status(
    authenticated: bool = Depends(verify_api_key)
):
    """Get cache status and statistics"""
    
    return {
        "cache_enabled": True,
        "ttl_seconds": config.get('cache_ttl_seconds', 3600),
        "items_cached": len(cache._cache),
        "memory_usage_bytes": sum(len(str(v)) for v in cache._cache.values())
    }


@app.delete("/api/v1/cache/clear", tags=["Cache"])
async def clear_cache(
    authenticated: bool = Depends(verify_api_key)
):
    """Clear all cached data"""
    
    cache.clear()
    
    return {"message": "Cache cleared successfully"}


# ============================================
# Webhook Endpoints for CI/CD Integration
# ============================================

@app.post("/api/v1/webhook/github", tags=["Webhooks"])
async def github_webhook(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """GitHub webhook for CI/CD compliance validation"""
    
    # Extract relevant information from GitHub payload
    action = payload.get('action')
    repository = payload.get('repository', {}).get('name')
    
    # Schedule compliance check in background
    background_tasks.add_task(
        process_github_webhook,
        payload
    )
    
    return {"message": "Webhook received", "repository": repository, "action": action}


@app.post("/api/v1/webhook/jenkins", tags=["Webhooks"])
async def jenkins_webhook(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Jenkins webhook for build compliance validation"""
    
    job_name = payload.get('name')
    build_number = payload.get('build', {}).get('number')
    
    # Schedule compliance check in background
    background_tasks.add_task(
        process_jenkins_webhook,
        payload
    )
    
    return {"message": "Webhook received", "job": job_name, "build": build_number}


# ============================================
# Background Tasks
# ============================================

async def record_assessment_analytics(results: Dict[str, Any]):
    """Record assessment analytics in background"""
    try:
        # Store analytics data
        query = """
            INSERT INTO assessment_analytics 
            (timestamp, company_name, region, frameworks, score)
            VALUES ($1, $2, $3, $4, $5)
        """
        
        await db_pool.execute_query(
            query,
            (
                datetime.now(),
                results['company'].get('name'),
                results['company'].get('region'),
                json.dumps(results['frameworks_assessed']),
                results['overall_compliance_score']
            )
        )
    except Exception as e:
        logger.error(f"Failed to record analytics: {e}")


async def process_github_webhook(payload: Dict[str, Any]):
    """Process GitHub webhook for compliance validation"""
    # Implement GitHub-specific compliance checks
    logger.info(f"Processing GitHub webhook: {payload.get('action')}")


async def process_jenkins_webhook(payload: Dict[str, Any]):
    """Process Jenkins webhook for compliance validation"""
    # Implement Jenkins-specific compliance checks
    logger.info(f"Processing Jenkins webhook: {payload.get('name')}")


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.application.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the server
    uvicorn.run(
        app,
        host=config.application.host,
        port=config.application.port,
        workers=config.application.workers,
        log_level=config.application.log_level.lower()
    )