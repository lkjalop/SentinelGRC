"""
Sentinel GRC Security Hardening Plan
====================================
Comprehensive security implementation for production deployment.
"""

import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
import re
from functools import wraps
import streamlit as st

logger = logging.getLogger(__name__)

# =============================================================================
# AUTHENTICATION & AUTHORIZATION
# =============================================================================

class SecurityManager:
    """Handles authentication, authorization, and security controls"""
    
    def __init__(self):
        self.secret_key = self._get_secret_key()
        self.failed_attempts = {}  # IP -> count
        self.session_tokens = {}   # token -> user_data
        
    def _get_secret_key(self) -> str:
        """Get or generate secure secret key"""
        import os
        key = os.getenv('JWT_SECRET_KEY')
        if not key:
            # Generate secure random key
            key = secrets.token_urlsafe(32)
            logger.warning("Generated temporary JWT key - set JWT_SECRET_KEY in production")
        return key
    
    def authenticate_user(self, username: str, password: str, client_ip: str) -> Dict[str, Any]:
        """Authenticate user with rate limiting"""
        
        # Rate limiting check
        if self._is_rate_limited(client_ip):
            return {"success": False, "error": "Too many failed attempts. Try again later."}
        
        # Simple demo authentication (replace with real auth)
        valid_users = {
            "admin": {"password": "sentinel_grc_2024!", "role": "admin"},
            "auditor": {"password": "audit_read_only", "role": "auditor"},
            "analyst": {"password": "analyst_assess", "role": "analyst"}
        }
        
        if username in valid_users and self._verify_password(password, valid_users[username]["password"]):
            # Reset failed attempts
            self.failed_attempts.pop(client_ip, None)
            
            # Generate JWT token
            token = self._generate_jwt_token({
                "username": username,
                "role": valid_users[username]["role"],
                "login_time": datetime.utcnow().isoformat()
            })
            
            return {
                "success": True,
                "token": token,
                "role": valid_users[username]["role"],
                "username": username
            }
        else:
            # Record failed attempt
            self.failed_attempts[client_ip] = self.failed_attempts.get(client_ip, 0) + 1
            return {"success": False, "error": "Invalid credentials"}
    
    def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if IP is rate limited (5 failed attempts)"""
        return self.failed_attempts.get(client_ip, 0) >= 5
    
    def _verify_password(self, provided: str, stored: str) -> bool:
        """Verify password (use proper hashing in production)"""
        # In production, use bcrypt or similar:
        # return bcrypt.checkpw(provided.encode('utf-8'), stored.encode('utf-8'))
        return provided == stored  # Demo only!
    
    def _generate_jwt_token(self, payload: Dict[str, Any]) -> str:
        """Generate JWT token"""
        payload['exp'] = datetime.utcnow() + timedelta(hours=8)  # 8-hour expiry
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {"valid": True, "user": payload}
        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"valid": False, "error": "Invalid token"}

def require_auth(required_role: str = None):
    """Decorator for requiring authentication"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if user is authenticated in Streamlit session
            if 'authenticated' not in st.session_state or not st.session_state.authenticated:
                st.error("🔒 Authentication required")
                st.stop()
            
            # Check role if specified
            if required_role:
                user_role = st.session_state.get('user_role', '')
                if user_role != required_role and user_role != 'admin':
                    st.error(f"🚫 Access denied. Required role: {required_role}")
                    st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# =============================================================================
# INPUT VALIDATION & SANITIZATION
# =============================================================================

