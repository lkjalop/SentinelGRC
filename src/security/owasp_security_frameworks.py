"""
OWASP Security Frameworks Integration for Cerberus AI
====================================================
Comprehensive implementation of OWASP Top 10 across all domains:
- Web Application Security
- Mobile Application Security  
- API Security
- AI/LLM Security

Implements "physician heal thyself" - platform self-defense mechanisms.
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class OWASPFramework(Enum):
    """OWASP security frameworks"""
    WEB_TOP10 = "owasp_web_top10"
    MOBILE_TOP10 = "owasp_mobile_top10"
    API_TOP10 = "owasp_api_top10"
    LLM_TOP10 = "owasp_llm_top10"

class SecurityRiskLevel(Enum):
    """Security risk assessment levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class SecurityFinding:
    """Security assessment finding"""
    finding_id: str
    owasp_category: str
    title: str
    description: str
    risk_level: SecurityRiskLevel
    cwe_id: Optional[str]
    remediation: str
    evidence: Dict[str, Any]
    framework: OWASPFramework

@dataclass
class SecurityAssessmentResult:
    """Complete security assessment result"""
    framework: OWASPFramework
    assessment_date: datetime
    findings: List[SecurityFinding]
    risk_score: int  # 0-100
    compliance_percentage: float
    recommendations: List[str]
    next_assessment_date: datetime

