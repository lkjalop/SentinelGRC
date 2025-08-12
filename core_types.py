"""
Sentinel GRC - Core Types and Configuration
==========================================

Shared types, enums, and configuration classes to prevent circular imports.
This module contains the fundamental data structures used across all agents.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from collections import deque
import weakref

# ============================================================================
# CONFIGURATION AND CONSTANTS
# ============================================================================

class Config:
    """
    Production configuration with enterprise-grade thresholds.
    Zero-budget optimization using open-source tools only.
    """
    
    # Confidence thresholds for enterprise decision-making
    MIN_CONFIDENCE_FOR_AUTO_APPROVAL = 0.85  # High confidence auto-approval
    MIN_CONFIDENCE_FOR_RECOMMENDATION = 0.70  # Medium confidence with review
    ALWAYS_ESCALATE_THRESHOLD = 0.60  # Low confidence requires human input
    
    # Risk thresholds for human escalation
    HIGH_RISK_FINANCIAL_THRESHOLD = 50000  # Dollar impact requiring executive review
    HIGH_RISK_EMPLOYEE_THRESHOLD = 500  # Company size requiring extra scrutiny
    
    # System behavior for enterprise performance
    MAX_AGENT_RETRIES = 3
    AGENT_TIMEOUT_SECONDS = 30
    CACHE_TTL_SECONDS = 3600
    PARALLEL_AGENT_LIMIT = 10  # Increased for enterprise load
    
    # Legal and ethical boundaries
    LEGAL_DISCLAIMER = """
    This assessment is provided by an AI system for informational purposes only.
    It does not constitute professional compliance advice. Please consult with
    qualified compliance professionals for official assessments and legal guidance.
    """
    
    # Industries requiring special care (enterprise focus)
    HIGH_RISK_INDUSTRIES = ["Healthcare", "Finance", "Government", "Defense", "Critical Infrastructure"]
    
    # Compliance frameworks available (expandable for US market)
    AVAILABLE_FRAMEWORKS = {
        # Australian Frameworks
        "Essential8": "Australian Essential Eight",
        "PrivacyAct": "Privacy Act 1988",
        "APRA_CPS234": "APRA CPS 234",
        "SOCI": "Security of Critical Infrastructure Act",
        
        # International Frameworks (for US expansion)
        "ISO27001": "ISO/IEC 27001:2022",
        "NIST_CSF": "NIST Cybersecurity Framework",
        "SOC2": "SOC 2 Type II",
        "PCI_DSS": "PCI Data Security Standard",
        "HIPAA": "Health Insurance Portability and Accountability Act",
        "SOX": "Sarbanes-Oxley Act"
    }
    
    # Database configuration (zero-budget approach)
    DATABASE_CONFIG = {
        "use_connection_pool": True,
        "max_connections": 20,
        "min_connections": 5,
        "connection_timeout": 30,
        "retry_attempts": 3
    }

# ============================================================================
# CORE ENUMERATIONS
# ============================================================================

class ConfidenceLevel(Enum):
    """Confidence levels for enterprise decision-making"""
    VERY_HIGH = "very_high"  # >90% - Auto-approval suitable
    HIGH = "high"  # 80-90% - Recommendation with light review  
    MEDIUM = "medium"  # 70-80% - Standard review required
    LOW = "low"  # 60-70% - Expert review required
    VERY_LOW = "very_low"  # <60% - Human intervention required

class EscalationType(Enum):
    """Types of human escalation required"""
    NONE = "none"
    REVIEW_RECOMMENDED = "review_recommended"
    EXPERT_REQUIRED = "expert_required"
    LEGAL_REQUIRED = "legal_required"
    EXECUTIVE_REQUIRED = "executive_required"

class AssessmentStatus(Enum):
    """Assessment execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"

