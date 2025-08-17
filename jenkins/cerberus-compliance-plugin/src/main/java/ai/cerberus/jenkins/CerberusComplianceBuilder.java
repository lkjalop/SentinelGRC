package ai.cerberus.jenkins;

import com.cloudbees.plugins.credentials.CredentialsProvider;
import com.cloudbees.plugins.credentials.common.StandardListBoxModel;
import com.cloudbees.plugins.credentials.common.StandardUsernamePasswordCredentials;
import com.cloudbees.plugins.credentials.domains.DomainRequirement;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import hudson.Extension;
import hudson.FilePath;
import hudson.Launcher;
import hudson.model.*;
import hudson.security.ACL;
import hudson.tasks.BuildStepDescriptor;
import hudson.tasks.Builder;
import hudson.util.FormValidation;
import hudson.util.ListBoxModel;
import jenkins.model.Jenkins;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.jenkinsci.Symbol;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.stapler.DataBoundSetter;
import org.kohsuke.stapler.QueryParameter;
import org.kohsuke.stapler.verb.POST;

import javax.annotation.Nonnull;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Cerberus AI Compliance Builder for Jenkins
 * Integrates compliance validation into Jenkins build pipelines
 */
public class CerberusComplianceBuilder extends Builder {

    private String serverUrl;
    private String credentialsId;
    private String frameworks;
    private String severityThreshold;
    private String mode;
    private String outputFormat;
    private boolean failOnViolations;
    private String humanReviewThreshold;
    private boolean publishResults;

    @DataBoundConstructor
    public CerberusComplianceBuilder(String serverUrl, String credentialsId) {
        this.serverUrl = serverUrl;
        this.credentialsId = credentialsId;
        
        // Set defaults
        this.frameworks = "essential8";
        this.severityThreshold = "medium";
        this.mode = "validate";
        this.outputFormat = "json";
        this.failOnViolations = true;
        this.humanReviewThreshold = "high";
        this.publishResults = true;
    }

    // Getters and Setters
    public String getServerUrl() { return serverUrl; }
    public String getCredentialsId() { return credentialsId; }
    public String getFrameworks() { return frameworks; }
    public String getSeverityThreshold() { return severityThreshold; }
    public String getMode() { return mode; }
    public String getOutputFormat() { return outputFormat; }
    public boolean isFailOnViolations() { return failOnViolations; }
    public String getHumanReviewThreshold() { return humanReviewThreshold; }
    public boolean isPublishResults() { return publishResults; }

    @DataBoundSetter
    public void setFrameworks(String frameworks) {
        this.frameworks = frameworks;
    }

    @DataBoundSetter
    public void setSeverityThreshold(String severityThreshold) {
        this.severityThreshold = severityThreshold;
    }

    @DataBoundSetter
    public void setMode(String mode) {
        this.mode = mode;
    }

    @DataBoundSetter
    public void setOutputFormat(String outputFormat) {
        this.outputFormat = outputFormat;
    }

    @DataBoundSetter
    public void setFailOnViolations(boolean failOnViolations) {
        this.failOnViolations = failOnViolations;
    }

    @DataBoundSetter
    public void setHumanReviewThreshold(String humanReviewThreshold) {
        this.humanReviewThreshold = humanReviewThreshold;
    }

    @DataBoundSetter
    public void setPublishResults(boolean publishResults) {
        this.publishResults = publishResults;
    }

    @Override
    public boolean perform(AbstractBuild<?, ?> build, Launcher launcher, BuildListener listener)
            throws InterruptedException, IOException {
        
        listener.getLogger().println("🔱 Starting Cerberus AI Compliance Validation");
        
        try {
            // Collect build context
            BuildContext context = collectBuildContext(build, listener);
            
            // Perform compliance validation
            ComplianceResult result = performComplianceValidation(context, listener);
            
            // Process and publish results
            processResults(build, result, listener);
            
            // Determine build status
            return evaluateBuildStatus(result, listener);
            
        } catch (Exception e) {
            listener.getLogger().println("❌ Cerberus AI validation failed: " + e.getMessage());
            e.printStackTrace(listener.getLogger());
            return false;
        }
    }

