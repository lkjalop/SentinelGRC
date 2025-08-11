"""
Security Utilities for Sentinel GRC
====================================
Basic security hardening for production deployment.
"""

import re
import html
import hashlib
import secrets
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class InputValidator:
    """Input validation and sanitization"""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 1000) -> str:
        """Sanitize text input to prevent XSS and injection attacks"""
        if not text:
            return ""
        
        # Remove any null bytes
        text = text.replace('\x00', '')
        
        # HTML escape
        text = html.escape(text)
        
        # Limit length
        text = text[:max_length]
        
        # Remove dangerous patterns
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe.*?>.*?</iframe>',
            r'eval\s*\(',
            r'expression\s*\('
        ]
        
        for pattern in dangerous_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_company_name(name: str) -> bool:
        """Validate company name"""
        if not name or len(name) < 2 or len(name) > 200:
            return False
        
        # Allow letters, numbers, spaces, and common business characters
        pattern = r'^[a-zA-Z0-9\s\-\.\,\&\'\"]+$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def validate_employee_count(count: Any) -> bool:
        """Validate employee count"""
        try:
            count = int(count)
            return 1 <= count <= 10000000  # Max 10 million employees
        except:
            return False
    
    @staticmethod
    def validate_industry(industry: str) -> bool:
        """Validate industry selection"""
        valid_industries = [
            "Healthcare", "Financial Services", "Technology", "Manufacturing",
            "Retail", "Government", "Education", "Energy", "Telecommunications",
            "Transportation", "Construction", "Agriculture", "Mining",
            "Professional Services", "Non-profit", "Other"
        ]
        return industry in valid_industries
    
    @staticmethod
    def sanitize_controls_list(controls: List[str]) -> List[str]:
        """Sanitize list of control IDs"""
        if not controls:
            return []
        
        # Valid control ID pattern
        pattern = r'^[A-Z0-9_]+$'
        sanitized = []
        
        for control in controls[:100]:  # Max 100 controls
            if isinstance(control, str) and re.match(pattern, control):
                sanitized.append(control[:50])  # Max 50 chars per control ID
        
        return sanitized

class RateLimiter:
    """Simple rate limiting implementation"""
    
    def __init__(self):
        self.requests = {}
        self.blocked_ips = set()
    
    def is_allowed(self, identifier: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
        """Check if request is allowed based on rate limit"""
        
        # Check if blocked
        if identifier in self.blocked_ips:
            return False
        
        now = datetime.now()
        
        # Clean old entries
        cutoff = now - timedelta(seconds=window_seconds)
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > cutoff
            ]
        
        # Check rate limit
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        if len(self.requests[identifier]) >= max_requests:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False
        
        self.requests[identifier].append(now)
        return True
    
    def block_identifier(self, identifier: str):
        """Block an identifier permanently"""
        self.blocked_ips.add(identifier)
        logger.warning(f"Blocked identifier: {identifier}")

class SecurityHeaders:
    """Security headers for web responses"""
    
    @staticmethod
    def get_headers() -> Dict[str, str]:
        """Get recommended security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }

class SessionManager:
    """Simple session management"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id: str) -> str:
        """Create a new session"""
        session_token = secrets.token_urlsafe(32)
        session_hash = hashlib.sha256(session_token.encode()).hexdigest()
        
        self.sessions[session_hash] = {
            "user_id": user_id,
            "created": datetime.now(),
            "last_activity": datetime.now()
        }
        
        return session_token
    
    def validate_session(self, session_token: str, max_age_hours: int = 24) -> Optional[str]:
        """Validate a session token"""
        session_hash = hashlib.sha256(session_token.encode()).hexdigest()
        
        if session_hash not in self.sessions:
            return None
        
        session = self.sessions[session_hash]
        
        # Check expiration
        age = datetime.now() - session["created"]
        if age.total_seconds() > max_age_hours * 3600:
            del self.sessions[session_hash]
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now()
        
        return session["user_id"]
    
    def destroy_session(self, session_token: str):
        """Destroy a session"""
        session_hash = hashlib.sha256(session_token.encode()).hexdigest()
        
        if session_hash in self.sessions:
            del self.sessions[session_hash]

