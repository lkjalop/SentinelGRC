# 🔱 Cerberus AI Jenkins Plugin

**Automated compliance validation for Jenkins pipelines**

Integrate Cerberus AI's multi-framework compliance checking directly into your Jenkins CI/CD pipelines.

## ✨ Features

- **🚀 Native Jenkins Integration**: Works with all Jenkins job types
- **🧠 Multi-Framework Support**: Essential 8, NIST CSF, SOC 2, GDPR, ISO 27001
- **👥 Human-in-the-Loop**: AI handles routine checks, experts handle complex decisions
- **📊 Rich Reporting**: JSON reports, build summaries, and UI integration
- **⚡ Fast Performance**: Optimized for CI/CD pipeline speeds
- **🔧 Flexible Configuration**: Configurable thresholds and failure conditions

## 🚀 Installation

### From Jenkins Update Center (Recommended)
1. Go to **Manage Jenkins** → **Manage Plugins**
2. Search for "Cerberus AI Compliance"
3. Install and restart Jenkins

### Manual Installation
1. Download the latest `.hpi` file from [releases](https://github.com/cerberus-ai/jenkins-plugin/releases)
2. Go to **Manage Jenkins** → **Manage Plugins** → **Advanced**
3. Upload the `.hpi` file
4. Restart Jenkins

## 🔧 Configuration

### Global Configuration
1. Go to **Manage Jenkins** → **Configure System**
2. Add Cerberus AI server URL in global settings (optional)
3. Configure default frameworks and thresholds

### Credentials Setup
1. Go to **Manage Jenkins** → **Manage Credentials**
2. Add new **Username with password** credential:
   - **Username**: Your Cerberus AI username
   - **Password**: Your Cerberus AI API key
   - **ID**: `cerberus-api-key` (or custom ID)

## 📋 Usage

### Freestyle Projects

1. Add build step **"🔱 Cerberus AI Compliance Check"**
2. Configure settings:
   - **Server URL**: `https://api.cerberus-ai.com`
   - **Credentials**: Select your API credentials
   - **Frameworks**: Choose compliance frameworks
   - **Mode**: Select validation mode
   - **Thresholds**: Configure severity and review levels

### Pipeline Projects

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Compliance Check') {
            steps {
                cerberusCompliance(
                    serverUrl: 'https://api.cerberus-ai.com',
                    credentialsId: 'cerberus-api-key',
                    frameworks: 'essential8,nistcsf',
                    mode: 'validate',
                    severityThreshold: 'medium',
                    failOnViolations: true
                )
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
            }
        }
    }
    
    post {
        always {
            // Archive compliance reports
            archiveArtifacts artifacts: 'cerberus-reports/**', allowEmptyArchive: true
        }
    }
}
```

### Advanced Pipeline Example

```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'COMPLIANCE_MODE',
            choices: ['validate', 'audit', 'monitor'],
            description: 'Compliance validation mode'
        )
        booleanParam(
            name: 'FAIL_ON_VIOLATIONS',
            defaultValue: true,
            description: 'Fail build on compliance violations'
        )
    }
    
    stages {
        stage('Comprehensive Compliance Check') {
            steps {
                script {
                    // Multi-framework validation
                    def result = cerberusCompliance(
                        serverUrl: 'https://enterprise.cerberus-ai.com',
                        credentialsId: 'cerberus-enterprise-key',
                        frameworks: 'essential8,nistcsf,soc2,gdpr,iso27001',
                        mode: params.COMPLIANCE_MODE,
                        severityThreshold: 'low',
                        humanReviewThreshold: 'medium',
                        failOnViolations: params.FAIL_ON_VIOLATIONS,
                        publishResults: true,
                        outputFormat: 'all'
                    )
                    
                    // Custom logic based on results
                    if (result.humanReviewRequired) {
                        echo "⚠️ Human review required for complex compliance scenarios"
                        // Trigger notification to GRC team
                        emailext(
                            subject: "Compliance Review Required: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                            body: "Build requires human expertise for compliance validation.",
                            to: "grc-team@company.com"
                        )
                    }
                    
                    // Set build description
                    currentBuild.description = "Compliance Score: ${result.complianceScore}%"
                }
            }
        }
        
        stage('Conditional Deploy') {
            when {
                expression { 
                    // Only deploy if compliance score is above threshold
                    return currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                }
            }
            steps {
                echo "✅ Compliance passed - proceeding with deployment"
                // Deployment steps here
            }
        }
    }
    
    post {
        always {
            // Publish compliance results
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: 'cerberus-reports',
                reportFiles: 'compliance-summary.html',
                reportName: 'Compliance Report'
            ])
        }
        
        failure {
            echo "❌ Build failed - check compliance violations"
        }
        
        success {
            echo "✅ Build passed all compliance checks"
        }
    }
}
```

## ⚙️ Configuration Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `serverUrl` | Cerberus AI server endpoint | `https://api.cerberus-ai.com` | Any valid URL |
| `credentialsId` | Jenkins credentials ID | - | Any credential ID |
| `frameworks` | Frameworks to validate | `essential8` | `essential8`, `nistcsf`, `soc2`, `gdpr`, `iso27001` |
| `mode` | Validation mode | `validate` | `validate`, `audit`, `monitor` |
| `severityThreshold` | Build failure threshold | `medium` | `low`, `medium`, `high`, `critical` |
| `humanReviewThreshold` | Human review trigger | `high` | `low`, `medium`, `high` |
| `outputFormat` | Report format | `json` | `json`, `summary`, `all` |
| `failOnViolations` | Fail build on violations | `true` | `true`, `false` |
| `publishResults` | Save reports to workspace | `true` | `true`, `false` |

## 🎯 Validation Modes

