package ai.cerberus.jenkins;

import java.io.Serializable;

/**
 * Represents a compliance violation found during validation
 */
public class ComplianceViolation implements Serializable {
    
    public String ruleId;
    public String ruleName;
    public String title;
    public String description;
    public String severity;
    public String framework;
    public String category;
    public String message;
    public String filePath;
    public Integer lineNumber;
    public String remediation;
    
    public String getSeverityIcon() {
        switch (severity.toLowerCase()) {
            case "critical": return "🔴";
            case "high": return "🟠";
            case "medium": return "🟡";
            case "low": return "🔵";
            default: return "⚪";
        }
    }
    
    public String getSeverityClass() {
        switch (severity.toLowerCase()) {
            case "critical": return "violation-critical";
            case "high": return "violation-high";
            case "medium": return "violation-medium";
            case "low": return "violation-low";
            default: return "violation-unknown";
        }
    }
}