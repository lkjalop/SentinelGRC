# 🔱 Cerberus AI GitLab CI Integration

**Automated compliance validation for GitLab CI/CD pipelines**

Integrate Cerberus AI's multi-framework compliance checking directly into your GitLab CI/CD workflows with native GitLab features integration.

## ✨ Features

- **🚀 Native GitLab Integration**: Works with GitLab CI/CD, Security Dashboard, and Code Quality
- **🧠 Multi-Framework Support**: Essential 8, NIST CSF, SOC 2, GDPR, ISO 27001, PCI DSS, HIPAA
- **👥 Human-in-the-Loop**: AI handles routine checks, experts review complex scenarios
- **📊 Rich Reporting**: SAST reports, Code Quality integration, custom dashboards
- **⚡ High Performance**: Optimized for CI/CD pipeline speeds with parallel execution
- **🔧 Flexible Configuration**: Template-based setup with environment-specific settings

## 🚀 Quick Start

### 1. Add to Your Pipeline

Add this to your `.gitlab-ci.yml`:

```yaml
include:
  - remote: 'https://raw.githubusercontent.com/cerberus-ai/gitlab-ci-templates/main/cerberus-compliance.yml'

variables:
  CERBERUS_API_KEY: $CERBERUS_API_KEY  # Set in CI/CD variables

cerberus_compliance:
  extends: .cerberus_compliance_template
  variables:
    CERBERUS_FRAMEWORKS: "essential8,nistcsf"
  only:
    - main
    - merge_requests
```

### 2. Set CI/CD Variables

In your GitLab project, go to **Settings** → **CI/CD** → **Variables** and add:

- **CERBERUS_API_KEY**: Your Cerberus AI API key (masked)
- **CERBERUS_SERVER_URL**: Server endpoint (optional, defaults to `https://api.cerberus-ai.com`)

### 3. Run Your Pipeline

Push to your repository and watch Cerberus AI validate compliance automatically!

## 📋 Full Configuration Example

```yaml
# Complete .gitlab-ci.yml example
stages:
  - build
  - test
  - compliance
  - deploy

# Include Cerberus AI template
include:
  - remote: 'https://raw.githubusercontent.com/cerberus-ai/gitlab-ci-templates/main/cerberus-compliance.yml'

# Build stage
build:
  stage: build
  script:
    - echo "Building application..."
    - ./build.sh

# Quick compliance check for MRs
cerberus_quick_check:
  extends: .cerberus_compliance_template
  stage: compliance
  variables:
    CERBERUS_FRAMEWORKS: "essential8"
    CERBERUS_MODE: "validate"
    CERBERUS_FAIL_ON_VIOLATIONS: "false"
  only:
    - merge_requests

# Full compliance validation for main
cerberus_full_validation:
  extends: .cerberus_compliance_template
  stage: compliance
  variables:
    CERBERUS_FRAMEWORKS: "essential8,nistcsf,soc2"
    CERBERUS_MODE: "validate"
    CERBERUS_SEVERITY_THRESHOLD: "medium"
    CERBERUS_FAIL_ON_VIOLATIONS: "true"
  only:
    - main

# Deploy only if compliance passes
deploy:
  stage: deploy
  script:
    - ./deploy.sh
  dependencies:
    - cerberus_full_validation
  only:
    - main
  when: manual
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `CERBERUS_SERVER_URL` | Server endpoint | `https://api.cerberus-ai.com` | Any valid URL |
| `CERBERUS_API_KEY` | Authentication key | **Required** | API key from dashboard |
| `CERBERUS_FRAMEWORKS` | Frameworks to check | `essential8` | Comma-separated list |
| `CERBERUS_MODE` | Validation mode | `validate` | `validate`, `audit`, `monitor` |
| `CERBERUS_SEVERITY_THRESHOLD` | Build failure threshold | `medium` | `low`, `medium`, `high`, `critical` |
| `CERBERUS_FAIL_ON_VIOLATIONS` | Fail build on violations | `true` | `true`, `false` |
| `CERBERUS_HUMAN_REVIEW_THRESHOLD` | Human review trigger | `high` | `low`, `medium`, `high` |
| `CERBERUS_OUTPUT_FORMAT` | Report format | `gitlab` | `json`, `gitlab`, `all` |

