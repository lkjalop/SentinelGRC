"""
Environment-Based Configuration Management
=========================================
Centralized configuration using environment variables with validation and fallbacks
Supports development, staging, and production environments
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class Environment(str, Enum):
    """Application environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class LogLevel(str, Enum):
    """Log level options"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://localhost:5432/sentinel_grc"))
    pool_size: int = field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "10")))
    max_overflow: int = field(default_factory=lambda: int(os.getenv("DB_MAX_OVERFLOW", "20")))
    pool_timeout: int = field(default_factory=lambda: int(os.getenv("DB_POOL_TIMEOUT", "30")))
    echo: bool = field(default_factory=lambda: os.getenv("DB_ECHO", "false").lower() == "true")
    
    def __post_init__(self):
        """Validate database configuration"""
        try:
            parsed_url = urlparse(self.url)
            if not parsed_url.scheme:
                raise ValueError("Database URL must include scheme")
        except Exception as e:
            logger.warning(f"Database URL validation failed: {e}")

@dataclass
class RedisConfig:
    """Redis configuration"""
    url: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379"))
    password: Optional[str] = field(default_factory=lambda: os.getenv("REDIS_PASSWORD"))
    db: int = field(default_factory=lambda: int(os.getenv("REDIS_DB", "0")))
    max_connections: int = field(default_factory=lambda: int(os.getenv("REDIS_MAX_CONNECTIONS", "10")))
    socket_timeout: float = field(default_factory=lambda: float(os.getenv("REDIS_SOCKET_TIMEOUT", "5.0")))
    socket_connect_timeout: float = field(default_factory=lambda: float(os.getenv("REDIS_CONNECT_TIMEOUT", "5.0")))
    retry_on_timeout: bool = field(default_factory=lambda: os.getenv("REDIS_RETRY_ON_TIMEOUT", "true").lower() == "true")

@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "change-this-in-production"))
    jwt_secret_key: str = field(default_factory=lambda: os.getenv("JWT_SECRET_KEY", "jwt-change-this-in-production"))
    jwt_algorithm: str = field(default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"))
    jwt_expiration_hours: int = field(default_factory=lambda: int(os.getenv("JWT_EXPIRATION_HOURS", "24")))
    api_key_header: str = field(default_factory=lambda: os.getenv("API_KEY_HEADER", "X-API-Key"))
    cors_origins: List[str] = field(default_factory=lambda: _parse_cors_origins())
    rate_limit_per_minute: int = field(default_factory=lambda: int(os.getenv("RATE_LIMIT_PER_MINUTE", "100")))
    max_request_size: int = field(default_factory=lambda: int(os.getenv("MAX_REQUEST_SIZE", "16777216")))  # 16MB
    
    def __post_init__(self):
        """Validate security configuration"""
        if self.secret_key == "change-this-in-production" and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("Secret key must be changed in production")
        if len(self.secret_key) < 32:
            logger.warning("Secret key should be at least 32 characters long")

@dataclass
class APIConfig:
    """External API configuration"""
    groq_api_key: Optional[str] = field(default_factory=lambda: os.getenv("GROQ_API_KEY"))
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    groq_model: str = field(default_factory=lambda: os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"))
    anthropic_model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"))
    timeout_seconds: int = field(default_factory=lambda: int(os.getenv("API_TIMEOUT", "30")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("API_MAX_RETRIES", "3")))
    
    def get_available_providers(self) -> List[str]:
        """Get list of available API providers"""
        providers = []
        if self.groq_api_key:
            providers.append("groq")
        if self.openai_api_key:
            providers.append("openai")
        if self.anthropic_api_key:
            providers.append("anthropic")
        return providers

@dataclass
class ApplicationConfig:
    """Application-level configuration"""
    name: str = field(default_factory=lambda: os.getenv("APP_NAME", "Sentinel GRC"))
    version: str = field(default_factory=lambda: os.getenv("APP_VERSION", "2.0.0"))
    environment: Environment = field(default_factory=lambda: Environment(os.getenv("ENVIRONMENT", "development")))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    workers: int = field(default_factory=lambda: int(os.getenv("WORKERS", "1")))
    log_level: LogLevel = field(default_factory=lambda: LogLevel(os.getenv("LOG_LEVEL", "INFO")))
    log_format: str = field(default_factory=lambda: os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    timezone: str = field(default_factory=lambda: os.getenv("TIMEZONE", "UTC"))
    
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION
    
    def is_testing(self) -> bool:
        return self.environment == Environment.TESTING

@dataclass
class FrameworkConfig:
    """Framework-specific configuration"""
    data_path: str = field(default_factory=lambda: os.getenv("FRAMEWORK_DATA_PATH", "data/frameworks"))
    cache_ttl_seconds: int = field(default_factory=lambda: int(os.getenv("FRAMEWORK_CACHE_TTL", "3600")))
    enable_caching: bool = field(default_factory=lambda: os.getenv("ENABLE_FRAMEWORK_CACHING", "true").lower() == "true")
    enable_validation: bool = field(default_factory=lambda: os.getenv("ENABLE_FRAMEWORK_VALIDATION", "true").lower() == "true")
    auto_update: bool = field(default_factory=lambda: os.getenv("FRAMEWORK_AUTO_UPDATE", "false").lower() == "true")
    oscal_endpoint: Optional[str] = field(default_factory=lambda: os.getenv("OSCAL_ENDPOINT"))
    olir_endpoint: Optional[str] = field(default_factory=lambda: os.getenv("OLIR_ENDPOINT"))
    
    def get_data_path(self) -> Path:
        """Get framework data path as Path object"""
        return Path(self.data_path)

@dataclass
class MonitoringConfig:
    """Monitoring and observability configuration"""
    enable_metrics: bool = field(default_factory=lambda: os.getenv("ENABLE_METRICS", "true").lower() == "true")
    metrics_port: int = field(default_factory=lambda: int(os.getenv("METRICS_PORT", "9090")))
    enable_tracing: bool = field(default_factory=lambda: os.getenv("ENABLE_TRACING", "false").lower() == "true")
    jaeger_endpoint: Optional[str] = field(default_factory=lambda: os.getenv("JAEGER_ENDPOINT"))
    prometheus_endpoint: Optional[str] = field(default_factory=lambda: os.getenv("PROMETHEUS_ENDPOINT"))
    health_check_interval: int = field(default_factory=lambda: int(os.getenv("HEALTH_CHECK_INTERVAL", "30")))

@dataclass
class StorageConfig:
    """Storage configuration"""
    file_storage_path: str = field(default_factory=lambda: os.getenv("FILE_STORAGE_PATH", "data/storage"))
    max_file_size: int = field(default_factory=lambda: int(os.getenv("MAX_FILE_SIZE", "52428800")))  # 50MB
    allowed_extensions: List[str] = field(default_factory=lambda: _parse_allowed_extensions())
    aws_s3_bucket: Optional[str] = field(default_factory=lambda: os.getenv("AWS_S3_BUCKET"))
    aws_access_key_id: Optional[str] = field(default_factory=lambda: os.getenv("AWS_ACCESS_KEY_ID"))
    aws_secret_access_key: Optional[str] = field(default_factory=lambda: os.getenv("AWS_SECRET_ACCESS_KEY"))
    aws_region: str = field(default_factory=lambda: os.getenv("AWS_REGION", "us-east-1"))

class Config:
    """Centralized configuration manager"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        self.app = ApplicationConfig()
        self.database = DatabaseConfig()
        self.redis = RedisConfig()
        self.security = SecurityConfig()
        self.api = APIConfig()
        self.framework = FrameworkConfig()
        self.monitoring = MonitoringConfig()
        self.storage = StorageConfig()
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration settings"""
        try:
            # Validate required settings for production
            if self.app.is_production():
                required_settings = [
                    (self.security.secret_key != "change-this-in-production", "SECRET_KEY must be set in production"),
                    (self.security.jwt_secret_key != "jwt-change-this-in-production", "JWT_SECRET_KEY must be set in production"),
                    (len(self.api.get_available_providers()) > 0, "At least one API provider must be configured"),
                ]
                
                for condition, message in required_settings:
                    if not condition:
                        raise ValueError(f"Production configuration error: {message}")
            
            # Create necessary directories
            directories = [
                self.framework.get_data_path(),
                Path(self.storage.file_storage_path)
            ]
            
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
            
            logger.info("Configuration validation completed successfully")
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            if self.app.is_production():
                raise
    
    def get_database_url(self) -> str:
        """Get database URL with fallback to SQLite for development"""
        if self.app.is_development() and not os.getenv("DATABASE_URL"):
            sqlite_path = Path("data/sentinel_grc.db")
            sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{sqlite_path.absolute()}"
        return self.database.url
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary for debugging (excludes secrets)"""
        config_dict = {
            "app": {
                "name": self.app.name,
                "version": self.app.version,
                "environment": self.app.environment.value,
                "debug": self.app.debug,
                "host": self.app.host,
                "port": self.app.port
            },
            "database": {
                "url": "***REDACTED***",
                "pool_size": self.database.pool_size
            },
            "redis": {
                "url": "***REDACTED***",
                "db": self.redis.db
            },
            "api": {
                "available_providers": self.api.get_available_providers(),
                "timeout": self.api.timeout_seconds
            },
            "framework": {
                "data_path": self.framework.data_path,
                "cache_enabled": self.framework.enable_caching
            }
        }
        return config_dict
    
    def __str__(self) -> str:
        """String representation of configuration"""
        return f"Config(environment={self.app.environment.value}, version={self.app.version})"

