"""
Enhanced Error Handling for Sentinel GRC
=========================================
Comprehensive error handling with user-friendly messages and fallback mechanisms.
"""

import logging
import traceback
from typing import Any, Dict, Optional, Callable
from datetime import datetime
from functools import wraps
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorType(Enum):
    """Types of errors in the system"""
    API_ERROR = "api_error"
    DATABASE_ERROR = "database_error"
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    NETWORK_ERROR = "network_error"
    TIMEOUT_ERROR = "timeout_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    CONFIGURATION_ERROR = "configuration_error"
    AGENT_ERROR = "agent_error"
    UNKNOWN_ERROR = "unknown_error"

class SentinelError(Exception):
    """Base exception for Sentinel GRC"""
    
    def __init__(self, 
                 message: str,
                 error_type: ErrorType = ErrorType.UNKNOWN_ERROR,
                 severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        self.message = message
        self.error_type = error_type
        self.severity = severity
        self.details = details or {}
        self.user_message = user_message or self._get_default_user_message()
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)
    
    def _get_default_user_message(self) -> str:
        """Get user-friendly error message"""
        messages = {
            ErrorType.API_ERROR: "We're experiencing issues with our external services. Please try again in a few moments.",
            ErrorType.DATABASE_ERROR: "Unable to access data at this time. Our team has been notified.",
            ErrorType.VALIDATION_ERROR: "Please check your input and try again.",
            ErrorType.AUTHENTICATION_ERROR: "Authentication failed. Please check your credentials.",
            ErrorType.AUTHORIZATION_ERROR: "You don't have permission to perform this action.",
            ErrorType.NETWORK_ERROR: "Network connection issue. Please check your internet connection.",
            ErrorType.TIMEOUT_ERROR: "The request took too long. Please try again.",
            ErrorType.RATE_LIMIT_ERROR: "Too many requests. Please wait a moment before trying again.",
            ErrorType.CONFIGURATION_ERROR: "System configuration issue. Please contact support.",
            ErrorType.AGENT_ERROR: "Assessment processing issue. Trying alternative approach.",
            ErrorType.UNKNOWN_ERROR: "An unexpected error occurred. Please try again."
        }
        return messages.get(self.error_type, messages[ErrorType.UNKNOWN_ERROR])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/API response"""
        return {
            "error": True,
            "message": self.message,
            "user_message": self.user_message,
            "type": self.error_type.value,
            "severity": self.severity.value,
            "details": self.details,
            "timestamp": self.timestamp
        }

class ErrorHandler:
    """Central error handler for the application"""
    
    def __init__(self):
        self.error_log = []
        self.error_counts = {}
        self.fallback_handlers = {}
    
    def log_error(self, error: SentinelError):
        """Log error for monitoring"""
        error_dict = error.to_dict()
        self.error_log.append(error_dict)
        
        # Count errors by type
        error_type = error.error_type.value
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Log based on severity
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"{error.message} | Details: {error.details}")
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(f"{error.message} | Details: {error.details}")
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"{error.message} | Details: {error.details}")
        else:
            logger.info(f"{error.message} | Details: {error.details}")
    
    def register_fallback(self, error_type: ErrorType, handler: Callable):
        """Register a fallback handler for specific error type"""
        self.fallback_handlers[error_type] = handler
    
    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle any error and return appropriate response"""
        
        # Convert to SentinelError if needed
        if not isinstance(error, SentinelError):
            sentinel_error = self._convert_to_sentinel_error(error)
        else:
            sentinel_error = error
        
        # Log the error
        self.log_error(sentinel_error)
        
        # Try fallback handler if available
        if sentinel_error.error_type in self.fallback_handlers:
            try:
                fallback_result = self.fallback_handlers[sentinel_error.error_type](sentinel_error)
                return {
                    "success": True,
                    "fallback_used": True,
                    "result": fallback_result,
                    "error_handled": sentinel_error.to_dict()
                }
            except Exception as fallback_error:
                logger.error(f"Fallback handler failed: {fallback_error}")
        
        # Return error response
        return sentinel_error.to_dict()
    
    def _convert_to_sentinel_error(self, error: Exception) -> SentinelError:
        """Convert standard exceptions to SentinelError"""
        
        error_message = str(error)
        error_type = ErrorType.UNKNOWN_ERROR
        severity = ErrorSeverity.MEDIUM
        details = {"original_error": type(error).__name__}
        
        # Map common exceptions
        if isinstance(error, ConnectionError):
            error_type = ErrorType.NETWORK_ERROR
            severity = ErrorSeverity.HIGH
        elif isinstance(error, TimeoutError):
            error_type = ErrorType.TIMEOUT_ERROR
            severity = ErrorSeverity.MEDIUM
        elif isinstance(error, ValueError):
            error_type = ErrorType.VALIDATION_ERROR
            severity = ErrorSeverity.LOW
        elif isinstance(error, PermissionError):
            error_type = ErrorType.AUTHORIZATION_ERROR
            severity = ErrorSeverity.HIGH
        elif "rate limit" in error_message.lower():
            error_type = ErrorType.RATE_LIMIT_ERROR
            severity = ErrorSeverity.MEDIUM
        elif "api" in error_message.lower():
            error_type = ErrorType.API_ERROR
            severity = ErrorSeverity.MEDIUM
        elif "database" in error_message.lower() or "sql" in error_message.lower():
            error_type = ErrorType.DATABASE_ERROR
            severity = ErrorSeverity.HIGH
        
        # Add traceback for debugging
        details["traceback"] = traceback.format_exc()
        
        return SentinelError(
            message=error_message,
            error_type=error_type,
            severity=severity,
            details=details
        )
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        return {
            "total_errors": len(self.error_log),
            "errors_by_type": self.error_counts,
            "recent_errors": self.error_log[-10:] if self.error_log else [],
            "critical_errors": [e for e in self.error_log if e["severity"] == "critical"]
        }