### Supported Frameworks

- **essential8** - Australian Cyber Security Centre's Essential 8
- **nistcsf** - NIST Cybersecurity Framework
- **soc2** - SOC 2 Type I/II
- **gdpr** - General Data Protection Regulation
- **iso27001** - ISO/IEC 27001
- **pcidss** - Payment Card Industry Data Security Standard
- **hipaa** - Health Insurance Portability and Accountability Act

## 📊 GitLab Integration Features

### Security Dashboard Integration

Cerberus AI automatically generates SAST reports visible in GitLab's Security Dashboard:

```yaml
cerberus_compliance:
  extends: .cerberus_compliance_template
  artifacts:
    reports:
      sast: cerberus-reports/gl-sast-report.json
```

### Code Quality Integration

Compliance violations appear as Code Quality issues:

```yaml
cerberus_compliance:
  extends: .cerberus_compliance_template
  artifacts:
    reports:
      codequality: cerberus-reports/gl-code-quality-report.json
```

### Merge Request Comments

Violations are automatically commented on merge requests with remediation suggestions.

### Coverage Integration

Compliance scores can be tracked as coverage metrics:

```yaml
cerberus_compliance:
  extends: .cerberus_compliance_template
  coverage: '/Compliance Score: (\d+)%/'
```

## 🎯 Advanced Use Cases

### Multi-Framework Parallel Validation

```yaml
cerberus_multi_framework:
  stage: compliance
  parallel:
    matrix:
      - FRAMEWORK: ["essential8", "nistcsf", "soc2", "gdpr"]
  extends: .cerberus_compliance_template
  variables:
    CERBERUS_FRAMEWORKS: $FRAMEWORK
```

### Regional Compliance Validation

```yaml
cerberus_regional:
  stage: compliance
  parallel:
    matrix:
      - REGION: ["australia", "united_states", "european_union"]
        FRAMEWORK: ["essential8", "nistcsf", "gdpr"]
  extends: .cerberus_compliance_template
  variables:
    CERBERUS_REGION: $REGION
    CERBERUS_FRAMEWORKS: $FRAMEWORK
```

### Container Security Compliance

```yaml
cerberus_container:
  stage: compliance
  image: registry.cerberus-ai.com/cerberus-cli:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_PROJECT_NAME:$CI_COMMIT_SHA .
    - cerberus-cli container-scan --image $CI_PROJECT_NAME:$CI_COMMIT_SHA
```

### Infrastructure as Code Compliance

```yaml
cerberus_iac:
  stage: compliance
  extends: .cerberus_compliance_template
  script:
    - cerberus-cli iac-scan --scan-path ./terraform --frameworks nistcsf,soc2
  only:
    changes:
      - "**/*.tf"
      - "**/*.yaml"
```

### Scheduled Comprehensive Audits

```yaml
cerberus_weekly_audit:
  extends: .cerberus_compliance_template
  variables:
    CERBERUS_FRAMEWORKS: "essential8,nistcsf,soc2,gdpr,iso27001"
    CERBERUS_MODE: "audit"
    CERBERUS_SEVERITY_THRESHOLD: "low"
  artifacts:
    expire_in: 90 days
  only:
    - schedules
```

## 🔄 Pipeline Templates

### Basic Template

```yaml
.cerberus_compliance_template: &cerberus_compliance
  stage: compliance
  image: registry.cerberus-ai.com/cerberus-cli:latest
  variables:
    CERBERUS_SERVER_URL: "https://api.cerberus-ai.com"
    CERBERUS_FRAMEWORKS: "essential8"
    CERBERUS_MODE: "validate"
  script:
    - cerberus-cli validate --server-url $CERBERUS_SERVER_URL --api-key $CERBERUS_API_KEY
  artifacts:
    reports:
      sast: cerberus-reports/gl-sast-report.json
      codequality: cerberus-reports/gl-code-quality-report.json
    paths:
      - cerberus-reports/
```