class OWASPWebTop10Agent:
    """OWASP Top 10 Web Application Security Agent"""
    
    def __init__(self):
        self.web_controls = self._initialize_web_controls()
        
    def _initialize_web_controls(self) -> Dict[str, Dict[str, Any]]:
        """Initialize OWASP Web Top 10 2021 controls"""
        
        return {
            "A01_2021": {
                "category": "Broken Access Control",
                "description": "Access control enforces policy such that users cannot act outside of their intended permissions",
                "risk_factors": ["Privilege escalation", "Unauthorized data access", "Missing authorization"],
                "assessment_checks": [
                    "Authentication mechanisms review",
                    "Authorization matrix validation", 
                    "Session management analysis",
                    "Privilege escalation testing"
                ],
                "remediation": "Implement robust access control with principle of least privilege"
            },
            
            "A02_2021": {
                "category": "Cryptographic Failures", 
                "description": "Failures related to cryptography which often leads to sensitive data exposure",
                "risk_factors": ["Weak encryption", "Key management issues", "Data in transit exposure"],
                "assessment_checks": [
                    "Encryption algorithm strength",
                    "Key management practices",
                    "TLS/SSL configuration",
                    "Data at rest encryption"
                ],
                "remediation": "Use strong encryption algorithms and proper key management"
            },
            
            "A03_2021": {
                "category": "Injection",
                "description": "Injection flaws occur when untrusted data is sent to an interpreter",
                "risk_factors": ["SQL injection", "Command injection", "LDAP injection"],
                "assessment_checks": [
                    "Input validation mechanisms",
                    "Parameterized queries usage",
                    "Output encoding practices",
                    "Dynamic query analysis"
                ],
                "remediation": "Use parameterized queries and proper input validation"
            },
            
            "A04_2021": {
                "category": "Insecure Design",
                "description": "Risks related to design flaws, calling for more use of threat modeling",
                "risk_factors": ["Missing security controls", "Inadequate threat modeling", "Design flaws"],
                "assessment_checks": [
                    "Threat modeling evidence",
                    "Security architecture review",
                    "Design pattern analysis",
                    "Security requirements validation"
                ],
                "remediation": "Implement secure design practices and threat modeling"
            },
            
            "A05_2021": {
                "category": "Security Misconfiguration",
                "description": "Security misconfiguration is commonly a result of insecure default configurations",
                "risk_factors": ["Default configurations", "Incomplete configurations", "Excessive permissions"],
                "assessment_checks": [
                    "Configuration hardening review",
                    "Default account analysis",
                    "Error handling assessment",
                    "Security header validation"
                ],
                "remediation": "Implement secure configuration standards and regular reviews"
            },
            
            "A06_2021": {
                "category": "Vulnerable and Outdated Components",
                "description": "Using components with known vulnerabilities is a prevalent issue",
                "risk_factors": ["Outdated libraries", "Unpatched components", "Unknown component inventory"],
                "assessment_checks": [
                    "Component inventory analysis",
                    "Vulnerability scanning",
                    "Patch management review",
                    "License compliance check"
                ],
                "remediation": "Maintain component inventory and implement vulnerability management"
            },
            
            "A07_2021": {
                "category": "Identification and Authentication Failures",
                "description": "Confirmation of the user's identity, authentication, and session management",
                "risk_factors": ["Weak passwords", "Session hijacking", "Credential stuffing"],
                "assessment_checks": [
                    "Password policy validation",
                    "Multi-factor authentication review",
                    "Session management analysis",
                    "Account lockout testing"
                ],
                "remediation": "Implement strong authentication and session management"
            },
            
            "A08_2021": {
                "category": "Software and Data Integrity Failures",
                "description": "Software and data integrity failures relate to code and infrastructure",
                "risk_factors": ["Unsigned updates", "CI/CD vulnerabilities", "Data tampering"],
                "assessment_checks": [
                    "Code signing verification",
                    "CI/CD pipeline security",
                    "Dependency validation",
                    "Data integrity controls"
                ],
                "remediation": "Implement integrity verification and secure CI/CD practices"
            },
            
            "A09_2021": {
                "category": "Security Logging and Monitoring Failures",
                "description": "Logging and monitoring is challenging to test and is often under-represented",
                "risk_factors": ["Insufficient logging", "Missing monitoring", "Poor incident response"],
                "assessment_checks": [
                    "Logging comprehensiveness",
                    "Monitoring effectiveness",
                    "Incident response procedures",
                    "Log protection measures"
                ],
                "remediation": "Implement comprehensive logging and monitoring systems"
            },
            
            "A10_2021": {
                "category": "Server-Side Request Forgery (SSRF)",
                "description": "SSRF flaws occur whenever a web application fetches a remote resource",
                "risk_factors": ["URL validation bypass", "Internal network access", "Cloud metadata exposure"],
                "assessment_checks": [
                    "URL validation mechanisms",
                    "Network segmentation review",
                    "Input sanitization analysis",
                    "Response filtering assessment"
                ],
                "remediation": "Implement proper URL validation and network controls"
            }
        }
    
    async def assess_web_security(self, target_system: Dict[str, Any]) -> SecurityAssessmentResult:
        """Assess web application against OWASP Top 10"""
        
        findings = []
        
        for control_id, control in self.web_controls.items():
            # Simulate security assessment (in production, integrate with security scanners)
            finding = await self._assess_web_control(control_id, control, target_system)
            if finding:
                findings.append(finding)
        
        risk_score = self._calculate_risk_score(findings)
        compliance_percentage = max(0, 100 - len(findings) * 10)
        
        recommendations = [
            "Implement Web Application Firewall (WAF)",
            "Regular security testing and code reviews", 
            "Security training for development teams",
            "Automated security scanning in CI/CD pipeline"
        ]
        
        return SecurityAssessmentResult(
            framework=OWASPFramework.WEB_TOP10,
            assessment_date=datetime.now(),
            findings=findings,
            risk_score=risk_score,
            compliance_percentage=compliance_percentage,
            recommendations=recommendations,
            next_assessment_date=datetime.now()
        )
    
    async def _assess_web_control(self, control_id: str, control: Dict[str, Any], 
                                 target_system: Dict[str, Any]) -> Optional[SecurityFinding]:
        """Assess individual web security control"""
        
        # Simulate assessment logic (in production, implement actual checks)
        system_type = target_system.get("type", "web_application")
        
        if system_type == "web_application":
            # High likelihood of findings in demonstration
            if control_id in ["A01_2021", "A05_2021", "A09_2021"]:
                return SecurityFinding(
                    finding_id=f"WEB_{control_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    owasp_category=control["category"],
                    title=f"{control['category']} - Implementation Gap",
                    description=f"Assessment identified potential {control['category'].lower()} vulnerabilities requiring attention.",
                    risk_level=SecurityRiskLevel.MEDIUM,
                    cwe_id=f"CWE-{hash(control_id) % 1000}",  # Demo CWE mapping
                    remediation=control["remediation"],
                    evidence={"assessment_checks": control["assessment_checks"]},
                    framework=OWASPFramework.WEB_TOP10
                )
        
        return None

