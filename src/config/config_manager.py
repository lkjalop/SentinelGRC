"""
Enterprise Configuration Management System
Centralizes all configuration with environment variable support
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Environment(Enum):
    """Deployment environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 20
    max_overflow: int = 40
    pool_timeout: int = 30
    ssl_enabled: bool = False
    
    @classmethod
    def from_env(cls, prefix: str = "DB") -> "DatabaseConfig":
        """Load database config from environment variables"""
        return cls(
            host=os.getenv(f"{prefix}_HOST", "localhost"),
            port=int(os.getenv(f"{prefix}_PORT", "5432")),
            database=os.getenv(f"{prefix}_NAME", "sentinelgrc"),
            username=os.getenv(f"{prefix}_USER", "postgres"),
            password=os.getenv(f"{prefix}_PASSWORD", ""),
            pool_size=int(os.getenv(f"{prefix}_POOL_SIZE", "20")),
            max_overflow=int(os.getenv(f"{prefix}_MAX_OVERFLOW", "40")),
            pool_timeout=int(os.getenv(f"{prefix}_POOL_TIMEOUT", "30")),
            ssl_enabled=os.getenv(f"{prefix}_SSL", "false").lower() == "true"
        )


@dataclass
class APIConfig:
    """API service configuration"""
    groq_api_key: Optional[str]
    openai_api_key: Optional[str]
    anthropic_api_key: Optional[str]
    supabase_url: Optional[str]
    supabase_key: Optional[str]
    neo4j_uri: Optional[str]
    neo4j_username: Optional[str]
    neo4j_password: Optional[str]
    
    @classmethod
    def from_env(cls) -> "APIConfig":
        """Load API config from environment variables"""
        return cls(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            supabase_url=os.getenv("SUPABASE_URL"),
            supabase_key=os.getenv("SUPABASE_ANON_KEY"),
            neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            neo4j_username=os.getenv("NEO4J_USERNAME", "neo4j"),
            neo4j_password=os.getenv("NEO4J_PASSWORD")
        )


@dataclass
class SecurityConfig:
    """Security configuration settings"""
    secret_key: str
    jwt_secret: str
    encryption_key: str
    cors_origins: list
    rate_limit_per_minute: int
    session_timeout_minutes: int
    max_login_attempts: int
    password_min_length: int
    require_mfa: bool
    
    @classmethod
    def from_env(cls) -> "SecurityConfig":
        """Load security config from environment variables"""
        return cls(
            secret_key=os.getenv("SECRET_KEY", os.urandom(32).hex()),
            jwt_secret=os.getenv("JWT_SECRET", os.urandom(32).hex()),
            encryption_key=os.getenv("ENCRYPTION_KEY", os.urandom(32).hex()),
            cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT", "60")),
            session_timeout_minutes=int(os.getenv("SESSION_TIMEOUT", "30")),
            max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),
            password_min_length=int(os.getenv("PASSWORD_MIN_LENGTH", "12")),
            require_mfa=os.getenv("REQUIRE_MFA", "false").lower() == "true"
        )


@dataclass
class ApplicationConfig:
    """Application-level configuration"""
    app_name: str
    app_version: str
    environment: Environment
    debug: bool
    log_level: str
    host: str
    port: int
    workers: int
    enable_metrics: bool
    enable_tracing: bool
    cache_ttl_seconds: int
    
    @classmethod
    def from_env(cls) -> "ApplicationConfig":
        """Load application config from environment variables"""
        env_str = os.getenv("ENVIRONMENT", "development").lower()
        try:
            environment = Environment(env_str)
        except ValueError:
            environment = Environment.DEVELOPMENT
            
        return cls(
            app_name=os.getenv("APP_NAME", "SentinelGRC"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            environment=environment,
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            workers=int(os.getenv("WORKERS", "4")),
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true",
            enable_tracing=os.getenv("ENABLE_TRACING", "false").lower() == "true",
            cache_ttl_seconds=int(os.getenv("CACHE_TTL", "3600"))
        )


class ConfigurationManager:
    """Centralized configuration management"""
    
    _instance = None
    _config_cache: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.load_environment_file()
        self.database = DatabaseConfig.from_env()
        self.api = APIConfig.from_env()
        self.security = SecurityConfig.from_env()
        self.application = ApplicationConfig.from_env()
        
        # Validate configuration
        self._validate_config()
        
        # Log configuration status (without secrets)
        logger.info(f"Configuration loaded for environment: {self.application.environment.value}")
    
    def load_environment_file(self, env_file: str = ".env"):
        """Load environment variables from .env file if it exists"""
        env_path = Path(env_file)
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip().strip('"').strip("'")
                logger.info(f"Loaded environment variables from {env_file}")
            except Exception as e:
                logger.warning(f"Failed to load {env_file}: {e}")
    
    def _validate_config(self):
        """Validate critical configuration values"""
        errors = []
        
        # Check critical security settings
        if self.application.environment == Environment.PRODUCTION:
            if self.application.debug:
                errors.append("DEBUG mode should be disabled in production")
            if not self.security.require_mfa:
                logger.warning("MFA is disabled in production environment")
            if self.security.secret_key == os.urandom(32).hex():
                errors.append("SECRET_KEY must be set in production")
                
        # Check database configuration
        if not self.database.password and self.application.environment == Environment.PRODUCTION:
            errors.append("Database password must be set in production")
            
        # Check API keys
        if not any([self.api.groq_api_key, self.api.openai_api_key, self.api.anthropic_api_key]):
            logger.warning("No AI API keys configured - AI features will be limited")
            
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(errors)
            logger.error(error_msg)
            if self.application.environment == Environment.PRODUCTION:
                raise ValueError(error_msg)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key"""
        # Example: config.get("database.host") or config.get("api.groq_api_key")
        parts = key.split('.')
        value = self
        
        try:
            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return default
            return value
        except Exception:
            return default
    
    def to_dict(self, include_secrets: bool = False) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        config_dict = {
            "application": {
                "name": self.application.app_name,
                "version": self.application.app_version,
                "environment": self.application.environment.value,
                "debug": self.application.debug,
                "host": self.application.host,
                "port": self.application.port,
                "workers": self.application.workers
            },
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "database": self.database.database,
                "pool_size": self.database.pool_size,
                "ssl_enabled": self.database.ssl_enabled
            }
        }
        
        if include_secrets:
            # Only include secrets if explicitly requested
            config_dict["security"] = {
                "cors_origins": self.security.cors_origins,
                "rate_limit": self.security.rate_limit_per_minute,
                "session_timeout": self.security.session_timeout_minutes
            }
        
        return config_dict
    
    def reload(self):
        """Reload configuration from environment"""
        self.__init__()
        logger.info("Configuration reloaded")


# Singleton instance
config = ConfigurationManager()