### Enterprise Template

```yaml
.cerberus_enterprise_template: &cerberus_enterprise
  stage: compliance
  image: registry.cerberus-ai.com/cerberus-cli:enterprise
  variables:
    CERBERUS_SERVER_URL: "https://enterprise.cerberus-ai.com"
    CERBERUS_FRAMEWORKS: "essential8,nistcsf,soc2,gdpr,iso27001,pcidss"
    CERBERUS_MODE: "audit"
    CERBERUS_SEVERITY_THRESHOLD: "low"
    CERBERUS_HUMAN_REVIEW_THRESHOLD: "medium"
  before_script:
    - cerberus-cli auth --verify
  script:
    - cerberus-cli enterprise-audit --comprehensive --include-trends
  after_script:
    - cerberus-cli generate-executive-summary --format pdf
  artifacts:
    reports:
      sast: cerberus-reports/gl-sast-report.json
      codequality: cerberus-reports/gl-code-quality-report.json
      performance: cerberus-reports/performance-metrics.json
    paths:
      - cerberus-reports/
      - executive-summary.pdf
    expire_in: 90 days
```

## 👥 Human Review Integration

### Slack Notifications

```yaml
cerberus_notify_humans:
  stage: compliance
  image: alpine:latest
  dependencies:
    - cerberus_compliance
  script:
    - |
      if [ "$(cat cerberus-reports/compliance-summary.json | jq -r '.human_review_required')" = "true" ]; then
        curl -X POST -H 'Content-type: application/json' \
          --data "{
            \"text\": \"🔱 Cerberus AI: Human review required for $CI_PROJECT_NAME\",
            \"blocks\": [{
              \"type\": \"section\",
              \"text\": {
                \"type\": \"mrkdwn\",
                \"text\": \"*Project:* $CI_PROJECT_NAME\n*Pipeline:* <$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\n*Action:* Review complex compliance scenarios\"
              }
            }]
          }" \
          $SLACK_WEBHOOK_URL
      fi
  when: always
```

### Email Notifications

```yaml
cerberus_email_notification:
  stage: compliance
  dependencies:
    - cerberus_compliance
  script:
    - |
      HUMAN_REVIEW=$(cat cerberus-reports/compliance-summary.json | jq -r '.human_review_required')
      if [ "$HUMAN_REVIEW" = "true" ]; then
        echo "Complex compliance scenarios require GRC expert review" | \
        mail -s "Cerberus AI: Review Required - $CI_PROJECT_NAME" grc-team@company.com
      fi
```

### Microsoft Teams Integration

```yaml
cerberus_teams_notification:
  stage: compliance
  script:
    - |
      curl -H "Content-Type: application/json" -d "{
        \"@type\": \"MessageCard\",
        \"@context\": \"http://schema.org/extensions\",
        \"summary\": \"Cerberus AI Compliance Review\",
        \"themeColor\": \"0076D7\",
        \"sections\": [{
          \"activityTitle\": \"🔱 Human Review Required\",
          \"activitySubtitle\": \"$CI_PROJECT_NAME - Pipeline #$CI_PIPELINE_ID\",
          \"facts\": [
            {\"name\": \"Project\", \"value\": \"$CI_PROJECT_NAME\"},
            {\"name\": \"Branch\", \"value\": \"$CI_COMMIT_REF_NAME\"},
            {\"name\": \"Pipeline\", \"value\": \"#$CI_PIPELINE_ID\"}
          ]
        }]
      }" $TEAMS_WEBHOOK_URL
```

## 🐳 Docker Integration

### Custom CLI Image