class OWASPMobileTop10Agent:
    """OWASP Mobile Top 10 Security Agent"""
    
    def __init__(self):
        self.mobile_controls = self._initialize_mobile_controls()
    
    def _initialize_mobile_controls(self) -> Dict[str, Dict[str, Any]]:
        """Initialize OWASP Mobile Top 10 2016 controls"""
        
        return {
            "M1": {
                "category": "Improper Platform Usage",
                "description": "Misuse of a platform feature or failure to use platform security controls",
                "assessment_checks": ["Platform API usage review", "Security control implementation"],
                "remediation": "Follow platform security guidelines and best practices"
            },
            "M2": {
                "category": "Insecure Data Storage", 
                "description": "Insecure data storage vulnerabilities occur when development teams assume that users or malware won't have access to a mobile device's filesystem",
                "assessment_checks": ["Data encryption at rest", "Keychain/Keystore usage", "Database security"],
                "remediation": "Encrypt sensitive data and use secure storage mechanisms"
            },
            "M3": {
                "category": "Insecure Communication",
                "description": "Poor handshaking, incorrect SSL versions, weak negotiation, cleartext communication",
                "assessment_checks": ["TLS implementation", "Certificate validation", "Network communication review"],
                "remediation": "Implement proper TLS and certificate validation"
            },
            "M4": {
                "category": "Insecure Authentication",
                "description": "Poor or missing authentication schemes that allow an adversary to execute functionality within the mobile app",
                "assessment_checks": ["Authentication mechanism review", "Session management", "Biometric implementation"],
                "remediation": "Implement strong authentication with proper session management"
            },
            "M5": {
                "category": "Insufficient Cryptography",
                "description": "Code applies cryptography to a sensitive information asset. However, the cryptography is insufficient in some way",
                "assessment_checks": ["Cryptographic algorithm strength", "Key management", "Random number generation"],
                "remediation": "Use strong cryptography and proper key management"
            }
        }
    
    async def assess_mobile_security(self, target_system: Dict[str, Any]) -> SecurityAssessmentResult:
        """Assess mobile application against OWASP Mobile Top 10"""
        
        findings = []
        
        for control_id, control in self.mobile_controls.items():
            finding = await self._assess_mobile_control(control_id, control, target_system)
            if finding:
                findings.append(finding)
        
        risk_score = self._calculate_risk_score(findings)
        compliance_percentage = max(0, 100 - len(findings) * 15)
        
        return SecurityAssessmentResult(
            framework=OWASPFramework.MOBILE_TOP10,
            assessment_date=datetime.now(),
            findings=findings,
            risk_score=risk_score,
            compliance_percentage=compliance_percentage,
            recommendations=[
                "Implement mobile application security testing (MAST)",
                "Use mobile device management (MDM) solutions",
                "Regular mobile security assessments"
            ],
            next_assessment_date=datetime.now()
        )
    
    async def _assess_mobile_control(self, control_id: str, control: Dict[str, Any],
                                   target_system: Dict[str, Any]) -> Optional[SecurityFinding]:
        """Assess individual mobile security control"""
        
        if target_system.get("type") == "mobile_application":
            if control_id in ["M2", "M3"]:  # Common mobile vulnerabilities
                return SecurityFinding(
                    finding_id=f"MOB_{control_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    owasp_category=control["category"],
                    title=f"Mobile {control['category']} Risk",
                    description=f"Mobile security assessment identified {control['category'].lower()} concerns.",
                    risk_level=SecurityRiskLevel.MEDIUM,
                    cwe_id=None,
                    remediation=control["remediation"],
                    evidence={"assessment_checks": control["assessment_checks"]},
                    framework=OWASPFramework.MOBILE_TOP10
                )
        
        return None