class RiskLevel(Enum):
    """Risk level classifications"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

# ============================================================================
# CORE DATA MODELS
# ============================================================================

@dataclass
class CompanyProfile:
    """Company profile for compliance assessment"""
    company_name: str
    industry: str
    employee_count: int
    country: str = "Australia"
    has_government_contracts: bool = False
    annual_revenue: Optional[float] = None
    current_controls: List[str] = None
    previous_incidents: List[str] = None
    compliance_history: Dict[str, Any] = None
    
    # Enterprise features
    business_units: List[str] = None
    cloud_providers: List[str] = None
    data_classifications: List[str] = None
    regulatory_requirements: List[str] = None
    
    def __post_init__(self):
        if self.current_controls is None:
            self.current_controls = []
        if self.previous_incidents is None:
            self.previous_incidents = []
        if self.compliance_history is None:
            self.compliance_history = {}
        if self.business_units is None:
            self.business_units = []
        if self.cloud_providers is None:
            self.cloud_providers = []
        if self.data_classifications is None:
            self.data_classifications = []
        if self.regulatory_requirements is None:
            self.regulatory_requirements = []

@dataclass
class AssessmentResult:
    """Standardized assessment result structure"""
    framework: str
    company: str
    timestamp: datetime
    status: AssessmentStatus
    confidence: float
    risk_level: RiskLevel
    
    # Assessment details
    controls_assessed: List[Dict[str, Any]]
    gaps_identified: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    evidence: List[Dict[str, Any]]
    
    # Scoring
    overall_score: float
    control_scores: Dict[str, float]
    maturity_scores: Dict[str, int]
    
    # Enterprise features
    executive_summary: str = ""
    business_impact: str = ""
    remediation_timeline: Dict[str, str] = None
    cost_estimates: Dict[str, float] = None
    
    def __post_init__(self):
        if self.remediation_timeline is None:
            self.remediation_timeline = {}
        if self.cost_estimates is None:
            self.cost_estimates = {}

# ============================================================================
# SHARED RESOURCE MANAGEMENT (Memory Leak Prevention)
# ============================================================================

class SharedKnowledgeGraphManager:
    """
    Singleton manager for shared knowledge graphs to prevent memory leaks.
    Each framework gets one shared instance instead of per-agent instances.
    """
    _instances = {}
    _lock = None
    
    @classmethod
    def get_instance(cls, framework: str):
        """Get or create shared knowledge graph instance for framework"""
        if framework not in cls._instances:
            # In a real implementation, this would load the actual knowledge graph
            # For now, we'll use a placeholder that represents the shared resource
            cls._instances[framework] = {
                "framework": framework,
                "graph_data": {},  # Placeholder for actual graph
                "created_at": datetime.now(),
                "access_count": 0
            }
        
        cls._instances[framework]["access_count"] += 1
        return cls._instances[framework]
    
    @classmethod
    def cleanup_unused(cls, max_idle_hours: int = 24):
        """Clean up unused knowledge graph instances"""
        current_time = datetime.now()
        to_remove = []
        
        for framework, instance in cls._instances.items():
            idle_hours = (current_time - instance["created_at"]).total_seconds() / 3600
            if idle_hours > max_idle_hours and instance["access_count"] == 0:
                to_remove.append(framework)
        
        for framework in to_remove:
            del cls._instances[framework]

class AgentMetricsTracker:
    """
    Track agent performance metrics with bounded storage to prevent memory leaks.
    Uses weak references to avoid circular references.
    """
    
    def __init__(self, max_history_size: int = 100):
        self.max_history_size = max_history_size
        self.confidence_history = deque(maxlen=max_history_size)
        self.decision_log = deque(maxlen=max_history_size)
        self.performance_metrics = {}
    
    def add_confidence_score(self, score: float):
        """Add confidence score with automatic bounded storage"""
        self.confidence_history.append({
            "score": score,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_decision(self, decision: str, reasoning: str, confidence: float, agent_name: str):
        """Add decision to log with automatic bounded storage"""
        self.decision_log.append({
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "reasoning": reasoning,
            "confidence": confidence,
            "agent": agent_name
        })
    
    def get_recent_confidence_average(self, last_n: int = 10) -> float:
        """Get average confidence from recent assessments"""
        if not self.confidence_history:
            return 0.7  # Default confidence
        
        recent_scores = list(self.confidence_history)[-last_n:]
        if recent_scores:
            import numpy as np
            return float(np.mean([entry["score"] for entry in recent_scores]))
        return 0.7
    
    def get_memory_usage(self) -> Dict[str, int]:
        """Get current memory usage statistics"""
        return {
            "confidence_history_size": len(self.confidence_history),
            "decision_log_size": len(self.decision_log),
            "max_history_size": self.max_history_size
        }

# ============================================================================
# ABSTRACT BASE CLASSES (Memory-Optimized)
# ============================================================================

class BaseComplianceAgent(ABC):
    """
    Base agent class for specialized compliance assessments.
    Implements enterprise-grade patterns with memory leak prevention.
    """
    
    def __init__(self, name: str, expertise: str, framework: str = "generic"):
        self.name = name
        self.expertise = expertise
        self.framework = framework
        
        # Use shared knowledge graph to prevent memory leaks
        self.knowledge_graph = SharedKnowledgeGraphManager.get_instance(framework)
        
        # Use bounded collections to prevent memory leaks
        self.metrics = AgentMetricsTracker(max_history_size=100)
        
        # Track agent lifecycle for cleanup
        self.created_at = datetime.now()
        self.last_used = datetime.now()
        
    @abstractmethod
    async def assess(self, company_profile: CompanyProfile) -> AssessmentResult:
        """Perform specialized compliance assessment"""
        pass
    
    def calculate_confidence(self, assessment_data: Dict[str, Any]) -> float:
        """Calculate confidence score with memory-efficient historical learning"""
        self.last_used = datetime.now()
        
        base_confidence = 0.7
        
        # Evidence quality factors
        if len(assessment_data.get("evidence", [])) > 5:
            base_confidence += 0.1
        
        if assessment_data.get("data_quality") == "HIGH":
            base_confidence += 0.1
        
        # Risk factors
        if assessment_data.get("ambiguous_findings", 0) > 2:
            base_confidence -= 0.15
        
        if assessment_data.get("missing_data", False):
            base_confidence -= 0.2
        
        # Historical learning with bounded memory
        avg_historical = self.metrics.get_recent_confidence_average(last_n=10)
        base_confidence = 0.7 * base_confidence + 0.3 * avg_historical
        
        confidence = max(0.0, min(1.0, base_confidence))
        
        # Store with automatic memory management
        self.metrics.add_confidence_score(confidence)
        
        return confidence
    
    def log_decision(self, decision: str, reasoning: str, confidence: float):
        """Log decision with bounded storage to prevent memory leaks"""
        self.last_used = datetime.now()
        self.metrics.add_decision(decision, reasoning, confidence, self.name)
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics for monitoring"""
        metrics = self.metrics.get_memory_usage()
        metrics.update({
            "agent_name": self.name,
            "framework": self.framework,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat(),
            "knowledge_graph_shared": True,
            "knowledge_graph_access_count": self.knowledge_graph.get("access_count", 0)
        })
        return metrics
    
    def cleanup(self):
        """Manual cleanup for agent resources"""
        # Cleanup metrics
        self.metrics.confidence_history.clear()
        self.metrics.decision_log.clear()
        
        # Mark knowledge graph as no longer needed by this agent
        if hasattr(self, 'knowledge_graph') and self.knowledge_graph:
            self.knowledge_graph["access_count"] = max(0, self.knowledge_graph["access_count"] - 1)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_risk_level(score: float) -> RiskLevel:
    """Convert numeric score to risk level"""
    if score >= 0.9:
        return RiskLevel.VERY_LOW
    elif score >= 0.7:
        return RiskLevel.LOW
    elif score >= 0.5:
        return RiskLevel.MEDIUM
    elif score >= 0.3:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL

def get_confidence_level(confidence: float) -> ConfidenceLevel:
    """Convert numeric confidence to confidence level"""
    if confidence >= 0.9:
        return ConfidenceLevel.VERY_HIGH
    elif confidence >= 0.8:
        return ConfidenceLevel.HIGH
    elif confidence >= 0.7:
        return ConfidenceLevel.MEDIUM
    elif confidence >= 0.6:
        return ConfidenceLevel.LOW
    else:
        return ConfidenceLevel.VERY_LOW

def determine_escalation(confidence: float, risk_level: RiskLevel, company_profile: CompanyProfile) -> EscalationType:
    """Determine required escalation level"""
    
    # Always escalate critical risks
    if risk_level == RiskLevel.CRITICAL:
        return EscalationType.EXECUTIVE_REQUIRED
    
    # Low confidence always requires review
    if confidence < Config.ALWAYS_ESCALATE_THRESHOLD:
        if company_profile.industry in Config.HIGH_RISK_INDUSTRIES:
            return EscalationType.LEGAL_REQUIRED
        return EscalationType.EXPERT_REQUIRED
    
    # High-risk industries get extra scrutiny
    if (company_profile.industry in Config.HIGH_RISK_INDUSTRIES and 
        confidence < Config.MIN_CONFIDENCE_FOR_AUTO_APPROVAL):
        return EscalationType.REVIEW_RECOMMENDED
    
    # Large organizations require review for medium confidence
    if (company_profile.employee_count > Config.HIGH_RISK_EMPLOYEE_THRESHOLD and
        confidence < Config.MIN_CONFIDENCE_FOR_AUTO_APPROVAL):
        return EscalationType.REVIEW_RECOMMENDED
    
    return EscalationType.NONE