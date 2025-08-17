"""
Thread-Safe Cache Manager for Sentinel GRC
==========================================

Enterprise-grade caching system with zero external dependencies.
Provides thread-safe operations and automatic cleanup for production use.
"""

import threading
import time
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple, List
from dataclasses import dataclass
import json
import weakref

@dataclass
class CacheEntry:
    """Thread-safe cache entry with metadata"""
    data: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int
    ttl_seconds: Optional[int] = None
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        if self.ttl_seconds is None:
            return False
        
        age_seconds = (datetime.now() - self.created_at).total_seconds()
        return age_seconds > self.ttl_seconds
    
    def touch(self):
        """Update last accessed time and increment access count"""
        self.last_accessed = datetime.now()
        self.access_count += 1

class ThreadSafeCacheManager:
    """
    Thread-safe cache manager for compliance assessments.
    
    Features:
    - Thread-safe read/write operations using RWLock pattern
    - Automatic TTL-based expiration
    - LRU eviction when cache size limit is reached
    - Memory usage monitoring
    - Statistical reporting for performance optimization
    """
    
    def __init__(self, max_size: int = 1000, default_ttl_seconds: int = 3600):
        self.max_size = max_size
        self.default_ttl_seconds = default_ttl_seconds
        
        # Cache storage
        self._cache: Dict[str, CacheEntry] = {}
        
        # Thread safety using reader-writer lock pattern
        self._lock = threading.RLock()  # Reentrant lock for nested calls
        self._readers = 0
        self._writers = 0
        self._read_ready = threading.Condition(self._lock)
        self._write_ready = threading.Condition(self._lock)
        
        # Statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0,
            "size_limit_reached": 0
        }
        
        # Cleanup tracking
        self._last_cleanup = datetime.now()
        self._cleanup_interval_seconds = 300  # 5 minutes
    
    def _acquire_read_lock(self):
        """Acquire read lock (multiple readers allowed)"""
        self._lock.acquire()
        try:
            while self._writers > 0:
                self._read_ready.wait()
            self._readers += 1
        finally:
            self._lock.release()
    
    def _release_read_lock(self):
        """Release read lock"""
        self._lock.acquire()
        try:
            self._readers -= 1
            if self._readers == 0:
                self._write_ready.notify_all()
        finally:
            self._lock.release()
    
    def _acquire_write_lock(self):
        """Acquire write lock (exclusive)"""
        self._lock.acquire()
        try:
            while self._readers > 0 or self._writers > 0:
                self._write_ready.wait()
            self._writers += 1
        finally:
            self._lock.release()
    
    def _release_write_lock(self):
        """Release write lock"""
        self._lock.acquire()
        try:
            self._writers -= 1
            self._read_ready.notify_all()
            self._write_ready.notify_all()
        finally:
            self._lock.release()
    
    def _generate_cache_key(self, data: Any) -> str:
        """Generate secure cache key from data"""
        if isinstance(data, dict):
            # Sort keys for consistent hashing
            sorted_data = json.dumps(data, sort_keys=True, default=str)
        else:
            sorted_data = str(data)
        
        # Use SHA-256 instead of MD5 for security
        return hashlib.sha256(sorted_data.encode('utf-8')).hexdigest()
    
    def _cleanup_expired_entries(self):
        """Clean up expired entries (must be called with write lock)"""
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self._cache.items():
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._cache[key]
            self._stats["expirations"] += 1
        
        self._last_cleanup = current_time
    
    def _evict_lru_entries(self, count: int):
        """Evict least recently used entries (must be called with write lock)"""
        if count <= 0 or not self._cache:
            return
        
        # Sort by last accessed time (oldest first)
        sorted_entries = sorted(
            self._cache.items(),
            key=lambda x: x[1].last_accessed
        )
        
        for i in range(min(count, len(sorted_entries))):
            key, _ = sorted_entries[i]
            del self._cache[key]
            self._stats["evictions"] += 1
    
    def get(self, key: str) -> Tuple[Optional[Any], bool]:
        """
        Get value from cache.
        Returns (value, hit) tuple where hit indicates if value was found.
        """
        self._acquire_read_lock()
        try:
            if key not in self._cache:
                self._stats["misses"] += 1
                return None, False
            
            entry = self._cache[key]
            if entry.is_expired():
                # Don't return expired entries, but let cleanup handle removal
                self._stats["misses"] += 1
                return None, False
            
            # Update access statistics
            entry.touch()
            self._stats["hits"] += 1
            return entry.data, True
            
        finally:
            self._release_read_lock()
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """
        Set value in cache.
        Returns True if successful, False if failed.
        """
        self._acquire_write_lock()
        try:
            # Perform periodic cleanup
            if (datetime.now() - self._last_cleanup).total_seconds() > self._cleanup_interval_seconds:
                self._cleanup_expired_entries()
            
            # Check if we need to make space
            if len(self._cache) >= self.max_size:
                if key not in self._cache:  # Only evict if it's a new entry
                    self._evict_lru_entries(1)
                    self._stats["size_limit_reached"] += 1
            
            # Create cache entry
            entry = CacheEntry(
                data=value,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=0,
                ttl_seconds=ttl_seconds or self.default_ttl_seconds
            )
            
            self._cache[key] = entry
            return True
            
        finally:
            self._release_write_lock()
    
    def delete(self, key: str) -> bool:
        """Delete entry from cache. Returns True if entry existed."""
        self._acquire_write_lock()
        try:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
        finally:
            self._release_write_lock()
    
    def clear(self):
        """Clear all cache entries"""
        self._acquire_write_lock()
        try:
            self._cache.clear()
        finally:
            self._release_write_lock()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        self._acquire_read_lock()
        try:
            current_size = len(self._cache)
            total_requests = self._stats["hits"] + self._stats["misses"]
            hit_rate = (self._stats["hits"] / total_requests) if total_requests > 0 else 0
            
            return {
                "current_size": current_size,
                "max_size": self.max_size,
                "utilization_percent": (current_size / self.max_size) * 100,
                "hit_rate_percent": hit_rate * 100,
                "total_requests": total_requests,
                **self._stats,
                "memory_efficiency": self._calculate_memory_efficiency()
            }
        finally:
            self._release_read_lock()
    
    def _calculate_memory_efficiency(self) -> Dict[str, float]:
        """Calculate memory efficiency metrics"""
        if not self._cache:
            return {"average_access_count": 0, "cache_effectiveness": 0}
        
        total_access_count = sum(entry.access_count for entry in self._cache.values())
        average_access = total_access_count / len(self._cache)
        
        # Cache effectiveness: average accesses per entry
        # Higher is better (entries being reused)
        effectiveness = min(100, (average_access - 1) * 20)  # Scale to 0-100
        
        return {
            "average_access_count": average_access,
            "cache_effectiveness_percent": max(0, effectiveness)
        }
    
    def optimize(self):
        """Perform cache optimization (cleanup expired, rebalance)"""
        self._acquire_write_lock()
        try:
            self._cleanup_expired_entries()
            
            # If still over capacity, evict least used entries
            if len(self._cache) > self.max_size * 0.9:  # 90% threshold
                evict_count = int(self.max_size * 0.1)  # Evict 10%
                self._evict_lru_entries(evict_count)
        finally:
            self._release_write_lock()