class OWASPAPITop10Agent:
    """OWASP API Security Top 10 Agent"""
    
    def __init__(self):
        self.api_controls = self._initialize_api_controls()
    
    def _initialize_api_controls(self) -> Dict[str, Dict[str, Any]]:
        """Initialize OWASP API Security Top 10 2023 controls"""
        
        return {
            "API1_2023": {
                "category": "Broken Object Level Authorization",
                "description": "APIs tend to expose endpoints that handle object identifiers, creating a wide attack surface",
                "assessment_checks": ["Authorization checks", "Object access control", "API endpoint analysis"],
                "remediation": "Implement proper object-level authorization checks"
            },
            "API2_2023": {
                "category": "Broken Authentication",
                "description": "Authentication mechanisms are often implemented incorrectly",
                "assessment_checks": ["Authentication mechanism review", "Token validation", "API key management"],
                "remediation": "Implement robust authentication mechanisms for APIs"
            },
            "API3_2023": {
                "category": "Broken Object Property Level Authorization",
                "description": "Lack of or improper authorization validation at the object property level",
                "assessment_checks": ["Property-level access control", "Field-level validation", "Data exposure analysis"],
                "remediation": "Validate authorization for object properties and fields"
            },
            "API4_2023": {
                "category": "Unrestricted Resource Consumption",
                "description": "APIs don't restrict the size or number of resources that can be requested",
                "assessment_checks": ["Rate limiting implementation", "Resource usage monitoring", "DoS protection"],
                "remediation": "Implement rate limiting and resource consumption controls"
            },
            "API5_2023": {
                "category": "Broken Function Level Authorization",
                "description": "Complex access control policies with different hierarchies, groups, and roles",
                "assessment_checks": ["Function-level access control", "Role-based permissions", "API method authorization"],
                "remediation": "Implement proper function-level authorization"
            }
        }
    
    async def assess_api_security(self, target_system: Dict[str, Any]) -> SecurityAssessmentResult:
        """Assess API against OWASP API Security Top 10"""
        
        findings = []
        
        for control_id, control in self.api_controls.items():
            finding = await self._assess_api_control(control_id, control, target_system)
            if finding:
                findings.append(finding)
        
        risk_score = self._calculate_risk_score(findings)
        compliance_percentage = max(0, 100 - len(findings) * 12)
        
        return SecurityAssessmentResult(
            framework=OWASPFramework.API_TOP10,
            assessment_date=datetime.now(),
            findings=findings,
            risk_score=risk_score,
            compliance_percentage=compliance_percentage,
            recommendations=[
                "Implement API gateway with security controls",
                "Use API security testing tools",
                "Regular API security assessments and monitoring"
            ],
            next_assessment_date=datetime.now()
        )
    
    async def _assess_api_control(self, control_id: str, control: Dict[str, Any],
                                target_system: Dict[str, Any]) -> Optional[SecurityFinding]:
        """Assess individual API security control"""
        
        if "api" in target_system.get("type", "").lower():
            if control_id in ["API1_2023", "API4_2023"]:  # Common API vulnerabilities
                return SecurityFinding(
                    finding_id=f"API_{control_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    owasp_category=control["category"],
                    title=f"API Security - {control['category']}",
                    description=f"API security assessment identified {control['category'].lower()} risks.",
                    risk_level=SecurityRiskLevel.HIGH,
                    cwe_id=None,
                    remediation=control["remediation"],
                    evidence={"assessment_checks": control["assessment_checks"]},
                    framework=OWASPFramework.API_TOP10
                )
        
        return None