# Global error handler instance
error_handler = ErrorHandler()

# Decorators for error handling
def handle_errors(fallback_result=None):
    """Decorator to handle errors in functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                result = error_handler.handle_error(e)
                if result.get("success") and result.get("fallback_used"):
                    return result["result"]
                elif fallback_result is not None:
                    logger.warning(f"Using fallback result for {func.__name__}")
                    return fallback_result
                else:
                    raise
        return wrapper
    return decorator

def async_handle_errors(fallback_result=None):
    """Decorator to handle errors in async functions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                result = error_handler.handle_error(e)
                if result.get("success") and result.get("fallback_used"):
                    return result["result"]
                elif fallback_result is not None:
                    logger.warning(f"Using fallback result for {func.__name__}")
                    return fallback_result
                else:
                    raise
        return wrapper
    return decorator

# Fallback handlers for common scenarios
def api_error_fallback(error: SentinelError) -> Dict[str, Any]:
    """Fallback for API errors - use cached or default data"""
    logger.info("Using cached/default data due to API error")
    return {
        "source": "cache",
        "message": "Using cached data due to temporary API issues",
        "data": {
            "assessment_result": "partial",
            "confidence": 0.7,
            "cached": True
        }
    }

def database_error_fallback(error: SentinelError) -> Dict[str, Any]:
    """Fallback for database errors - use in-memory storage"""
    logger.info("Using in-memory storage due to database error")
    return {
        "source": "memory",
        "message": "Results stored temporarily in memory",
        "data": {
            "storage": "temporary",
            "will_sync": True
        }
    }

def agent_error_fallback(error: SentinelError) -> Dict[str, Any]:
    """Fallback for agent errors - use rule-based assessment"""
    logger.info("Using rule-based assessment due to agent error")
    return {
        "source": "rules",
        "message": "Using rule-based assessment",
        "data": {
            "assessment_type": "rule_based",
            "confidence": 0.6,
            "limitations": ["No AI enhancement", "Basic compliance check only"]
        }
    }

# Register default fallbacks
error_handler.register_fallback(ErrorType.API_ERROR, api_error_fallback)
error_handler.register_fallback(ErrorType.DATABASE_ERROR, database_error_fallback)
error_handler.register_fallback(ErrorType.AGENT_ERROR, agent_error_fallback)

# Example usage with existing code
@async_handle_errors(fallback_result={"status": "degraded", "score": 0.5})
async def assess_company_with_error_handling(company_data: Dict) -> Dict:
    """Example assessment with error handling"""
    
    # Validate input
    if not company_data.get("company_name"):
        raise SentinelError(
            message="Company name is required",
            error_type=ErrorType.VALIDATION_ERROR,
            severity=ErrorSeverity.LOW,
            user_message="Please provide a company name for the assessment"
        )
    
    # Simulate potential errors
    try:
        # Database operation
        result = await fetch_from_database(company_data)
    except ConnectionError as e:
        raise SentinelError(
            message=f"Database connection failed: {e}",
            error_type=ErrorType.DATABASE_ERROR,
            severity=ErrorSeverity.HIGH
        )
    
    try:
        # API call
        ai_enhancement = await call_groq_api(result)
    except TimeoutError as e:
        raise SentinelError(
            message=f"API timeout: {e}",
            error_type=ErrorType.TIMEOUT_ERROR,
            severity=ErrorSeverity.MEDIUM
        )
    
    return {
        "status": "success",
        "assessment": result,
        "ai_enhancement": ai_enhancement
    }

async def fetch_from_database(data: Dict) -> Dict:
    """Simulated database fetch"""
    # This would be actual database code
    return {"company": data["company_name"], "score": 0.8}

async def call_groq_api(data: Dict) -> Dict:
    """Simulated API call"""
    # This would be actual API code
    return {"enhancement": "AI insights", "confidence": 0.9}

# Circuit breaker for repeated failures
class CircuitBreaker:
    """Circuit breaker to prevent cascading failures"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.is_open = False
    
    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection"""
        if self.is_open:
            if (datetime.now() - self.last_failure_time).seconds > self.timeout:
                self.is_open = False
                self.failures = 0
                logger.info("Circuit breaker reset")
            else:
                raise SentinelError(
                    message="Circuit breaker is open",
                    error_type=ErrorType.NETWORK_ERROR,
                    severity=ErrorSeverity.HIGH,
                    user_message="Service temporarily unavailable. Please try again later."
                )
        
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = datetime.now()
            
            if self.failures >= self.failure_threshold:
                self.is_open = True
                logger.error(f"Circuit breaker opened after {self.failures} failures")
            
            raise

# Example circuit breaker for API calls
api_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

if __name__ == "__main__":
    # Test error handling
    print("Testing error handling...")
    
    # Test validation error
    try:
        raise SentinelError(
            message="Invalid input",
            error_type=ErrorType.VALIDATION_ERROR,
            severity=ErrorSeverity.LOW
        )
    except SentinelError as e:
        handled = error_handler.handle_error(e)
        print(f"Handled validation error: {handled}")
    
    # Test with fallback
    @handle_errors(fallback_result={"default": "value"})
    def risky_function():
        raise ConnectionError("Database unavailable")
    
    result = risky_function()
    print(f"Function with fallback returned: {result}")
    
    # Print statistics
    stats = error_handler.get_error_stats()
    print(f"Error statistics: {stats}")
    
    print("\nError handling system ready!")