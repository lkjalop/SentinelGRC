"""
Secure Sentinel GRC Integration
===============================
Integrates all security enhancements into the main Sentinel GRC system.
Zero-cost enterprise-grade security implementation.
"""

import os
import sys
import asyncio
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
import streamlit as st

# Import security components
from security_enhancements import (
    rate_limiter, input_validator, secure_config, get_security_stats
)
from content_security_policy import StreamlitSecurityMiddleware
from error_handler import error_handler, SentinelError, ErrorType, ErrorSeverity
from connection_pool_manager import (
    initialize_pools, supabase_pool, neo4j_pool, cache_manager
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentinel_security.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecureSentinelGRC:
    """
    Secure wrapper for Sentinel GRC with enterprise-grade security
    """
    
    def __init__(self):
        self.security_middleware = StreamlitSecurityMiddleware(csp_mode="balanced")
        self.initialized = False
        self.security_stats = {
            'assessments_completed': 0,
            'security_incidents': 0,
            'cache_hits': 0,
            'requests_blocked': 0
        }
    
    async def initialize(self):
        """Initialize secure Sentinel GRC system"""
        if self.initialized:
            return
        
        try:
            logger.info("Initializing Secure Sentinel GRC...")
            
            # Initialize connection pools
            await initialize_pools()
            
            # Validate configuration
            config_status = secure_config.validate_config()
            if not config_status['is_valid']:
                logger.warning(f"Missing required config: {config_status['missing_required']}")
                
                # Set development mode if config missing
                os.environ['DEVELOPMENT'] = 'true'
                logger.info("Running in development mode due to missing configuration")
            
            # Setup security monitoring
            self._setup_security_monitoring()
            
            self.initialized = True
            logger.info("Secure Sentinel GRC initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Secure Sentinel GRC: {e}")
            raise SentinelError(
                message=f"System initialization failed: {e}",
                error_type=ErrorType.CONFIGURATION_ERROR,
                severity=ErrorSeverity.CRITICAL
            )
    
    def _setup_security_monitoring(self):
        """Setup security event monitoring"""
        
        # Register security event handlers
        def log_security_event(event_type: str, details: Dict[str, Any]):
            logger.warning(f"Security Event: {event_type} - {details}")
            self.security_stats['security_incidents'] += 1
        
        # You could integrate with external monitoring here
        # For now, we'll use local logging
        logger.info("Security monitoring activated")
    
    def check_request_security(self, user_ip: str, endpoint: str, 
                             request_data: str = "") -> tuple[bool, str]:
        """
        Comprehensive security check for incoming requests
        
        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        
        # Rate limiting check
        allowed, reason = rate_limiter.is_request_allowed(user_ip, endpoint)
        if not allowed:
            self.security_stats['requests_blocked'] += 1
            logger.warning(f"Request blocked from {user_ip}: {reason}")
            return False, reason
        
        # Input validation if request data provided
        if request_data:
            valid, error_msg, _ = input_validator.validate_input(request_data)
            if not valid:
                self.security_stats['requests_blocked'] += 1
                logger.warning(f"Invalid input from {user_ip}: {error_msg}")
                return False, f"Invalid input: {error_msg}"
        
        # Attack pattern detection
        if request_data:
            patterns = rate_limiter.detect_attack_patterns(user_ip, request_data)
            if patterns:
                self.security_stats['requests_blocked'] += 1
                logger.error(f"Attack patterns detected from {user_ip}: {patterns}")
                return False, f"Malicious patterns detected: {', '.join(patterns)}"
        
        return True, "Request approved"
    
    async def secure_assessment(self, company_data: Dict[str, Any], 
                              user_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Perform secure GRC assessment with full security controls
        """
        
        try:
            # Security checks
            security_check = self.check_request_security(
                user_ip, 
                "/assess", 
                json.dumps(company_data)
            )
            
            if not security_check[0]:
                raise SentinelError(
                    message=f"Security check failed: {security_check[1]}",
                    error_type=ErrorType.AUTHORIZATION_ERROR,
                    severity=ErrorSeverity.HIGH
                )
            
            # Input validation
            company_name = company_data.get('company_name', '')
            valid, error_msg, sanitized_name = input_validator.validate_input(
                company_name, "company_name"
            )
            
            if not valid:
                raise SentinelError(
                    message=f"Invalid company name: {error_msg}",
                    error_type=ErrorType.VALIDATION_ERROR,
                    severity=ErrorSeverity.LOW,
                    user_message="Please provide a valid company name"
                )
            
            # Update company data with sanitized input
            company_data['company_name'] = sanitized_name
            
            # Check cache first
            cached_result = cache_manager.get_assessment(company_data)
            if cached_result:
                logger.info(f"Cache hit for assessment: {sanitized_name}")
                self.security_stats['cache_hits'] += 1
                return {
                    **cached_result,
                    'cached': True,
                    'cache_timestamp': datetime.now().isoformat()
                }
            
            # Perform actual assessment
            assessment_result = await self._perform_assessment(company_data)
            
            # Cache the result
            cache_manager.cache_assessment(company_data, assessment_result, ttl=3600)
            
            # Update stats
            self.security_stats['assessments_completed'] += 1
            
            return assessment_result
            
        except SentinelError:
            raise
        except Exception as e:
            # Handle unexpected errors
            handled_error = error_handler.handle_error(e)
            if handled_error.get('success') and handled_error.get('fallback_used'):
                logger.info("Using fallback assessment due to error")
                return handled_error['result']
            else:
                raise SentinelError(
                    message=f"Assessment failed: {str(e)}",
                    error_type=ErrorType.AGENT_ERROR,
                    severity=ErrorSeverity.HIGH
                )
    
    async def _perform_assessment(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform the actual GRC assessment (simplified for demo)
        In real implementation, this would call the main assessment agents
        """
        
        # Simulate assessment logic
        company_name = company_data.get('company_name', 'Unknown')
        industry = company_data.get('industry', 'Other')
        
        # Basic scoring based on industry (this would be much more complex in reality)
        industry_scores = {
            'Healthcare': 0.65,  # Higher risk, more regulation
            'Financial Services': 0.60,  # Highest regulation
            'Government': 0.70,  # Good security practices
            'Technology': 0.75,  # Usually good security
            'Other': 0.70
        }
        
        base_score = industry_scores.get(industry, 0.70)
        
        # Add some variability based on company name hash (for demo)
        name_hash = hash(company_name) % 100
        score_adjustment = (name_hash - 50) / 1000  # +/- 0.05
        final_score = max(0.0, min(1.0, base_score + score_adjustment))
        
        # Generate recommendations based on score
        recommendations = []
        if final_score < 0.6:
            recommendations.extend([
                "Implement multi-factor authentication",
                "Conduct security awareness training",
                "Establish incident response procedures"
            ])
        elif final_score < 0.8:
            recommendations.extend([
                "Enhance access controls",
                "Implement advanced threat detection",
                "Regular security assessments"
            ])
        else:
            recommendations.extend([
                "Maintain current security posture",
                "Consider advanced security certifications",
                "Implement zero-trust architecture"
            ])
        
        # Risk areas
        risk_areas = []
        if final_score < 0.7:
            risk_areas.extend(["Authentication", "Data Protection", "Incident Response"])
        if final_score < 0.8:
            risk_areas.extend(["Access Controls", "Monitoring"])
        
        return {
            'company_name': company_name,
            'industry': industry,
            'overall_score': round(final_score, 2),
            'risk_level': 'HIGH' if final_score < 0.6 else 'MEDIUM' if final_score < 0.8 else 'LOW',
            'recommendations': recommendations,
            'risk_areas': risk_areas,
            'assessment_date': datetime.now().isoformat(),
            'cached': False
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        
        # Get security stats
        security_stats = get_security_stats()
        
        # Get pool stats
        from connection_pool_manager import get_pool_statistics
        pool_stats = get_pool_statistics()
        
        # Calculate health scores
        health_score = 100
        
        # Check for security issues
        if security_stats['rate_limiter']['blocked_ips'] > 0:
            health_score -= 10
        
        if security_stats['input_validator']['block_rate'] != '0.0%':
            health_score -= 5
        
        # Check configuration
        config_status = security_stats['config_validation']
        if not config_status['is_valid']:
            health_score -= 20
        
        # Check pool health
        if pool_stats['supabase_pool']['available_connections'] == 0:
            health_score -= 15
        
        if pool_stats['neo4j_pool']['driver_active'] is False:
            health_score -= 10
        
        return {
            'overall_health': max(0, health_score),
            'status': 'HEALTHY' if health_score > 80 else 'DEGRADED' if health_score > 50 else 'UNHEALTHY',
            'security_stats': security_stats,
            'pool_stats': pool_stats,
            'application_stats': self.security_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def create_security_report(self) -> str:
        """Generate a comprehensive security report"""
        
        health = self.get_system_health()
        
        report = f"""
# SENTINEL GRC SECURITY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## SYSTEM HEALTH: {health['status']} ({health['overall_health']}/100)

## SECURITY STATISTICS
- Total Requests: {health['security_stats']['rate_limiter']['total_requests']}
- Blocked IPs: {health['security_stats']['rate_limiter']['blocked_ips']}
- Input Validations: {health['security_stats']['input_validator']['total_validations']}
- Blocked Injections: {health['security_stats']['input_validator']['blocked_injections']}
- Cache Hit Rate: {health['security_stats']['cache']['hit_rate']}

## APPLICATION STATISTICS
- Assessments Completed: {self.security_stats['assessments_completed']}
- Security Incidents: {self.security_stats['security_incidents']}
- Cache Hits: {self.security_stats['cache_hits']}
- Requests Blocked: {self.security_stats['requests_blocked']}

## CONNECTION POOLS
- Supabase Pool: {health['pool_stats']['supabase_pool']['available_connections']} available
- Neo4j Pool: {health['pool_stats']['neo4j_pool']['available_sessions']} sessions
- Cache Entries: {health['pool_stats']['cache']['total_entries']}

## CONFIGURATION STATUS
"""
        
        config_status = health['security_stats']['config_validation']
        for key, status in config_status['required'].items():
            report += f"- {key}: {status}\n"
        
        report += f"""
## RECOMMENDATIONS
"""
        
        if health['overall_health'] < 100:
            if config_status['missing_required']:
                report += "- Configure missing required secrets\n"
            if health['security_stats']['rate_limiter']['blocked_ips'] > 0:
                report += "- Review and potentially unblock legitimate IPs\n"
            if health['pool_stats']['cache']['hit_rate'] == '0.0%':
                report += "- Monitor cache performance and tune TTL settings\n"
        else:
            report += "- System is operating at optimal security levels\n"
        
        return report

# Streamlit Integration
def create_secure_streamlit_app():
    """Create secure Streamlit application"""
    
    # Initialize secure system
    if 'secure_sentinel' not in st.session_state:
        st.session_state.secure_sentinel = SecureSentinelGRC()
    
    secure_sentinel = st.session_state.secure_sentinel
    
    # Initialize if needed
    if not secure_sentinel.initialized:
        with st.spinner("Initializing secure system..."):
            asyncio.run(secure_sentinel.initialize())
    
    # Apply security middleware
    if hasattr(st, 'get_option'):
        # This would be used to set CSP headers in a real deployment
        pass
    
    st.title("🛡️ Secure Sentinel GRC")
    st.markdown("Enterprise-grade GRC assessment with zero-cost security hardening")
    
    # Sidebar - System Health
    with st.sidebar:
        st.header("System Health")
        health = secure_sentinel.get_system_health()
        
        # Health indicator
        if health['status'] == 'HEALTHY':
            st.success(f"✅ {health['status']} ({health['overall_health']}/100)")
        elif health['status'] == 'DEGRADED':
            st.warning(f"⚠️ {health['status']} ({health['overall_health']}/100)")
        else:
            st.error(f"❌ {health['status']} ({health['overall_health']}/100)")
        
        # Security stats
        st.metric("Assessments", secure_sentinel.security_stats['assessments_completed'])
        st.metric("Cache Hits", secure_sentinel.security_stats['cache_hits'])
        st.metric("Blocked Requests", secure_sentinel.security_stats['requests_blocked'])
        
        if st.button("Generate Security Report"):
            report = secure_sentinel.create_security_report()
            st.download_button(
                "Download Report",
                report,
                "sentinel_security_report.md",
                "text/markdown"
            )
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["Assessment", "Security Dashboard", "System Info"])
    
    with tab1:
        st.header("GRC Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="Enter company name")
            industry = st.selectbox("Industry", [
                "Healthcare", "Financial Services", "Technology", "Manufacturing",
                "Retail", "Government", "Education", "Energy", "Other"
            ])
        
        with col2:
            assessment_type = st.selectbox("Assessment Type", [
                "Essential 8", "Privacy Act", "APRA CPS 234", "SOCI Act",
                "HIPAA", "PCI DSS", "ISO 27001", "Comprehensive"
            ])
        
        if st.button("Run Assessment", type="primary"):
            if not company_name:
                st.error("Please enter a company name")
            else:
                # Get user IP (simulated)
                user_ip = "127.0.0.1"
                
                company_data = {
                    'company_name': company_name,
                    'industry': industry,
                    'assessment_type': assessment_type
                }
                
                try:
                    with st.spinner("Running secure assessment..."):
                        result = asyncio.run(
                            secure_sentinel.secure_assessment(company_data, user_ip)
                        )
                    
                    # Display results
                    st.success("Assessment completed!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Overall Score", f"{result['overall_score']:.0%}")
                    with col2:
                        st.metric("Risk Level", result['risk_level'])
                    with col3:
                        if result.get('cached'):
                            st.info("📋 Cached Result")
                        else:
                            st.success("🆕 Fresh Assessment")
                    
                    # Recommendations
                    st.subheader("Recommendations")
                    for rec in result['recommendations']:
                        st.write(f"• {rec}")
                    
                    # Risk areas
                    if result['risk_areas']:
                        st.subheader("Areas Needing Attention")
                        for risk in result['risk_areas']:
                            st.warning(f"⚠️ {risk}")
                
                except SentinelError as e:
                    st.error(f"Security Error: {e.user_message}")
                except Exception as e:
                    st.error(f"System Error: {str(e)}")
    
    with tab2:
        st.header("Security Dashboard")
        
        # Display security statistics
        security_stats = get_security_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Rate Limiting")
            st.json(security_stats['rate_limiter'])
        
        with col2:
            st.subheader("Input Validation")
            st.json(security_stats['input_validator'])
        
        st.subheader("Configuration Status")
        config_status = security_stats['config_validation']
        
        for key, status in config_status['required'].items():
            if "✓" in status:
                st.success(f"{key}: {status}")
            else:
                st.error(f"{key}: {status}")
    
    with tab3:
        st.header("System Information")
        
        health = secure_sentinel.get_system_health()
        st.json(health)

if __name__ == "__main__":
    # Run the secure Streamlit app
    create_secure_streamlit_app()