class OWASPLLMTop10Agent:
    """OWASP LLM Top 10 AI/ML Security Agent"""
    
    def __init__(self):
        self.llm_controls = self._initialize_llm_controls()
    
    def _initialize_llm_controls(self) -> Dict[str, Dict[str, Any]]:
        """Initialize OWASP LLM Top 10 2023 controls"""
        
        return {
            "LLM01": {
                "category": "Prompt Injection",
                "description": "Bypassing filters or manipulating the LLM using crafted inputs",
                "assessment_checks": ["Input validation", "Prompt sanitization", "Context separation"],
                "remediation": "Implement robust input validation and prompt sanitization"
            },
            "LLM02": {
                "category": "Insecure Output Handling",
                "description": "Insufficient validation, sanitization, and handling of LLM outputs",
                "assessment_checks": ["Output validation", "Content filtering", "Response sanitization"],
                "remediation": "Validate and sanitize all LLM outputs before processing"
            },
            "LLM03": {
                "category": "Training Data Poisoning",
                "description": "Vulnerabilities due to tampered training data or fine-tuning data",
                "assessment_checks": ["Data source validation", "Training data integrity", "Model validation"],
                "remediation": "Implement training data validation and integrity checks"
            },
            "LLM04": {
                "category": "Model Denial of Service",
                "description": "Resource-heavy operations that cause service degradation",
                "assessment_checks": ["Resource monitoring", "Query complexity limits", "Rate limiting"],
                "remediation": "Implement resource limits and DoS protection"
            },
            "LLM05": {
                "category": "Supply Chain Vulnerabilities",
                "description": "Vulnerabilities in third-party datasets, pre-trained models, and plugins",
                "assessment_checks": ["Model provenance", "Dependency scanning", "Third-party validation"],
                "remediation": "Validate all AI/ML supply chain components"
            },
            "LLM06": {
                "category": "Sensitive Information Disclosure",
                "description": "LLM accidentally reveals confidential data in its responses",
                "assessment_checks": ["Data leakage testing", "Privacy controls", "Information filtering"],
                "remediation": "Implement privacy controls and information filtering"
            }
        }
    
    async def assess_llm_security(self, target_system: Dict[str, Any]) -> SecurityAssessmentResult:
        """Assess AI/LLM system against OWASP LLM Top 10"""
        
        findings = []
        
        for control_id, control in self.llm_controls.items():
            finding = await self._assess_llm_control(control_id, control, target_system)
            if finding:
                findings.append(finding)
        
        risk_score = self._calculate_risk_score(findings)
        compliance_percentage = max(0, 100 - len(findings) * 10)
        
        return SecurityAssessmentResult(
            framework=OWASPFramework.LLM_TOP10,
            assessment_date=datetime.now(),
            findings=findings,
            risk_score=risk_score,
            compliance_percentage=compliance_percentage,
            recommendations=[
                "Implement AI/ML security monitoring",
                "Regular model validation and testing",
                "AI ethics and safety controls",
                "Continuous AI security assessment"
            ],
            next_assessment_date=datetime.now()
        )
    
    async def _assess_llm_control(self, control_id: str, control: Dict[str, Any],
                                target_system: Dict[str, Any]) -> Optional[SecurityFinding]:
        """Assess individual LLM security control"""
        
        if "ai" in target_system.get("type", "").lower() or "llm" in target_system.get("type", "").lower():
            # High likelihood for AI systems to have LLM security considerations
            if control_id in ["LLM01", "LLM02", "LLM06"]:
                return SecurityFinding(
                    finding_id=f"LLM_{control_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    owasp_category=control["category"],
                    title=f"AI/LLM Security - {control['category']}",
                    description=f"AI security assessment identified {control['category'].lower()} vulnerabilities.",
                    risk_level=SecurityRiskLevel.HIGH,
                    cwe_id=None,
                    remediation=control["remediation"],
                    evidence={"assessment_checks": control["assessment_checks"]},
                    framework=OWASPFramework.LLM_TOP10
                )
        
        return None

