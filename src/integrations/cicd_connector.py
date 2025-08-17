"""
CI/CD Integration Connector
===========================
Connects compliance monitoring to CI/CD pipelines for continuous compliance.
Supports GitHub Actions, Jenkins, GitLab CI, and Azure DevOps.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

class CICDProvider(Enum):
    """Supported CI/CD providers"""
    GITHUB_ACTIONS = "github_actions"
    JENKINS = "jenkins"
    GITLAB_CI = "gitlab_ci"
    AZURE_DEVOPS = "azure_devops"
    GENERIC_WEBHOOK = "generic_webhook"

class ComplianceCheckResult(Enum):
    """Compliance check results"""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIP = "skip"

@dataclass
class CICDConfig:
    """CI/CD integration configuration"""
    provider: CICDProvider
    webhook_url: Optional[str] = None
    api_token: Optional[str] = None
    repository_url: Optional[str] = None
    branch_patterns: List[str] = None
    compliance_gates: List[str] = None

@dataclass
class ComplianceGate:
    """Compliance gate for CI/CD pipeline"""
    name: str
    framework: str
    min_score: int
    required_controls: List[str]
    blocking: bool = True

class CICDIntegrator:
    """
    CI/CD pipeline integrator for continuous compliance monitoring
    Implements shift-left security and compliance-as-code practices
    """
    
    def __init__(self):
        self.configs: Dict[str, CICDConfig] = {}
        self.compliance_gates: Dict[str, ComplianceGate] = {}
        self.webhook_handlers: Dict[CICDProvider, callable] = {
            CICDProvider.GITHUB_ACTIONS: self._handle_github_webhook,
            CICDProvider.JENKINS: self._handle_jenkins_webhook,
            CICDProvider.GITLAB_CI: self._handle_gitlab_webhook,
            CICDProvider.AZURE_DEVOPS: self._handle_azure_webhook,
            CICDProvider.GENERIC_WEBHOOK: self._handle_generic_webhook
        }
        
        # Initialize default compliance gates
        self._initialize_default_gates()
        
        logger.info("🔄 CI/CD integrator initialized with compliance gates")
    
    def _initialize_default_gates(self):
        """Initialize default compliance gates"""
        
        self.compliance_gates = {
            "security_baseline": ComplianceGate(
                name="Security Baseline Check",
                framework="nist_800_53",
                min_score=75,
                required_controls=["AC-2", "AC-3", "IA-2", "SI-2", "SI-4"],
                blocking=True
            ),
            "vulnerability_scan": ComplianceGate(
                name="Vulnerability Scan",
                framework="essential_eight",
                min_score=85,
                required_controls=["E8_2", "E8_7"],
                blocking=True
            ),
            "code_security": ComplianceGate(
                name="Code Security Review",
                framework="soc2",
                min_score=80,
                required_controls=["CC6.1", "CC7.1"],
                blocking=False  # Warning only
            ),
            "privacy_check": ComplianceGate(
                name="Privacy Impact Assessment",
                framework="privacy_act",
                min_score=70,
                required_controls=["P1", "P2", "P3"],
                blocking=False
            )
        }
    
    def register_pipeline(self, pipeline_id: str, config: CICDConfig) -> bool:
        """Register a CI/CD pipeline for compliance monitoring"""
        try:
            self.configs[pipeline_id] = config
            
            logger.info(f"✅ Registered {config.provider.value} pipeline: {pipeline_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register pipeline {pipeline_id}: {e}")
            return False
    
    async def run_compliance_checks(self, pipeline_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run compliance checks for a CI/CD pipeline execution
        """
        try:
            config = self.configs.get(pipeline_id)
            if not config:
                raise ValueError(f"Pipeline {pipeline_id} not registered")
            
            logger.info(f"🔍 Running compliance checks for pipeline: {pipeline_id}")
            
            results = {
                "pipeline_id": pipeline_id,
                "timestamp": datetime.now().isoformat(),
                "provider": config.provider.value,
                "context": context,
                "gate_results": {},
                "overall_result": ComplianceCheckResult.PASS,
                "blocking_failures": [],
                "warnings": [],
                "recommendations": []
            }
            
            # Run each compliance gate
            for gate_name, gate in self.compliance_gates.items():
                if config.compliance_gates and gate_name not in config.compliance_gates:
                    continue  # Skip gates not enabled for this pipeline
                
                gate_result = await self._run_compliance_gate(gate, context)
                results["gate_results"][gate_name] = gate_result
                
                if gate_result["result"] == ComplianceCheckResult.FAIL and gate.blocking:
                    results["blocking_failures"].append(gate_name)
                    results["overall_result"] = ComplianceCheckResult.FAIL
                elif gate_result["result"] == ComplianceCheckResult.WARNING:
                    results["warnings"].append(gate_name)
                    if results["overall_result"] == ComplianceCheckResult.PASS:
                        results["overall_result"] = ComplianceCheckResult.WARNING
            
            # Send results to CI/CD system
            await self._send_results_to_pipeline(pipeline_id, results)
            
            logger.info(f"✅ Compliance checks complete for {pipeline_id}: {results['overall_result'].value}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Compliance checks failed for {pipeline_id}: {e}")
            return {
                "pipeline_id": pipeline_id,
                "timestamp": datetime.now().isoformat(),
                "overall_result": ComplianceCheckResult.FAIL,
                "error": str(e)
            }
    
    async def _run_compliance_gate(self, gate: ComplianceGate, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a specific compliance gate"""
        try:
            gate_result = {
                "gate_name": gate.name,
                "framework": gate.framework,
                "result": ComplianceCheckResult.PASS,
                "score": 0,
                "control_results": {},
                "messages": []
            }
            
            # Simulate framework-specific checks
            if gate.framework == "nist_800_53":
                gate_result.update(await self._check_nist_controls(gate, context))
            elif gate.framework == "essential_eight":
                gate_result.update(await self._check_essential_eight(gate, context))
            elif gate.framework == "soc2":
                gate_result.update(await self._check_soc2_controls(gate, context))
            elif gate.framework == "privacy_act":
                gate_result.update(await self._check_privacy_controls(gate, context))
            else:
                gate_result["result"] = ComplianceCheckResult.SKIP
                gate_result["messages"].append(f"Framework {gate.framework} not implemented")
            
            return gate_result
            
        except Exception as e:
            logger.error(f"❌ Gate {gate.name} failed: {e}")
            return {
                "gate_name": gate.name,
                "result": ComplianceCheckResult.FAIL,
                "error": str(e)
            }
    
    async def _check_nist_controls(self, gate: ComplianceGate, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check NIST SP 800-53 controls"""
        
        # Simulate NIST control checks based on context
        score = 85  # Base score
        control_results = {}
        messages = []
        
        # Check for security scanning results
        if "security_scan" in context:
            scan_results = context["security_scan"]
            if scan_results.get("critical_vulnerabilities", 0) > 0:
                score -= 20
                messages.append(f"Critical vulnerabilities found: {scan_results['critical_vulnerabilities']}")
        
        # Check for code analysis
        if "code_analysis" in context:
            code_results = context["code_analysis"]
            if code_results.get("security_issues", 0) > 5:
                score -= 15
                messages.append(f"Security issues in code: {code_results['security_issues']}")
        
        # Simulate control checks
        for control_id in gate.required_controls:
            control_score = max(60, score + (hash(control_id) % 20) - 10)
            control_results[control_id] = {
                "score": control_score,
                "status": "pass" if control_score >= 70 else "fail"
            }
        
        result = ComplianceCheckResult.PASS
        if score < gate.min_score:
            result = ComplianceCheckResult.FAIL if gate.blocking else ComplianceCheckResult.WARNING
        
        return {
            "score": score,
            "result": result,
            "control_results": control_results,
            "messages": messages
        }
    
    async def _check_essential_eight(self, gate: ComplianceGate, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check Essential Eight controls"""
        
        score = 90  # Base score for Essential Eight
        control_results = {}
        messages = []
        
        # Check for patch management
        if "patch_status" in context:
            patch_data = context["patch_status"]
            if patch_data.get("outdated_packages", 0) > 10:
                score -= 25
                messages.append(f"Outdated packages detected: {patch_data['outdated_packages']}")
        
        # Check for application control
        if "application_allowlist" in context:
            if not context["application_allowlist"].get("enabled", False):
                score -= 20
                messages.append("Application allowlist not properly configured")
        
        for control_id in gate.required_controls:
            control_score = max(70, score + (hash(control_id) % 15) - 5)
            control_results[control_id] = {
                "score": control_score,
                "status": "pass" if control_score >= 80 else "fail"
            }
        
        result = ComplianceCheckResult.PASS
        if score < gate.min_score:
            result = ComplianceCheckResult.FAIL if gate.blocking else ComplianceCheckResult.WARNING
        
        return {
            "score": score,
            "result": result, 
            "control_results": control_results,
            "messages": messages
        }
    
    async def _check_soc2_controls(self, gate: ComplianceGate, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check SOC 2 controls"""
        
        score = 80
        control_results = {}
        messages = []
        
        # Check logging and monitoring
        if "logging_enabled" in context and not context["logging_enabled"]:
            score -= 20
            messages.append("Insufficient logging configuration detected")
        
        # Check access controls
        if "access_review" in context:
            if context["access_review"].get("last_review_days", 180) > 90:
                score -= 15
                messages.append("Access review overdue")
        
        for control_id in gate.required_controls:
            control_score = max(65, score + (hash(control_id) % 20) - 8)
            control_results[control_id] = {
                "score": control_score,
                "status": "pass" if control_score >= 75 else "fail"
            }
        
        result = ComplianceCheckResult.PASS
        if score < gate.min_score:
            result = ComplianceCheckResult.WARNING  # SOC 2 is usually non-blocking
        
        return {
            "score": score,
            "result": result,
            "control_results": control_results,
            "messages": messages
        }
    
    async def _check_privacy_controls(self, gate: ComplianceGate, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check privacy controls"""
        
        score = 75
        control_results = {}
        messages = []
        
        # Check for PII handling
        if "data_classification" in context:
            if "PII" in context["data_classification"] and not context.get("encryption_enabled", False):
                score -= 25
                messages.append("PII detected without proper encryption")
        
        # Check retention policies
        if not context.get("data_retention_policy", False):
            score -= 15
            messages.append("Data retention policy not implemented")
        
        for control_id in gate.required_controls:
            control_score = max(60, score + (hash(control_id) % 15) - 5)
            control_results[control_id] = {
                "score": control_score,
                "status": "pass" if control_score >= 70 else "fail"
            }
        
        result = ComplianceCheckResult.PASS
        if score < gate.min_score:
            result = ComplianceCheckResult.WARNING  # Privacy is usually non-blocking
        
        return {
            "score": score,
            "result": result,
            "control_results": control_results,
            "messages": messages
        }
    
    async def _send_results_to_pipeline(self, pipeline_id: str, results: Dict[str, Any]) -> bool:
        """Send compliance results back to the CI/CD pipeline"""
        try:
            config = self.configs.get(pipeline_id)
            if not config or not config.webhook_url:
                return False
            
            # Format results for CI/CD system
            formatted_results = self._format_results_for_cicd(config.provider, results)
            
            # Send webhook (in production, would use async HTTP client)
            # For demo, we'll just log the results
            logger.info(f"📡 Sending compliance results to {config.provider.value}")
            logger.info(f"Results: {formatted_results['summary']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send results to pipeline {pipeline_id}: {e}")
            return False
    
    def _format_results_for_cicd(self, provider: CICDProvider, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format results for specific CI/CD provider"""
        
        summary = f"Compliance Check: {results['overall_result'].value.upper()}"
        details = []
        
        for gate_name, gate_result in results.get("gate_results", {}).items():
            status_emoji = "✅" if gate_result["result"] == ComplianceCheckResult.PASS else "❌"
            details.append(f"{status_emoji} {gate_result['gate_name']}: {gate_result.get('score', 0)}%")
        
        if provider == CICDProvider.GITHUB_ACTIONS:
            return {
                "summary": summary,
                "details": "\n".join(details),
                "annotations": [
                    {
                        "path": "compliance-check",
                        "message": summary,
                        "annotation_level": "notice" if results["overall_result"] == ComplianceCheckResult.PASS else "failure"
                    }
                ]
            }
        elif provider == CICDProvider.JENKINS:
            return {
                "summary": summary,
                "description": "\n".join(details),
                "result": "SUCCESS" if results["overall_result"] == ComplianceCheckResult.PASS else "FAILURE"
            }
        else:
            return {
                "summary": summary,
                "details": details,
                "status": results["overall_result"].value
            }
    
    async def _handle_github_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle GitHub Actions webhook"""
        return {"status": "processed", "provider": "github"}
    
    async def _handle_jenkins_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Jenkins webhook"""
        return {"status": "processed", "provider": "jenkins"}
    
    async def _handle_gitlab_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle GitLab CI webhook"""
        return {"status": "processed", "provider": "gitlab"}
    
    async def _handle_azure_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Azure DevOps webhook"""
        return {"status": "processed", "provider": "azure"}
    
    async def _handle_generic_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic webhook"""
        return {"status": "processed", "provider": "generic"}
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get CI/CD integration statistics"""
        return {
            "registered_pipelines": len(self.configs),
            "compliance_gates": len(self.compliance_gates),
            "supported_providers": [provider.value for provider in CICDProvider],
            "gate_definitions": {
                name: {
                    "framework": gate.framework,
                    "min_score": gate.min_score,
                    "blocking": gate.blocking
                }
                for name, gate in self.compliance_gates.items()
            }
        }

# Demo/test function
async def demo_cicd_integration():
    """Demonstrate CI/CD integration capabilities"""
    
    integrator = CICDIntegrator()
    
    # Register a GitHub Actions pipeline
    github_config = CICDConfig(
        provider=CICDProvider.GITHUB_ACTIONS,
        webhook_url="https://api.github.com/repos/org/repo/check-runs",
        api_token="demo_token",
        repository_url="https://github.com/org/repo",
        branch_patterns=["main", "develop"],
        compliance_gates=["security_baseline", "vulnerability_scan"]
    )
    
    integrator.register_pipeline("github-main-pipeline", github_config)
    
    # Simulate pipeline execution context
    pipeline_context = {
        "commit_sha": "abc123def456",
        "branch": "main", 
        "author": "developer@company.com",
        "security_scan": {
            "critical_vulnerabilities": 0,
            "high_vulnerabilities": 2,
            "medium_vulnerabilities": 5
        },
        "code_analysis": {
            "security_issues": 3,
            "code_smells": 12
        },
        "patch_status": {
            "outdated_packages": 5,
            "security_patches_available": 2
        },
        "logging_enabled": True,
        "encryption_enabled": True,
        "data_retention_policy": True
    }
    
    # Run compliance checks
    results = await integrator.run_compliance_checks("github-main-pipeline", pipeline_context)
    
    logger.info("🎯 CI/CD Integration Demo Complete")
    logger.info(f"Results: {json.dumps(results, indent=2, default=str)}")
    
    return results

if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_cicd_integration())