class InputValidator:
    """Validates and sanitizes user inputs"""
    
    @staticmethod
    def validate_company_name(name: str) -> Dict[str, Any]:
        """Validate company name"""
        if not name or len(name.strip()) < 2:
            return {"valid": False, "error": "Company name must be at least 2 characters"}
        
        if len(name) > 100:
            return {"valid": False, "error": "Company name too long (max 100 characters)"}
        
        # Check for suspicious patterns
        if re.search(r'[<>"\'\&]', name):
            return {"valid": False, "error": "Company name contains invalid characters"}
        
        return {"valid": True, "sanitized": name.strip()}
    
    @staticmethod
    def validate_employee_count(count: int) -> Dict[str, Any]:
        """Validate employee count"""
        if not isinstance(count, int) or count < 1:
            return {"valid": False, "error": "Employee count must be a positive integer"}
        
        if count > 1000000:  # 1 million max
            return {"valid": False, "error": "Employee count seems unrealistic"}
        
        return {"valid": True, "sanitized": count}
    
    @staticmethod
    def validate_industry(industry: str) -> Dict[str, Any]:
        """Validate industry selection"""
        valid_industries = [
            "Healthcare", "Finance", "Banking", "Insurance", "Superannuation",
            "Technology", "Education", "Government", "Energy", "Telecommunications",
            "Transport", "Water", "Defence", "Manufacturing", "Retail", "Other"
        ]
        
        if industry not in valid_industries:
            return {"valid": False, "error": "Invalid industry selection"}
        
        return {"valid": True, "sanitized": industry}
    
    @staticmethod
    def sanitize_text_input(text: str, max_length: int = 1000) -> str:
        """Sanitize general text input"""
        if not text:
            return ""
        
        # Remove potential XSS patterns
        text = re.sub(r'[<>"\'\&]', '', text)
        
        # Limit length
        text = text[:max_length]
        
        return text.strip()

# =============================================================================
# AUDIT LOGGING
# =============================================================================

class SecurityAuditLogger:
    """Logs security events and user actions"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup security audit logging"""
        import os
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Configure security logger
        security_logger = logging.getLogger('security_audit')
        security_logger.setLevel(logging.INFO)
        
        # File handler for security events
        handler = logging.FileHandler('logs/security_audit.log')
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S UTC'
        )
        handler.setFormatter(formatter)
        security_logger.addHandler(handler)
        
        self.logger = security_logger
    
    def log_login_attempt(self, username: str, client_ip: str, success: bool):
        """Log login attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"LOGIN_{status} | User: {username} | IP: {client_ip}")
    
    def log_assessment_access(self, username: str, company_name: str, client_ip: str):
        """Log assessment access"""
        self.logger.info(f"ASSESSMENT_ACCESS | User: {username} | Company: {company_name} | IP: {client_ip}")
    
    def log_data_export(self, username: str, data_type: str, client_ip: str):
        """Log data export"""
        self.logger.info(f"DATA_EXPORT | User: {username} | Type: {data_type} | IP: {client_ip}")
    
    def log_security_event(self, event_type: str, details: str, client_ip: str):
        """Log general security event"""
        self.logger.warning(f"SECURITY_EVENT | Type: {event_type} | Details: {details} | IP: {client_ip}")

# =============================================================================
# DATA ENCRYPTION
# =============================================================================

class DataEncryption:
    """Handles sensitive data encryption"""
    
    def __init__(self):
        self.key = self._get_encryption_key()
    
    def _get_encryption_key(self) -> bytes:
        """Get or generate encryption key"""
        import os
        from cryptography.fernet import Fernet
        
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key().decode()
            logger.warning("Generated temporary encryption key - set ENCRYPTION_KEY in production")
        
        return key.encode()
    
    def encrypt_sensitive_data(self, data: Dict[str, Any]) -> str:
        """Encrypt sensitive assessment data"""
        from cryptography.fernet import Fernet
        import json
        
        f = Fernet(self.key)
        
        # Convert to JSON and encrypt
        json_data = json.dumps(data, default=str)
        encrypted_data = f.encrypt(json_data.encode())
        
        return encrypted_data.decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt sensitive assessment data"""
        from cryptography.fernet import Fernet
        import json
        
        f = Fernet(self.key)
        
        # Decrypt and parse JSON
        decrypted_data = f.decrypt(encrypted_data.encode())
        return json.loads(decrypted_data.decode())

# =============================================================================
# SECURITY MIDDLEWARE FOR STREAMLIT
# =============================================================================

def init_security_middleware():
    """Initialize security middleware for Streamlit"""
    
    # Initialize security components
    if 'security_manager' not in st.session_state:
        st.session_state.security_manager = SecurityManager()
        st.session_state.audit_logger = SecurityAuditLogger()
        st.session_state.input_validator = InputValidator()
        st.session_state.data_encryption = DataEncryption()
    
    # Check authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    return {
        'security_manager': st.session_state.security_manager,
        'audit_logger': st.session_state.audit_logger,
        'input_validator': st.session_state.input_validator,
        'data_encryption': st.session_state.data_encryption
    }

