package ai.cerberus.jenkins;

import com.fasterxml.jackson.databind.JsonNode;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * Represents the result of a Cerberus AI compliance validation
 */
public class ComplianceResult implements Serializable {
    
    public int complianceScore;
    public List<ComplianceViolation> violations;
    public List<String> frameworksChecked;
    public boolean humanReviewRequired;
    public String reportUrl;
    
    public ComplianceResult() {
        this.violations = new ArrayList<>();
        this.frameworksChecked = new ArrayList<>();
    }
    
    public static ComplianceResult fromJson(JsonNode json) {
        ComplianceResult result = new ComplianceResult();
        
        result.complianceScore = json.path("compliance_score").asInt(0);
        result.humanReviewRequired = json.path("human_review_required").asBoolean(false);
        result.reportUrl = json.path("report_url").asText(null);
        
        // Parse frameworks checked
        JsonNode frameworksNode = json.path("frameworks_checked");
        if (frameworksNode.isArray()) {
            for (JsonNode framework : frameworksNode) {
                result.frameworksChecked.add(framework.asText());
            }
        }
        
        // Parse violations
        JsonNode violationsNode = json.path("violations");
        if (violationsNode.isArray()) {
            for (JsonNode violationNode : violationsNode) {
                ComplianceViolation violation = new ComplianceViolation();
                violation.ruleId = violationNode.path("rule_id").asText();
                violation.ruleName = violationNode.path("rule_name").asText();
                violation.title = violationNode.path("title").asText();
                violation.description = violationNode.path("description").asText();
                violation.severity = violationNode.path("severity").asText();
                violation.framework = violationNode.path("framework").asText();
                violation.category = violationNode.path("category").asText();
                violation.message = violationNode.path("message").asText();
                violation.filePath = violationNode.path("file_path").asText(null);
                violation.lineNumber = violationNode.path("line_number").asInt(0);
                violation.remediation = violationNode.path("remediation").asText(null);
                
                result.violations.add(violation);
            }
        }
        
        return result;
    }
}