class PlatformSelfDefenseAgent:
    """Platform Self-Defense Agent - 'Physician Heal Thyself'"""
    
    def __init__(self):
        self.self_defense_controls = self._initialize_self_defense_controls()
    
    def _initialize_self_defense_controls(self) -> Dict[str, Dict[str, Any]]:
        """Initialize platform self-defense controls"""
        
        return {
            "PLATFORM_AUTH": {
                "category": "Platform Authentication Security",
                "controls": ["Multi-factor authentication", "API key management", "Session security"],
                "monitoring": "Authentication failure monitoring and alerting"
            },
            "PLATFORM_DATA": {
                "category": "Platform Data Protection",
                "controls": ["Assessment data encryption", "Customer data isolation", "Backup security"],
                "monitoring": "Data access logging and anomaly detection"
            },
            "PLATFORM_INFRA": {
                "category": "Platform Infrastructure Security",
                "controls": ["Container security", "Network segmentation", "Vulnerability management"],
                "monitoring": "Infrastructure monitoring and threat detection"
            },
            "PLATFORM_AI": {
                "category": "AI Model Security",
                "controls": ["Model integrity", "Prompt injection protection", "Output validation"],
                "monitoring": "AI model behavior monitoring and anomaly detection"
            }
        }
    
    async def assess_platform_security(self) -> SecurityAssessmentResult:
        """Assess Cerberus AI platform security - self-assessment"""
        
        findings = []
        
        # Platform security self-assessment
        for control_area, control_info in self.self_defense_controls.items():
            finding = await self._assess_platform_control(control_area, control_info)
            if finding:
                findings.append(finding)
        
        risk_score = self._calculate_risk_score(findings)
        compliance_percentage = max(0, 100 - len(findings) * 8)
        
        return SecurityAssessmentResult(
            framework=OWASPFramework.WEB_TOP10,  # Platform is web-based
            assessment_date=datetime.now(),
            findings=findings,
            risk_score=risk_score,
            compliance_percentage=compliance_percentage,
            recommendations=[
                "Continuous platform security monitoring",
                "Regular security assessments of platform components",
                "Implementation of security incident response procedures",
                "Platform security training for development team"
            ],
            next_assessment_date=datetime.now()
        )
    
    async def _assess_platform_control(self, control_area: str, 
                                     control_info: Dict[str, Any]) -> Optional[SecurityFinding]:
        """Assess platform self-defense control"""
        
        # Simulate platform security assessment
        if control_area in ["PLATFORM_AI"]:  # Focus on AI-specific security
            return SecurityFinding(
                finding_id=f"PLAT_{control_area}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                owasp_category=control_info["category"],
                title=f"Platform Security - {control_info['category']}",
                description=f"Platform self-assessment identified {control_info['category'].lower()} considerations.",
                risk_level=SecurityRiskLevel.MEDIUM,
                cwe_id=None,
                remediation=f"Implement {control_info['monitoring']} for enhanced platform security",
                evidence={"controls": control_info["controls"]},
                framework=OWASPFramework.LLM_TOP10  # AI-specific framework
            )
        
        return None

