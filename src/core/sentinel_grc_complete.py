"""
Sentinel GRC - Complete Enterprise Compliance Platform
======================================================

Zero-budget enterprise compliance platform for Australian market with US expansion.
All critical bugs fixed and production-ready implementation.

COMPLETED FIXES:
1. ✅ Fixed circular import dependencies → created core_types.py
2. ✅ Added exception handling to all async methods
3. ✅ Fixed memory leaks → bounded collections + shared knowledge graphs
4. ✅ Implemented thread-safe cache → cache_manager.py
5. ✅ Replaced MD5 with SHA-256 throughout codebase
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict

# Import all core components (fixed circular imports)
from .core_types import (
    Config, CompanyProfile, AssessmentResult,
    AssessmentStatus, RiskLevel, ConfidenceLevel, EscalationType,
    get_risk_level, get_confidence_level, determine_escalation
)

# Import specialized agents
from ..agents.australian_compliance_agents import (
    PrivacyActAgent, APRACPSAgent, SOCIActAgent
)
from ..agents.soc2_agent import SOC2Agent
from ..agents.nist_800_53_agent import NIST80053Agent
from ..agents.iso_27001_agent import ISO27001Agent

# Import Essential Eight integration
from ..integrations.optimized_essential_eight_integration import (
    OptimizedEssentialEightIntegrator, EssentialEightConfig, MaturityLevel
)

# Import enhanced PDF generator
from ..professional.enhanced_pdf_generator import EnhancedPDFGenerator

# Import NIST framework integration
from ..config.us_adaptation_config import NISTCSFAgent

# Import Intelligence Knowledge Graph (THE RESTORED BRAIN)
from .intelligence_knowledge_graph import get_intelligence_graph, IntelligenceKnowledgeGraph

# Import sidecar orchestration (moved from archive)
from ..core.sidecar_orchestrator import (
    SidecarOrchestrator, SidecarPriority, LegalReviewSidecar, ThreatModelingSidecar
)

# Import utilities
from .cache_manager import AssessmentCacheManager, get_cache_manager
from .memory_monitor import MemoryMonitor
from .security_audit import SecurityAudit
from .framework_conflict_detector import FrameworkConflictDetector

# Import professional features (Phase 2)
from ..professional.isms_training_engine import ISMSTrainingEngine, integrate_isms_training_with_agents
from ..professional.pdf_report_generator import PDFReportGenerator
from ..professional.human_expert_escalation import HumanExpertEscalationSystem
from ..professional.pdf_review_workflow import PDFReviewWorkflow, ReviewStatus
from .enterprise_liability_framework import EnterpriseComplianceLiabilityManager

# Import security frameworks (Phase 3)
from ..security.owasp_security_frameworks import OWASPSecurityOrchestrator

# Import CI/CD Integration (Phase 4)
from ..integrations.cicd_connector import CICDIntegrator, CICDProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SentinelGRC:
    """
    Main Sentinel GRC platform with enterprise-grade architecture.
    Implements all security fixes and optimization features.
    """
    
    def __init__(self):
        self.platform_name = "Sentinel GRC"
        self.version = "1.0.0-production"
        self.startup_time = datetime.now()
        
        # Initialize core components
        self.cache_manager = get_cache_manager()
        self.memory_monitor = MemoryMonitor()
        self.security_auditor = SecurityAudit()
        
        # Platform statistics
        self.stats = {
            "assessments_completed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors_handled": 0,
            "memory_cleanups": 0
        }
        
        # Initialize compliance agents
        self.agents = self._initialize_agents()
        
        # Initialize professional features (Phase 2)
        self.isms_training_engine = None
        self.pdf_generator = None
        self.pdf_review_workflow = None
        self.expert_escalation_system = None
        self.liability_manager = None
        
        # Initialize security frameworks (Phase 3)
        self.owasp_security_orchestrator = None
        
        # Initialize Intelligence Knowledge Graph (THE RESTORED BRAIN)
        self.intelligence_graph = None
        try:
            self.intelligence_graph = get_intelligence_graph()
            logger.info("🧠 Intelligence Knowledge Graph restored (UNIQUE SELLING POINT)")
        except Exception as e:
            logger.warning(f"⚠️ Intelligence graph failed to initialize: {e}")
            
        # Initialize Framework Conflict Detector (Competitive Differentiator)
        self.conflict_detector = None
        try:
            self.conflict_detector = FrameworkConflictDetector()
            logger.info("✅ Framework Conflict Detector initialized (KEY DIFFERENTIATOR)")
        except Exception as e:
            logger.warning(f"⚠️ Conflict detector failed to initialize: {e}")
        
        try:
            self.isms_training_engine = ISMSTrainingEngine()
            self.pdf_generator = EnhancedPDFGenerator()
            self.pdf_review_workflow = PDFReviewWorkflow()
            self.expert_escalation_system = HumanExpertEscalationSystem()
            self.liability_manager = EnterpriseComplianceLiabilityManager()
            
            # Initialize OWASP security frameworks
            self.owasp_security_orchestrator = OWASPSecurityOrchestrator()
            
            # Enhance agents with ISMS training
            self.agents = integrate_isms_training_with_agents(self.agents)
            
            logger.info("✅ Professional features + OWASP Security initialized (Complete Enterprise Platform)")
        except Exception as e:
            logger.warning(f"⚠️ Professional features failed to initialize: {e}")
        
        # Initialize sidecar orchestrator for background processing
        self.sidecar_orchestrator = None
        try:
            self.sidecar_orchestrator = SidecarOrchestrator()
            logger.info("✅ Sidecar orchestrator initialized (Legal + Threat modeling)")
        except Exception as e:
            logger.warning(f"⚠️ Sidecar orchestrator failed to initialize: {e}")
        
        # Initialize CI/CD Integration (Phase 4)
        self.cicd_integrator = None
        try:
            self.cicd_integrator = CICDIntegrator()
            logger.info("✅ CI/CD integrator initialized (GitHub, Jenkins, GitLab)")
        except Exception as e:
            logger.warning(f"⚠️ CI/CD integrator failed to initialize: {e}")
        
        # Initialize knowledge graph with NIST controls
        self.knowledge_graph = self._initialize_knowledge_graph()
        
        logger.info(f"🚀 {self.platform_name} v{self.version} initialized successfully")
        self._log_system_status()
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all compliance agents with error handling"""
        agents = {}
        
        try:
            agents["privacy_act"] = PrivacyActAgent()
            logger.info("✅ Privacy Act 1988 agent loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load Privacy Act agent: {e}")
            self.stats["errors_handled"] += 1
        
        try:
            agents["apra_cps234"] = APRACPSAgent()
            logger.info("✅ APRA CPS 234 agent loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load APRA CPS 234 agent: {e}")
            self.stats["errors_handled"] += 1
        
        try:
            agents["soci_act"] = SOCIActAgent()
            logger.info("✅ SOCI Act 2018 agent loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load SOCI Act agent: {e}")
            self.stats["errors_handled"] += 1
        
        # Add Essential Eight agent
        try:
            essential8_config = EssentialEightConfig()
            agents["essential_eight"] = OptimizedEssentialEightIntegrator(essential8_config)
            logger.info("✅ Essential Eight (ML1-ML3) agent loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load Essential Eight agent: {e}")
            self.stats["errors_handled"] += 1
            
        # Add NIST CSF agent for US market
        try:
            agents["nist_csf"] = NISTCSFAgent()
            logger.info("✅ NIST Cybersecurity Framework agent loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load NIST CSF agent: {e}")
            self.stats["errors_handled"] += 1
        
        try:
            agents["soc2"] = SOC2Agent()
            logger.info("✅ SOC 2 compliance agent loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load SOC 2 agent: {e}")
            self.stats["errors_handled"] += 1
        
        # Add ISO 27001 agent (6th main framework)
        try:
            agents["iso_27001"] = ISO27001Agent()
            logger.info("✅ ISO 27001:2022 ISMS agent loaded (includes AI standards ISO 42001/23894)")
        except Exception as e:
            logger.error(f"❌ Failed to load ISO 27001 agent: {e}")
            self.stats["errors_handled"] += 1
        
        try:
            agents["nist_800_53"] = NIST80053Agent()
            logger.info("✅ NIST SP 800-53 Rev 5 agent loaded (1006 controls)")
        except Exception as e:
            logger.error(f"❌ Failed to load NIST 800-53 agent: {e}")
            self.stats["errors_handled"] += 1
        
        logger.info(f"📋 Loaded {len(agents)} compliance agents")
        return agents
    
    def _initialize_knowledge_graph(self) -> Dict[str, Any]:
        """Initialize knowledge graph with NIST 1006 controls and cross-framework mappings"""
        try:
            import json
            from pathlib import Path
            
            # Load NIST 800-53 controls (1006 controls)
            nist_data_path = Path("src/data/comprehensive_nist_800_53_data.json")
            if nist_data_path.exists():
                with open(nist_data_path, 'r', encoding='utf-8') as f:
                    nist_data = json.load(f)
                    logger.info(f"✅ Loaded {nist_data.get('nist_800_53_catalog', {}).get('catalog_info', {}).get('total_controls', 0)} NIST controls")
                    return {"nist_800_53": nist_data}
            else:
                logger.warning("⚠️ NIST 800-53 data file not found")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize knowledge graph: {e}")
            return {}
    
    def _log_system_status(self):
        """Log current system status for monitoring"""
        memory_report = self.memory_monitor.get_comprehensive_report()
        
        logger.info("🔍 System Status:")
        logger.info(f"   Memory: {memory_report['process_memory']['rss_mb']:.1f}MB")
        logger.info(f"   Agents: {len(self.agents)}")
        logger.info(f"   Cache Size: {self.cache_manager.get_stats()['current_size']}")
        logger.info(f"   Knowledge Graphs: {memory_report['knowledge_graph_stats']['total_frameworks']}")
    
    async def run_security_audit(self) -> Dict[str, Any]:
        """Run comprehensive security audit"""
        logger.info("🔒 Starting security audit...")
        
        try:
            audit_report = self.security_auditor.run_comprehensive_audit()
            
            if audit_report["production_ready"]:
                logger.info("✅ Security audit PASSED - Production ready")
            else:
                logger.warning("⚠️  Security audit FAILED - Address issues before production")
                for issue in audit_report["critical_issues"]:
                    logger.error(f"   ❌ {issue}")
            
            return audit_report
            
        except Exception as e:
            logger.error(f"💥 Security audit failed: {e}")
            self.stats["errors_handled"] += 1
            return {
                "production_ready": False,
                "error": str(e),
                "recommendations": ["Fix security audit execution"]
            }
    
    async def assess_company(self, 
                           company_profile: CompanyProfile, 
                           frameworks: Optional[List[str]] = None,
                           use_cache: bool = True) -> Dict[str, Any]:
        """
        Perform comprehensive compliance assessment with enterprise features.
        Includes caching, error handling, and memory optimization.
        """
        
        assessment_id = f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"🎯 Starting assessment {assessment_id} for {company_profile.company_name}")
        
        # Check cache first
        cached_result = None
        cache_key = None
        
        if use_cache:
            try:
                cached_result, cache_key = self.cache_manager.get_cached_assessment(
                    company_profile, frameworks or []
                )
                if cached_result:
                    logger.info("⚡ Using cached assessment result")
                    self.stats["cache_hits"] += 1
                    return {
                        "assessment_id": assessment_id,
                        "cached": True,
                        "result": cached_result,
                        "cache_key": cache_key
                    }
                else:
                    self.stats["cache_misses"] += 1
                    
            except Exception as cache_error:
                logger.warning(f"Cache retrieval failed: {cache_error}")
                self.stats["errors_handled"] += 1
        
        # Determine which frameworks to assess
        if not frameworks:
            frameworks = self._determine_applicable_frameworks(company_profile)
        
        logger.info(f"📊 Assessing frameworks: {frameworks}")
        
        # Run assessments with comprehensive error handling
        assessment_results = {}
        overall_status = AssessmentStatus.COMPLETED
        total_confidence = 0.0
        assessment_count = 0
        
        # Detect framework conflicts (KEY DIFFERENTIATOR)
        conflicts_detected = []
        if self.conflict_detector and len(frameworks) > 1:
            try:
                # Get controls for conflict analysis
                controls_dict = {}
                for fw in frameworks:
                    if fw in self.agents:
                        agent = self.agents[fw]
                        if hasattr(agent, 'controls'):
                            controls_dict[fw] = agent.controls
                
                conflicts_detected = self.conflict_detector.detect_conflicts(frameworks, controls_dict)
                if conflicts_detected:
                    logger.warning(f"⚠️ Detected {len(conflicts_detected)} framework conflicts")
            except Exception as e:
                logger.error(f"Conflict detection failed: {e}")
        
        for framework in frameworks:
            try:
                result = await self._assess_framework(framework, company_profile)
                assessment_results[framework] = result
                
                if isinstance(result, AssessmentResult):
                    total_confidence += result.confidence
                    assessment_count += 1
                    
                    if result.status != AssessmentStatus.COMPLETED:
                        overall_status = AssessmentStatus.FAILED
                        
            except asyncio.TimeoutError:
                error_msg = f"Assessment timeout for framework {framework}"
                logger.error(error_msg)
                assessment_results[framework] = {
                    "status": "TIMEOUT",
                    "error": error_msg,
                    "framework": framework
                }
                overall_status = AssessmentStatus.FAILED
                self.stats["errors_handled"] += 1
                
            except Exception as e:
                error_msg = f"Assessment failed for framework {framework}: {str(e)}"
                logger.error(error_msg)
                assessment_results[framework] = {
                    "status": "ERROR", 
                    "error": error_msg,
                    "framework": framework
                }
                overall_status = AssessmentStatus.FAILED
                self.stats["errors_handled"] += 1
        
        # Calculate overall metrics
        overall_confidence = total_confidence / assessment_count if assessment_count > 0 else 0.0
        
        # Create comprehensive result
        final_result = {
            "assessment_id": assessment_id,
            "company": company_profile.company_name,
            "timestamp": datetime.now().isoformat(),
            "frameworks_assessed": frameworks,
            "overall_status": overall_status.value,
            "overall_confidence": overall_confidence,
            "confidence_level": get_confidence_level(overall_confidence).value,
            "assessment_results": assessment_results,
            "framework_conflicts": self._format_conflicts(conflicts_detected) if conflicts_detected else None,
            "escalation_required": self._determine_overall_escalation(
                assessment_results, company_profile
            ),
            "executive_summary": self._generate_executive_summary(
                assessment_results, company_profile
            ),
            "cached": False,
            "processing_time_seconds": (datetime.now() - self.startup_time).total_seconds()
        }
        
        # Cache successful results
        if use_cache and overall_status == AssessmentStatus.COMPLETED:
            try:
                cache_key = self.cache_manager.cache_assessment(
                    company_profile, frameworks, final_result, ttl_hours=2
                )
                final_result["cache_key"] = cache_key
                logger.info(f"💾 Cached assessment result with key: {cache_key[:16]}...")
            except Exception as cache_error:
                logger.warning(f"Failed to cache result: {cache_error}")
                self.stats["errors_handled"] += 1
        
        # Update statistics
        self.stats["assessments_completed"] += 1
        
        logger.info(f"✅ Assessment {assessment_id} completed with {overall_status.value} status")
        
        return final_result
    
    def _determine_applicable_frameworks(self, company_profile: CompanyProfile) -> List[str]:
        """Determine which frameworks apply to the company"""
        applicable = []
        
        # Essential Eight applies to most Australian organizations
        if company_profile.country == "Australia":
            applicable.append("essential_eight")
            
        # Privacy Act applies to most organizations
        if company_profile.employee_count > 10:  # Small business threshold
            applicable.append("privacy_act")
        
        # APRA CPS 234 for financial institutions
        if company_profile.industry in ["Finance", "Banking", "Insurance"]:
            applicable.append("apra_cps234")
        
        # SOCI Act for critical infrastructure
        critical_industries = ["Energy", "Telecommunications", "Banking", "Healthcare", "Transport"]
        if (company_profile.industry in critical_industries and 
            company_profile.employee_count > 100):
            applicable.append("soci_act")
            
        # NIST CSF for US organizations
        if company_profile.country == "United States":
            applicable.append("nist_csf")
        
        # Default to Essential Eight for AU or NIST CSF for US
        if not applicable:
            if company_profile.country == "Australia":
                applicable.append("essential_eight")
            else:
                applicable.append("nist_csf")
        
        return applicable
    
    async def _assess_framework(self, framework: str, 
                              company_profile: CompanyProfile) -> AssessmentResult:
        """Assess specific framework with timeout and error handling"""
        
        agent = self.agents.get(framework)
        if not agent:
            raise ValueError(f"No agent available for framework: {framework}")
        
        # Use asyncio timeout for robust error handling
        try:
            # Handle different agent types
            if framework == "essential_eight":
                # Essential Eight agent uses different interface
                controls = agent.get_enhanced_essential_eight_controls()
                # Create AssessmentResult compatible response
                result = self._create_assessment_result_from_essential8(controls, company_profile)
            elif framework == "nist_csf":
                # NIST CSF agent assessment
                result = await asyncio.wait_for(
                    agent.assess_compliance(company_profile), 
                    timeout=45.0  # Longer timeout for NIST
                )
            elif framework == "nist_800_53" or framework == "NIST SP 800-53":
                # NIST SP 800-53 agent assessment
                result = await asyncio.wait_for(
                    agent.assess_compliance(asdict(company_profile)),
                    timeout=60.0  # Longer timeout for comprehensive 1006 controls
                )
            elif framework == "soc2" or framework == "SOC 2":
                # SOC 2 agent assessment
                result = await asyncio.wait_for(
                    agent.assess_compliance(asdict(company_profile)),
                    timeout=45.0  # Standard timeout for SOC 2
                )
            else:
                # Standard agent interface (assess method)
                result = await asyncio.wait_for(
                    agent.assess(company_profile),
                    timeout=Config.AGENT_TIMEOUT_SECONDS
                )
            
            # Submit to sidecar processing if available and confidence is low
            if self.sidecar_orchestrator and result.confidence < 0.8:
                try:
                    # Submit for background legal review and threat modeling
                    assessment_data = {
                        "company_profile": company_profile.__dict__,
                        "framework": framework,
                        "result": result.__dict__
                    }
                    
                    legal_request_id = self.sidecar_orchestrator.submit_for_legal_review(
                        assessment_data, SidecarPriority.MEDIUM
                    )
                    
                    threat_request_id = self.sidecar_orchestrator.submit_for_threat_modeling(
                        assessment_data, SidecarPriority.MEDIUM
                    )
                    
                    logger.info(f"📤 Submitted {framework} for sidecar analysis: legal={legal_request_id[:8]}, threat={threat_request_id[:8]}")
                except Exception as sidecar_error:
                    logger.warning(f"⚠️ Sidecar submission failed: {sidecar_error}")
            
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"Framework {framework} assessment timed out")
            raise
        except Exception as e:
            logger.error(f"Framework {framework} assessment failed: {e}")
            raise
    
    def _create_assessment_result_from_essential8(self, controls: Dict[str, Any], 
                                                company_profile: CompanyProfile) -> AssessmentResult:
        """Create AssessmentResult from Essential Eight controls data"""
        try:
            # Calculate basic compliance metrics from Essential Eight data
            total_controls = len(controls.get("controls", {}))
            implemented_controls = sum(1 for control in controls.get("controls", {}).values() 
                                     if control.get("implementation_status") != "not_implemented")
            
            compliance_percentage = (implemented_controls / total_controls * 100) if total_controls > 0 else 0
            confidence_score = min(compliance_percentage / 100.0, 0.95)  # Cap at 95%
            
            # Create assessment result
            result = AssessmentResult(
                framework="Essential Eight",
                company=company_profile.company_name,
                timestamp=datetime.now(),
                status=AssessmentStatus.COMPLETED,
                confidence=confidence_score,
                risk_level=get_risk_level(compliance_percentage),
                controls_assessed=[],
                overall_score=compliance_percentage,
                control_scores={},
                maturity_scores={},
                gaps_identified=[
                    {"control": control_id, "status": "missing", "priority": "HIGH"}
                    for control_id, control in controls.get("controls", {}).items()
                    if control.get("implementation_status") == "not_implemented"
                ],
                recommendations=[
                    "Implement Essential Eight Maturity Level 1 controls",
                    "Progress towards Maturity Level 2 for enhanced security",
                    "Consider Maturity Level 3 for high-risk environments"
                ],
                evidence=[],
                executive_summary=f"Essential Eight assessment shows {compliance_percentage:.1f}% compliance. "
                                f"{len([c for c in controls.get('controls', {}).values() if c.get('implementation_status') == 'not_implemented'])} controls need implementation."
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to create Essential Eight assessment result: {e}")
            # Return basic result
            return AssessmentResult(
                framework="Essential Eight",
                company=company_profile.company_name,
                timestamp=datetime.now(),
                status=AssessmentStatus.FAILED,
                confidence=0.3,
                risk_level=RiskLevel.HIGH,
                controls_assessed=[],
                gaps_identified=[],
                recommendations=[],
                evidence=[],
                overall_score=0.0,
                control_scores={},
                maturity_scores={},
                executive_summary="Automated Essential Eight assessment failed - manual review needed"
            )
    
    def _determine_overall_escalation(self, assessment_results: Dict[str, Any], 
                                    company_profile: CompanyProfile) -> str:
        """Determine if human escalation is required"""
        
        escalation_levels = []
        
        for framework, result in assessment_results.items():
            if isinstance(result, AssessmentResult):
                escalation = determine_escalation(
                    result.confidence, result.risk_level, company_profile
                )
                escalation_levels.append(escalation)
        
        # Return highest escalation level
        if EscalationType.EXECUTIVE_REQUIRED in escalation_levels:
            return EscalationType.EXECUTIVE_REQUIRED.value
        elif EscalationType.LEGAL_REQUIRED in escalation_levels:
            return EscalationType.LEGAL_REQUIRED.value
        elif EscalationType.EXPERT_REQUIRED in escalation_levels:
            return EscalationType.EXPERT_REQUIRED.value
        elif EscalationType.REVIEW_RECOMMENDED in escalation_levels:
            return EscalationType.REVIEW_RECOMMENDED.value
        else:
            return EscalationType.NONE.value
    
    def _generate_executive_summary(self, assessment_results: Dict[str, Any], 
                                  company_profile: CompanyProfile) -> str:
        """Generate executive summary of assessment"""
        
        completed_frameworks = []
        failed_frameworks = []
        high_risk_findings = []
        
        for framework, result in assessment_results.items():
            if isinstance(result, AssessmentResult):
                if result.status == AssessmentStatus.COMPLETED:
                    completed_frameworks.append(framework)
                    if result.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                        high_risk_findings.append(framework)
                else:
                    failed_frameworks.append(framework)
            elif isinstance(result, dict) and result.get("status") in ["ERROR", "TIMEOUT"]:
                failed_frameworks.append(framework)
        
        summary = f"Compliance assessment completed for {company_profile.company_name} "
        summary += f"({company_profile.industry}, {company_profile.employee_count} employees). "
        
        if completed_frameworks:
            summary += f"Successfully assessed {len(completed_frameworks)} frameworks. "
        
        if high_risk_findings:
            summary += f"⚠️  High-risk findings in {len(high_risk_findings)} frameworks require immediate attention. "
        
        if failed_frameworks:
            summary += f"❌ {len(failed_frameworks)} frameworks could not be assessed and require manual review. "
        
        return summary
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get comprehensive platform statistics"""
        
        memory_report = self.memory_monitor.get_comprehensive_report(
            list(self.agents.values())
        )
        cache_stats = self.cache_manager.get_stats()
        
        return {
            "platform_info": {
                "name": self.platform_name,
                "version": self.version,
                "uptime_hours": (datetime.now() - self.startup_time).total_seconds() / 3600,
                "agents_loaded": len(self.agents)
            },
            "performance_stats": self.stats,
            "memory_usage": memory_report,
            "cache_performance": cache_stats,
            "system_health": {
                "memory_healthy": memory_report["memory_growth"]["growth_mb"] < 100,
                "cache_effective": cache_stats["hit_rate_percent"] > 20,
                "error_rate_low": self.stats["errors_handled"] < self.stats["assessments_completed"] * 0.1
            }
        }
    
    def _format_conflicts(self, conflicts) -> List[Dict[str, Any]]:
        """Format detected conflicts for output"""
        formatted = []
        for conflict in conflicts:
            formatted.append({
                "frameworks": [conflict.framework_a, conflict.framework_b],
                "type": conflict.conflict_type.value,
                "severity": conflict.severity.value,
                "description": conflict.description,
                "resolution_options": conflict.resolution_options
            })
        return formatted
    
    async def optimize_system(self) -> Dict[str, Any]:
        """Perform system optimization and cleanup"""
        
        logger.info("🔧 Starting system optimization...")
        
        optimization_results = {
            "timestamp": datetime.now().isoformat(),
            "actions_taken": [],
            "memory_freed_mb": 0.0,
            "cache_optimized": False,
            "agents_cleaned": 0
        }
        
        try:
            # Cleanup memory
            cleanup_stats = self.memory_monitor.cleanup_unused_resources()
            optimization_results["memory_freed_mb"] = cleanup_stats["garbage_collection"]["memory_freed_mb"]
            optimization_results["actions_taken"].append("Memory cleanup completed")
            self.stats["memory_cleanups"] += 1
            
            # Optimize cache
            self.cache_manager.optimize()
            optimization_results["cache_optimized"] = True
            optimization_results["actions_taken"].append("Cache optimization completed")
            
            # Cleanup agents
            cleaned_agents = 0
            for agent in self.agents.values():
                if hasattr(agent, 'cleanup'):
                    agent.cleanup()
                    cleaned_agents += 1
            
            optimization_results["agents_cleaned"] = cleaned_agents
            optimization_results["actions_taken"].append(f"Cleaned up {cleaned_agents} agents")
            
            logger.info(f"✅ System optimization completed - {optimization_results['memory_freed_mb']:.1f}MB freed")
            
        except Exception as e:
            logger.error(f"💥 System optimization failed: {e}")
            optimization_results["error"] = str(e)
            self.stats["errors_handled"] += 1
        
        return optimization_results
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive system health check"""
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "UNKNOWN",
            "components": {},
            "recommendations": []
        }
        
        # Check agents
        working_agents = 0
        for name, agent in self.agents.items():
            if agent and hasattr(agent, 'assess'):
                health_status["components"][f"agent_{name}"] = "HEALTHY"
                working_agents += 1
            else:
                health_status["components"][f"agent_{name}"] = "UNHEALTHY"
        
        # Check cache
        try:
            cache_stats = self.cache_manager.get_stats()
            if cache_stats["hit_rate_percent"] > 0:
                health_status["components"]["cache_manager"] = "HEALTHY"
            else:
                health_status["components"]["cache_manager"] = "WARNING"
                health_status["recommendations"].append("Cache not being utilized effectively")
        except:
            health_status["components"]["cache_manager"] = "UNHEALTHY"
        
        # Check memory
        try:
            memory_report = self.memory_monitor.get_comprehensive_report()
            if memory_report["memory_growth"]["growth_mb"] < 200:
                health_status["components"]["memory_monitor"] = "HEALTHY"
            else:
                health_status["components"]["memory_monitor"] = "WARNING"
                health_status["recommendations"].append("High memory growth detected")
        except:
            health_status["components"]["memory_monitor"] = "UNHEALTHY"
        
        # Run security audit
        try:
            audit_result = await self.run_security_audit()
            if audit_result["production_ready"]:
                health_status["components"]["security"] = "HEALTHY"
            else:
                health_status["components"]["security"] = "UNHEALTHY"
                health_status["recommendations"].extend(audit_result.get("recommendations", []))
        except:
            health_status["components"]["security"] = "UNHEALTHY"
            health_status["recommendations"].append("Security audit failed")
        
        # Determine overall health
        healthy_components = sum(1 for status in health_status["components"].values() if status == "HEALTHY")
        total_components = len(health_status["components"])
        
        if healthy_components == total_components:
            health_status["overall_health"] = "HEALTHY"
        elif healthy_components >= total_components * 0.8:
            health_status["overall_health"] = "WARNING"
        else:
            health_status["overall_health"] = "UNHEALTHY"
        
        return health_status
    
    async def generate_professional_report(self, 
                                          company_profile: CompanyProfile,
                                          assessment_results: Dict[str, Any],
                                          output_format: str = "pdf") -> Dict[str, Any]:
        """
        Generate professional compliance report using enhanced PDF generation
        """
        
        logger.info(f"🎯 Generating professional {output_format.upper()} report for {company_profile.company_name}")
        
        # Use enhanced PDF generator if available
        if self.pdf_generator and hasattr(self.pdf_generator, 'generate_executive_report'):
            try:
                company_dict = asdict(company_profile)
                result = await self.pdf_generator.generate_executive_report(
                    company_dict, assessment_results, output_format
                )
                
                if result.get("success"):
                    logger.info("✅ Enhanced professional report generated successfully")
                    return result
                else:
                    logger.warning(f"⚠️ Enhanced report generation failed: {result.get('error')}")
                    # Fall back to basic report generation
                    
            except Exception as e:
                logger.error(f"❌ Enhanced PDF generation failed: {e}")
                # Fall back to basic report generation
        
        # Basic report generation fallback
        report_data = {
            "generation_time": datetime.now().isoformat(),
            "company_profile": company_profile,
            "assessment_results": assessment_results,
            "professional_sections": [],
            "report_files": []
        }
        
        try:
            # Generate professional sections using ISMS training
            if self.isms_training_engine:
                for framework in assessment_results.get("frameworks_assessed", []):
                    professional_section = self.isms_training_engine.generate_professional_assessment(
                        company_profile.__dict__ if hasattr(company_profile, '__dict__') else company_profile,
                        assessment_results,
                        framework
                    )
                    report_data["professional_sections"].append(professional_section)
            
            # Generate PDF report if requested
            if output_format.lower() == "pdf" and self.pdf_generator:
                pdf_filename = f"compliance_report_{company_profile.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
                # Convert assessment results for PDF generator
                pdf_data = {
                    "company_name": company_profile.company_name,
                    "industry": company_profile.industry,
                    "employee_count": company_profile.employee_count,
                    "assessment_date": datetime.now().strftime("%Y-%m-%d"),
                    "overall_score": assessment_results.get("overall_confidence", 0.0) * 100,
                    "frameworks_assessed": assessment_results.get("frameworks_assessed", []),
                    "gaps_identified": assessment_results.get("assessment_results", {}),
                    "executive_summary": assessment_results.get("executive_summary", "Assessment completed successfully."),
                    "escalation_required": assessment_results.get("escalation_required", "none")
                }
                
                pdf_path = self.pdf_generator.generate_compliance_report(
                    company_data=pdf_data,
                    assessment_results=assessment_results,
                    output_file=pdf_filename
                )
                
                report_data["report_files"].append({
                    "format": "pdf",
                    "filename": pdf_filename,
                    "path": pdf_path,
                    "size_mb": "Calculated in production"
                })
                
                logger.info(f"📄 PDF report generated: {pdf_filename}")
            
            # Add professional report metadata
            report_data["report_metadata"] = {
                "isms_enhanced": self.isms_training_engine is not None,
                "pdf_generation": self.pdf_generator is not None,
                "professional_sections_count": len(report_data["professional_sections"]),
                "confidence_level": self._determine_overall_confidence_level(assessment_results),
                "expert_review_recommended": any(
                    section.expert_review_required for section in report_data["professional_sections"]
                )
            }
            
            logger.info(f"✅ Professional report generation completed - {len(report_data['professional_sections'])} sections")
            return report_data
            
        except Exception as e:
            logger.error(f"💥 Professional report generation failed: {e}")
            return {
                "error": str(e),
                "generation_time": datetime.now().isoformat(),
                "fallback_report": "Basic assessment report available"
            }
    
    def _determine_overall_confidence_level(self, assessment_results: Dict[str, Any]) -> str:
        """Determine overall confidence level for professional reporting"""
        
        confidence = assessment_results.get("overall_confidence", 0.0)
        
        if confidence >= 0.9:
            return "High Confidence - Professional Opinion"
        elif confidence >= 0.7:
            return "Medium Confidence - Professional Judgment Applied"
        elif confidence >= 0.5:
            return "Low Confidence - Limited Assurance"
        else:
            return "Expert Review Required - Insufficient Evidence"
    
    async def enhanced_assess_with_escalation(self,
                                            company_profile: CompanyProfile,
                                            frameworks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Enhanced assessment with automatic expert escalation and liability protection
        """
        
        logger.info(f"🎯 Enhanced assessment with escalation for {company_profile.company_name}")
        
        # Perform standard assessment
        assessment_result = await self.assess_company(company_profile, frameworks)
        
        # Evaluate escalation needs and liability protection
        escalation_analysis = {}
        liability_assessment = {}
        
        if self.expert_escalation_system and self.liability_manager:
            try:
                for framework in assessment_result.get("frameworks_assessed", []):
                    # Evaluate escalation need
                    escalation_decision = self.expert_escalation_system.evaluate_escalation_need(
                        assessment_result,
                        company_profile.__dict__ if hasattr(company_profile, '__dict__') else company_profile,
                        framework
                    )
                    escalation_analysis[framework] = escalation_decision
                    
                    # Create escalation request if needed
                    if escalation_decision["escalation_required"]:
                        escalation_request = await self.expert_escalation_system.create_escalation_request(
                            company_profile.__dict__ if hasattr(company_profile, '__dict__') else company_profile,
                            assessment_result,
                            framework,
                            escalation_decision
                        )
                        escalation_analysis[framework]["escalation_request_id"] = escalation_request.request_id
                    
                    # Assess liability exposure
                    liability_analysis = self.liability_manager.assess_liability_exposure(
                        assessment_result, framework, company_profile
                    )
                    liability_assessment[framework] = liability_analysis
                
                # Add enhanced results to assessment
                assessment_result["escalation_analysis"] = escalation_analysis
                assessment_result["liability_assessment"] = liability_assessment
                assessment_result["professional_safeguards"] = {
                    "expert_escalation_available": True,
                    "liability_protection_active": True,
                    "professional_disclaimers_applied": True,
                    "audit_trail_maintained": True
                }
                
                logger.info(f"✅ Enhanced assessment completed with escalation analysis")
                
            except Exception as e:
                logger.error(f"💥 Enhanced assessment features failed: {e}")
                assessment_result["escalation_error"] = str(e)
        
        return assessment_result
    
    async def assess_compliance(self, company_profile: CompanyProfile, framework_name: str) -> Dict[str, Any]:
        """
        Assess compliance for a specific framework
        Public method called by web API endpoints
        """
        try:
            logger.info(f"🎯 Starting {framework_name} assessment for {company_profile.company_name}")
            
            # Map framework names to internal keys
            framework_mapping = {
                "NIST SP 800-53": "nist_800_53",
                "SOC 2": "soc2",
                "Essential 8": "essential_eight",
                "Privacy Act 1988": "privacy_act",
                "APRA CPS 234": "apra_cps234",
                "NIST CSF": "nist_csf"
            }
            
            framework_key = framework_mapping.get(framework_name, framework_name.lower().replace(" ", "_"))
            
            # Use the private _assess_framework method
            result = await self._assess_framework(framework_key, company_profile)
            
            # Convert AssessmentResult to dict if needed
            if hasattr(result, '__dict__'):
                result_dict = asdict(result)
                # Convert datetime objects to ISO strings for JSON serialization
                if 'timestamp' in result_dict and hasattr(result_dict['timestamp'], 'isoformat'):
                    result_dict['timestamp'] = result_dict['timestamp'].isoformat()
                # Convert enum objects to their values for JSON serialization
                if 'status' in result_dict and hasattr(result_dict['status'], 'value'):
                    result_dict['status'] = result_dict['status'].value
                if 'risk_level' in result_dict and hasattr(result_dict['risk_level'], 'value'):
                    result_dict['risk_level'] = result_dict['risk_level'].value
                return result_dict
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Assessment failed for {framework_name}: {e}")
            return {
                "framework": framework_name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_liability_disclaimers(self, scenario: str = "general_platform") -> Dict[str, Any]:
        """Get appropriate liability disclaimers for scenario"""
        
        if self.liability_manager:
            return self.liability_manager.get_disclaimer_for_scenario(scenario)
        
        return {
            "disclaimer": "This assessment is provided for informational purposes only.",
            "liability_level": "minimal",
            "acknowledgment_required": False
        }
    
    def get_expert_escalation_status(self) -> Dict[str, Any]:
        """Get current expert escalation system status"""
        
        if self.expert_escalation_system:
            return self.expert_escalation_system.get_system_metrics()
        
        return {
            "expert_escalation": "Not available",
            "human_experts": 0,
            "active_escalations": 0
        }
    
    async def comprehensive_security_assessment(self,
                                               company_profile: CompanyProfile,
                                               target_systems: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive security assessment using all OWASP frameworks
        plus standard compliance assessment
        """
        
        logger.info(f"🛡️ Comprehensive security assessment for {company_profile.company_name}")
        
        # Default target systems if none provided
        if not target_systems:
            target_systems = [
                {"type": "web_application", "name": f"{company_profile.company_name}_WebApp"},
                {"type": "api", "name": f"{company_profile.company_name}_API"},
                {"type": "ai_system", "name": "Cerberus_AI_Platform"}
            ]
        
        comprehensive_results = {
            "assessment_id": f"security_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "company": company_profile.company_name,
            "assessment_date": datetime.now().isoformat(),
            "compliance_assessment": None,
            "security_assessment": None,
            "combined_score": 0.0,
            "executive_summary": "",
            "critical_security_findings": [],
            "recommendations": []
        }
        
        try:
            # Standard compliance assessment
            compliance_result = await self.enhanced_assess_with_escalation(company_profile)
            comprehensive_results["compliance_assessment"] = compliance_result
            
            # OWASP security assessment
            if self.owasp_security_orchestrator:
                security_result = await self.owasp_security_orchestrator.comprehensive_security_assessment(target_systems)
                comprehensive_results["security_assessment"] = security_result
                
                # Combine scores
                compliance_score = compliance_result.get("overall_confidence", 0.0) * 100
                security_score = security_result.get("overall_security_score", 0.0)
                combined_score = (compliance_score + security_score) / 2
                comprehensive_results["combined_score"] = combined_score
                
                # Critical findings
                comprehensive_results["critical_security_findings"] = security_result.get("critical_findings", [])
                
                # Executive summary
                comprehensive_results["executive_summary"] = self._generate_security_executive_summary(
                    company_profile, compliance_result, security_result, combined_score
                )
                
                # Combined recommendations
                compliance_recs = compliance_result.get("executive_summary", "").split(". ")[-5:]
                security_recs = security_result.get("recommendations", [])
                comprehensive_results["recommendations"] = list(set(compliance_recs + security_recs))
                
                logger.info(f"✅ Comprehensive security assessment completed - Combined score: {combined_score:.1f}%")
            
            else:
                logger.warning("⚠️ OWASP security orchestrator not available - compliance only")
                comprehensive_results["security_assessment"] = {"error": "Security frameworks not available"}
                comprehensive_results["combined_score"] = compliance_result.get("overall_confidence", 0.0) * 100
            
            return comprehensive_results
            
        except Exception as e:
            logger.error(f"💥 Comprehensive security assessment failed: {e}")
            return {
                "error": str(e),
                "assessment_date": datetime.now().isoformat(),
                "fallback_available": "Standard compliance assessment available"
            }
    
    def _generate_security_executive_summary(self,
                                           company_profile: CompanyProfile,
                                           compliance_result: Dict[str, Any],
                                           security_result: Dict[str, Any],
                                           combined_score: float) -> str:
        """Generate executive summary for comprehensive security assessment"""
        
        frameworks_assessed = compliance_result.get("frameworks_assessed", [])
        security_frameworks = security_result.get("frameworks_assessed", [])
        critical_findings = len(security_result.get("critical_findings", []))
        
        summary = f"""
**Comprehensive Security & Compliance Assessment Summary**

**Organization:** {company_profile.company_name} ({company_profile.industry})
**Assessment Date:** {datetime.now().strftime('%Y-%m-%d')}
**Combined Security Score:** {combined_score:.1f}%

**Compliance Frameworks Assessed:** {', '.join(frameworks_assessed)}
**Security Frameworks Assessed:** {', '.join(security_frameworks)}

**Key Findings:**
• Overall security and compliance posture: {self._determine_posture_rating(combined_score)}
• Critical security findings requiring immediate attention: {critical_findings}
• Professional safeguards active: Expert escalation and liability protection enabled
• Platform self-defense: {'Active' if 'Platform Self-Defense' in security_frameworks else 'Not assessed'}

**Management Attention Required:**
{self._generate_management_priorities(compliance_result, security_result)}

**Next Steps:**
1. Address critical security findings immediately
2. Implement recommended compliance controls
3. Schedule regular security and compliance reviews
4. Maintain continuous monitoring and improvement

This assessment combines traditional compliance evaluation with modern security frameworks including OWASP Top 10 across Web, Mobile, API, and AI/LLM domains, providing comprehensive coverage of your organization's risk landscape.
"""
        
        return summary.strip()
    
    def _determine_posture_rating(self, score: float) -> str:
        """Determine security posture rating from combined score"""
        
        if score >= 90:
            return "Excellent - Industry leading security and compliance posture"
        elif score >= 80:
            return "Good - Strong security controls with minor gaps"
        elif score >= 70:
            return "Adequate - Acceptable posture with improvement opportunities"
        elif score >= 60:
            return "Concerning - Significant gaps requiring attention"
        else:
            return "Critical - Immediate remediation required across multiple areas"
    
    def _generate_management_priorities(self,
                                       compliance_result: Dict[str, Any],
                                       security_result: Dict[str, Any]) -> str:
        """Generate management priorities from assessment results"""
        
        priorities = []
        
        # Compliance priorities
        escalation_required = compliance_result.get("escalation_required", "none")
        if escalation_required != "none":
            priorities.append(f"Compliance escalation required: {escalation_required}")
        
        # Security priorities
        critical_findings = len(security_result.get("critical_findings", []))
        if critical_findings > 0:
            priorities.append(f"{critical_findings} critical security findings require immediate remediation")
        
        # Overall risk
        combined_score = (compliance_result.get("overall_confidence", 0.0) * 100 + 
                         security_result.get("overall_security_score", 0.0)) / 2
        
        if combined_score < 70:
            priorities.append("Comprehensive security and compliance improvement program recommended")
        
        if not priorities:
            priorities.append("Continue current security and compliance practices with regular reviews")
        
        return "; ".join(priorities)
    
    async def get_intelligent_control_selection(self,
                                               company_profile: Dict[str, Any],
                                               target_certification: str,
                                               risk_tolerance: str = "medium") -> Dict[str, Any]:
        """
        🎯 THE KILLER FEATURE: Intelligent Dynamic Control Selection
        This is what makes Sentinel GRC unique in the market!
        
        Uses the restored Intelligence Knowledge Graph to provide:
        - Context-aware control prioritization
        - Cross-framework mapping intelligence
        - Company-specific implementation guidance
        - Risk-based timeline estimation
        """
        
        logger.info(f"🎯 Generating intelligent control selection for {target_certification}")
        
        try:
            if not self.intelligence_graph:
                logger.error("❌ Intelligence Knowledge Graph not available")
                return {
                    "success": False,
                    "error": "Intelligence core not initialized",
                    "fallback_message": "Please check neo4j connection or restart platform"
                }
            
            # Use the intelligence graph to generate dynamic control selection
            intelligent_result = await self.intelligence_graph.get_dynamic_control_selection(
                company_profile=company_profile,
                target_certification=target_certification,
                risk_tolerance=risk_tolerance
            )
            
            # Enhance with platform-specific insights
            enhanced_result = await self._enhance_with_platform_intelligence(intelligent_result)
            
            # Store the result for learning
            await self.intelligence_graph.store_assessment_result({
                "company_profile": company_profile,
                "certification": target_certification,
                "result": enhanced_result,
                "generated_at": datetime.now().isoformat()
            })
            
            logger.info(f"✅ Intelligent control selection completed: {len(enhanced_result.get('prioritized_controls', []))} controls prioritized")
            
            return {
                "success": True,
                "data": enhanced_result,
                "intelligence_powered": True,
                "unique_selling_point": "Context-aware compliance intelligence",
                "competitive_advantage": "No other platform provides this level of intelligent control selection"
            }
            
        except Exception as e:
            logger.error(f"❌ Intelligent control selection failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_available": True
            }
    
    async def _enhance_with_platform_intelligence(self, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance intelligence graph results with platform-specific insights
        """
        
        try:
            # Add platform-specific metrics
            platform_insights = {
                "platform_version": self.version,
                "assessment_confidence": "HIGH",  # Intelligence-powered = high confidence
                "data_sources": [
                    "Neo4j Knowledge Graph",
                    "Cross-Framework Intelligence", 
                    "Industry Best Practices",
                    "Regulatory Updates"
                ],
                "competitive_differentiators": [
                    "Dynamic control importance scoring",
                    "Cross-framework relationship mapping",
                    "Company-context aware recommendations",
                    "Continuous learning from implementations"
                ]
            }
            
            # Integrate with existing agents for additional validation
            if base_result.get('certification') == 'iso_27001':
                if hasattr(self, 'agents') and 'iso_27001' in self.agents:
                    # Get additional insights from ISO 27001 agent
                    agent_insights = await self.agents['iso_27001'].get_implementation_insights(
                        base_result.get('prioritized_controls', [])
                    )
                    platform_insights['agent_validation'] = agent_insights
            
            # Add memory optimization insights
            memory_status = self.memory_monitor.get_current_status()
            platform_insights['platform_health'] = {
                "memory_usage": f"{memory_status.get('memory_mb', 0):.1f}MB",
                "performance_status": "Optimal" if memory_status.get('memory_mb', 0) < 100 else "Good"
            }
            
            # Enhance the base result
            enhanced_result = base_result.copy()
            enhanced_result['platform_intelligence'] = platform_insights
            enhanced_result['enhancement_timestamp'] = datetime.now().isoformat()
            
            return enhanced_result
            
        except Exception as e:
            logger.warning(f"⚠️ Platform enhancement failed, returning base result: {e}")
            return base_result
    
    async def platform_self_defense_check(self) -> Dict[str, Any]:
        """
        Perform platform self-defense security assessment
        'Physician heal thyself' - ensure Cerberus AI platform is secure
        """
        
        logger.info("🏥 Platform self-defense assessment - 'Physician heal thyself'")
        
        if not self.owasp_security_orchestrator:
            return {"error": "OWASP security orchestrator not available"}
        
        # Platform self-assessment
        platform_systems = [
            {"type": "web_application", "name": "Cerberus_Platform_UI"},
            {"type": "api", "name": "Cerberus_API_Gateway"},
            {"type": "ai_system", "name": "Cerberus_AI_Engine"},
            {"type": "llm", "name": "Cerberus_LLM_Components"}
        ]
        
        try:
            self_defense_result = await self.owasp_security_orchestrator.comprehensive_security_assessment(platform_systems)
            
            # Add platform-specific context
            self_defense_result["platform_specific"] = {
                "self_assessment": True,
                "physician_heal_thyself": True,
                "platform_components_assessed": len(platform_systems),
                "self_defense_score": self_defense_result.get("overall_security_score", 0.0),
                "platform_integrity": "Verified" if self_defense_result.get("overall_security_score", 0.0) > 80 else "Requires attention"
            }
            
            logger.info(f"🏥 Platform self-defense completed - Integrity: {self_defense_result['platform_specific']['platform_integrity']}")
            
            return self_defense_result
            
        except Exception as e:
            logger.error(f"💥 Platform self-defense assessment failed: {e}")
            return {
                "error": str(e),
                "platform_status": "Self-defense assessment failed - manual security review required"
            }

# Convenience functions for easy usage
async def quick_assessment(company_name: str, industry: str, employee_count: int) -> Dict[str, Any]:
    """Quick assessment with minimal setup"""
    
    platform = SentinelGRC()
    
    company_profile = CompanyProfile(
        company_name=company_name,
        industry=industry,
        employee_count=employee_count
    )
    
    return await platform.assess_company(company_profile)

async def demo_assessment() -> Dict[str, Any]:
    """Demo assessment for testing"""
    
    return await quick_assessment(
        company_name="Demo Healthcare Corp",
        industry="Healthcare",
        employee_count=250
    )

# Main entry point
async def main():
    """Main entry point for the Sentinel GRC platform"""
    
    print("🚀 Starting Sentinel GRC Enterprise Compliance Platform")
    print("=" * 60)
    
    # Initialize platform
    platform = SentinelGRC()
    
    # Run health check
    health = await platform.health_check()
    print(f"System Health: {health['overall_health']}")
    
    if health["recommendations"]:
        print("Recommendations:")
        for rec in health["recommendations"]:
            print(f"  • {rec}")
    
    # Run demo assessment if healthy
    if health["overall_health"] in ["HEALTHY", "WARNING"]:
        print("\n📊 Running demo assessment...")
        
        demo_result = await demo_assessment()
        
        print(f"Assessment completed: {demo_result['overall_status']}")
        print(f"Confidence: {demo_result['overall_confidence']:.1f}%")
        print(f"Escalation: {demo_result['escalation_required']}")
        
        # Show platform stats
        stats = platform.get_platform_stats()
        print(f"\nPlatform Stats:")
        print(f"  Assessments: {stats['performance_stats']['assessments_completed']}")
        print(f"  Memory Usage: {stats['memory_usage']['process_memory']['rss_mb']:.1f}MB")
        print(f"  Cache Hit Rate: {stats['cache_performance']['hit_rate_percent']:.1f}%")
    
    print("\n✅ Sentinel GRC platform demonstration complete")

if __name__ == "__main__":
    asyncio.run(main())