def render_login_page():
    """Render secure login page"""
    
    st.markdown("# 🔐 Sentinel GRC - Secure Login")
    
    security_components = init_security_middleware()
    security_manager = security_components['security_manager']
    audit_logger = security_components['audit_logger']
    
    with st.form("login_form"):
        st.markdown("### Authentication Required")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if username and password:
                # Get client IP (simplified for demo)
                client_ip = "127.0.0.1"  # In production, extract real IP
                
                # Attempt authentication
                auth_result = security_manager.authenticate_user(username, password, client_ip)
                
                # Log attempt
                audit_logger.log_login_attempt(username, client_ip, auth_result["success"])
                
                if auth_result["success"]:
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = auth_result["role"]
                    st.session_state.jwt_token = auth_result["token"]
                    
                    st.success(f"✅ Login successful! Role: {auth_result['role']}")
                    st.rerun()
                else:
                    st.error(f"❌ {auth_result['error']}")
            else:
                st.error("Please enter both username and password")
    
    # Demo credentials info
    st.markdown("---")
    st.markdown("### Demo Credentials:")
    st.code("""
    Admin:   admin / sentinel_grc_2024!
    Auditor: auditor / audit_read_only  
    Analyst: analyst / analyst_assess
    """)

# =============================================================================
# PRODUCTION SECURITY CHECKLIST
# =============================================================================

SECURITY_CHECKLIST = """
PRODUCTION SECURITY CHECKLIST
=============================

🔒 AUTHENTICATION & AUTHORIZATION
☐ Implement proper password hashing (bcrypt/scrypt)
☐ Add multi-factor authentication (MFA)
☐ Set up session management with secure cookies
☐ Implement role-based access control (RBAC)
☐ Add OAuth integration (Google/Microsoft)

🛡️ INPUT VALIDATION & SANITIZATION  
☐ Validate all user inputs server-side
☐ Implement XSS protection
☐ Add CSRF protection
☐ Sanitize file uploads
☐ Rate limit API endpoints

🔐 DATA PROTECTION
☐ Encrypt sensitive data at rest
☐ Implement secure key management
☐ Add database encryption
☐ Set up automated backups
☐ Implement data retention policies

📊 MONITORING & LOGGING
☐ Set up comprehensive audit logging
☐ Implement intrusion detection
☐ Add performance monitoring
☐ Set up security alerting
☐ Regular security scans

🌐 INFRASTRUCTURE SECURITY
☐ Configure HTTPS/TLS properly
☐ Set up web application firewall (WAF)
☐ Implement network segmentation
☐ Regular security updates
☐ Container security scanning

📋 COMPLIANCE & GOVERNANCE
☐ GDPR compliance implementation
☐ Data processing agreements
☐ Privacy policy and terms
☐ Regular security audits
☐ Incident response plan
"""

def generate_security_report() -> str:
    """Generate security status report"""
    
    current_status = {
        "Authentication": "🟡 Basic demo auth implemented",
        "Authorization": "🟡 Role-based access partial", 
        "Input Validation": "🟡 Basic validation added",
        "Data Encryption": "🟡 Framework implemented",
        "Audit Logging": "✅ Comprehensive logging ready",
        "Rate Limiting": "🔴 Not implemented",
        "HTTPS/TLS": "🔴 Development mode only",
        "Database Security": "🟡 Basic RLS in Supabase",
        "API Security": "🔴 No API authentication",
        "Monitoring": "🔴 No security monitoring"
    }
    
    report = "SENTINEL GRC SECURITY STATUS REPORT\n"
    report += "=" * 40 + "\n\n"
    
    for component, status in current_status.items():
        report += f"{component}: {status}\n"
    
    report += f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "\nLegend: ✅ Complete  🟡 Partial  🔴 Missing\n"
    
    return report

if __name__ == "__main__":
    print(SECURITY_CHECKLIST)
    print("\n" + generate_security_report())