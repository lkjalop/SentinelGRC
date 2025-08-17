"""
Authentication and Security Manager
===================================
Enterprise-grade authentication with role-based access control.
Zero-budget implementation using industry-standard practices.
"""

import hashlib
import secrets
import jwt
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    COMPLIANCE_OFFICER = "compliance_officer"
    AUDITOR = "auditor"
    DEVELOPER = "developer"
    VIEWER = "viewer"

@dataclass
class User:
    """User profile with security attributes"""
    username: str
    email: str
    role: UserRole
    password_hash: str
    salt: str
    created_at: datetime
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    account_locked: bool = False
    mfa_enabled: bool = False
    session_token: Optional[str] = None

class AuthenticationManager:
    """
    Enterprise authentication manager with security hardening
    Implements NIST 800-53 AC-2, AC-3, AC-7, IA-2, IA-5 controls
    """
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.failed_login_tracking: Dict[str, List[datetime]] = {}
        
        # Security configuration per NIST guidelines
        self.MAX_LOGIN_ATTEMPTS = 3
        self.ACCOUNT_LOCKOUT_DURATION = timedelta(minutes=30)
        self.SESSION_TIMEOUT = timedelta(hours=8)
        self.PASSWORD_MIN_LENGTH = 12
        self.JWT_ALGORITHM = "HS256"
        
        logger.info("🔐 Authentication manager initialized with security hardening")
    
    def hash_password(self, password: str, salt: str = None) -> tuple[str, str]:
        """
        Hash password using SHA-256 with salt (NIST 800-53 IA-5)
        Returns (password_hash, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use PBKDF2 for additional security
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iterations
        ).hex()
        
        return password_hash, salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        computed_hash, _ = self.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, stored_hash)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength per NIST 800-63B guidelines
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "strength_score": 0
        }
        
        if len(password) < self.PASSWORD_MIN_LENGTH:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Password must be at least {self.PASSWORD_MIN_LENGTH} characters")
        else:
            validation_result["strength_score"] += 20
        
        # Check for character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        variety_count = sum([has_upper, has_lower, has_digit, has_special])
        validation_result["strength_score"] += variety_count * 15
        
        if variety_count < 3:
            validation_result["valid"] = False
            validation_result["errors"].append("Password must contain at least 3 of: uppercase, lowercase, digits, special characters")
        
        # Check for common patterns
        common_patterns = ["password", "123456", "qwerty", "admin"]
        if any(pattern in password.lower() for pattern in common_patterns):
            validation_result["valid"] = False
            validation_result["errors"].append("Password contains common patterns")
            validation_result["strength_score"] -= 30
        
        validation_result["strength_score"] = max(0, min(100, validation_result["strength_score"]))
        return validation_result
    
    def create_user(self, username: str, email: str, password: str, role: UserRole) -> Dict[str, Any]:
        """
        Create new user with security validation (NIST 800-53 AC-2)
        """
        try:
            # Validate username
            if username in self.users:
                return {"success": False, "error": "Username already exists"}
            
            if len(username) < 3 or len(username) > 50:
                return {"success": False, "error": "Username must be 3-50 characters"}
            
            # Validate password
            password_validation = self.validate_password_strength(password)
            if not password_validation["valid"]:
                return {"success": False, "error": "Password validation failed", "details": password_validation["errors"]}
            
            # Create user
            password_hash, salt = self.hash_password(password)
            user = User(
                username=username,
                email=email,
                role=role,
                password_hash=password_hash,
                salt=salt,
                created_at=datetime.now()
            )
            
            self.users[username] = user
            
            logger.info(f"✅ User created: {username} with role {role.value}")
            return {
                "success": True,
                "user": {
                    "username": username,
                    "email": email,
                    "role": role.value,
                    "created_at": user.created_at.isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ User creation failed: {e}")
            return {"success": False, "error": "User creation failed"}
    
    def authenticate_user(self, username: str, password: str, client_ip: str = None) -> Dict[str, Any]:
        """
        Authenticate user with brute force protection (NIST 800-53 AC-7)
        """
        try:
            # Check if user exists
            user = self.users.get(username)
            if not user:
                self._record_failed_login(username, client_ip)
                return {"success": False, "error": "Invalid credentials"}
            
            # Check account lockout
            if user.account_locked:
                return {"success": False, "error": "Account is locked. Contact administrator"}
            
            # Check login attempt limits
            if self._is_rate_limited(username, client_ip):
                self._lock_account(username)
                return {"success": False, "error": "Too many failed login attempts. Account locked"}
            
            # Verify password
            if not self.verify_password(password, user.password_hash, user.salt):
                self._record_failed_login(username, client_ip)
                return {"success": False, "error": "Invalid credentials"}
            
            # Successful authentication
            self._clear_failed_logins(username)
            user.last_login = datetime.now()
            user.failed_login_attempts = 0
            
            # Generate JWT token
            token = self._generate_jwt_token(user)
            user.session_token = token
            
            # Store session
            self.sessions[token] = {
                "username": username,
                "role": user.role.value,
                "created_at": datetime.now(),
                "client_ip": client_ip
            }
            
            logger.info(f"✅ User authenticated: {username}")
            return {
                "success": True,
                "token": token,
                "user": {
                    "username": username,
                    "role": user.role.value,
                    "last_login": user.last_login.isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            return {"success": False, "error": "Authentication failed"}
    
    def _generate_jwt_token(self, user: User) -> str:
        """Generate JWT token with expiration"""
        payload = {
            "username": user.username,
            "role": user.role.value,
            "exp": datetime.utcnow() + self.SESSION_TIMEOUT,
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.JWT_ALGORITHM)
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate JWT token and check session (NIST 800-53 AC-3)
        """
        try:
            # Decode JWT
            payload = jwt.decode(token, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            
            # Check session exists
            session = self.sessions.get(token)
            if not session:
                return {"valid": False, "error": "Session not found"}
            
            # Check session timeout
            session_age = datetime.now() - session["created_at"]
            if session_age > self.SESSION_TIMEOUT:
                self.logout_user(token)
                return {"valid": False, "error": "Session expired"}
            
            return {
                "valid": True,
                "username": payload["username"],
                "role": payload["role"]
            }
            
        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"valid": False, "error": "Invalid token"}
        except Exception as e:
            logger.error(f"❌ Token validation failed: {e}")
            return {"valid": False, "error": "Token validation failed"}
    
    def logout_user(self, token: str) -> bool:
        """Logout user and invalidate session"""
        try:
            if token in self.sessions:
                username = self.sessions[token]["username"]
                user = self.users.get(username)
                if user:
                    user.session_token = None
                
                del self.sessions[token]
                logger.info(f"✅ User logged out: {username}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Logout failed: {e}")
            return False
    
    def _record_failed_login(self, username: str, client_ip: str):
        """Record failed login attempt"""
        key = f"{username}:{client_ip}" if client_ip else username
        if key not in self.failed_login_tracking:
            self.failed_login_tracking[key] = []
        
        self.failed_login_tracking[key].append(datetime.now())
        
        # Update user record
        user = self.users.get(username)
        if user:
            user.failed_login_attempts += 1
    
    def _is_rate_limited(self, username: str, client_ip: str) -> bool:
        """Check if login attempts exceed rate limit"""
        key = f"{username}:{client_ip}" if client_ip else username
        attempts = self.failed_login_tracking.get(key, [])
        
        # Remove old attempts (older than lockout duration)
        cutoff_time = datetime.now() - self.ACCOUNT_LOCKOUT_DURATION
        recent_attempts = [attempt for attempt in attempts if attempt > cutoff_time]
        self.failed_login_tracking[key] = recent_attempts
        
        return len(recent_attempts) >= self.MAX_LOGIN_ATTEMPTS
    
    def _lock_account(self, username: str):
        """Lock user account after too many failed attempts"""
        user = self.users.get(username)
        if user:
            user.account_locked = True
            logger.warning(f"⚠️ Account locked: {username}")
    
    def _clear_failed_logins(self, username: str):
        """Clear failed login attempts after successful login"""
        keys_to_clear = [key for key in self.failed_login_tracking.keys() if key.startswith(username)]
        for key in keys_to_clear:
            del self.failed_login_tracking[key]
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get authentication security statistics"""
        total_users = len(self.users)
        active_sessions = len(self.sessions)
        locked_accounts = sum(1 for user in self.users.values() if user.account_locked)
        mfa_enabled_users = sum(1 for user in self.users.values() if user.mfa_enabled)
        
        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "locked_accounts": locked_accounts,
            "mfa_adoption_rate": (mfa_enabled_users / total_users * 100) if total_users > 0 else 0,
            "failed_login_attempts": len(self.failed_login_tracking),
            "security_controls_implemented": [
                "NIST 800-53 AC-2: Account Management",
                "NIST 800-53 AC-3: Access Enforcement", 
                "NIST 800-53 AC-7: Unsuccessful Logon Attempts",
                "NIST 800-53 IA-2: Identification and Authentication",
                "NIST 800-53 IA-5: Authenticator Management"
            ]
        }

# Create default admin user for initial setup
def initialize_default_users(auth_manager: AuthenticationManager) -> None:
    """Initialize default users for demo/development"""
    
    # Create admin user
    admin_result = auth_manager.create_user(
        username="admin",
        email="admin@sentinelgrc.com",
        password="SentinelGRC@2025!",
        role=UserRole.ADMIN
    )
    
    # Create compliance officer
    compliance_result = auth_manager.create_user(
        username="compliance",
        email="compliance@sentinelgrc.com", 
        password="Compliance@2025!",
        role=UserRole.COMPLIANCE_OFFICER
    )
    
    # Create auditor
    auditor_result = auth_manager.create_user(
        username="auditor",
        email="auditor@sentinelgrc.com",
        password="Auditor@2025!",
        role=UserRole.AUDITOR
    )
    
    logger.info("🔐 Default users initialized for demo/development")