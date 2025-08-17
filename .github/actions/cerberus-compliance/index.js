const core = require('@actions/core');
const github = require('@actions/github');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

/**
 * Cerberus AI GitHub Actions Integration
 * Provides automated compliance checking in CI/CD pipelines
 */
class CerberusGitHubAction {
  constructor() {
    this.serverUrl = core.getInput('server-url');
    this.apiKey = core.getInput('api-key');
    this.frameworks = core.getInput('frameworks').split(',').map(f => f.trim());
    this.severityThreshold = core.getInput('severity-threshold');
    this.mode = core.getInput('mode');
    this.outputFormat = core.getInput('output-format');
    this.failOnViolations = core.getInput('fail-on-violations') === 'true';
    this.humanReviewThreshold = core.getInput('human-review-threshold');
  }

  async run() {
    try {
      core.info('🔱 Cerberus AI - Starting compliance validation...');
      
      // Collect repository context
      const context = await this.collectRepositoryContext();
      
      // Perform compliance check
      const complianceResult = await this.performComplianceCheck(context);
      
      // Process results
      await this.processResults(complianceResult);
      
      // Set outputs
      this.setActionOutputs(complianceResult);
      
      // Create PR comment if needed
      if (github.context.eventName === 'pull_request') {
        await this.createPullRequestComment(complianceResult);
      }
      
      // Handle build failure
      if (this.shouldFailBuild(complianceResult)) {
        core.setFailed(`Compliance violations found: ${complianceResult.violations.length}`);
      } else {
        core.info('✅ Compliance validation completed successfully');
      }
      
    } catch (error) {
      core.setFailed(`Action failed: ${error.message}`);
    }
  }

  async collectRepositoryContext() {
    const context = {
      repository: {
        name: github.context.repo.repo,
        owner: github.context.repo.owner,
        full_name: `${github.context.repo.owner}/${github.context.repo.repo}`,
        default_branch: github.context.ref.replace('refs/heads/', '')
      },
      commit: {
        sha: github.context.sha,
        message: await this.getCommitMessage(),
        author: github.context.actor
      },
      pull_request: github.context.payload.pull_request || null,
      workflow: {
        name: github.context.workflow,
        run_id: github.context.runId,
        run_number: github.context.runNumber
      },
      files_changed: await this.getChangedFiles(),
      timestamp: new Date().toISOString()
    };

    core.debug(`Repository context: ${JSON.stringify(context, null, 2)}`);
    return context;
  }

  async getCommitMessage() {
    try {
      const octokit = github.getOctokit(this.apiKey);
      const commit = await octokit.rest.repos.getCommit({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        ref: github.context.sha
      });
      return commit.data.commit.message;
    } catch (error) {
      core.warning(`Could not fetch commit message: ${error.message}`);
      return 'Unknown';
    }
  }

  async getChangedFiles() {
    try {
      if (github.context.eventName === 'pull_request') {
        const octokit = github.getOctokit(this.apiKey);
        const files = await octokit.rest.pulls.listFiles({
          owner: github.context.repo.owner,
          repo: github.context.repo.repo,
          pull_number: github.context.payload.pull_request.number
        });
        return files.data.map(file => ({
          filename: file.filename,
          status: file.status,
          changes: file.changes,
          patch: file.patch
        }));
      } else {
        // For push events, get files changed in the commit
        return this.getCommitChangedFiles();
      }
    } catch (error) {
      core.warning(`Could not fetch changed files: ${error.message}`);
      return [];
    }
  }

  async getCommitChangedFiles() {
    // Scan common source directories for changes
    const commonDirs = ['src', 'lib', 'app', 'components', 'services', 'api'];
    const changedFiles = [];
    
    for (const dir of commonDirs) {
      if (fs.existsSync(dir)) {
        const files = this.scanDirectory(dir);
        changedFiles.push(...files);
      }
    }
    
    return changedFiles.slice(0, 100); // Limit to prevent payload bloat
  }