    private BuildContext collectBuildContext(AbstractBuild<?, ?> build, BuildListener listener) throws IOException {
        listener.getLogger().println("📊 Collecting build context...");
        
        BuildContext context = new BuildContext();
        context.jobName = build.getProject().getName();
        context.buildNumber = build.getNumber();
        context.buildUrl = build.getUrl();
        context.timestamp = Instant.now().toString();
        context.workspace = build.getWorkspace().getRemote();
        
        // Collect environment variables
        context.environment = build.getEnvironment(listener);
        
        // Collect changed files (simplified for demo)
        context.changedFiles = collectChangedFiles(build, listener);
        
        // Add Jenkins-specific metadata
        context.jenkinsVersion = Jenkins.getVersion().toString();
        context.nodeLabel = build.getBuiltOnStr();
        
        listener.getLogger().println("📊 Build context collected: " + context.jobName + " #" + context.buildNumber);
        
        return context;
    }

    private List<String> collectChangedFiles(AbstractBuild<?, ?> build, BuildListener listener) {
        List<String> changedFiles = new ArrayList<>();
        
        try {
            // Get files from workspace (simplified approach)
            FilePath workspace = build.getWorkspace();
            if (workspace != null) {
                // Collect common source files
                String[] patterns = {"**/*.java", "**/*.py", "**/*.js", "**/*.ts", "**/*.yml", "**/*.yaml", "**/*.json"};
                
                for (String pattern : patterns) {
                    List<FilePath> files = workspace.list(pattern);
                    changedFiles.addAll(files.stream()
                            .limit(50) // Limit to prevent payload bloat
                            .map(f -> f.getRemote())
                            .collect(Collectors.toList()));
                }
            }
        } catch (Exception e) {
            listener.getLogger().println("⚠️ Could not collect changed files: " + e.getMessage());
        }
        
        return changedFiles;
    }

    private ComplianceResult performComplianceValidation(BuildContext context, BuildListener listener) throws IOException {
        listener.getLogger().println("🔍 Performing compliance validation...");
        listener.getLogger().println("   Server: " + serverUrl);
        listener.getLogger().println("   Frameworks: " + frameworks);
        listener.getLogger().println("   Mode: " + mode);
        
        // Get API credentials
        String apiKey = getApiKey(listener);
        if (apiKey == null) {
            throw new IOException("Could not retrieve API credentials");
        }
        
        // Build request payload
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> payload = new HashMap<>();
        payload.put("context", context.toMap());
        payload.put("frameworks", Arrays.asList(frameworks.split(",")));
        payload.put("mode", mode);
        
        Map<String, Object> options = new HashMap<>();
        options.put("severity_threshold", severityThreshold);
        options.put("human_review_threshold", humanReviewThreshold);
        options.put("include_suggestions", true);
        options.put("include_evidence", true);
        payload.put("options", options);
        
        String jsonPayload = mapper.writeValueAsString(payload);
        
        // Make API call
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost request = new HttpPost(serverUrl + "/api/v1/compliance/jenkins-validate");
            request.setHeader("Authorization", "Bearer " + apiKey);
            request.setHeader("Content-Type", "application/json");
            request.setHeader("User-Agent", "Cerberus-AI-Jenkins-Plugin/1.0");
            
            request.setEntity(new StringEntity(jsonPayload));
            
            HttpResponse response = httpClient.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());
            
            if (response.getStatusLine().getStatusCode() != 200) {
                throw new IOException("API request failed: " + response.getStatusLine().getStatusCode() + " - " + responseBody);
            }
            