class AssessmentCacheManager(ThreadSafeCacheManager):
    """
    Specialized cache manager for compliance assessments.
    Provides assessment-specific caching logic and optimizations.
    """
    
    def __init__(self):
        # 1 hour TTL, max 500 assessments
        super().__init__(max_size=500, default_ttl_seconds=3600)
    
    def cache_assessment(self, 
                        company_profile: Any, 
                        frameworks: List[str], 
                        assessment_result: Any,
                        ttl_hours: int = 1) -> str:
        """
        Cache assessment result with intelligent key generation.
        Returns cache key for reference.
        """
        cache_data = {
            "company_name": company_profile.company_name if hasattr(company_profile, 'company_name') else str(company_profile),
            "industry": company_profile.industry if hasattr(company_profile, 'industry') else "unknown",
            "employee_count": company_profile.employee_count if hasattr(company_profile, 'employee_count') else 0,
            "frameworks": sorted(frameworks) if frameworks else [],
            "timestamp": datetime.now().isoformat()
        }
        
        cache_key = self._generate_cache_key(cache_data)
        ttl_seconds = ttl_hours * 3600
        
        success = self.set(cache_key, assessment_result, ttl_seconds)
        return cache_key if success else None
    
    def get_cached_assessment(self, 
                             company_profile: Any, 
                             frameworks: List[str]) -> Tuple[Optional[Any], str]:
        """
        Get cached assessment if available.
        Returns (assessment_result, cache_key) tuple.
        """
        cache_data = {
            "company_name": company_profile.company_name if hasattr(company_profile, 'company_name') else str(company_profile),
            "industry": company_profile.industry if hasattr(company_profile, 'industry') else "unknown",
            "employee_count": company_profile.employee_count if hasattr(company_profile, 'employee_count') else 0,
            "frameworks": sorted(frameworks) if frameworks else [],
            "timestamp": datetime.now().isoformat()
        }
        
        cache_key = self._generate_cache_key(cache_data)
        result, hit = self.get(cache_key)
        
        return (result, cache_key) if hit else (None, cache_key)
    
    def invalidate_company_assessments(self, company_name: str):
        """Invalidate all cached assessments for a specific company"""
        self._acquire_write_lock()
        try:
            keys_to_remove = []
            for key, entry in self._cache.items():
                # This is a simplified approach - in production, you'd want
                # more sophisticated key pattern matching
                try:
                    if hasattr(entry.data, 'company_name') and entry.data.company_name == company_name:
                        keys_to_remove.append(key)
                except:
                    pass  # Skip entries that don't have company_name
            
            for key in keys_to_remove:
                del self._cache[key]
                
        finally:
            self._release_write_lock()

# Global instance for use across the application
assessment_cache = AssessmentCacheManager()

def get_cache_manager() -> AssessmentCacheManager:
    """Get the global assessment cache manager instance"""
    return assessment_cache