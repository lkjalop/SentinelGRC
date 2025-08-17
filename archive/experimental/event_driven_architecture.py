"""
Event-Driven Microservices Architecture for Sentinel GRC
========================================================
Implements pub/sub messaging, event sourcing, and service orchestration
Supports horizontal scaling and real-time framework updates
"""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid
from abc import ABC, abstractmethod
import aioredis
from concurrent.futures import ThreadPoolExecutor
import hashlib

logger = logging.getLogger(__name__)

class EventType(str, Enum):
    """Event types for the system"""
    FRAMEWORK_UPDATED = "framework.updated"
    ASSESSMENT_STARTED = "assessment.started" 
    ASSESSMENT_COMPLETED = "assessment.completed"
    MAPPING_GENERATED = "mapping.generated"
    DASHBOARD_REQUESTED = "dashboard.requested"
    COMPLIANCE_ALERT = "compliance.alert"
    USER_ACTION = "user.action"
    SYSTEM_HEALTH = "system.health"
    AUDIT_LOG = "audit.log"

class ServiceType(str, Enum):
    """Microservice types"""
    FRAMEWORK_SERVICE = "framework_service"
    ASSESSMENT_SERVICE = "assessment_service"
    MAPPING_SERVICE = "mapping_service"
    DASHBOARD_SERVICE = "dashboard_service"
    NOTIFICATION_SERVICE = "notification_service"
    AUDIT_SERVICE = "audit_service"

@dataclass
class Event:
    """Event model for pub/sub messaging"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = field(default=EventType.USER_ACTION)
    source_service: ServiceType = field(default=ServiceType.FRAMEWORK_SERVICE)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "source_service": self.source_service.value,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
            "correlation_id": self.correlation_id,
            "user_id": self.user_id,
            "organization_id": self.organization_id,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create event from dictionary"""
        return cls(
            event_id=data["event_id"],
            event_type=EventType(data["event_type"]),
            source_service=ServiceType(data["source_service"]),
            timestamp=datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00')),
            payload=data.get("payload", {}),
            correlation_id=data.get("correlation_id"),
            user_id=data.get("user_id"),
            organization_id=data.get("organization_id"),
            version=data.get("version", "1.0")
        )

class EventHandler(ABC):
    """Abstract base class for event handlers"""
    
    @abstractmethod
    async def handle(self, event: Event) -> Optional[Event]:
        """Handle event and optionally return response event"""
        pass
    
    @abstractmethod
    def can_handle(self, event: Event) -> bool:
        """Check if handler can process this event type"""
        pass

