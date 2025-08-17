package ai.cerberus.jenkins;

import hudson.model.Action;
import hudson.model.Run;

import java.util.List;

/**
 * Jenkins Action to display Cerberus AI compliance results in the build UI
 */
public class CerberusComplianceAction implements Action {
    
    private final ComplianceResult result;
    private final Run<?, ?> build;
    
    public CerberusComplianceAction(ComplianceResult result) {
        this.result = result;
        this.build = null;
    }
    
    public CerberusComplianceAction(ComplianceResult result, Run<?, ?> build) {
        this.result = result;
        this.build = build;
    }

    @Override
    public String getIconFileName() {
        return "plugin/cerberus-compliance-plugin/icons/cerberus-24x24.png";
    }

    @Override
    public String getDisplayName() {
        return "🔱 Cerberus AI Compliance";
    }

    @Override
    public String getUrlName() {
        return "cerberus-compliance";
    }
    
    // Getters for Jelly templates
    public ComplianceResult getResult() {
        return result;
    }
    
    public Run<?, ?> getBuild() {
        return build;
    }
    
    public int getComplianceScore() {
        return result != null ? result.complianceScore : 0;
    }
    
    public List<String> getFrameworksChecked() {
        return result != null ? result.frameworksChecked : null;
    }
    
    public List<ComplianceViolation> getViolations() {
        return result != null ? result.violations : null;
    }
    
    public boolean isHumanReviewRequired() {
        return result != null && result.humanReviewRequired;
    }
    
    public String getScoreColor() {
        if (result == null) return "gray";
        
        int score = result.complianceScore;
        if (score >= 90) return "green";
        if (score >= 80) return "yellow";
        if (score >= 70) return "orange";
        return "red";
    }
    
    public String getScoreIcon() {
        if (result == null) return "⚪";
        
        int score = result.complianceScore;
        if (score >= 90) return "✅";
        if (score >= 80) return "🟡";
        if (score >= 70) return "🟠";
        return "🔴";
    }
    
    public long getCriticalViolations() {
        return getViolationsBySeverity("critical");
    }
    
    public long getHighViolations() {
        return getViolationsBySeverity("high");
    }
    
    public long getMediumViolations() {
        return getViolationsBySeverity("medium");
    }
    
    public long getLowViolations() {
        return getViolationsBySeverity("low");
    }
    
    private long getViolationsBySeverity(String severity) {
        if (result == null || result.violations == null) return 0;
        
        return result.violations.stream()
            .filter(v -> severity.equalsIgnoreCase(v.severity))
            .count();
    }
}