class DataSanitizer:
    """Sanitize data for storage and display"""
    
    @staticmethod
    def sanitize_assessment_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize assessment data before storage"""
        validator = InputValidator()
        
        sanitized = {}
        
        # Sanitize company info
        if "company_name" in data:
            sanitized["company_name"] = validator.sanitize_text(data["company_name"], 200)
        
        if "industry" in data:
            if validator.validate_industry(data["industry"]):
                sanitized["industry"] = data["industry"]
        
        if "employee_count" in data:
            if validator.validate_employee_count(data["employee_count"]):
                sanitized["employee_count"] = int(data["employee_count"])
        
        # Sanitize controls
        if "current_controls" in data:
            sanitized["current_controls"] = validator.sanitize_controls_list(data["current_controls"])
        
        # Add metadata
        sanitized["sanitized_at"] = datetime.now().isoformat()
        sanitized["version"] = "1.0"
        
        return sanitized
    
    @staticmethod
    def sanitize_output(text: str) -> str:
        """Sanitize output for display"""
        if not text:
            return ""
        
        # Basic HTML escaping for display
        text = html.escape(text)
        
        # Convert newlines to breaks for display
        text = text.replace('\n', '<br>')
        
        return text

# Utility functions for easy integration
def validate_and_sanitize_input(form_data: Dict[str, Any]) -> tuple[bool, Dict[str, Any], List[str]]:
    """
    Validate and sanitize form input
    Returns: (is_valid, sanitized_data, error_messages)
    """
    validator = InputValidator()
    sanitizer = DataSanitizer()
    errors = []
    
    # Validate required fields
    if not form_data.get("company_name"):
        errors.append("Company name is required")
    elif not validator.validate_company_name(form_data["company_name"]):
        errors.append("Invalid company name format")
    
    if not form_data.get("industry"):
        errors.append("Industry is required")
    elif not validator.validate_industry(form_data["industry"]):
        errors.append("Invalid industry selection")
    
    if not form_data.get("employee_count"):
        errors.append("Employee count is required")
    elif not validator.validate_employee_count(form_data["employee_count"]):
        errors.append("Invalid employee count")
    
    if errors:
        return False, {}, errors
    
    # Sanitize data
    sanitized = sanitizer.sanitize_assessment_data(form_data)
    
    return True, sanitized, []

def apply_security_headers(response):
    """Apply security headers to a response object"""
    headers = SecurityHeaders.get_headers()
    for key, value in headers.items():
        response.headers[key] = value
    return response

# Rate limiter instance
rate_limiter = RateLimiter()

def check_rate_limit(identifier: str) -> bool:
    """Check if request is within rate limits"""
    return rate_limiter.is_allowed(identifier)

# Session manager instance
session_manager = SessionManager()

def create_user_session(user_id: str) -> str:
    """Create a new user session"""
    return session_manager.create_session(user_id)

def validate_user_session(token: str) -> Optional[str]:
    """Validate a user session token"""
    return session_manager.validate_session(token)

# Example usage in Streamlit
def secure_streamlit_form():
    """Example of using security utilities in Streamlit"""
    import streamlit as st
    
    # Apply rate limiting
    user_ip = st.session_state.get("user_ip", "127.0.0.1")
    if not check_rate_limit(user_ip):
        st.error("Too many requests. Please try again later.")
        return
    
    # Form with validation
    with st.form("secure_assessment"):
        company_name = st.text_input("Company Name")
        industry = st.selectbox("Industry", ["Healthcare", "Financial Services", "Technology"])
        employee_count = st.number_input("Employee Count", min_value=1, max_value=1000000)
        
        if st.form_submit_button("Submit"):
            # Validate and sanitize
            is_valid, sanitized_data, errors = validate_and_sanitize_input({
                "company_name": company_name,
                "industry": industry,
                "employee_count": employee_count
            })
            
            if not is_valid:
                for error in errors:
                    st.error(error)
            else:
                st.success("Assessment data validated and sanitized")
                # Process sanitized_data
                
if __name__ == "__main__":
    # Test security utilities
    validator = InputValidator()
    
    # Test text sanitization
    dangerous_text = "<script>alert('XSS')</script>Hello"
    safe_text = validator.sanitize_text(dangerous_text)
    print(f"Sanitized: {safe_text}")
    
    # Test email validation
    print(f"Valid email: {validator.validate_email('test@example.com')}")
    print(f"Invalid email: {validator.validate_email('not-an-email')}")
    
    # Test rate limiting
    for i in range(12):
        allowed = check_rate_limit("test_user")
        print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'}")
    
    print("\nSecurity utilities ready for production!")