class EventBus:
    """Central event bus for pub/sub messaging"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client: Optional[aioredis.Redis] = None
        self.handlers: Dict[EventType, List[EventHandler]] = {}
        self.running = False
        self.subscriber_tasks: List[asyncio.Task] = []
    
    async def start(self):
        """Start the event bus"""
        try:
            self.redis_client = aioredis.from_url(
                self.redis_url, 
                decode_responses=True,
                retry_on_timeout=True
            )
            await self.redis_client.ping()
            self.running = True
            
            # Start subscriber tasks for each event type
            for event_type in EventType:
                task = asyncio.create_task(self._subscribe_to_events(event_type))
                self.subscriber_tasks.append(task)
            
            logger.info(f"Event bus started with {len(self.handlers)} handler types")
        except Exception as e:
            logger.error(f"Failed to start event bus: {e}")
            raise
    
    async def stop(self):
        """Stop the event bus"""
        self.running = False
        
        # Cancel subscriber tasks
        for task in self.subscriber_tasks:
            task.cancel()
        
        if self.subscriber_tasks:
            await asyncio.gather(*self.subscriber_tasks, return_exceptions=True)
        
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("Event bus stopped")
    
    def register_handler(self, event_type: EventType, handler: EventHandler):
        """Register event handler for specific event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"Registered handler for {event_type.value}")
    
    async def publish(self, event: Event) -> bool:
        """Publish event to Redis pub/sub"""
        try:
            if not self.redis_client or not self.running:
                logger.warning("Event bus not running, cannot publish event")
                return False
            
            channel = f"events:{event.event_type.value}"
            message = json.dumps(event.to_dict())
            
            # Publish to Redis
            result = await self.redis_client.publish(channel, message)
            
            # Also store in event store for audit
            await self._store_event(event)
            
            logger.debug(f"Published event {event.event_id} to {channel}")
            return result > 0
            
        except Exception as e:
            logger.error(f"Failed to publish event {event.event_id}: {e}")
            return False
    
    async def _subscribe_to_events(self, event_type: EventType):
        """Subscribe to events of specific type"""
        channel = f"events:{event_type.value}"
        
        try:
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe(channel)
            
            logger.info(f"Subscribed to channel: {channel}")
            
            async for message in pubsub.listen():
                if not self.running:
                    break
                
                if message["type"] == "message":
                    try:
                        event_data = json.loads(message["data"])
                        event = Event.from_dict(event_data)
                        
                        # Process event with registered handlers
                        await self._process_event(event)
                        
                    except Exception as e:
                        logger.error(f"Error processing event from {channel}: {e}")
        
        except asyncio.CancelledError:
            logger.info(f"Subscription to {channel} cancelled")
        except Exception as e:
            logger.error(f"Error in subscription to {channel}: {e}")
        finally:
            if 'pubsub' in locals():
                await pubsub.unsubscribe(channel)
                await pubsub.close()
    
    async def _process_event(self, event: Event):
        """Process event with registered handlers"""
        handlers = self.handlers.get(event.event_type, [])
        
        if not handlers:
            logger.debug(f"No handlers registered for {event.event_type.value}")
            return
        
        # Process handlers concurrently
        tasks = []
        for handler in handlers:
            if handler.can_handle(event):
                task = asyncio.create_task(self._handle_event_safely(handler, event))
                tasks.append(task)
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Publish any response events
            for result in results:
                if isinstance(result, Event):
                    await self.publish(result)
    
    async def _handle_event_safely(self, handler: EventHandler, event: Event) -> Optional[Event]:
        """Handle event with error handling"""
        try:
            return await handler.handle(event)
        except Exception as e:
            logger.error(f"Handler {handler.__class__.__name__} failed for event {event.event_id}: {e}")
            
            # Publish error event
            error_event = Event(
                event_type=EventType.SYSTEM_HEALTH,
                source_service=ServiceType.FRAMEWORK_SERVICE,
                payload={
                    "error": str(e),
                    "failed_handler": handler.__class__.__name__,
                    "original_event_id": event.event_id
                },
                correlation_id=event.correlation_id
            )
            return error_event
    
    async def _store_event(self, event: Event):
        """Store event in event store for audit and replay"""
        try:
            event_key = f"event_store:{event.event_id}"
            event_data = json.dumps(event.to_dict())
            
            # Store with TTL (30 days)
            await self.redis_client.setex(event_key, 2592000, event_data)
            
            # Add to timeline
            timeline_key = f"timeline:{datetime.now().strftime('%Y-%m-%d')}"
            await self.redis_client.zadd(
                timeline_key, 
                {event.event_id: event.timestamp.timestamp()}
            )
            
        except Exception as e:
            logger.warning(f"Failed to store event {event.event_id}: {e}")

