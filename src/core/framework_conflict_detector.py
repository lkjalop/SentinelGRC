"""
Framework Conflict Detection Engine
===================================
Competitive differentiator that automatically detects and resolves
conflicts between different compliance framework requirements.

This is a KEY DIFFERENTIATOR for Sentinel GRC - no other platform
automatically identifies when frameworks have conflicting requirements.
"""

import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ConflictType(Enum):
    """Types of conflicts between frameworks"""
    MUTUALLY_EXCLUSIVE = "mutually_exclusive"  # Cannot satisfy both
    RESOURCE_COMPETITION = "resource_competition"  # Both need same resource
    TIMELINE_CONFLICT = "timeline_conflict"  # Different deadlines
    SCOPE_MISMATCH = "scope_mismatch"  # Different scope requirements
    TECHNICAL_INCOMPATIBILITY = "technical_incompatibility"  # Technical requirements conflict
    COST_PROHIBITIVE = "cost_prohibitive"  # Combined cost exceeds budget

class ConflictSeverity(Enum):
    """Severity levels for conflicts"""
    CRITICAL = "critical"  # Must be resolved immediately
    HIGH = "high"  # Significant business impact
    MEDIUM = "medium"  # Moderate impact
    LOW = "low"  # Minor inconvenience

@dataclass
class FrameworkConflict:
    """Represents a conflict between framework requirements"""
    framework_a: str
    control_a: str
    framework_b: str
    control_b: str
    conflict_type: ConflictType
    severity: ConflictSeverity
    description: str
    resolution_options: List[str]
    estimated_resolution_cost: Optional[float] = None
    detected_at: datetime = None
    
    def __post_init__(self):
        if self.detected_at is None:
            self.detected_at = datetime.now()