### `validate` (Default)
- **Purpose**: Fast compliance checking for CI/CD
- **Speed**: Sub-30 seconds for most projects
- **Output**: Basic compliance score and violations
- **Use Case**: Pre-commit hooks, PR validation

### `audit`
- **Purpose**: Comprehensive compliance assessment
- **Speed**: 2-5 minutes depending on project size
- **Output**: Detailed evidence collection and audit trails
- **Use Case**: Release validation, quarterly audits

### `monitor`
- **Purpose**: Continuous compliance tracking
- **Speed**: Varies based on monitoring scope
- **Output**: Trend analysis and compliance drift detection
- **Use Case**: Production monitoring, compliance dashboards

## 📊 Understanding Results

### Compliance Score
- **90-100%**: ✅ Excellent - Minimal compliance gaps
- **80-89%**: 🟡 Good - Minor issues to address
- **70-79%**: 🟠 Fair - Moderate compliance gaps
- **Below 70%**: 🔴 Poor - Significant remediation needed

### Violation Severities
- **🔴 Critical**: Immediate action required, security risk
- **🟠 High**: Important issue, should be fixed soon
- **🟡 Medium**: Moderate issue, plan remediation
- **🔵 Low**: Minor issue, fix when convenient

### Human Review Indicators
- **👥 Required**: Complex scenarios need GRC expert input
- **🤖 Automated**: AI handled all compliance checks
- **⚖️ Escalated**: Regulatory interpretation needed

## 🔍 Troubleshooting

### Common Issues

**Plugin Not Loading**
```
Error: Plugin failed to load
```
- Verify Jenkins version compatibility (2.401.3+)
- Check plugin dependencies are installed
- Review Jenkins logs for detailed error messages

**Authentication Failed**
```
Error: 401 Unauthorized
```
- Verify API credentials are correct
- Check credential ID matches configuration
- Ensure API key hasn't expired

**Connection Timeout**
```
Error: Connection timeout to server
```
- Verify server URL is correct
- Check network connectivity from Jenkins
- Confirm firewall rules allow outbound HTTPS

**Build Hangs**
```
Build stuck at "Performing compliance validation..."
```
- Check server response times
- Verify project size isn't too large
- Try `validate` mode instead of `audit`

### Debug Mode

Enable debug logging by adding to Jenkins system properties:
```bash
-Dlogger.ai.cerberus.jenkins.level=DEBUG
```

Or set environment variable in pipeline:
```groovy
environment {
    CERBERUS_DEBUG = 'true'
}
```

### Plugin Logs

Check Jenkins logs at:
- **System Log**: `Manage Jenkins` → `System Log`
- **Build Console**: Individual build console output
- **Plugin Log**: Look for `ai.cerberus.jenkins` entries

## 📈 Best Practices

### 1. **Staged Rollout**
```groovy
stage('Compliance - Quick Check') {
    steps {
        cerberusCompliance(
            mode: 'validate',
            frameworks: 'essential8',
            failOnViolations: false  // Don't block initially
        )
    }
}
```

### 2. **Framework Progression**
```groovy
// Start with one framework
frameworks: 'essential8'

// Add gradually
frameworks: 'essential8,nistcsf'

// Full enterprise coverage
frameworks: 'essential8,nistcsf,soc2,gdpr,iso27001'
```

### 3. **Environment-Specific Settings**
```groovy
script {
    def frameworks = env.BRANCH_NAME == 'main' ? 
        'essential8,nistcsf,soc2' :  // Production
        'essential8'                 // Development
        
    cerberusCompliance(frameworks: frameworks)
}
```

### 4. **Custom Notifications**
```groovy
post {
    always {
        script {
            def result = currentBuild.rawBuild.getAction(ai.cerberus.jenkins.CerberusComplianceAction.class)
            
            if (result?.humanReviewRequired) {
                slackSend(
                    channel: '#grc-team',
                    message: "🔱 Human review needed: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n" +
                            "Compliance Score: ${result.complianceScore}%\n" +
                            "Violations: ${result.violations.size()}"
                )
            }
        }
    }
}
```

## 🔗 Integration Examples

### With SonarQube
```groovy
stage('Quality & Compliance') {
    parallel {
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn sonar:sonar'
                }
            }
        }
        stage('Cerberus Compliance') {
            steps {
                cerberusCompliance(
                    frameworks: 'nistcsf,soc2',
                    mode: 'validate'
                )
            }
        }
    }
}
```

### With Docker
```groovy
stage('Container Compliance') {
    steps {
        script {
            // Build container
            docker.build("myapp:${env.BUILD_NUMBER}")
            
            // Check compliance
            cerberusCompliance(
                frameworks: 'essential8,nistcsf',
                mode: 'validate',
                severityThreshold: 'medium'
            )
        }
    }
}
```

### With Kubernetes
```groovy
stage('Deploy to K8s') {
    when {
        expression {
            // Only deploy if compliance passed
            def result = currentBuild.rawBuild.getAction(ai.cerberus.jenkins.CerberusComplianceAction.class)
            return result?.complianceScore >= 80
        }
    }
    steps {
        kubernetesDeploy(...)
    }
}
```

## 🆘 Support

- **Documentation**: [https://docs.cerberus-ai.com/jenkins](https://docs.cerberus-ai.com/jenkins)
- **Issues**: [GitHub Issues](https://github.com/cerberus-ai/jenkins-plugin/issues)
- **Community**: [Community Forum](https://community.cerberus-ai.com)
- **Enterprise Support**: support@cerberus-ai.com

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 🔱 About Cerberus AI

Cerberus AI is the three-headed guardian of enterprise compliance, providing unified intelligence across DevOps and GRC teams.

**One Intelligence. Two Interfaces. Complete Compliance.**