class MicroserviceBase:
    """Base class for microservices"""
    
    def __init__(self, service_type: ServiceType, event_bus: EventBus):
        self.service_type = service_type
        self.event_bus = event_bus
        self.service_id = f"{service_type.value}_{uuid.uuid4().hex[:8]}"
        self.running = False
        self.health_check_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the microservice"""
        self.running = True
        await self._register_handlers()
        
        # Start health check
        self.health_check_task = asyncio.create_task(self._health_check_loop())
        
        logger.info(f"Microservice {self.service_id} started")
    
    async def stop(self):
        """Stop the microservice"""
        self.running = False
        
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"Microservice {self.service_id} stopped")
    
    async def _register_handlers(self):
        """Register event handlers - override in subclasses"""
        pass
    
    async def _health_check_loop(self):
        """Periodic health check"""
        while self.running:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                if self.running:
                    health_event = Event(
                        event_type=EventType.SYSTEM_HEALTH,
                        source_service=self.service_type,
                        payload={
                            "service_id": self.service_id,
                            "status": "healthy",
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                    )
                    await self.event_bus.publish(health_event)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check failed for {self.service_id}: {e}")

# Specific Handlers
class FrameworkUpdateHandler(EventHandler):
    """Handler for framework update events"""
    
    def __init__(self, framework_integrators: Dict[str, Any]):
        self.framework_integrators = framework_integrators
    
    def can_handle(self, event: Event) -> bool:
        return event.event_type == EventType.FRAMEWORK_UPDATED
    
    async def handle(self, event: Event) -> Optional[Event]:
        """Handle framework update"""
        try:
            framework_name = event.payload.get("framework_name")
            update_type = event.payload.get("update_type", "data_refresh")
            
            logger.info(f"Processing framework update: {framework_name} ({update_type})")
            
            # Refresh framework data
            if framework_name in self.framework_integrators:
                integrator = self.framework_integrators[framework_name]
                
                # Force refresh if supported
                if hasattr(integrator, 'refresh_data'):
                    await asyncio.to_thread(integrator.refresh_data)
                
                # Clear caches if supported
                if hasattr(integrator, 'clear_cache'):
                    await asyncio.to_thread(integrator.clear_cache)
            
            # Return completion event
            return Event(
                event_type=EventType.USER_ACTION,
                source_service=ServiceType.FRAMEWORK_SERVICE,
                payload={
                    "action": "framework_refreshed",
                    "framework_name": framework_name,
                    "status": "success"
                },
                correlation_id=event.correlation_id
            )
            
        except Exception as e:
            logger.error(f"Failed to handle framework update: {e}")
            raise

class AssessmentHandler(EventHandler):
    """Handler for assessment events"""
    
    def __init__(self, harmonization_reporter):
        self.harmonization_reporter = harmonization_reporter
    
    def can_handle(self, event: Event) -> bool:
        return event.event_type in [EventType.ASSESSMENT_STARTED, EventType.ASSESSMENT_COMPLETED]
    
    async def handle(self, event: Event) -> Optional[Event]:
        """Handle assessment events"""
        try:
            if event.event_type == EventType.ASSESSMENT_STARTED:
                return await self._handle_assessment_started(event)
            elif event.event_type == EventType.ASSESSMENT_COMPLETED:
                return await self._handle_assessment_completed(event)
        except Exception as e:
            logger.error(f"Assessment handler failed: {e}")
            raise
    
    async def _handle_assessment_started(self, event: Event) -> Optional[Event]:
        """Handle assessment start"""
        assessment_id = event.payload.get("assessment_id")
        organization = event.payload.get("organization")
        
        logger.info(f"Assessment started: {assessment_id} for {organization}")
        
        # Could trigger notifications, logging, etc.
        return None
    
    async def _handle_assessment_completed(self, event: Event) -> Optional[Event]:
        """Handle assessment completion"""
        assessment_id = event.payload.get("assessment_id")
        results = event.payload.get("results", {})
        
        logger.info(f"Assessment completed: {assessment_id}")
        
        # Could trigger report generation, notifications, etc.
        return Event(
            event_type=EventType.AUDIT_LOG,
            source_service=ServiceType.AUDIT_SERVICE,
            payload={
                "action": "assessment_completed",
                "assessment_id": assessment_id,
                "compliance_score": results.get("overall_compliance_score", 0),
                "frameworks": results.get("frameworks_assessed", [])
            },
            correlation_id=event.correlation_id,
            user_id=event.user_id,
            organization_id=event.organization_id
        )

class NotificationHandler(EventHandler):
    """Handler for notification events"""
    
    def can_handle(self, event: Event) -> bool:
        return event.event_type == EventType.COMPLIANCE_ALERT
    
    async def handle(self, event: Event) -> Optional[Event]:
        """Handle notification events"""
        try:
            alert_type = event.payload.get("alert_type")
            severity = event.payload.get("severity", "medium")
            message = event.payload.get("message")
            
            logger.info(f"Compliance alert: {alert_type} ({severity})")
            
            # In production, this would send emails, Slack messages, etc.
            notification_methods = event.payload.get("notification_methods", ["email"])
            
            for method in notification_methods:
                await self._send_notification(method, alert_type, severity, message, event)
            
            return Event(
                event_type=EventType.AUDIT_LOG,
                source_service=ServiceType.NOTIFICATION_SERVICE,
                payload={
                    "action": "notification_sent",
                    "alert_type": alert_type,
                    "severity": severity,
                    "methods": notification_methods
                },
                correlation_id=event.correlation_id
            )
            
        except Exception as e:
            logger.error(f"Notification handler failed: {e}")
            raise
    
    async def _send_notification(self, method: str, alert_type: str, severity: str, message: str, event: Event):
        """Send notification via specific method"""
        # Placeholder for actual notification sending
        logger.info(f"Sending {method} notification: {alert_type} - {message}")

# Service Implementations
class FrameworkService(MicroserviceBase):
    """Framework management microservice"""
    
    def __init__(self, event_bus: EventBus, framework_integrators: Dict[str, Any]):
        super().__init__(ServiceType.FRAMEWORK_SERVICE, event_bus)
        self.framework_integrators = framework_integrators
    
    async def _register_handlers(self):
        """Register framework-specific handlers"""
        framework_handler = FrameworkUpdateHandler(self.framework_integrators)
        self.event_bus.register_handler(EventType.FRAMEWORK_UPDATED, framework_handler)

class AssessmentService(MicroserviceBase):
    """Assessment processing microservice"""
    
    def __init__(self, event_bus: EventBus, harmonization_reporter):
        super().__init__(ServiceType.ASSESSMENT_SERVICE, event_bus)
        self.harmonization_reporter = harmonization_reporter
    
    async def _register_handlers(self):
        """Register assessment-specific handlers"""
        assessment_handler = AssessmentHandler(self.harmonization_reporter)
        self.event_bus.register_handler(EventType.ASSESSMENT_STARTED, assessment_handler)
        self.event_bus.register_handler(EventType.ASSESSMENT_COMPLETED, assessment_handler)

class NotificationService(MicroserviceBase):
    """Notification microservice"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__(ServiceType.NOTIFICATION_SERVICE, event_bus)
    
    async def _register_handlers(self):
        """Register notification-specific handlers"""
        notification_handler = NotificationHandler()
        self.event_bus.register_handler(EventType.COMPLIANCE_ALERT, notification_handler)

