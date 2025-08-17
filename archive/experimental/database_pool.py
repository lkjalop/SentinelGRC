"""
Enterprise Database Connection Pool Manager
Implements connection pooling for high-performance database operations
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
import asyncpg
import psycopg2
from psycopg2 import pool
from sqlalchemy import create_engine, pool as sa_pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import time
from config_manager import config

logger = logging.getLogger(__name__)


class DatabasePoolManager:
    """Manages database connection pools for different database types"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._pools: Dict[str, Any] = {}
        self._metrics = ConnectionPoolMetrics()
        
        # Initialize pools based on configuration
        self._initialize_pools()
    
    def _initialize_pools(self):
        """Initialize connection pools based on configuration"""
        try:
            # PostgreSQL sync pool
            self._init_postgres_sync_pool()
            
            # PostgreSQL async pool
            asyncio.create_task(self._init_postgres_async_pool())
            
            # SQLAlchemy pools
            self._init_sqlalchemy_pools()
            
            logger.info("Database connection pools initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database pools: {e}")
            raise
    
    def _init_postgres_sync_pool(self):
        """Initialize synchronous PostgreSQL connection pool"""
        try:
            dsn = f"host={config.database.host} port={config.database.port} " \
                  f"dbname={config.database.database} user={config.database.username} " \
                  f"password={config.database.password}"
            
            self._pools['postgres_sync'] = psycopg2.pool.ThreadedConnectionPool(
                minconn=5,
                maxconn=config.database.pool_size,
                dsn=dsn
            )
            logger.info("PostgreSQL sync pool created")
        except Exception as e:
            logger.warning(f"PostgreSQL sync pool not available: {e}")
    
    async def _init_postgres_async_pool(self):
        """Initialize asynchronous PostgreSQL connection pool"""
        try:
            dsn = f"postgresql://{config.database.username}:{config.database.password}@" \
                  f"{config.database.host}:{config.database.port}/{config.database.database}"
            
            self._pools['postgres_async'] = await asyncpg.create_pool(
                dsn=dsn,
                min_size=5,
                max_size=config.database.pool_size,
                max_queries=50000,
                max_inactive_connection_lifetime=300,
                timeout=config.database.pool_timeout
            )
            logger.info("PostgreSQL async pool created")
        except Exception as e:
            logger.warning(f"PostgreSQL async pool not available: {e}")
    
    def _init_sqlalchemy_pools(self):
        """Initialize SQLAlchemy connection pools"""
        try:
            # Sync SQLAlchemy engine
            sync_url = f"postgresql://{config.database.username}:{config.database.password}@" \
                       f"{config.database.host}:{config.database.port}/{config.database.database}"
            
            self._pools['sqlalchemy_sync'] = create_engine(
                sync_url,
                poolclass=sa_pool.QueuePool,
                pool_size=config.database.pool_size,
                max_overflow=config.database.max_overflow,
                pool_timeout=config.database.pool_timeout,
                pool_pre_ping=True,  # Verify connections before using
                echo=config.application.debug
            )
            
            self._pools['sqlalchemy_session'] = sessionmaker(
                bind=self._pools['sqlalchemy_sync'],
                expire_on_commit=False
            )
            
            # Async SQLAlchemy engine
            async_url = f"postgresql+asyncpg://{config.database.username}:{config.database.password}@" \
                        f"{config.database.host}:{config.database.port}/{config.database.database}"
            
            self._pools['sqlalchemy_async'] = create_async_engine(
                async_url,
                pool_size=config.database.pool_size,
                max_overflow=config.database.max_overflow,
                pool_timeout=config.database.pool_timeout,
                pool_pre_ping=True,
                echo=config.application.debug
            )
            
            self._pools['sqlalchemy_async_session'] = async_sessionmaker(
                bind=self._pools['sqlalchemy_async'],
                expire_on_commit=False,
                class_=AsyncSession
            )
            
            logger.info("SQLAlchemy pools created")
        except Exception as e:
            logger.warning(f"SQLAlchemy pools not available: {e}")
    
    @contextmanager
    def get_postgres_connection(self):
        """Get a synchronous PostgreSQL connection from pool"""
        conn = None
        start_time = time.time()
        
        try:
            if 'postgres_sync' in self._pools:
                conn = self._pools['postgres_sync'].getconn()
                self._metrics.record_connection_acquired(time.time() - start_time)
                yield conn
            else:
                raise RuntimeError("PostgreSQL sync pool not initialized")
        finally:
            if conn and 'postgres_sync' in self._pools:
                self._pools['postgres_sync'].putconn(conn)
                self._metrics.record_connection_released()
    
    @asynccontextmanager
    async def get_async_postgres_connection(self):
        """Get an asynchronous PostgreSQL connection from pool"""
        start_time = time.time()
        
        try:
            if 'postgres_async' in self._pools:
                async with self._pools['postgres_async'].acquire() as conn:
                    self._metrics.record_connection_acquired(time.time() - start_time)
                    yield conn
            else:
                raise RuntimeError("PostgreSQL async pool not initialized")
        finally:
            self._metrics.record_connection_released()
    
    @contextmanager
    def get_sqlalchemy_session(self) -> Session:
        """Get a SQLAlchemy session from pool"""
        session = None
        start_time = time.time()
        
        try:
            if 'sqlalchemy_session' in self._pools:
                session = self._pools['sqlalchemy_session']()
                self._metrics.record_connection_acquired(time.time() - start_time)
                yield session
                session.commit()
            else:
                raise RuntimeError("SQLAlchemy session pool not initialized")
        except Exception as e:
            if session:
                session.rollback()
            raise e
        finally:
            if session:
                session.close()
                self._metrics.record_connection_released()
    
    @asynccontextmanager
    async def get_async_sqlalchemy_session(self) -> AsyncSession:
        """Get an async SQLAlchemy session from pool"""
        session = None
        start_time = time.time()
        
        try:
            if 'sqlalchemy_async_session' in self._pools:
                session = self._pools['sqlalchemy_async_session']()
                self._metrics.record_connection_acquired(time.time() - start_time)
                yield session
                await session.commit()
            else:
                raise RuntimeError("Async SQLAlchemy session pool not initialized")
        except Exception as e:
            if session:
                await session.rollback()
            raise e
        finally:
            if session:
                await session.close()
                self._metrics.record_connection_released()
    
    async def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Execute a query using async connection pool"""
        async with self.get_async_postgres_connection() as conn:
            if params:
                result = await conn.fetch(query, *params)
            else:
                result = await conn.fetch(query)
            return [dict(row) for row in result]
    
    async def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """Execute multiple queries using async connection pool"""
        async with self.get_async_postgres_connection() as conn:
            await conn.executemany(query, params_list)
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get current status of all connection pools"""
        status = {
            'metrics': self._metrics.get_metrics()
        }
        
        # PostgreSQL sync pool status
        if 'postgres_sync' in self._pools:
            pool = self._pools['postgres_sync']
            status['postgres_sync'] = {
                'min_connections': pool.minconn,
                'max_connections': pool.maxconn
            }
        
        # PostgreSQL async pool status
        if 'postgres_async' in self._pools:
            pool = self._pools['postgres_async']
            status['postgres_async'] = {
                'size': pool.get_size(),
                'free_connections': pool.get_idle_size(),
                'min_size': pool.get_min_size(),
                'max_size': pool.get_max_size()
            }
        
        # SQLAlchemy pool status
        if 'sqlalchemy_sync' in self._pools:
            pool = self._pools['sqlalchemy_sync'].pool
            status['sqlalchemy_sync'] = {
                'size': pool.size(),
                'checked_in': pool.checkedin(),
                'overflow': pool.overflow(),
                'total': pool.size() + pool.overflow()
            }
        
        return status
    
    async def close_all_pools(self):
        """Close all connection pools gracefully"""
        logger.info("Closing all database connection pools...")
        
        # Close PostgreSQL async pool
        if 'postgres_async' in self._pools:
            await self._pools['postgres_async'].close()
        
        # Close PostgreSQL sync pool
        if 'postgres_sync' in self._pools:
            self._pools['postgres_sync'].closeall()
        
        # Dispose SQLAlchemy engines
        if 'sqlalchemy_sync' in self._pools:
            self._pools['sqlalchemy_sync'].dispose()
        
        if 'sqlalchemy_async' in self._pools:
            await self._pools['sqlalchemy_async'].dispose()
        
        logger.info("All database connection pools closed")