def _parse_cors_origins() -> List[str]:
    """Parse CORS origins from environment variable"""
    cors_origins_str = os.getenv("CORS_ORIGINS", "*")
    if cors_origins_str == "*":
        return ["*"]
    return [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

def _parse_allowed_extensions() -> List[str]:
    """Parse allowed file extensions from environment variable"""
    extensions_str = os.getenv("ALLOWED_EXTENSIONS", "json,csv,xlsx,pdf,txt")
    return [ext.strip().lower() for ext in extensions_str.split(",") if ext.strip()]

def load_config() -> Config:
    """Load and return configuration singleton"""
    if not hasattr(load_config, "_config"):
        load_config._config = Config()
    return load_config._config

def create_env_file_template(file_path: str = ".env.template"):
    """Create environment file template with all configuration options"""
    template = """
# Sentinel GRC Environment Configuration Template
# Copy this file to .env and customize for your environment

# Application Configuration
APP_NAME=Sentinel GRC
APP_VERSION=2.0.0
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
WORKERS=1
LOG_LEVEL=INFO
TIMEZONE=UTC

# Security Configuration
SECRET_KEY=change-this-to-a-strong-secret-key-in-production
JWT_SECRET_KEY=change-this-to-a-strong-jwt-secret-key-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
API_KEY_HEADER=X-API-Key
CORS_ORIGINS=*
RATE_LIMIT_PER_MINUTE=100
MAX_REQUEST_SIZE=16777216

# Database Configuration
DATABASE_URL=postgresql://localhost:5432/sentinel_grc
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_ECHO=false

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_MAX_CONNECTIONS=10
REDIS_SOCKET_TIMEOUT=5.0
REDIS_CONNECT_TIMEOUT=5.0
REDIS_RETRY_ON_TIMEOUT=true

# External API Configuration
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
OPENAI_MODEL=gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-haiku-20240307
API_TIMEOUT=30
API_MAX_RETRIES=3

# Framework Configuration
FRAMEWORK_DATA_PATH=data/frameworks
FRAMEWORK_CACHE_TTL=3600
ENABLE_FRAMEWORK_CACHING=true
ENABLE_FRAMEWORK_VALIDATION=true
FRAMEWORK_AUTO_UPDATE=false
OSCAL_ENDPOINT=https://pages.nist.gov/OSCAL
OLIR_ENDPOINT=https://csrc.nist.gov/Projects/olir

# Storage Configuration
FILE_STORAGE_PATH=data/storage
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=json,csv,xlsx,pdf,txt
AWS_S3_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
ENABLE_TRACING=false
JAEGER_ENDPOINT=
PROMETHEUS_ENDPOINT=
HEALTH_CHECK_INTERVAL=30

# Production-specific settings (uncomment for production)
# SECRET_KEY=generate-a-strong-random-secret-key
# JWT_SECRET_KEY=generate-a-strong-random-jwt-secret-key
# DATABASE_URL=postgresql://user:password@localhost:5432/sentinel_grc_prod
# REDIS_URL=redis://redis-server:6379
# CORS_ORIGINS=https://sentinelgrc.com,https://api.sentinelgrc.com
# DEBUG=false
# ENVIRONMENT=production
# LOG_LEVEL=WARNING
"""
    
    with open(file_path, 'w') as f:
        f.write(template.strip())
    
    logger.info(f"Environment template created at {file_path}")

# Global configuration instance
config = load_config()

if __name__ == "__main__":
    # Create environment template if run directly
    create_env_file_template()
    
    # Display current configuration
    print("Current Configuration:")
    print(json.dumps(config.get_config_dict(), indent=2))
    
    print(f"\nEnvironment: {config.app.environment.value}")
    print(f"Available API Providers: {config.api.get_available_providers()}")
    print(f"Database URL: {'SQLite (development)' if 'sqlite' in config.get_database_url() else 'PostgreSQL'}")
    print(f"Framework Data Path: {config.framework.get_data_path()}")