# 🔱 Cerberus AI - GitHub Actions Integration

**The first compliance platform built for DevOps speed and GRC expertise**

Automatically validate compliance in your CI/CD pipelines with AI-powered intelligence across multiple regulatory frameworks.

## ✨ Features

- **🚀 Zero-Friction Integration**: Add compliance to any GitHub workflow in minutes
- **🧠 Multi-Framework Intelligence**: Essential 8, NIST CSF, SOC 2, GDPR, and more
- **👥 Human-in-the-Loop**: AI handles routine checks, experts handle strategic decisions
- **📊 Rich Reporting**: JSON, SARIF, and markdown reports with actionable insights
- **💬 PR Comments**: Automated compliance feedback directly in pull requests
- **⚡ Fast Performance**: Sub-30-second validation for most repositories

## 🚀 Quick Start

### Basic Usage

```yaml
name: Compliance Check
on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Cerberus AI Compliance Check
        uses: ./path/to/cerberus-compliance
        with:
          api-key: ${{ secrets.CERBERUS_API_KEY }}
          frameworks: 'essential8,nistcsf'
          severity-threshold: 'medium'
```

### Enterprise Setup

```yaml
name: Enterprise Compliance Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  compliance-validation:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      pull-requests: write
      
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Cerberus AI - Full Compliance Scan
        uses: ./path/to/cerberus-compliance
        with:
          server-url: 'https://enterprise.cerberus-ai.com'
          api-key: ${{ secrets.CERBERUS_ENTERPRISE_KEY }}
          frameworks: 'essential8,nistcsf,soc2,gdpr,iso27001'
          severity-threshold: 'low'
          mode: 'audit'
          output-format: 'sarif'
          fail-on-violations: 'true'
          human-review-threshold: 'medium'
      
      - name: Upload SARIF Results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: cerberus-reports/compliance-results.sarif
      
      - name: Archive Reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: compliance-reports
          path: cerberus-reports/
```

## 📋 Input Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `server-url` | Cerberus AI server endpoint | ✅ | `https://api.cerberus-ai.com` |
| `api-key` | Authentication API key | ✅ | - |
| `frameworks` | Frameworks to validate (comma-separated) | ❌ | `essential8` |
| `severity-threshold` | Minimum severity to fail build | ❌ | `medium` |
| `mode` | Validation mode: `validate`, `audit`, `monitor` | ❌ | `validate` |
| `output-format` | Report format: `json`, `sarif`, `summary` | ❌ | `summary` |
| `fail-on-violations` | Fail build on violations | ❌ | `true` |
| `human-review-threshold` | When to require human review | ❌ | `high` |

## 📊 Output Parameters

| Parameter | Description |
|-----------|-------------|
| `violations-found` | Number of compliance violations |
| `frameworks-checked` | List of validated frameworks |
| `compliance-score` | Overall score (0-100) |
| `human-review-required` | Whether expert review is needed |
| `report-url` | Link to detailed report |

## 🔧 Supported Frameworks

### Current Support
- **Essential 8** - Australian Cyber Security Centre
- **NIST Cybersecurity Framework** - US National Institute of Standards
- **SOC 2** - System and Organization Controls
- **GDPR** - General Data Protection Regulation
- **ISO 27001/27002** - Information Security Management

### Coming Soon
- **PCI DSS** - Payment Card Industry
- **HIPAA** - Healthcare compliance
- **FISMA** - Federal Information Security
- **CIS Controls** - Center for Internet Security

## 🎯 Validation Modes

### `validate` (Default)
- Fast compliance checking
- Suitable for pre-commit and PR validation
- Basic remediation suggestions

### `audit`
- Comprehensive compliance assessment  
- Detailed evidence collection
- Audit-ready documentation

### `monitor`
- Continuous compliance tracking
- Trend analysis and reporting
- No build failures, monitoring only

## 📈 Output Formats

### JSON Report
Complete machine-readable results with:
- Detailed violation information
- Framework mapping
- Remediation suggestions
- Evidence collection

### SARIF Report
GitHub Security tab integration:
- Native security findings display
- Code annotations
- Workflow integration

### Summary Report
Human-readable markdown with:
- Executive summary
- Key findings
- Action items
- Compliance score

## 🎨 Example Workflows

### Pre-commit Validation
```yaml
name: Pre-commit Compliance
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quick-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./path/to/cerberus-compliance
        with:
          api-key: ${{ secrets.CERBERUS_API_KEY }}
          mode: 'validate'
          severity-threshold: 'high'
          fail-on-violations: 'false'  # Don't block, just warn
```

### Nightly Compliance Audit
```yaml
name: Nightly Compliance Audit
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily

jobs:
  full-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./path/to/cerberus-compliance
        with:
          api-key: ${{ secrets.CERBERUS_API_KEY }}
          frameworks: 'essential8,nistcsf,soc2,gdpr,iso27001'
          mode: 'audit'
          output-format: 'json'
          human-review-threshold: 'low'
```

## 🔐 Authentication & Security

### API Key Setup
1. Generate API key in Cerberus AI dashboard
2. Add to GitHub repository secrets as `CERBERUS_API_KEY`
3. Reference in workflow: `${{ secrets.CERBERUS_API_KEY }}`

### Permissions Required
```yaml
permissions:
  contents: read          # Read repository code
  security-events: write  # Upload SARIF results
  pull-requests: write    # Comment on PRs
```

## 🎭 Human-in-the-Loop Intelligence

Cerberus AI doesn't replace compliance experts—it amplifies them:

- **AI Automation**: Handles routine, repetitive compliance checks
- **Human Expertise**: Complex decisions, regulatory interpretation, strategic risk
- **Smart Escalation**: Automatically routes complex issues to GRC professionals
- **Collaborative Workflow**: AI findings + human judgment = better compliance

### When Human Review is Required
- High-complexity regulatory scenarios
- Novel compliance situations
- Strategic risk assessment needs
- Regulatory gray areas requiring interpretation

## 📊 Compliance Score Calculation

The compliance score (0-100) reflects:
- **Framework Coverage** (40%): Percentage of applicable controls checked
- **Violation Severity** (35%): Impact of identified issues
- **Best Practices** (15%): Adoption of recommended practices
- **Trend Analysis** (10%): Improvement over time

## 🔍 Troubleshooting

### Common Issues

**Authentication Failed**
```
Error: Cerberus AI API returned 401: Invalid API key
```
- Verify API key is correct in secrets
- Check key hasn't expired in Cerberus AI dashboard

**Network Timeout**
```
Error: Could not connect to Cerberus AI server
```
- Check server-url parameter
- Verify network connectivity from runner
- Confirm firewall rules allow outbound HTTPS

**Large Repository Timeout**
```
Error: Request timeout after 300 seconds
```
- Use `mode: 'validate'` for faster checks
- Limit `frameworks` to essential ones
- Contact support for enterprise optimization

### Debug Mode
Enable debug logging:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

## 🆘 Support

- **Documentation**: https://docs.cerberus-ai.com/github-actions
- **Community**: https://community.cerberus-ai.com
- **Enterprise Support**: support@cerberus-ai.com
- **Issues**: https://github.com/cerberus-ai/github-action/issues

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**🔱 Powered by Cerberus AI - The three-headed guardian of enterprise compliance**

*One Intelligence. Two Interfaces. Complete Compliance.*