class OWASPSecurityOrchestrator:
    """Main OWASP Security Assessment Orchestrator"""
    
    def __init__(self):
        self.web_agent = OWASPWebTop10Agent()
        self.mobile_agent = OWASPMobileTop10Agent()
        self.api_agent = OWASPAPITop10Agent()
        self.llm_agent = OWASPLLMTop10Agent()
        self.self_defense_agent = PlatformSelfDefenseAgent()
        
        logger.info("✅ OWASP Security Orchestrator initialized with all frameworks")
    
    async def comprehensive_security_assessment(self, 
                                              target_systems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive OWASP security assessment across all frameworks"""
        
        logger.info(f"🛡️ Starting comprehensive OWASP security assessment for {len(target_systems)} systems")
        
        assessment_results = {
            "assessment_date": datetime.now().isoformat(),
            "frameworks_assessed": [],
            "security_results": {},
            "overall_security_score": 0.0,
            "critical_findings": [],
            "platform_self_defense": None,
            "recommendations": []
        }
        
        # Assess each target system against applicable frameworks
        for system in target_systems:
            system_type = system.get("type", "unknown")
            system_name = system.get("name", f"System_{system_type}")
            
            logger.info(f"🔍 Assessing {system_name} ({system_type})")
            
            system_results = {}
            
            # Web application security
            if "web" in system_type.lower():
                web_result = await self.web_agent.assess_web_security(system)
                system_results["web_security"] = web_result
                assessment_results["frameworks_assessed"].append("OWASP Web Top 10")
            
            # Mobile application security
            if "mobile" in system_type.lower():
                mobile_result = await self.mobile_agent.assess_mobile_security(system)
                system_results["mobile_security"] = mobile_result
                assessment_results["frameworks_assessed"].append("OWASP Mobile Top 10")
            
            # API security
            if "api" in system_type.lower():
                api_result = await self.api_agent.assess_api_security(system)
                system_results["api_security"] = api_result
                assessment_results["frameworks_assessed"].append("OWASP API Top 10")
            
            # AI/LLM security
            if "ai" in system_type.lower() or "llm" in system_type.lower():
                llm_result = await self.llm_agent.assess_llm_security(system)
                system_results["llm_security"] = llm_result
                assessment_results["frameworks_assessed"].append("OWASP LLM Top 10")
            
            assessment_results["security_results"][system_name] = system_results
        
        # Platform self-defense assessment
        platform_result = await self.self_defense_agent.assess_platform_security()
        assessment_results["platform_self_defense"] = platform_result
        assessment_results["frameworks_assessed"].append("Platform Self-Defense")
        
        # Calculate overall security metrics
        all_results = []
        for system_results in assessment_results["security_results"].values():
            all_results.extend(system_results.values())
        all_results.append(platform_result)
        
        if all_results:
            overall_score = sum(result.compliance_percentage for result in all_results) / len(all_results)
            assessment_results["overall_security_score"] = overall_score
            
            # Collect critical findings
            for result in all_results:
                critical_findings = [f for f in result.findings if f.risk_level == SecurityRiskLevel.CRITICAL]
                assessment_results["critical_findings"].extend(critical_findings)
        
        # Generate comprehensive recommendations
        assessment_results["recommendations"] = [
            "Implement comprehensive security monitoring across all OWASP frameworks",
            "Regular security assessments and penetration testing",
            "Security training for development and operations teams",
            "Automated security testing in CI/CD pipelines",
            "Incident response procedures for security events",
            "Platform self-defense mechanisms and monitoring"
        ]
        
        logger.info(f"✅ Comprehensive OWASP security assessment completed - Score: {assessment_results['overall_security_score']:.1f}%")
        
        return assessment_results
    
    def _calculate_risk_score(self, findings: List[SecurityFinding]) -> int:
        """Calculate overall risk score from findings"""
        
        if not findings:
            return 100  # Perfect score
        
        risk_weights = {
            SecurityRiskLevel.CRITICAL: 25,
            SecurityRiskLevel.HIGH: 15,
            SecurityRiskLevel.MEDIUM: 10,
            SecurityRiskLevel.LOW: 5,
            SecurityRiskLevel.INFO: 1
        }
        
        total_risk = sum(risk_weights.get(finding.risk_level, 5) for finding in findings)
        risk_score = max(0, 100 - total_risk)
        
        return risk_score

# Shared method for all agents
def _calculate_risk_score(findings: List[SecurityFinding]) -> int:
    """Calculate risk score from security findings"""
    orchestrator = OWASPSecurityOrchestrator()
    return orchestrator._calculate_risk_score(findings)

# Add method to all agent classes
OWASPWebTop10Agent._calculate_risk_score = staticmethod(_calculate_risk_score)
OWASPMobileTop10Agent._calculate_risk_score = staticmethod(_calculate_risk_score) 
OWASPAPITop10Agent._calculate_risk_score = staticmethod(_calculate_risk_score)
OWASPLLMTop10Agent._calculate_risk_score = staticmethod(_calculate_risk_score)
PlatformSelfDefenseAgent._calculate_risk_score = staticmethod(_calculate_risk_score)