  scanDirectory(dirPath) {
    const files = [];
    try {
      const entries = fs.readdirSync(dirPath, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        
        if (entry.isDirectory() && !entry.name.startsWith('.')) {
          files.push(...this.scanDirectory(fullPath));
        } else if (entry.isFile()) {
          files.push({
            filename: fullPath,
            status: 'modified', // We can't determine exact status without git
            changes: 0,
            content: this.readFileContent(fullPath)
          });
        }
      }
    } catch (error) {
      core.debug(`Error scanning directory ${dirPath}: ${error.message}`);
    }
    
    return files;
  }

  readFileContent(filePath) {
    try {
      const stats = fs.statSync(filePath);
      if (stats.size > 1024 * 1024) { // Skip files larger than 1MB
        return '[File too large]';
      }
      return fs.readFileSync(filePath, 'utf8');
    } catch (error) {
      return '[Could not read file]';
    }
  }

  async performComplianceCheck(context) {
    const payload = {
      context: context,
      frameworks: this.frameworks,
      mode: this.mode,
      options: {
        severity_threshold: this.severityThreshold,
        human_review_threshold: this.humanReviewThreshold,
        include_suggestions: true,
        include_evidence: true
      }
    };

    core.info(`Checking compliance for frameworks: ${this.frameworks.join(', ')}`);
    core.debug(`API payload: ${JSON.stringify(payload, null, 2)}`);

    try {
      const response = await axios.post(
        `${this.serverUrl}/api/v1/compliance/github-validate`,
        payload,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
            'User-Agent': 'Cerberus-AI-GitHub-Action/1.0'
          },
          timeout: 300000 // 5 minutes
        }
      );