class ConnectionPoolMetrics:
    """Track connection pool performance metrics"""
    
    def __init__(self):
        self.connections_acquired = 0
        self.connections_released = 0
        self.total_wait_time = 0.0
        self.max_wait_time = 0.0
        self.errors = 0
        self._lock = asyncio.Lock()
    
    def record_connection_acquired(self, wait_time: float):
        """Record successful connection acquisition"""
        self.connections_acquired += 1
        self.total_wait_time += wait_time
        self.max_wait_time = max(self.max_wait_time, wait_time)
    
    def record_connection_released(self):
        """Record connection release"""
        self.connections_released += 1
    
    def record_error(self):
        """Record connection error"""
        self.errors += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        avg_wait_time = (self.total_wait_time / self.connections_acquired 
                        if self.connections_acquired > 0 else 0)
        
        return {
            'connections_acquired': self.connections_acquired,
            'connections_released': self.connections_released,
            'connections_active': self.connections_acquired - self.connections_released,
            'average_wait_time_ms': avg_wait_time * 1000,
            'max_wait_time_ms': self.max_wait_time * 1000,
            'errors': self.errors
        }


# Singleton instance
db_pool = DatabasePoolManager()


# Convenience functions
async def execute_query(query: str, params: Optional[tuple] = None) -> List[Dict]:
    """Execute a database query using the connection pool"""
    return await db_pool.execute_query(query, params)


async def execute_many(query: str, params_list: List[tuple]) -> None:
    """Execute multiple database queries using the connection pool"""
    return await db_pool.execute_many(query, params_list)


def get_pool_status() -> Dict[str, Any]:
    """Get current connection pool status"""
    return db_pool.get_pool_status()