            JsonNode responseJson = mapper.readTree(responseBody);
            return ComplianceResult.fromJson(responseJson);
            
        } catch (Exception e) {
            listener.getLogger().println("❌ API request failed: " + e.getMessage());
            throw new IOException("Compliance validation failed", e);
        }
    }

    private String getApiKey(BuildListener listener) {
        try {
            StandardUsernamePasswordCredentials credentials = CredentialsProvider.findCredentialById(
                credentialsId,
                StandardUsernamePasswordCredentials.class,
                Jenkins.get(),
                ACL.SYSTEM,
                Collections.emptyList()
            );
            
            if (credentials != null) {
                return credentials.getPassword().getPlainText();
            }
        } catch (Exception e) {
            listener.getLogger().println("⚠️ Could not retrieve credentials: " + e.getMessage());
        }
        
        return null;
    }

    private void processResults(AbstractBuild<?, ?> build, ComplianceResult result, BuildListener listener) throws IOException {
        listener.getLogger().println("📊 Processing compliance results...");
        listener.getLogger().println("   Compliance Score: " + result.complianceScore + "/100");
        listener.getLogger().println("   Violations Found: " + result.violations.size());
        listener.getLogger().println("   Human Review Required: " + result.humanReviewRequired);
        
        // Log violations by severity
        if (!result.violations.isEmpty()) {
            Map<String, Long> violationsBySeverity = result.violations.stream()
                .collect(Collectors.groupingBy(v -> v.severity, Collectors.counting()));
            
            listener.getLogger().println("📋 Violations by severity:");
            violationsBySeverity.forEach((severity, count) -> 
                listener.getLogger().println("   " + getSeverityIcon(severity) + " " + severity + ": " + count));
        }
        
        // Save results to workspace
        if (publishResults) {
            saveResultsToWorkspace(build, result, listener);
        }
        
        // Add build action for UI display
        build.addAction(new CerberusComplianceAction(result));
    }

    private void saveResultsToWorkspace(AbstractBuild<?, ?> build, ComplianceResult result, BuildListener listener) throws IOException {
        FilePath workspace = build.getWorkspace();
        if (workspace == null) return;
        
        FilePath reportsDir = workspace.child("cerberus-reports");
        reportsDir.mkdirs();
        
        ObjectMapper mapper = new ObjectMapper();
        
        // Save JSON report
        if ("json".equals(outputFormat) || "all".equals(outputFormat)) {
            FilePath jsonReport = reportsDir.child("compliance-report.json");
            jsonReport.write(mapper.writeValueAsString(result), "UTF-8");
            listener.getLogger().println("📄 JSON report saved: " + jsonReport.getRemote());
        }
        
        // Save summary report
        FilePath summaryReport = reportsDir.child("compliance-summary.md");
        summaryReport.write(generateMarkdownReport(result), "UTF-8");
        listener.getLogger().println("📝 Summary report saved: " + summaryReport.getRemote());
    }

    private String generateMarkdownReport(ComplianceResult result) {
        StringBuilder report = new StringBuilder();
        
        report.append("# 🔱 Cerberus AI - Jenkins Compliance Report\n\n");
        report.append("**Overall Score:** ").append(result.complianceScore).append("/100\n");
        report.append("**Frameworks Checked:** ").append(String.join(", ", result.frameworksChecked)).append("\n");
        report.append("**Human Review Required:** ").append(result.humanReviewRequired ? "⚠️ Yes" : "✅ No").append("\n");
        report.append("**Generated:** ").append(Instant.now()).append("\n\n");
        
        if (!result.violations.isEmpty()) {
            report.append("## 🚨 Violations Found (").append(result.violations.size()).append(")\n\n");
            
            int index = 1;
            for (ComplianceViolation violation : result.violations) {
                String icon = getSeverityIcon(violation.severity);
                report.append("### ").append(index++).append(". ").append(icon).append(" ").append(violation.title).append("\n");
                report.append("**Severity:** ").append(violation.severity).append("\n");
                report.append("**Framework:** ").append(violation.framework).append("\n");
                report.append("**Description:** ").append(violation.description).append("\n");
                
                if (violation.remediation != null && !violation.remediation.isEmpty()) {
                    report.append("**Remediation:** ").append(violation.remediation).append("\n");
                }
                
                if (violation.filePath != null && !violation.filePath.isEmpty()) {
                    report.append("**File:** `").append(violation.filePath).append("`");
                    if (violation.lineNumber != null && violation.lineNumber > 0) {
                        report.append(":").append(violation.lineNumber);
                    }
                    report.append("\n");
                }
                
                report.append("\n");
            }
        } else {
            report.append("## ✅ No Violations Found\n\nAll compliance checks passed successfully!\n\n");
        }
        
        if (result.humanReviewRequired) {
            report.append("## 👥 Human Review Required\n\n");
            report.append("This assessment requires human expertise for:\n");
            report.append("- Complex regulatory interpretation\n");
            report.append("- Strategic risk assessment\n");
            report.append("- Business context evaluation\n\n");
            report.append("Please review the detailed report and provide expert guidance.\n\n");
        }
        
        report.append("---\n");
        report.append("*Generated by Cerberus AI - Jenkins Plugin v1.0*\n");
        
        return report.toString();
    }

    private String getSeverityIcon(String severity) {
        switch (severity.toLowerCase()) {
            case "critical": return "🔴";
            case "high": return "🟠";
            case "medium": return "🟡";
            case "low": return "🔵";
            default: return "⚪";
        }
    }

    private boolean evaluateBuildStatus(ComplianceResult result, BuildListener listener) {
        if (!failOnViolations) {
            listener.getLogger().println("✅ Build continuing despite violations (failOnViolations=false)");
            return true;
        }
        
        if (result.violations.isEmpty()) {
            listener.getLogger().println("✅ Compliance validation passed - no violations found");
            return true;
        }
        
        // Check if any violations meet the severity threshold
        String[] severityOrder = {"low", "medium", "high", "critical"};
        int thresholdIndex = Arrays.asList(severityOrder).indexOf(severityThreshold.toLowerCase());
        
        boolean hasFailingViolations = result.violations.stream()
            .anyMatch(violation -> {
                int violationIndex = Arrays.asList(severityOrder).indexOf(violation.severity.toLowerCase());
                return violationIndex >= thresholdIndex;
            });
        
        if (hasFailingViolations) {
            listener.getLogger().println("❌ Build failed due to compliance violations at or above " + severityThreshold + " severity");
            return false;
        } else {
            listener.getLogger().println("✅ Build passed - no violations at or above " + severityThreshold + " threshold");
            return true;
        }
    }

    @Symbol("cerberusCompliance")
    @Extension
    public static final class DescriptorImpl extends BuildStepDescriptor<Builder> {

        @Override
        public boolean isApplicable(Class<? extends AbstractProject> aClass) {
            return true;
        }

        @Override
        public String getDisplayName() {
            return "🔱 Cerberus AI Compliance Check";
        }

        @POST
        public FormValidation doCheckServerUrl(@QueryParameter String value) {
            if (value == null || value.trim().isEmpty()) {
                return FormValidation.error("Server URL is required");
            }
            
            if (!value.startsWith("http://") && !value.startsWith("https://")) {
                return FormValidation.error("Server URL must start with http:// or https://");
            }
            
            return FormValidation.ok();
        }

        @POST
        public FormValidation doTestConnection(@QueryParameter String serverUrl, @QueryParameter String credentialsId) {
            if (serverUrl == null || serverUrl.trim().isEmpty()) {
                return FormValidation.error("Please enter a server URL");
            }
            
            try {
                // Test connection to health endpoint
                try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
                    HttpPost request = new HttpPost(serverUrl + "/api/v1/health");
                    request.setHeader("User-Agent", "Cerberus-AI-Jenkins-Plugin/1.0");
                    
                    HttpResponse response = httpClient.execute(request);
                    
                    if (response.getStatusLine().getStatusCode() == 200) {
                        return FormValidation.ok("✅ Connection successful");
                    } else {
                        return FormValidation.error("Connection failed: " + response.getStatusLine().getStatusCode());
                    }
                }
            } catch (Exception e) {
                return FormValidation.error("Connection failed: " + e.getMessage());
            }
        }

        public ListBoxModel doFillCredentialsIdItems(@QueryParameter String serverUrl) {
            return new StandardListBoxModel()
                .includeEmptyValue()
                .includeAs(ACL.SYSTEM, Jenkins.get(), StandardUsernamePasswordCredentials.class,
                    Collections.emptyList());
        }

        public ListBoxModel doFillFrameworksItems() {
            return new ListBoxModel(
                new ListBoxModel.Option("Essential 8", "essential8"),
                new ListBoxModel.Option("NIST Cybersecurity Framework", "nistcsf"),
                new ListBoxModel.Option("SOC 2", "soc2"),
                new ListBoxModel.Option("GDPR", "gdpr"),
                new ListBoxModel.Option("ISO 27001", "iso27001"),
                new ListBoxModel.Option("Multiple Frameworks", "essential8,nistcsf,soc2")
            );
        }

        public ListBoxModel doFillSeverityThresholdItems() {
            return new ListBoxModel(
                new ListBoxModel.Option("Low", "low"),
                new ListBoxModel.Option("Medium", "medium"),
                new ListBoxModel.Option("High", "high"),
                new ListBoxModel.Option("Critical", "critical")
            );
        }

        public ListBoxModel doFillModeItems() {
            return new ListBoxModel(
                new ListBoxModel.Option("Validate", "validate"),
                new ListBoxModel.Option("Audit", "audit"),
                new ListBoxModel.Option("Monitor", "monitor")
            );
        }

        public ListBoxModel doFillOutputFormatItems() {
            return new ListBoxModel(
                new ListBoxModel.Option("JSON", "json"),
                new ListBoxModel.Option("Summary", "summary"),
                new ListBoxModel.Option("All Formats", "all")
            );
        }

        public ListBoxModel doFillHumanReviewThresholdItems() {
            return new ListBoxModel(
                new ListBoxModel.Option("Low", "low"),
                new ListBoxModel.Option("Medium", "medium"),
                new ListBoxModel.Option("High", "high")
            );
        }
    }
}