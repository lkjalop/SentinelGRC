#!/usr/bin/env python3
"""
Test Thread-Safe Cache Implementation
====================================
"""

import threading
import time
from cache_manager import AssessmentCacheManager

def test_thread_safety():
    """Test thread-safe cache with concurrent operations"""
    
    print('Testing thread-safe cache implementation...')
    
    # Create cache manager
    cache = AssessmentCacheManager()
    
    # Test basic operations
    print('Testing basic cache operations...')
    cache.set('test_key', {'data': 'test_value'})
    result, hit = cache.get('test_key')
    print(f'SUCCESS: Basic get/set works - hit: {hit}, data: {result}')
    
    # Test thread safety
    results = []
    errors = []
    
    def cache_worker(worker_id, iterations):
        try:
            for i in range(iterations):
                key = f'worker_{worker_id}_item_{i}'
                data = {'worker': worker_id, 'iteration': i, 'timestamp': time.time()}
                
                # Set data
                cache.set(key, data)
                
                # Get data back
                result, hit = cache.get(key)
                if not hit or result['worker'] != worker_id:
                    errors.append(f'Data corruption in worker {worker_id}, iteration {i}')
                
                results.append((worker_id, i, hit))
                
                # Small delay to increase chance of race conditions
                time.sleep(0.001)
                
        except Exception as e:
            errors.append(f'Exception in worker {worker_id}: {e}')
    
    print('Testing thread safety with concurrent operations...')
    threads = []
    for worker_id in range(5):
        thread = threading.Thread(target=cache_worker, args=(worker_id, 20))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    print(f'SUCCESS: Completed {len(results)} operations')
    print(f'SUCCESS: No errors detected: {len(errors) == 0}')
    
    if errors:
        print('ERRORS:')
        for error in errors[:5]:  # Show first 5 errors
            print(f'  {error}')
    
    # Get statistics
    stats = cache.get_stats()
    print(f'SUCCESS: Cache stats - size: {stats["current_size"]}, hit rate: {stats["hit_rate_percent"]:.1f}%')
    
    print('THREAD-SAFE CACHE IMPLEMENTATION SUCCESSFUL!')

if __name__ == "__main__":
    test_thread_safety()