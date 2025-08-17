package ai.cerberus.jenkins;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Represents the build context for compliance validation
 */
public class BuildContext implements Serializable {
    
    public String jobName;
    public int buildNumber;
    public String buildUrl;
    public String timestamp;
    public String workspace;
    public Map<String, String> environment;
    public List<String> changedFiles;
    public String jenkinsVersion;
    public String nodeLabel;
    
    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        
        Map<String, Object> jenkins = new HashMap<>();
        jenkins.put("job_name", jobName);
        jenkins.put("build_number", buildNumber);
        jenkins.put("build_url", buildUrl);
        jenkins.put("workspace", workspace);
        jenkins.put("jenkins_version", jenkinsVersion);
        jenkins.put("node_label", nodeLabel);
        
        Map<String, Object> build = new HashMap<>();
        build.put("timestamp", timestamp);
        build.put("files_changed", changedFiles);
        build.put("environment", environment);
        
        map.put("jenkins", jenkins);
        map.put("build", build);
        
        return map;
    }
}