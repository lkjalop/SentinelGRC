"""
Security Enhancements for Sentinel GRC
======================================
Advanced rate limiting, input validation, and secure configuration management.
Zero-cost security hardening implementation.
"""

import os
import time
import hashlib
import hmac
import re
import html
import json
import getpass
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# ADVANCED RATE LIMITING
# ============================================================================

class AdvancedRateLimiter:
    """Advanced rate limiter with IP blocking and pattern detection"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.blocked_ips = set()
        self.suspicious_patterns = defaultdict(int)
        self.whitelist = set()  # Trusted IPs
        self.request_signatures = defaultdict(list)
    
    def add_to_whitelist(self, ip: str):
        """Add IP to whitelist (skip rate limiting)"""
        self.whitelist.add(ip)
        logger.info(f"Added {ip} to rate limiter whitelist")
    
    def is_request_allowed(self, identifier: str, endpoint: str = "/assess", 
                          request_size: int = 0) -> Tuple[bool, str]:
        """
        Check if request is allowed based on rate limits and patterns
        
        Args:
            identifier: IP address or user ID
            endpoint: API endpoint being accessed
            request_size: Size of request payload in bytes
        
        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        current_time = time.time()
        
        # Skip rate limiting for whitelisted IPs
        if identifier in self.whitelist:
            return True, "Whitelisted IP"
        
        # Clean old requests (keep last 24 hours)
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < 86400  # 24 hours
        ]
        
        # Check if blocked
        if identifier in self.blocked_ips:
            return False, "IP blocked due to suspicious activity"
        
        # Rate limits by endpoint
        limits = {
            "/assess": {"requests": 10, "window": 600, "max_size": 1024*1024},    # 10 per 10min, 1MB max
            "/api/groq": {"requests": 20, "window": 3600, "max_size": 512*1024}, # 20 per hour, 512KB max
            "/api/neo4j": {"requests": 50, "window": 3600, "max_size": 256*1024}, # 50 per hour, 256KB max
            "/health": {"requests": 60, "window": 60, "max_size": 1024},          # 60 per minute, 1KB max
            "/upload": {"requests": 5, "window": 3600, "max_size": 10*1024*1024}, # 5 per hour, 10MB max
            "/download": {"requests": 20, "window": 3600, "max_size": 1024}       # 20 per hour, 1KB max
        }
        
        # Default limits for unknown endpoints
        limit_config = limits.get(endpoint, limits["/assess"])
        
        # Check request size
        if request_size > limit_config["max_size"]:
            self.suspicious_patterns[identifier] += 1
            return False, f"Request too large (max {limit_config['max_size']} bytes)"
        
        # Count recent requests in time window
        window_start = current_time - limit_config["window"]
        recent_requests = [
            req_time for req_time in self.requests[identifier]
            if req_time >= window_start
        ]
        
        # Check rate limit
        if len(recent_requests) >= limit_config["requests"]:
            # Detect rapid-fire requests (potential attack)
            if len(recent_requests) >= 2:
                time_diff = recent_requests[-1] - recent_requests[-2]
                if time_diff < 1:  # Less than 1 second between requests
                    self.suspicious_patterns[identifier] += 2
                    logger.warning(f"Rapid requests detected from {identifier}")
            
            self.suspicious_patterns[identifier] += 1
            
            # Block if too many violations
            if self.suspicious_patterns[identifier] > 5:
                self.blocked_ips.add(identifier)
                logger.error(f"Blocked IP {identifier} for repeated rate limit violations")
                return False, "IP blocked for repeated violations"
            
            return False, f"Rate limit exceeded. Try again in {limit_config['window']} seconds"
        
        # Log successful request
        self.requests[identifier].append(current_time)
        return True, "Request allowed"
    
    def validate_request_signature(self, request_data: str, signature: str, 
                                 secret: str) -> bool:
        """Validate HMAC request signature to prevent tampering"""
        if not secret or not signature:
            return False
            
        try:
            expected_signature = hmac.new(
                secret.encode(),
                request_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Use constant-time comparison to prevent timing attacks
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Signature validation error: {e}")
            return False
    
    def detect_attack_patterns(self, identifier: str, request_data: str) -> List[str]:
        """Detect common attack patterns in requests"""
        patterns = []
        
        # SQL injection patterns
        sql_patterns = [
            r'(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b)',
            r'(--|#|\/\*|\*\/)',
            r'(\bOR\b.*=|\bAND\b.*=)',
            r'(\bEXEC\b|\bEXECUTE\b)'
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, request_data, re.IGNORECASE):
                patterns.append("sql_injection")
                break
        
        # Script injection patterns
        script_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'expression\s*\('
        ]
        
        for pattern in script_patterns:
            if re.search(pattern, request_data, re.IGNORECASE):
                patterns.append("script_injection")
                break
        
        # Path traversal patterns
        path_patterns = [
            r'\.\.\/',
            r'\.\.\\'
        ]
        
        for pattern in path_patterns:
            if re.search(pattern, request_data):
                patterns.append("path_traversal")
                break
        
        # If attack patterns detected, increase suspicion
        if patterns:
            self.suspicious_patterns[identifier] += len(patterns) * 2
            logger.warning(f"Attack patterns detected from {identifier}: {patterns}")
        
        return patterns
    
    def unblock_ip(self, identifier: str) -> bool:
        """Manually unblock an IP (admin function)"""
        if identifier in self.blocked_ips:
            self.blocked_ips.remove(identifier)
            self.suspicious_patterns[identifier] = 0
            logger.info(f"Unblocked IP: {identifier}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics"""
        total_requests = sum(len(reqs) for reqs in self.requests.values())
        active_ips = len([ip for ip, reqs in self.requests.items() if reqs])
        
        return {
            "total_requests": total_requests,
            "active_ips": active_ips,
            "blocked_ips": len(self.blocked_ips),
            "whitelisted_ips": len(self.whitelist),
            "suspicious_activities": sum(self.suspicious_patterns.values()),
            "most_active_ips": sorted(
                [(ip, len(reqs)) for ip, reqs in self.requests.items()],
                key=lambda x: x[1], reverse=True
            )[:10]
        }

# ============================================================================
# ENHANCED INPUT VALIDATION
# ============================================================================

class AdvancedInputValidator:
    """Comprehensive input validation with injection attack detection"""
    
    def __init__(self):
        self.malicious_patterns = {
            'sql_injection': [
                r'(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b)',
                r'(--|#|\/\*|\*\/)',
                r'(\bOR\b.*=|\bAND\b.*=)',
                r'(\bEXEC\b|\bEXECUTE\b)',
                r'(\bCREATE\b|\bALTER\b|\bTRUNCATE\b)',
                r'(xp_|sp_|fn_)'
            ],
            'script_injection': [
                r'<script[^>]*>.*?</script>',
                r'javascript:',
                r'on\w+\s*=',
                r'eval\s*\(',
                r'expression\s*\(',
                r'<iframe[^>]*>',
                r'<object[^>]*>',
                r'<embed[^>]*>'
            ],
            'path_traversal': [
                r'\.\.\/',
                r'\.\.\\\\',
                r'%2e%2e%2f',
                r'%2e%2e%5c',
                r'\.\.%2f',
                r'\.\.%5c'
            ],
            'command_injection': [
                r'[;&|`]',
                r'\$\(',
                r'`[^`]*`',
                r'\|\s*\w+',
                r'&&\s*\w+',
                r';\s*\w+'
            ]
        }
        
        # Whitelist patterns for valid inputs
        self.valid_patterns = {
            'company_name': r'^[a-zA-Z0-9\s\-\.\,\&\'\"\(\)]{1,100}$',
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[1-9]\d{1,14}$',
            'url': r'^https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/[^\s]*)?$',
            'alphanumeric': r'^[a-zA-Z0-9\s]{1,50}$',
            'numeric': r'^\d+(\.\d+)?$',
            'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        }
        
        # Validation stats
        self.validation_stats = {
            'total_validations': 0,
            'blocked_injections': 0,
            'sanitized_inputs': 0,
            'validation_errors': 0
        }
    
    def validate_input(self, value: Any, input_type: str = "general", 
                      max_length: int = 1000) -> Tuple[bool, str, Optional[str]]:
        """
        Comprehensive input validation
        
        Args:
            value: Input value to validate
            input_type: Type of input (company_name, email, etc.)
            max_length: Maximum allowed length
        
        Returns:
            Tuple of (is_valid: bool, error_message: str, sanitized_value: str)
        """
        self.validation_stats['total_validations'] += 1
        
        # Type checking
        if not isinstance(value, str):
            if value is None:
                return False, "Input cannot be None", None
            # Convert to string if possible
            try:
                value = str(value)
            except Exception:
                self.validation_stats['validation_errors'] += 1
                return False, "Input must be convertible to string", None
        
        # Length limits
        if len(value) > max_length:
            self.validation_stats['validation_errors'] += 1
            return False, f"Input too long (max {max_length} characters)", None
        
        if len(value.strip()) == 0:
            self.validation_stats['validation_errors'] += 1
            return False, "Input cannot be empty", None
        
        # Check for malicious patterns
        for pattern_type, patterns in self.malicious_patterns.items():
            for pattern in patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    self.validation_stats['blocked_injections'] += 1
                    logger.warning(f"Blocked {pattern_type}: {pattern}")
                    return False, f"Potentially malicious input detected: {pattern_type}", None
        
        # Type-specific validation
        if input_type in self.valid_patterns:
            if not re.match(self.valid_patterns[input_type], value):
                self.validation_stats['validation_errors'] += 1
                return False, f"Invalid format for {input_type}", None
        
        # Additional business logic validation
        if input_type == "industry":
            valid_industries = [
                "Healthcare", "Financial Services", "Technology", "Manufacturing",
                "Retail", "Government", "Education", "Energy", "Telecommunications",
                "Transportation", "Real Estate", "Hospitality", "Media", "Other"
            ]
            if value not in valid_industries:
                self.validation_stats['validation_errors'] += 1
                return False, "Invalid industry selection", None
        
        elif input_type == "assessment_type":
            valid_types = [
                "Essential 8", "Privacy Act", "APRA CPS 234", "SOCI Act",
                "HIPAA", "PCI DSS", "ISO 27001", "NIST", "SOC 2", "Custom"
            ]
            if value not in valid_types:
                self.validation_stats['validation_errors'] += 1
                return False, "Invalid assessment type", None
        
        # Sanitize input
        sanitized_value = self.sanitize_input(value)
        if sanitized_value != value:
            self.validation_stats['sanitized_inputs'] += 1
        
        return True, "Valid input", sanitized_value
    
    def sanitize_input(self, value: str) -> str:
        """Sanitize input for safe processing"""
        if not isinstance(value, str):
            return str(value)
        
        # HTML escape
        value = html.escape(value)
        
        # Remove null bytes and control characters
        value = ''.join(char for char in value if ord(char) >= 32 or char in '\t\n\r')
        
        # Normalize whitespace
        value = ' '.join(value.split())
        
        # Remove potentially dangerous characters for file paths
        dangerous_chars = ['<', '>', '"', '|', '?', '*', ':', '\\', '/']
        for char in dangerous_chars:
            value = value.replace(char, '')
        
        return value.strip()
    
    def validate_file_upload(self, filename: str, content_type: str, 
                           file_size: int) -> Tuple[bool, str]:
        """Validate file uploads"""
        # Check filename
        if not filename or '..' in filename or '/' in filename or '\\' in filename:
            return False, "Invalid filename"
        
        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.csv', '.xlsx', '.png', '.jpg', '.jpeg']
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in allowed_extensions:
            return False, f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        
        # Check content type
        allowed_types = [
            'application/pdf', 'application/msword', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain', 'text/csv', 'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'image/png', 'image/jpeg', 'image/jpg'
        ]
        if content_type not in allowed_types:
            return False, "Invalid content type"
        
        # Check file size (10MB max)
        max_size = 10 * 1024 * 1024
        if file_size > max_size:
            return False, f"File too large (max 10MB)"
        
        return True, "Valid file"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        total = self.validation_stats['total_validations']
        if total > 0:
            block_rate = (self.validation_stats['blocked_injections'] / total) * 100
            error_rate = (self.validation_stats['validation_errors'] / total) * 100
            sanitization_rate = (self.validation_stats['sanitized_inputs'] / total) * 100
        else:
            block_rate = error_rate = sanitization_rate = 0
        
        return {
            **self.validation_stats,
            'block_rate': f"{block_rate:.1f}%",
            'error_rate': f"{error_rate:.1f}%",
            'sanitization_rate': f"{sanitization_rate:.1f}%"
        }

# ============================================================================
# SECURE CONFIGURATION MANAGEMENT
# ============================================================================

class SecureConfig:
    """Secure configuration management with encryption"""
    
    def __init__(self, key_file: str = ".sentinel_key"):
        self.key_file = key_file
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        self.config_cache = {}
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            
            # Add to .gitignore if it exists
            if os.path.exists('.gitignore'):
                with open('.gitignore', 'r') as f:
                    gitignore_content = f.read()
                
                if self.key_file not in gitignore_content:
                    with open('.gitignore', 'a') as f:
                        f.write(f"\n{self.key_file}\n")
            
            logger.info(f"Created new encryption key: {self.key_file}")
            return key
    
    def encrypt_secret(self, value: str) -> str:
        """Encrypt a secret value"""
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_secret(self, encrypted_value: str) -> str:
        """Decrypt a secret value"""
        return self.cipher.decrypt(encrypted_value.encode()).decode()
    
    def store_secret(self, key_name: str, value: str):
        """Store an encrypted secret"""
        os.makedirs('.secrets', exist_ok=True)
        encrypted_value = self.encrypt_secret(value)
        
        secret_file = f".secrets/{key_name}.enc"
        with open(secret_file, 'w') as f:
            f.write(encrypted_value)
        
        # Add .secrets to .gitignore
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
            
            if '.secrets/' not in gitignore_content:
                with open('.gitignore', 'a') as f:
                    f.write("\n.secrets/\n")
        
        logger.info(f"Stored encrypted secret: {key_name}")
    
    def get_secret(self, key_name: str, prompt_if_missing: bool = True) -> Optional[str]:
        """Get a secret value from multiple sources"""
        
        # 1. Try environment variable first
        value = os.getenv(key_name)
        if value:
            return value
        
        # 2. Try encrypted file
        secret_file = f".secrets/{key_name}.enc"
        if os.path.exists(secret_file):
            try:
                with open(secret_file, 'r') as f:
                    encrypted_value = f.read()
                return self.decrypt_secret(encrypted_value)
            except Exception as e:
                logger.error(f"Failed to decrypt secret {key_name}: {e}")
        
        # 3. Try cache
        if key_name in self.config_cache:
            return self.config_cache[key_name]
        
        # 4. Prompt user (development only)
        if prompt_if_missing and os.getenv("DEVELOPMENT", "false").lower() == "true":
            try:
                value = getpass.getpass(f"Enter {key_name}: ")
                if value:
                    # Cache for this session
                    self.config_cache[key_name] = value
                    return value
            except KeyboardInterrupt:
                logger.info("Secret input cancelled by user")
        
        return None
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate that all required configuration is present"""
        required_secrets = [
            "GROQ_API_KEY",
            "SUPABASE_URL",
            "SUPABASE_ANON_KEY",
            "NEO4J_URI",
            "NEO4J_USERNAME", 
            "NEO4J_PASSWORD"
        ]
        
        optional_secrets = [
            "SLACK_WEBHOOK_URL",
            "GITHUB_TOKEN",
            "HMAC_SECRET"
        ]
        
        config_status = {
            "required": {},
            "optional": {},
            "missing_required": [],
            "missing_optional": []
        }
        
        # Check required secrets
        for secret in required_secrets:
            value = self.get_secret(secret, prompt_if_missing=False)
            if value:
                config_status["required"][secret] = "✓ Present"
            else:
                config_status["required"][secret] = "✗ Missing"
                config_status["missing_required"].append(secret)
        
        # Check optional secrets
        for secret in optional_secrets:
            value = self.get_secret(secret, prompt_if_missing=False)
            if value:
                config_status["optional"][secret] = "✓ Present"
            else:
                config_status["optional"][secret] = "✗ Missing"
                config_status["missing_optional"].append(secret)
        
        config_status["is_valid"] = len(config_status["missing_required"]) == 0
        
        return config_status

# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

# Initialize security components
rate_limiter = AdvancedRateLimiter()
input_validator = AdvancedInputValidator()
secure_config = SecureConfig()

# Add localhost to whitelist for development
rate_limiter.add_to_whitelist("127.0.0.1")
rate_limiter.add_to_whitelist("::1")

def get_security_stats() -> Dict[str, Any]:
    """Get comprehensive security statistics"""
    from connection_pool_manager import cache_manager
    
    return {
        "rate_limiter": rate_limiter.get_stats(),
        "input_validator": input_validator.get_stats(),
        "config_validation": secure_config.validate_config(),
        "cache": cache_manager.get_stats(),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Test security components
    print("Testing security enhancements...")
    
    # Test rate limiter
    print("\n1. Testing Rate Limiter:")
    allowed, reason = rate_limiter.is_request_allowed("192.168.1.100", "/assess")
    print(f"Request allowed: {allowed} - {reason}")
    
    # Test input validator
    print("\n2. Testing Input Validator:")
    valid, error, sanitized = input_validator.validate_input("Test Company Inc.", "company_name")
    print(f"Valid: {valid}, Sanitized: '{sanitized}'")
    
    # Test malicious input
    malicious_input = "'; DROP TABLE users; --"
    valid, error, sanitized = input_validator.validate_input(malicious_input, "company_name")
    print(f"Malicious input blocked: {not valid} - {error}")
    
    # Test config validation
    print("\n3. Testing Config Validation:")
    config_status = secure_config.validate_config()
    print(f"Config valid: {config_status['is_valid']}")
    print(f"Missing required: {config_status['missing_required']}")
    
    # Print overall stats
    print("\n4. Security Statistics:")
    stats = get_security_stats()
    print(json.dumps(stats, indent=2))
    
    print("\nSecurity enhancements ready! [Shield deployed]")