class ServiceOrchestrator:
    """Orchestrates multiple microservices"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.event_bus = EventBus(redis_url)
        self.services: List[MicroserviceBase] = []
        self.running = False
    
    def add_service(self, service: MicroserviceBase):
        """Add microservice to orchestrator"""
        self.services.append(service)
        logger.info(f"Added service: {service.service_id}")
    
    async def start(self):
        """Start all services"""
        try:
            # Start event bus first
            await self.event_bus.start()
            
            # Start all services
            for service in self.services:
                await service.start()
            
            self.running = True
            logger.info(f"Service orchestrator started with {len(self.services)} services")
            
        except Exception as e:
            logger.error(f"Failed to start service orchestrator: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Stop all services"""
        self.running = False
        
        # Stop services
        for service in self.services:
            try:
                await service.stop()
            except Exception as e:
                logger.error(f"Error stopping service {service.service_id}: {e}")
        
        # Stop event bus
        await self.event_bus.stop()
        logger.info("Service orchestrator stopped")
    
    async def get_service_health(self) -> Dict[str, Any]:
        """Get health status of all services"""
        health_status = {
            "orchestrator_running": self.running,
            "event_bus_running": self.event_bus.running,
            "services": []
        }
        
        for service in self.services:
            health_status["services"].append({
                "service_id": service.service_id,
                "service_type": service.service_type.value,
                "running": service.running
            })
        
        return health_status

async def setup_microservices(framework_integrators: Dict[str, Any], redis_url: str = "redis://localhost:6379") -> ServiceOrchestrator:
    """Set up and configure microservices architecture"""
    try:
        orchestrator = ServiceOrchestrator(redis_url)
        
        # Create services
        framework_service = FrameworkService(orchestrator.event_bus, framework_integrators)
        assessment_service = AssessmentService(orchestrator.event_bus, framework_integrators.get("harmonization"))
        notification_service = NotificationService(orchestrator.event_bus)
        
        # Add services to orchestrator
        orchestrator.add_service(framework_service)
        orchestrator.add_service(assessment_service)
        orchestrator.add_service(notification_service)
        
        return orchestrator
        
    except Exception as e:
        logger.error(f"Failed to setup microservices: {e}")
        raise

# Example usage and testing
async def test_event_driven_architecture():
    """Test the event-driven architecture"""
    logger.info("Testing event-driven architecture...")
    
    try:
        # Mock framework integrators for testing
        framework_integrators = {
            "nist_csf": type('MockIntegrator', (), {
                'refresh_data': lambda: logger.info("Refreshing NIST CSF data"),
                'clear_cache': lambda: logger.info("Clearing NIST CSF cache")
            })(),
            "harmonization": type('MockHarmonization', (), {
                'generate_analysis': lambda frameworks, org_size: {"score": 85}
            })()
        }
        
        # Setup microservices
        orchestrator = await setup_microservices(framework_integrators)
        
        # Start services
        await orchestrator.start()
        
        # Test event publishing
        test_event = Event(
            event_type=EventType.FRAMEWORK_UPDATED,
            source_service=ServiceType.FRAMEWORK_SERVICE,
            payload={
                "framework_name": "nist_csf",
                "update_type": "data_refresh"
            }
        )
        
        success = await orchestrator.event_bus.publish(test_event)
        logger.info(f"Test event published: {success}")
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Check service health
        health = await orchestrator.get_service_health()
        logger.info(f"Service health: {health}")
        
        # Stop services
        await orchestrator.stop()
        
        logger.info("Event-driven architecture test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Event-driven architecture test failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run test
    try:
        result = asyncio.run(test_event_driven_architecture())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        sys.exit(1)