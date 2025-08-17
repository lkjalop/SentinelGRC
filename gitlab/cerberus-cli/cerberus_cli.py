#!/usr/bin/env python3
"""
Cerberus AI CLI for GitLab CI Integration
Command-line interface for compliance validation in GitLab pipelines
"""

import argparse
import json
import os
import sys
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CerberusCLI:
    """Main CLI class for Cerberus AI compliance validation"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.server_url = None
        self.api_key = None
        self.session = requests.Session()
        
    def setup_session(self, server_url: str, api_key: str):
        """Setup HTTP session with authentication"""
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': f'Cerberus-CLI/{self.version}'
        })
    
    def validate_compliance(self, args) -> Dict[str, Any]:
        """Run compliance validation"""
        
        logger.info("🔱 Starting Cerberus AI compliance validation")
        logger.info(f"Server: {args.server_url}")
        logger.info(f"Frameworks: {args.frameworks}")
        logger.info(f"Mode: {args.mode}")
        
        # Collect GitLab CI context
        context = self.collect_gitlab_context(args)
        
        # Build request payload
        payload = {
            'context': context,
            'frameworks': args.frameworks.split(','),
            'mode': args.mode,
            'options': {
                'severity_threshold': args.severity_threshold,
                'human_review_threshold': args.human_review_threshold,
                'include_suggestions': True,
                'include_evidence': True
            }
        }
        
        # Make API request
        try:
            response = self.session.post(
                f'{self.server_url}/api/v1/compliance/gitlab-validate',
                json=payload,
                timeout=300
            )
            
            if response.status_code != 200:
                logger.error(f"API request failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                sys.exit(1)
            
            result = response.json()
            logger.info(f"✅ Compliance validation completed")
            logger.info(f"Score: {result.get('compliance_score', 0)}/100")
            logger.info(f"Violations: {len(result.get('violations', []))}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request failed: {e}")
            sys.exit(1)
    
    def collect_gitlab_context(self, args) -> Dict[str, Any]:
        """Collect GitLab CI context from environment variables"""
        
        context = {
            'gitlab': {
                'project_id': os.getenv('CI_PROJECT_ID'),
                'project_name': os.getenv('CI_PROJECT_NAME'),
                'project_url': os.getenv('CI_PROJECT_URL'),
                'pipeline_id': os.getenv('CI_PIPELINE_ID'),
                'pipeline_url': os.getenv('CI_PIPELINE_URL'),
                'job_id': os.getenv('CI_JOB_ID'),
                'job_name': os.getenv('CI_JOB_NAME'),
                'job_url': os.getenv('CI_JOB_URL'),
                'commit_sha': args.commit_sha or os.getenv('CI_COMMIT_SHA'),
                'commit_ref': os.getenv('CI_COMMIT_REF_NAME'),
                'commit_message': os.getenv('CI_COMMIT_MESSAGE'),
                'commit_author': os.getenv('CI_COMMIT_AUTHOR'),
                'merge_request_iid': args.merge_request_iid or os.getenv('CI_MERGE_REQUEST_IID'),
                'gitlab_user_login': os.getenv('GITLAB_USER_LOGIN'),
                'runner_description': os.getenv('CI_RUNNER_DESCRIPTION')
            },
            'build': {
                'timestamp': datetime.now().isoformat(),
                'branch': args.branch or os.getenv('CI_COMMIT_REF_NAME'),
                'workspace': args.project_path or os.getenv('CI_PROJECT_DIR', os.getcwd()),
                'files_changed': self.collect_changed_files(args.project_path or os.getcwd())
            },
            'environment': {
                'gitlab_ci': True,
                'runner_tags': os.getenv('CI_RUNNER_TAGS', '').split(',') if os.getenv('CI_RUNNER_TAGS') else [],
                'deployment_environment': os.getenv('CI_ENVIRONMENT_NAME'),
                'deployment_url': os.getenv('CI_ENVIRONMENT_URL')
            }
        }
        
        return context
    
    def collect_changed_files(self, project_path: str) -> List[str]:
        """Collect changed files from the project"""
        
        changed_files = []
        try:
            project_dir = Path(project_path)
            
            # Common file patterns for compliance scanning
            patterns = [
                '**/*.py', '**/*.js', '**/*.ts', '**/*.java', '**/*.cs',
                '**/*.go', '**/*.rs', '**/*.php', '**/*.rb',
                '**/*.yml', '**/*.yaml', '**/*.json', '**/*.xml',
                '**/*.tf', '**/*.dockerfile', '**/Dockerfile',
                '**/*.sql', '**/*.sh', '**/*.ps1'
            ]
            
            for pattern in patterns:
                files = list(project_dir.glob(pattern))
                changed_files.extend([str(f.relative_to(project_dir)) for f in files[:20]])  # Limit to prevent bloat
                
                if len(changed_files) >= 100:  # Hard limit
                    break
            
        except Exception as e:
            logger.warning(f"Could not collect changed files: {e}")
        
        return changed_files
    
    def save_results(self, result: Dict[str, Any], output_dir: str, output_format: str):
        """Save compliance results to files"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📄 Saving results to {output_path}")
        
        # Save JSON report
        if output_format in ['json', 'all']:
            json_file = output_path / 'compliance-report.json'
            with open(json_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            logger.info(f"JSON report saved: {json_file}")
        
        # Save GitLab-specific formats
        if output_format in ['gitlab', 'all']:
            self.generate_gitlab_reports(result, output_path)
        
        # Save summary
        summary_file = output_path / 'compliance-summary.json'
        summary = {
            'compliance_score': result.get('compliance_score', 0),
            'violations_count': len(result.get('violations', [])),
            'frameworks_checked': result.get('frameworks_checked', []),
            'human_review_required': result.get('human_review_required', False),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save markdown report
        self.generate_markdown_report(result, output_path / 'compliance-report.md')
    
    def generate_gitlab_reports(self, result: Dict[str, Any], output_path: Path):
        """Generate GitLab-specific report formats"""
        
        # GitLab SAST format
        sast_report = self.convert_to_gitlab_sast(result)
        sast_file = output_path / 'gl-sast-report.json'
        with open(sast_file, 'w') as f:
            json.dump(sast_report, f, indent=2)
        logger.info(f"GitLab SAST report saved: {sast_file}")
        
        # GitLab Code Quality format
        codequality_report = self.convert_to_gitlab_codequality(result)
        codequality_file = output_path / 'gl-code-quality-report.json'
        with open(codequality_file, 'w') as f:
            json.dump(codequality_report, f, indent=2)
        logger.info(f"GitLab Code Quality report saved: {codequality_file}")
    
    def convert_to_gitlab_sast(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Cerberus results to GitLab SAST format"""
        
        sast_report = {
            "version": "14.0.0",
            "scan": {
                "scanner": {
                    "id": "cerberus-ai",
                    "name": "Cerberus AI",
                    "version": self.version,
                    "vendor": {"name": "Cerberus AI"}
                },
                "type": "sast",
                "start_time": datetime.now().isoformat(),
                "end_time": datetime.now().isoformat(),
                "status": "success"
            },
            "vulnerabilities": []
        }
        
        for violation in result.get('violations', []):
            vulnerability = {
                "id": f"cerberus-{violation.get('rule_id', 'unknown')}",
                "category": "sast",
                "name": violation.get('title', 'Compliance Violation'),
                "description": violation.get('description', ''),
                "severity": self.map_severity_to_gitlab(violation.get('severity', 'medium')),
                "confidence": "High",
                "scanner": {"id": "cerberus-ai", "name": "Cerberus AI"},
                "location": {
                    "file": violation.get('file_path', 'unknown'),
                    "start_line": violation.get('line_number', 1),
                    "end_line": violation.get('line_number', 1)
                },
                "identifiers": [{
                    "type": "cerberus_rule",
                    "name": violation.get('rule_name', ''),
                    "value": violation.get('rule_id', '')
                }]
            }
            
            sast_report["vulnerabilities"].append(vulnerability)
        
        return sast_report
    
    def convert_to_gitlab_codequality(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert Cerberus results to GitLab Code Quality format"""
        
        codequality_report = []
        
        for violation in result.get('violations', []):
            issue = {
                "description": violation.get('title', 'Compliance Violation'),
                "check_name": violation.get('rule_name', 'compliance_rule'),
                "fingerprint": f"cerberus-{violation.get('rule_id', 'unknown')}",
                "severity": self.map_severity_to_codequality(violation.get('severity', 'medium')),
                "location": {
                    "path": violation.get('file_path', 'unknown'),
                    "lines": {
                        "begin": violation.get('line_number', 1),
                        "end": violation.get('line_number', 1)
                    }
                },
                "categories": ["Security"],
                "type": "issue",
                "engine_name": "cerberus-ai"
            }
            
            codequality_report.append(issue)
        
        return codequality_report
    
    def map_severity_to_gitlab(self, severity: str) -> str:
        """Map Cerberus severity to GitLab SAST severity"""
        mapping = {
            'critical': 'Critical',
            'high': 'High',
            'medium': 'Medium',
            'low': 'Low'
        }
        return mapping.get(severity.lower(), 'Medium')
    
    def map_severity_to_codequality(self, severity: str) -> str:
        """Map Cerberus severity to GitLab Code Quality severity"""
        mapping = {
            'critical': 'blocker',
            'high': 'major',
            'medium': 'minor',
            'low': 'info'
        }
        return mapping.get(severity.lower(), 'minor')
    
    def generate_markdown_report(self, result: Dict[str, Any], output_file: Path):
        """Generate markdown compliance report"""
        
        report = []
        report.append("# 🔱 Cerberus AI - GitLab Compliance Report\n")
        report.append(f"**Overall Score:** {result.get('compliance_score', 0)}/100\n")
        report.append(f"**Frameworks Checked:** {', '.join(result.get('frameworks_checked', []))}\n")
        report.append(f"**Human Review Required:** {'⚠️ Yes' if result.get('human_review_required') else '✅ No'}\n")
        report.append(f"**Generated:** {datetime.now().isoformat()}\n\n")
        
        violations = result.get('violations', [])
        if violations:
            report.append(f"## 🚨 Violations Found ({len(violations)})\n\n")
            
            for i, violation in enumerate(violations, 1):
                severity_icon = self.get_severity_icon(violation.get('severity', 'medium'))
                report.append(f"### {i}. {severity_icon} {violation.get('title', 'Unknown Violation')}\n")
                report.append(f"**Severity:** {violation.get('severity', 'medium')}\n")
                report.append(f"**Framework:** {violation.get('framework', 'unknown')}\n")
                report.append(f"**Description:** {violation.get('description', '')}\n")
                
                if violation.get('file_path'):
                    file_path = violation['file_path']
                    line_number = violation.get('line_number')
                    if line_number:
                        report.append(f"**Location:** `{file_path}:{line_number}`\n")
                    else:
                        report.append(f"**File:** `{file_path}`\n")
                
                if violation.get('remediation'):
                    report.append(f"**Remediation:** {violation['remediation']}\n")
                
                report.append("\n")
        else:
            report.append("## ✅ No Violations Found\n\nAll compliance checks passed successfully!\n\n")
        
        if result.get('human_review_required'):
            report.append("## 👥 Human Review Required\n\n")
            report.append("This validation requires human expertise for complex compliance scenarios.\n")
            report.append("Please review the detailed findings and provide expert guidance.\n\n")
        
        report.append("---\n")
        report.append("*Generated by Cerberus AI - GitLab CI Integration*\n")
        
        with open(output_file, 'w') as f:
            f.write(''.join(report))
        
        logger.info(f"Markdown report saved: {output_file}")
    
    def get_severity_icon(self, severity: str) -> str:
        """Get icon for severity level"""
        icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🔵'
        }
        return icons.get(severity.lower(), '⚪')
    
    def check_failure_conditions(self, result: Dict[str, Any], args) -> bool:
        """Check if build should fail based on results"""
        
        if not args.fail_on_violations:
            logger.info("✅ Not failing build (fail_on_violations=false)")
            return False
        
        violations = result.get('violations', [])
        if not violations:
            logger.info("✅ No violations found")
            return False
        
        # Check severity threshold
        severity_order = ['low', 'medium', 'high', 'critical']
        threshold_index = severity_order.index(args.severity_threshold.lower())
        
        failing_violations = [
            v for v in violations
            if severity_order.index(v.get('severity', 'medium').lower()) >= threshold_index
        ]
        
        if failing_violations:
            logger.error(f"❌ {len(failing_violations)} violations at or above {args.severity_threshold} severity")
            return True
        else:
            logger.info(f"✅ No violations at or above {args.severity_threshold} threshold")
            return False

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(description='Cerberus AI CLI for GitLab CI compliance validation')
    
    # Connection settings
    parser.add_argument('--server-url', required=True, help='Cerberus AI server URL')
    parser.add_argument('--api-key', required=True, help='API authentication key')
    
    # Validation settings
    parser.add_argument('--frameworks', default='essential8', help='Comma-separated list of frameworks')
    parser.add_argument('--mode', choices=['validate', 'audit', 'monitor'], default='validate', help='Validation mode')
    parser.add_argument('--severity-threshold', choices=['low', 'medium', 'high', 'critical'], default='medium', help='Severity threshold for build failure')
    parser.add_argument('--human-review-threshold', choices=['low', 'medium', 'high'], default='high', help='Threshold for requiring human review')
    
    # Output settings
    parser.add_argument('--output-format', choices=['json', 'gitlab', 'all'], default='gitlab', help='Output report format')
    parser.add_argument('--output-dir', default='cerberus-reports', help='Directory for output files')
    parser.add_argument('--fail-on-violations', type=lambda x: x.lower() == 'true', default=True, help='Fail build on violations')
    
    # GitLab CI context
    parser.add_argument('--project-path', help='Project directory path')
    parser.add_argument('--commit-sha', help='Commit SHA')
    parser.add_argument('--branch', help='Branch name')
    parser.add_argument('--merge-request-iid', help='Merge request IID')
    
    # Utility commands
    parser.add_argument('--version', action='version', version=f'Cerberus CLI {CerberusCLI().version}')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = CerberusCLI()
    cli.setup_session(args.server_url, args.api_key)
    
    try:
        # Run compliance validation
        result = cli.validate_compliance(args)
        
        # Save results
        cli.save_results(result, args.output_dir, args.output_format)
        
        # Check if build should fail
        should_fail = cli.check_failure_conditions(result, args)
        
        if should_fail:
            logger.error("❌ Build failed due to compliance violations")
            sys.exit(1)
        else:
            logger.info("✅ Compliance validation passed")
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()