```dockerfile
FROM registry.cerberus-ai.com/cerberus-cli:latest

# Add custom compliance rules
COPY compliance-rules/ /opt/compliance-rules/

# Add organization-specific configuration
COPY cerberus-config.yaml /etc/cerberus/config.yaml

# Set environment defaults
ENV CERBERUS_CUSTOM_RULES_PATH=/opt/compliance-rules
ENV CERBERUS_CONFIG_PATH=/etc/cerberus/config.yaml
```

### Multi-Stage Pipeline

```yaml
stages:
  - build
  - test
  - package
  - compliance
  - deploy

build_image:
  stage: build
  script:
    - docker build -t $CI_PROJECT_NAME:$CI_COMMIT_SHA .

compliance_scan:
  stage: compliance
  dependencies:
    - build_image
  script:
    - cerberus-cli container-scan --image $CI_PROJECT_NAME:$CI_COMMIT_SHA
```

## 📈 Monitoring & Metrics

### Performance Metrics

```yaml
cerberus_performance:
  extends: .cerberus_compliance_template
  script:
    - |
      START_TIME=$(date +%s)
      cerberus-cli validate --measure-performance
      END_TIME=$(date +%s)
      DURATION=$((END_TIME - START_TIME))
      echo "Compliance validation duration: ${DURATION}s"
  artifacts:
    reports:
      performance: cerberus-reports/performance-metrics.json
```

### Trend Analysis

```yaml
cerberus_trends:
  extends: .cerberus_compliance_template
  variables:
    CERBERUS_MODE: "monitor"
  script:
    - cerberus-cli trend-analysis --historical-data --generate-charts
  artifacts:
    paths:
      - cerberus-reports/trends/
    expire_in: 30 days
```

## 🔍 Troubleshooting

### Debug Mode

Enable debug logging:

```yaml
cerberus_debug:
  extends: .cerberus_compliance_template
  variables:
    CERBERUS_DEBUG: "true"
    CERBERUS_LOG_LEVEL: "DEBUG"
```

### Common Issues

**Authentication Failed**
```
Error: 401 Unauthorized
```
- Verify `CERBERUS_API_KEY` is set correctly in CI/CD variables
- Check if API key is marked as "masked" in GitLab
- Ensure key hasn't expired in Cerberus AI dashboard

**Pipeline Timeout**
```
Job exceeded maximum time limit
```
- Reduce frameworks: `CERBERUS_FRAMEWORKS: "essential8"`
- Use validate mode: `CERBERUS_MODE: "validate"`
- Increase GitLab job timeout in `.gitlab-ci.yml`

**Large Repository Scanning**
```
Error: Repository too large for analysis
```
- Use `.cerberus-ignore` file to exclude directories
- Limit file patterns in CLI configuration
- Consider breaking into multiple jobs

### Health Checks

```yaml
cerberus_health_check:
  stage: .pre
  image: registry.cerberus-ai.com/cerberus-cli:latest
  script:
    - cerberus-cli health --server-url $CERBERUS_SERVER_URL
    - cerberus-cli auth --verify --api-key $CERBERUS_API_KEY
```

## 🆘 Support & Resources

- **📖 Documentation**: [https://docs.cerberus-ai.com/gitlab](https://docs.cerberus-ai.com/gitlab)
- **💻 Templates Repository**: [https://gitlab.com/cerberus-ai/gitlab-ci-templates](https://gitlab.com/cerberus-ai/gitlab-ci-templates)
- **🎯 Examples**: [https://gitlab.com/cerberus-ai/examples](https://gitlab.com/cerberus-ai/examples)
- **🐛 Issues**: [https://gitlab.com/cerberus-ai/gitlab-integration/issues](https://gitlab.com/cerberus-ai/gitlab-integration/issues)
- **💬 Community**: [https://community.cerberus-ai.com](https://community.cerberus-ai.com)
- **🏢 Enterprise Support**: support@cerberus-ai.com

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🔱 Powered by Cerberus AI - The Three-Headed Guardian of Enterprise Compliance**

*One Intelligence. Two Interfaces. Complete Compliance.*