      core.info(`✅ Compliance check completed with status: ${response.status}`);
      return response.data;

    } catch (error) {
      if (error.response) {
        core.error(`API Error: ${error.response.status} - ${error.response.data?.message || error.message}`);
        throw new Error(`Cerberus AI API returned ${error.response.status}: ${error.response.data?.message || 'Unknown error'}`);
      } else if (error.request) {
        core.error('No response from Cerberus AI server');
        throw new Error('Could not connect to Cerberus AI server. Please check server-url and network connectivity.');
      } else {
        core.error(`Request setup error: ${error.message}`);
        throw new Error(`Failed to setup request: ${error.message}`);
      }
    }
  }

  async processResults(result) {
    core.info(`📊 Compliance Results:`);
    core.info(`   Score: ${result.compliance_score}/100`);
    core.info(`   Violations: ${result.violations?.length || 0}`);
    core.info(`   Frameworks: ${result.frameworks_checked?.join(', ') || 'none'}`);
    core.info(`   Human Review: ${result.human_review_required ? 'Required' : 'Not Required'}`);

    // Log violations by severity
    if (result.violations && result.violations.length > 0) {
      const bySeverity = {};
      result.violations.forEach(v => {
        bySeverity[v.severity] = (bySeverity[v.severity] || 0) + 1;
      });
      
      core.info(`📋 Violations by severity:`);
      Object.entries(bySeverity).forEach(([severity, count]) => {
        const icon = this.getSeverityIcon(severity);
        core.info(`   ${icon} ${severity}: ${count}`);
      });
    }

    // Create output files
    await this.createOutputFiles(result);
  }

  async createOutputFiles(result) {
    const outputDir = path.join(process.env.GITHUB_WORKSPACE || '.', 'cerberus-reports');
    
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // JSON report
    if (this.outputFormat === 'json' || this.outputFormat === 'all') {
      const jsonPath = path.join(outputDir, 'compliance-report.json');
      fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
      core.info(`📄 JSON report saved: ${jsonPath}`);
    }

    // SARIF report for GitHub Security tab
    if (this.outputFormat === 'sarif' || this.outputFormat === 'all') {
      const sarifReport = this.convertToSarif(result);
      const sarifPath = path.join(outputDir, 'compliance-results.sarif');
      fs.writeFileSync(sarifPath, JSON.stringify(sarifReport, null, 2));
      core.info(`🔍 SARIF report saved: ${sarifPath}`);
    }

    // Summary report
    const summaryPath = path.join(outputDir, 'compliance-summary.md');
    const summaryContent = this.generateSummaryReport(result);
    fs.writeFileSync(summaryPath, summaryContent);
    core.info(`📝 Summary report saved: ${summaryPath}`);
  }

  convertToSarif(result) {
    const sarif = {
      version: '2.1.0',
      $schema: 'https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json',
      runs: [{
        tool: {
          driver: {
            name: 'Cerberus AI',
            version: '1.0.0',
            informationUri: 'https://cerberus-ai.com',
            rules: []
          }
        },
        results: []
      }]
    };

    if (result.violations) {
      result.violations.forEach((violation, index) => {
        // Add rule
        sarif.runs[0].tool.driver.rules.push({
          id: `cerberus-${violation.rule_id}`,
          name: violation.rule_name,
          shortDescription: { text: violation.title },
          fullDescription: { text: violation.description },
          help: {
            text: violation.remediation || 'No remediation provided'
          },
          properties: {
            tags: [violation.framework, violation.category]
          }
        });

        // Add result
        sarif.runs[0].results.push({
          ruleId: `cerberus-${violation.rule_id}`,
          level: this.mapSeverityToSarif(violation.severity),
          message: { text: violation.message },
          locations: [{
            physicalLocation: {
              artifactLocation: {
                uri: violation.file_path || 'unknown'
              },
              region: {
                startLine: violation.line_number || 1,
                startColumn: 1
              }
            }
          }]
        });
      });
    }

    return sarif;
  }

  mapSeverityToSarif(severity) {
    const mapping = {
      'critical': 'error',
      'high': 'error',
      'medium': 'warning',
      'low': 'note'
    };
    return mapping[severity.toLowerCase()] || 'warning';
  }

  generateSummaryReport(result) {
    const { compliance_score, violations, frameworks_checked, human_review_required } = result;
    
    let report = `# 🔱 Cerberus AI - Compliance Report\n\n`;
    report += `**Overall Score:** ${compliance_score}/100\n`;
    report += `**Frameworks Checked:** ${frameworks_checked?.join(', ') || 'None'}\n`;
    report += `**Human Review Required:** ${human_review_required ? '⚠️ Yes' : '✅ No'}\n`;
    report += `**Generated:** ${new Date().toISOString()}\n\n`;

    if (violations && violations.length > 0) {
      report += `## 🚨 Violations Found (${violations.length})\n\n`;
      
      violations.forEach((violation, index) => {
        const icon = this.getSeverityIcon(violation.severity);
        report += `### ${index + 1}. ${icon} ${violation.title}\n`;
        report += `**Severity:** ${violation.severity}\n`;
        report += `**Framework:** ${violation.framework}\n`;
        report += `**Description:** ${violation.description}\n`;
        
        if (violation.remediation) {
          report += `**Remediation:** ${violation.remediation}\n`;
        }
        
        if (violation.file_path) {
          report += `**File:** \`${violation.file_path}\``;
          if (violation.line_number) {
            report += `:${violation.line_number}`;
          }
          report += `\n`;
        }
        
        report += `\n`;
      });
    } else {
      report += `## ✅ No Violations Found\n\nAll compliance checks passed successfully!\n\n`;
    }

    if (human_review_required) {
      report += `## 👥 Human Review Required\n\n`;
      report += `This assessment requires human expertise for:\n`;
      report += `- Complex regulatory interpretation\n`;
      report += `- Strategic risk assessment\n`;
      report += `- Business context evaluation\n\n`;
      report += `Please review the detailed report and provide expert guidance.\n\n`;
    }

    report += `---\n`;
    report += `*Generated by Cerberus AI - Compliance Intelligence Platform*\n`;
    
    return report;
  }

  getSeverityIcon(severity) {
    const icons = {
      'critical': '🔴',
      'high': '🟠',
      'medium': '🟡',
      'low': '🔵'
    };
    return icons[severity.toLowerCase()] || '⚪';
  }

  async createPullRequestComment(result) {
    try {
      const octokit = github.getOctokit(this.apiKey);
      const comment = this.generatePullRequestComment(result);
      
      await octokit.rest.issues.createComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        issue_number: github.context.payload.pull_request.number,
        body: comment
      });
      
      core.info('💬 Pull request comment created');
    } catch (error) {
      core.warning(`Could not create PR comment: ${error.message}`);
    }
  }

  generatePullRequestComment(result) {
    const { compliance_score, violations, frameworks_checked, human_review_required } = result;
    
    let comment = `## 🔱 Cerberus AI - Compliance Check\n\n`;
    
    // Score badge
    const scoreColor = compliance_score >= 90 ? 'brightgreen' : 
                      compliance_score >= 70 ? 'yellow' : 'red';
    comment += `![Compliance Score](https://img.shields.io/badge/Compliance%20Score-${compliance_score}%25-${scoreColor})\n\n`;
    
    // Summary
    comment += `| Metric | Value |\n`;
    comment += `|--------|-------|\n`;
    comment += `| **Score** | ${compliance_score}/100 |\n`;
    comment += `| **Violations** | ${violations?.length || 0} |\n`;
    comment += `| **Frameworks** | ${frameworks_checked?.join(', ') || 'None'} |\n`;
    comment += `| **Human Review** | ${human_review_required ? '⚠️ Required' : '✅ Not Required'} |\n\n`;
    
    if (violations && violations.length > 0) {
      comment += `### 🚨 Violations by Severity\n\n`;
      const bySeverity = {};
      violations.forEach(v => {
        bySeverity[v.severity] = (bySeverity[v.severity] || 0) + 1;
      });
      
      Object.entries(bySeverity).forEach(([severity, count]) => {
        const icon = this.getSeverityIcon(severity);
        comment += `- ${icon} **${severity}**: ${count}\n`;
      });
      
      comment += `\n<details><summary>View Details</summary>\n\n`;
      violations.slice(0, 5).forEach((violation, index) => {
        comment += `**${index + 1}. ${violation.title}**\n`;
        comment += `- Severity: ${violation.severity}\n`;
        comment += `- Framework: ${violation.framework}\n`;
        comment += `- ${violation.description}\n\n`;
      });
      
      if (violations.length > 5) {
        comment += `... and ${violations.length - 5} more violations.\n\n`;
      }
      comment += `</details>\n\n`;
    } else {
      comment += `### ✅ All Checks Passed!\n\nNo compliance violations found.\n\n`;
    }
    
    if (human_review_required) {
      comment += `### 👥 Human Expertise Required\n\n`;
      comment += `This PR requires review from GRC professionals for complex compliance decisions.\n\n`;
    }
    
    comment += `---\n`;
    comment += `*🔱 Powered by [Cerberus AI](https://cerberus-ai.com) - The only platform uniting DevOps speed with GRC expertise*`;
    
    return comment;
  }

  shouldFailBuild(result) {
    if (!this.failOnViolations) {
      return false;
    }

    if (!result.violations || result.violations.length === 0) {
      return false;
    }

    // Check if any violations meet the severity threshold
    const thresholdOrder = ['low', 'medium', 'high', 'critical'];
    const thresholdIndex = thresholdOrder.indexOf(this.severityThreshold);
    
    return result.violations.some(violation => {
      const violationIndex = thresholdOrder.indexOf(violation.severity);
      return violationIndex >= thresholdIndex;
    });
  }

  setActionOutputs(result) {
    core.setOutput('violations-found', result.violations?.length || 0);
    core.setOutput('frameworks-checked', result.frameworks_checked?.join(',') || '');
    core.setOutput('compliance-score', result.compliance_score || 0);
    core.setOutput('human-review-required', result.human_review_required || false);
    core.setOutput('report-url', result.report_url || '');
  }
}

// Execute the action
(async () => {
  const action = new CerberusGitHubAction();
  await action.run();
})();