"""
Security Audit Utility for Sentinel GRC
=======================================

Zero-cost security audit tool to verify secure coding practices.
Scans codebase for common security vulnerabilities and provides recommendations.
"""

import os
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class SecurityIssue:
    """Represents a security issue found in the code"""
    file_path: str
    line_number: int
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    issue_type: str
    description: str
    recommendation: str
    code_snippet: str

class SecurityAuditor:
    """
    Automated security auditing for compliance assessment platform.
    Identifies common security vulnerabilities and provides recommendations.
    """
    
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        
        # Security patterns to detect
        self.security_patterns = {
            "insecure_hash": {
                "patterns": [
                    r"hashlib\.md5\(",
                    r"hashlib\.sha1\(",
                    r"\.md5\(",
                    r"\.sha1\("
                ],
                "severity": "HIGH",
                "description": "Insecure hash function usage",
                "recommendation": "Use SHA-256 or SHA-3 for cryptographic operations"
            },
            "hardcoded_secrets": {
                "patterns": [
                    r"password\s*=\s*['\"][^'\"]+['\"]",
                    r"api_key\s*=\s*['\"][^'\"]+['\"]",
                    r"secret\s*=\s*['\"][^'\"]+['\"]",
                    r"token\s*=\s*['\"][^'\"]+['\"]"
                ],
                "severity": "CRITICAL",
                "description": "Hardcoded secrets detected",
                "recommendation": "Use environment variables or secure vaults for secrets"
            },
            "sql_injection": {
                "patterns": [
                    r'execute\s*\(\s*f?[\'"].*\{.*\}.*[\'"]',
                    r'query\s*\(\s*f?[\'"].*\{.*\}.*[\'"]',
                    r'SELECT.*\{.*\}.*FROM',
                    r'INSERT.*\{.*\}.*INTO'
                ],
                "severity": "CRITICAL",
                "description": "Potential SQL injection vulnerability",
                "recommendation": "Use parameterized queries instead of string formatting"
            },
            "unsafe_deserialization": {
                "patterns": [
                    r"pickle\.loads?\(",
                    r"eval\(",
                    r"exec\(",
                    r"__import__\("
                ],
                "severity": "HIGH",
                "description": "Unsafe deserialization or code execution",
                "recommendation": "Use safe alternatives like json.loads() or ast.literal_eval()"
            },
            "weak_random": {
                "patterns": [
                    r"random\.random\(",
                    r"random\.randint\(",
                    r"random\.choice\("
                ],
                "severity": "MEDIUM",
                "description": "Weak random number generation for security purposes",
                "recommendation": "Use secrets module for cryptographic randomness"
            },
            "debug_mode": {
                "patterns": [
                    r"debug\s*=\s*True",
                    r"DEBUG\s*=\s*True",
                    r"print\s*\(.*password.*\)",
                    r"print\s*\(.*secret.*\)",
                    r"print\s*\(.*token.*\)"
                ],
                "severity": "MEDIUM",
                "description": "Debug mode or sensitive information logging",
                "recommendation": "Disable debug mode and avoid logging sensitive information"
            },
            "unsafe_temp_files": {
                "patterns": [
                    r"tempfile\.mktemp\(",
                    r"tmp\/"
                ],
                "severity": "LOW",
                "description": "Potentially unsafe temporary file usage",
                "recommendation": "Use tempfile.mkstemp() or tempfile.NamedTemporaryFile()"
            }
        }
    
    def audit_file(self, file_path: str):
        """Audit a single Python file for security issues"""
        if not file_path.endswith('.py'):
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                self._check_line_security(file_path, line_num, line)
                
        except Exception as e:
            print(f"Error auditing {file_path}: {e}")
    
    def _check_line_security(self, file_path: str, line_number: int, line: str):
        """Check a single line for security issues"""
        line_stripped = line.strip()
        
        for issue_type, config in self.security_patterns.items():
            for pattern in config["patterns"]:
                if re.search(pattern, line_stripped, re.IGNORECASE):
                    # Filter out comments and test files
                    if line_stripped.startswith('#'):
                        continue
                    if 'test_' in file_path.lower():
                        continue
                    
                    issue = SecurityIssue(
                        file_path=file_path,
                        line_number=line_number,
                        severity=config["severity"],
                        issue_type=issue_type,
                        description=config["description"],
                        recommendation=config["recommendation"],
                        code_snippet=line_stripped
                    )
                    self.issues.append(issue)
                    break  # Only report first match per line
    
    def audit_directory(self, directory: str = "."):
        """Audit all Python files in a directory"""
        for root, dirs, files in os.walk(directory):
            # Skip virtual environments and common ignore dirs
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'env', 'node_modules']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.audit_file(file_path)
    
    def get_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        severity_counts = {}
        issue_type_counts = {}
        
        for issue in self.issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
            issue_type_counts[issue.issue_type] = issue_type_counts.get(issue.issue_type, 0) + 1
        
        # Calculate security score (0-100)
        critical_issues = severity_counts.get("CRITICAL", 0)
        high_issues = severity_counts.get("HIGH", 0)
        medium_issues = severity_counts.get("MEDIUM", 0)
        low_issues = severity_counts.get("LOW", 0)
        
        # Penalty scoring
        penalty = (critical_issues * 30) + (high_issues * 15) + (medium_issues * 5) + (low_issues * 2)
        security_score = max(0, 100 - penalty)
        
        return {
            "total_issues": len(self.issues),
            "security_score": security_score,
            "severity_breakdown": severity_counts,
            "issue_types": issue_type_counts,
            "critical_issues": [issue for issue in self.issues if issue.severity == "CRITICAL"],
            "high_issues": [issue for issue in self.issues if issue.severity == "HIGH"],
            "recommendations": self._get_top_recommendations()
        }
    
    def _get_top_recommendations(self) -> List[str]:
        """Get top security recommendations based on issues found"""
        recommendations = []
        
        if any(issue.issue_type == "hardcoded_secrets" for issue in self.issues):
            recommendations.append("Implement secure secret management using environment variables")
        
        if any(issue.issue_type == "insecure_hash" for issue in self.issues):
            recommendations.append("Replace MD5/SHA1 with SHA-256 for all cryptographic operations")
        
        if any(issue.issue_type == "sql_injection" for issue in self.issues):
            recommendations.append("Use parameterized queries to prevent SQL injection attacks")
        
        if any(issue.issue_type == "unsafe_deserialization" for issue in self.issues):
            recommendations.append("Replace unsafe deserialization with secure alternatives")
        
        if any(issue.issue_type == "debug_mode" for issue in self.issues):
            recommendations.append("Disable debug mode and implement secure logging practices")
        
        return recommendations[:5]  # Top 5 recommendations
    
    def print_security_report(self):
        """Print formatted security report"""
        report = self.get_security_report()
        
        print("=== SENTINEL GRC SECURITY AUDIT REPORT ===")
        print()
        print(f"Security Score: {report['security_score']}/100")
        print(f"Total Issues Found: {report['total_issues']}")
        print()
        
        if report["severity_breakdown"]:
            print("Issue Breakdown by Severity:")
            for severity, count in sorted(report["severity_breakdown"].items(), 
                                        key=lambda x: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].index(x[0])):
                print(f"  {severity}: {count}")
            print()
        
        # Show critical and high issues
        critical_and_high = report["critical_issues"] + report["high_issues"]
        if critical_and_high:
            print("CRITICAL & HIGH SEVERITY ISSUES:")
            print("-" * 40)
            for issue in critical_and_high[:10]:  # Show first 10
                print(f"[{issue.severity}] {issue.file_path}:{issue.line_number}")
                print(f"  Issue: {issue.description}")
                print(f"  Code: {issue.code_snippet}")
                print(f"  Fix: {issue.recommendation}")
                print()
        
        if report["recommendations"]:
            print("TOP SECURITY RECOMMENDATIONS:")
            print("-" * 32)
            for i, rec in enumerate(report["recommendations"], 1):
                print(f"{i}. {rec}")
            print()
        
        # Security grade
        score = report['security_score']
        if score >= 90:
            grade = "A"
            status = "EXCELLENT"
        elif score >= 80:
            grade = "B"
            status = "GOOD"
        elif score >= 70:
            grade = "C"
            status = "FAIR"
        elif score >= 60:
            grade = "D"
            status = "POOR"
        else:
            grade = "F"
            status = "FAILING"
        
        print(f"Overall Security Grade: {grade} ({status})")
        print("=== END SECURITY AUDIT REPORT ===")

def run_security_audit():
    """Run security audit on the current directory"""
    auditor = SecurityAuditor()
    auditor.audit_directory(".")
    auditor.print_security_report()
    return auditor

if __name__ == "__main__":
    run_security_audit()