class FrameworkConflictDetector:
    """
    Advanced conflict detection engine that identifies conflicts
    between multiple compliance frameworks.
    
    This is a UNIQUE COMPETITIVE ADVANTAGE - no other GRC platform
    provides automated conflict detection and resolution.
    """
    
    def __init__(self):
        self.known_conflicts = self._load_known_conflicts()
        self.resolution_strategies = self._load_resolution_strategies()
        self.detected_conflicts: List[FrameworkConflict] = []
        logger.info("🔍 Framework Conflict Detector initialized")
    
    def _load_known_conflicts(self) -> Dict[str, List[Dict]]:
        """Load database of known framework conflicts"""
        return {
            # Privacy conflicts
            "privacy_retention": {
                "frameworks": ["GDPR", "Privacy Act 1988", "CCPA"],
                "conflict": "Different data retention requirements",
                "type": ConflictType.TIMELINE_CONFLICT,
                "resolution": "Use shortest retention period"
            },
            
            # Security conflicts
            "encryption_standards": {
                "frameworks": ["NIST 800-53", "ISO 27001", "Essential Eight"],
                "conflict": "Different encryption strength requirements",
                "type": ConflictType.TECHNICAL_INCOMPATIBILITY,
                "resolution": "Use highest encryption standard"
            },
            
            # Access control conflicts
            "mfa_requirements": {
                "frameworks": ["SOC 2", "Essential Eight ML3", "NIST CSF"],
                "conflict": "Different MFA implementation requirements",
                "type": ConflictType.SCOPE_MISMATCH,
                "resolution": "Implement most comprehensive MFA"
            },
            
            # Audit conflicts
            "audit_frequency": {
                "frameworks": ["SOC 2", "ISO 27001", "APRA CPS 234"],
                "conflict": "Different audit frequency requirements",
                "type": ConflictType.RESOURCE_COMPETITION,
                "resolution": "Align to most frequent requirement"
            },
            
            # Incident response conflicts
            "incident_timeline": {
                "frameworks": ["SOCI Act", "GDPR", "Privacy Act"],
                "conflict": "Different incident notification timelines",
                "type": ConflictType.TIMELINE_CONFLICT,
                "resolution": "Use shortest notification window"
            }
        }
    
    def _load_resolution_strategies(self) -> Dict[ConflictType, List[str]]:
        """Load resolution strategies for each conflict type"""
        return {
            ConflictType.MUTUALLY_EXCLUSIVE: [
                "Choose primary framework based on business priority",
                "Seek exemption or compensating control",
                "Implement separate systems for each requirement",
                "Escalate to legal/compliance team"
            ],
            
            ConflictType.RESOURCE_COMPETITION: [
                "Increase resource allocation",
                "Implement time-sharing schedule",
                "Automate to reduce resource needs",
                "Prioritize based on risk assessment"
            ],
            
            ConflictType.TIMELINE_CONFLICT: [
                "Adopt shortest/most restrictive timeline",
                "Implement automated compliance calendar",
                "Create buffer periods between requirements",
                "Negotiate timeline adjustments where possible"
            ],
            
            ConflictType.SCOPE_MISMATCH: [
                "Implement superset of all requirements",
                "Create framework-specific implementations",
                "Document scope variations clearly",
                "Apply most comprehensive scope"
            ],
            
            ConflictType.TECHNICAL_INCOMPATIBILITY: [
                "Implement highest/strictest standard",
                "Use framework-specific technical controls",
                "Deploy compatibility layer/wrapper",
                "Seek technical exception with compensating controls"
            ],
            
            ConflictType.COST_PROHIBITIVE: [
                "Prioritize based on business risk",
                "Phase implementation over time",
                "Seek budget increase or reallocation",
                "Identify cost-effective alternatives"
            ]
        }
    
    def detect_conflicts(self, active_frameworks: List[str], 
                        controls: Dict[str, List[Dict]]) -> List[FrameworkConflict]:
        """
        Detect conflicts between active frameworks and their controls.
        
        Args:
            active_frameworks: List of framework names being assessed
            controls: Dictionary of framework controls
            
        Returns:
            List of detected conflicts
        """
        conflicts = []
        
        # Check for known conflicts
        for conflict_key, conflict_data in self.known_conflicts.items():
            affected_frameworks = [f for f in active_frameworks 
                                  if f in conflict_data["frameworks"]]
            
            if len(affected_frameworks) >= 2:
                # Create conflict record
                for i in range(len(affected_frameworks)):
                    for j in range(i + 1, len(affected_frameworks)):
                        conflict = FrameworkConflict(
                            framework_a=affected_frameworks[i],
                            control_a=f"{affected_frameworks[i]}_control",
                            framework_b=affected_frameworks[j],
                            control_b=f"{affected_frameworks[j]}_control",
                            conflict_type=conflict_data["type"],
                            severity=self._assess_severity(conflict_data["type"]),
                            description=conflict_data["conflict"],
                            resolution_options=[conflict_data["resolution"]]
                        )
                        conflicts.append(conflict)
        
        # Detect dynamic conflicts based on control analysis
        dynamic_conflicts = self._detect_dynamic_conflicts(active_frameworks, controls)
        conflicts.extend(dynamic_conflicts)
        
        self.detected_conflicts = conflicts
        logger.info(f"🔍 Detected {len(conflicts)} framework conflicts")
        
        return conflicts
    
    def _detect_dynamic_conflicts(self, frameworks: List[str], 
                                 controls: Dict[str, List[Dict]]) -> List[FrameworkConflict]:
        """Detect conflicts by analyzing control requirements dynamically"""
        conflicts = []
        
        # Analyze control overlaps and conflicts
        for i, framework_a in enumerate(frameworks):
            if framework_a not in controls:
                continue
                
            for j, framework_b in enumerate(frameworks[i+1:], i+1):
                if framework_b not in controls:
                    continue
                
                # Check for conflicting requirements
                conflicts_found = self._compare_framework_controls(
                    framework_a, controls[framework_a],
                    framework_b, controls[framework_b]
                )
                conflicts.extend(conflicts_found)
        
        return conflicts
    
    def _compare_framework_controls(self, framework_a: str, controls_a: List[Dict],
                                   framework_b: str, controls_b: List[Dict]) -> List[FrameworkConflict]:
        """Compare controls between two frameworks to find conflicts"""
        conflicts = []
        
        # Example conflict detection logic
        for control_a in controls_a:
            for control_b in controls_b:
                # Check for encryption conflicts
                if 'encryption' in str(control_a).lower() and 'encryption' in str(control_b).lower():
                    if self._has_encryption_conflict(control_a, control_b):
                        conflicts.append(FrameworkConflict(
                            framework_a=framework_a,
                            control_a=control_a.get('id', 'unknown'),
                            framework_b=framework_b,
                            control_b=control_b.get('id', 'unknown'),
                            conflict_type=ConflictType.TECHNICAL_INCOMPATIBILITY,
                            severity=ConflictSeverity.HIGH,
                            description="Conflicting encryption requirements",
                            resolution_options=self.resolution_strategies[ConflictType.TECHNICAL_INCOMPATIBILITY]
                        ))
                
                # Check for timeline conflicts
                if 'timeline' in str(control_a).lower() or 'deadline' in str(control_a).lower():
                    if self._has_timeline_conflict(control_a, control_b):
                        conflicts.append(FrameworkConflict(
                            framework_a=framework_a,
                            control_a=control_a.get('id', 'unknown'),
                            framework_b=framework_b,
                            control_b=control_b.get('id', 'unknown'),
                            conflict_type=ConflictType.TIMELINE_CONFLICT,
                            severity=ConflictSeverity.MEDIUM,
                            description="Conflicting timeline requirements",
                            resolution_options=self.resolution_strategies[ConflictType.TIMELINE_CONFLICT]
                        ))
        
        return conflicts
    
    def _has_encryption_conflict(self, control_a: Dict, control_b: Dict) -> bool:
        """Check if two controls have conflicting encryption requirements"""
        # Simplified logic - would be more sophisticated in production
        a_strength = control_a.get('encryption_bits', 128)
        b_strength = control_b.get('encryption_bits', 128)
        return abs(a_strength - b_strength) > 64
    
    def _has_timeline_conflict(self, control_a: Dict, control_b: Dict) -> bool:
        """Check if two controls have conflicting timeline requirements"""
        # Simplified logic
        a_days = control_a.get('timeline_days', 30)
        b_days = control_b.get('timeline_days', 30)
        return abs(a_days - b_days) > 7
    
    def _assess_severity(self, conflict_type: ConflictType) -> ConflictSeverity:
        """Assess the severity of a conflict based on its type"""
        severity_mapping = {
            ConflictType.MUTUALLY_EXCLUSIVE: ConflictSeverity.CRITICAL,
            ConflictType.TECHNICAL_INCOMPATIBILITY: ConflictSeverity.HIGH,
            ConflictType.RESOURCE_COMPETITION: ConflictSeverity.MEDIUM,
            ConflictType.TIMELINE_CONFLICT: ConflictSeverity.MEDIUM,
            ConflictType.SCOPE_MISMATCH: ConflictSeverity.LOW,
            ConflictType.COST_PROHIBITIVE: ConflictSeverity.HIGH
        }
        return severity_mapping.get(conflict_type, ConflictSeverity.MEDIUM)
    
    def resolve_conflict(self, conflict: FrameworkConflict, 
                        chosen_strategy: str) -> Dict[str, Any]:
        """
        Apply a resolution strategy to a conflict.
        
        Args:
            conflict: The conflict to resolve
            chosen_strategy: The resolution strategy to apply
            
        Returns:
            Resolution details including steps and estimated effort
        """
        resolution = {
            "conflict": {
                "frameworks": [conflict.framework_a, conflict.framework_b],
                "type": conflict.conflict_type.value,
                "severity": conflict.severity.value
            },
            "strategy": chosen_strategy,
            "implementation_steps": self._generate_implementation_steps(conflict, chosen_strategy),
            "estimated_effort_hours": self._estimate_effort(conflict, chosen_strategy),
            "success_criteria": self._define_success_criteria(conflict, chosen_strategy),
            "risks": self._identify_resolution_risks(conflict, chosen_strategy)
        }
        
        logger.info(f"📋 Generated resolution for {conflict.conflict_type.value} conflict")
        return resolution
    
    def _generate_implementation_steps(self, conflict: FrameworkConflict, 
                                      strategy: str) -> List[str]:
        """Generate specific implementation steps for resolution"""
        base_steps = [
            f"1. Document the conflict between {conflict.framework_a} and {conflict.framework_b}",
            f"2. Apply resolution strategy: {strategy}",
            "3. Update compliance documentation",
            "4. Implement technical controls if needed",
            "5. Validate resolution effectiveness",
            "6. Monitor for recurring conflicts"
        ]
        
        # Add type-specific steps
        if conflict.conflict_type == ConflictType.TECHNICAL_INCOMPATIBILITY:
            base_steps.insert(3, "3a. Review technical specifications")
            base_steps.insert(4, "3b. Design compatibility layer if needed")
        elif conflict.conflict_type == ConflictType.TIMELINE_CONFLICT:
            base_steps.insert(3, "3a. Create unified compliance calendar")
            base_steps.insert(4, "3b. Set up automated reminders")
        
        return base_steps
    
    def _estimate_effort(self, conflict: FrameworkConflict, strategy: str) -> int:
        """Estimate effort hours for resolution"""
        base_effort = {
            ConflictSeverity.CRITICAL: 40,
            ConflictSeverity.HIGH: 24,
            ConflictSeverity.MEDIUM: 16,
            ConflictSeverity.LOW: 8
        }
        return base_effort.get(conflict.severity, 16)
    
    def _define_success_criteria(self, conflict: FrameworkConflict, 
                                strategy: str) -> List[str]:
        """Define success criteria for resolution"""
        return [
            "Both framework requirements are satisfied",
            "No compliance violations detected",
            "Resolution is documented and auditable",
            "Stakeholders approve the resolution",
            "No negative impact on other controls"
        ]
    
    def _identify_resolution_risks(self, conflict: FrameworkConflict, 
                                  strategy: str) -> List[str]:
        """Identify risks in the resolution approach"""
        return [
            "Resolution may not satisfy all auditors",
            "Additional costs may be incurred",
            "Technical complexity may increase",
            "Timeline extensions may be needed",
            "Stakeholder alignment challenges"
        ]
    
    def generate_conflict_report(self) -> Dict[str, Any]:
        """Generate comprehensive conflict analysis report"""
        if not self.detected_conflicts:
            return {
                "status": "no_conflicts",
                "message": "No framework conflicts detected",
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "status": "conflicts_detected",
            "summary": {
                "total_conflicts": len(self.detected_conflicts),
                "critical": len([c for c in self.detected_conflicts 
                               if c.severity == ConflictSeverity.CRITICAL]),
                "high": len([c for c in self.detected_conflicts 
                           if c.severity == ConflictSeverity.HIGH]),
                "medium": len([c for c in self.detected_conflicts 
                             if c.severity == ConflictSeverity.MEDIUM]),
                "low": len([c for c in self.detected_conflicts 
                          if c.severity == ConflictSeverity.LOW])
            },
            "conflicts": [
                {
                    "frameworks": [c.framework_a, c.framework_b],
                    "type": c.conflict_type.value,
                    "severity": c.severity.value,
                    "description": c.description,
                    "resolution_options": c.resolution_options
                }
                for c in self.detected_conflicts
            ],
            "recommendations": self._generate_recommendations(),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations based on conflicts"""
        recommendations = []
        
        if any(c.severity == ConflictSeverity.CRITICAL for c in self.detected_conflicts):
            recommendations.append("⚠️ Address critical conflicts immediately")
        
        if len(self.detected_conflicts) > 5:
            recommendations.append("📊 Consider framework rationalization")
        
        tech_conflicts = [c for c in self.detected_conflicts 
                         if c.conflict_type == ConflictType.TECHNICAL_INCOMPATIBILITY]
        if len(tech_conflicts) > 2:
            recommendations.append("🔧 Review technical architecture for compatibility")
        
        timeline_conflicts = [c for c in self.detected_conflicts 
                             if c.conflict_type == ConflictType.TIMELINE_CONFLICT]
        if timeline_conflicts:
            recommendations.append("📅 Implement unified compliance calendar")
        
        return recommendations if recommendations else ["✅ Conflicts are manageable with standard processes"]