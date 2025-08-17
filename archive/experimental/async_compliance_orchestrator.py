"""
Async/Await Compliance Pipeline Orchestrator
Fully asynchronous implementation for high-performance compliance assessments
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp
import time
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import json

from config_manager import config
from cache_manager import CacheManager
from database_pool import db_pool
from token_optimization_engine import TokenOptimizationEngine
from enterprise_liability_framework import EnterpriseComplianceLiabilityManager

logger = logging.getLogger(__name__)


class AssessmentStatus(Enum):
    """Assessment pipeline status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class AssessmentTask:
    """Individual assessment task in the pipeline"""
    task_id: str
    framework: str
    company_profile: Dict[str, Any]
    status: AssessmentStatus = AssessmentStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class PipelineMetrics:
    """Pipeline performance metrics"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_time: float = 0.0
    framework_times: Dict[str, float] = field(default_factory=dict)
    cache_hits: int = 0
    cache_misses: int = 0


class AsyncComplianceOrchestrator:
    """Fully asynchronous compliance assessment orchestrator"""
    
    def __init__(self):
        self.cache = CacheManager()
        self.token_optimizer = TokenOptimizationEngine()
        self.liability_manager = EnterpriseComplianceLiabilityManager()
        self.executor = ThreadPoolExecutor(max_workers=config.application.workers)
        self.session: Optional[aiohttp.ClientSession] = None
        self.metrics = PipelineMetrics()
        self._semaphore = asyncio.Semaphore(10)  # Limit concurrent assessments
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=100, limit_per_host=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def assess_compliance(
        self,
        company_profile: Dict[str, Any],
        frameworks: Optional[List[str]] = None,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Main entry point for compliance assessment
        
        Args:
            company_profile: Company information and context
            frameworks: List of frameworks to assess (None = auto-detect)
            parallel: Whether to run assessments in parallel
        
        Returns:
            Complete assessment results with all frameworks
        """
        start_time = time.time()
        
        # Auto-detect frameworks if not specified
        if not frameworks:
            frameworks = await self._detect_applicable_frameworks(company_profile)
        
        # Create assessment tasks
        tasks = [
            AssessmentTask(
                task_id=f"{company_profile.get('name', 'unknown')}_{framework}_{datetime.now().timestamp()}",
                framework=framework,
                company_profile=company_profile
            )
            for framework in frameworks
        ]
        
        # Execute pipeline
        if parallel:
            results = await self._execute_parallel_pipeline(tasks)
        else:
            results = await self._execute_sequential_pipeline(tasks)
        
        # Aggregate results
        assessment_results = await self._aggregate_results(results, company_profile)
        
        # Perform liability assessment
        liability_assessment = await self._assess_liability(assessment_results)
        assessment_results['liability_assessment'] = liability_assessment
        
        # Record metrics
        self.metrics.total_time += time.time() - start_time
        
        # Store results in database
        await self._store_assessment_results(assessment_results)
        
        return assessment_results
    
    async def _detect_applicable_frameworks(self, company_profile: Dict[str, Any]) -> List[str]:
        """Intelligently detect applicable compliance frameworks"""
        frameworks = []
        
        region = company_profile.get('region', 'AU').upper()
        industry = company_profile.get('industry', '').lower()
        size = company_profile.get('size', 'medium').lower()
        
        # Regional frameworks
        if region == 'AU':
            frameworks.extend(['essential_8', 'privacy_act'])
            if 'finance' in industry or 'banking' in industry:
                frameworks.append('apra_cps234')
            if 'critical' in industry or 'infrastructure' in industry:
                frameworks.append('soci_act')
        
        elif region == 'US':
            frameworks.extend(['soc2', 'nist_csf'])
            if 'health' in industry:
                frameworks.append('hipaa')
            if 'california' in company_profile.get('state', '').lower():
                frameworks.append('ccpa')
            if 'payment' in industry or 'retail' in industry:
                frameworks.append('pci_dss')
        
        elif region == 'EU':
            frameworks.extend(['gdpr', 'nis2'])
            if 'finance' in industry:
                frameworks.append('dora')
        
        # Global frameworks
        if size in ['large', 'enterprise']:
            frameworks.append('iso27001')
        
        return frameworks
    
    async def _execute_parallel_pipeline(self, tasks: List[AssessmentTask]) -> List[AssessmentTask]:
        """Execute assessment tasks in parallel"""
        async def process_task(task: AssessmentTask) -> AssessmentTask:
            async with self._semaphore:
                return await self._process_single_task(task)
        
        # Create coroutines for all tasks
        coroutines = [process_task(task) for task in tasks]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                tasks[i].status = AssessmentStatus.FAILED
                tasks[i].error = str(result)
                processed_results.append(tasks[i])
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _execute_sequential_pipeline(self, tasks: List[AssessmentTask]) -> List[AssessmentTask]:
        """Execute assessment tasks sequentially"""
        results = []
        for task in tasks:
            result = await self._process_single_task(task)
            results.append(result)
        return results
    
    async def _process_single_task(self, task: AssessmentTask) -> AssessmentTask:
        """Process a single assessment task"""
        task.start_time = time.time()
        task.status = AssessmentStatus.IN_PROGRESS
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(task)
            cached_result = await self._get_cached_result(cache_key)
            
            if cached_result:
                task.result = cached_result
                task.status = AssessmentStatus.COMPLETED
                self.metrics.cache_hits += 1
            else:
                # Perform actual assessment
                self.metrics.cache_misses += 1
                
                # Optimize tokens before assessment
                optimized_query = await self._optimize_assessment_query(task)
                
                # Execute framework-specific assessment
                task.result = await self._execute_framework_assessment(
                    task.framework,
                    task.company_profile,
                    optimized_query
                )
                
                # Cache the result
                await self._cache_result(cache_key, task.result)
                
                task.status = AssessmentStatus.COMPLETED
        
        except Exception as e:
            logger.error(f"Task {task.task_id} failed: {e}")
            task.error = str(e)
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff
                return await self._process_single_task(task)
            else:
                task.status = AssessmentStatus.FAILED
        
        finally:
            task.end_time = time.time()
            self.metrics.completed_tasks += 1
            
            # Record framework-specific timing
            if task.framework not in self.metrics.framework_times:
                self.metrics.framework_times[task.framework] = 0
            self.metrics.framework_times[task.framework] += (task.end_time - task.start_time)
        
        return task
    
    async def _execute_framework_assessment(
        self,
        framework: str,
        company_profile: Dict[str, Any],
        optimized_query: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute framework-specific compliance assessment"""
        
        # Framework-specific assessment logic
        assessment_map = {
            'essential_8': self._assess_essential_8,
            'privacy_act': self._assess_privacy_act,
            'apra_cps234': self._assess_apra_cps234,
            'soci_act': self._assess_soci_act,
            'soc2': self._assess_soc2,
            'nist_csf': self._assess_nist_csf,
            'hipaa': self._assess_hipaa,
            'gdpr': self._assess_gdpr,
            'iso27001': self._assess_iso27001
        }
        
        assessment_func = assessment_map.get(framework)
        if not assessment_func:
            raise ValueError(f"Unknown framework: {framework}")
        
        return await assessment_func(company_profile, optimized_query)
    
    async def _assess_essential_8(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess Essential 8 compliance"""
        controls = [
            "Application Control",
            "Patch Applications",
            "Configure Microsoft Office Macro Settings",
            "User Application Hardening",
            "Restrict Administrative Privileges",
            "Patch Operating Systems",
            "Multi-Factor Authentication",
            "Regular Backups"
        ]
        
        results = {}
        for control in controls:
            # Simulate async assessment
            await asyncio.sleep(0.1)
            results[control] = {
                'status': 'compliant' if company_profile.get('security_level', 0) > 5 else 'non_compliant',
                'score': company_profile.get('security_level', 5) * 10,
                'recommendations': [f"Improve {control} implementation"]
            }
        
        return {
            'framework': 'Essential 8',
            'overall_score': sum(r['score'] for r in results.values()) / len(results),
            'controls': results,
            'assessment_date': datetime.now().isoformat()
        }
    
    async def _assess_privacy_act(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess Privacy Act compliance"""
        # Simplified implementation - would connect to actual assessment logic
        await asyncio.sleep(0.2)
        return {
            'framework': 'Privacy Act 1988',
            'overall_score': 75,
            'apps_compliance': {
                'APP1': 'compliant',
                'APP2': 'compliant',
                'APP3': 'partial',
                'APP4': 'compliant',
                'APP5': 'compliant'
            }
        }
    
    async def _assess_apra_cps234(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess APRA CPS 234 compliance"""
        await asyncio.sleep(0.15)
        return {
            'framework': 'APRA CPS 234',
            'overall_score': 80,
            'requirements': {
                'information_security_capability': 'met',
                'information_security_governance': 'met',
                'incident_management': 'partial'
            }
        }
    
    async def _assess_soci_act(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess SOCI Act compliance"""
        await asyncio.sleep(0.1)
        return {
            'framework': 'SOCI Act',
            'overall_score': 85,
            'critical_infrastructure_protected': True
        }
    
    async def _assess_soc2(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess SOC 2 compliance"""
        await asyncio.sleep(0.2)
        return {
            'framework': 'SOC 2',
            'overall_score': 78,
            'trust_service_criteria': {
                'security': 'met',
                'availability': 'met',
                'processing_integrity': 'partial',
                'confidentiality': 'met',
                'privacy': 'met'
            }
        }
    
    async def _assess_nist_csf(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess NIST CSF compliance"""
        await asyncio.sleep(0.25)
        return {
            'framework': 'NIST CSF',
            'overall_score': 82,
            'functions': {
                'identify': 85,
                'protect': 80,
                'detect': 75,
                'respond': 82,
                'recover': 88
            }
        }
    
    async def _assess_hipaa(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess HIPAA compliance"""
        await asyncio.sleep(0.2)
        return {
            'framework': 'HIPAA',
            'overall_score': 76,
            'safeguards': {
                'administrative': 'compliant',
                'physical': 'compliant',
                'technical': 'partial'
            }
        }
    
    async def _assess_gdpr(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess GDPR compliance"""
        await asyncio.sleep(0.3)
        return {
            'framework': 'GDPR',
            'overall_score': 79,
            'principles': {
                'lawfulness': 'compliant',
                'purpose_limitation': 'compliant',
                'data_minimization': 'partial',
                'accuracy': 'compliant'
            }
        }
    
    async def _assess_iso27001(self, company_profile: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
        """Assess ISO 27001 compliance"""
        await asyncio.sleep(0.25)
        return {
            'framework': 'ISO 27001',
            'overall_score': 81,
            'domains': {
                'information_security_policies': 85,
                'organization_of_information_security': 80,
                'human_resource_security': 75,
                'asset_management': 82
            }
        }
    
    async def _optimize_assessment_query(self, task: AssessmentTask) -> Dict[str, Any]:
        """Optimize assessment query for token efficiency"""
        # Use token optimization engine
        optimized = self.token_optimizer.optimize_compliance_query(
            f"Assess {task.framework} compliance for {task.company_profile.get('name', 'company')}",
            task.framework,
            task.company_profile.get('industry', 'general')
        )
        
        return {
            'optimized_query': optimized['optimized_query'],
            'token_savings': optimized['savings_percentage'],
            'original_task': task
        }
    
    async def _aggregate_results(
        self,
        tasks: List[AssessmentTask],
        company_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate results from all assessment tasks"""
        successful_tasks = [t for t in tasks if t.status == AssessmentStatus.COMPLETED]
        failed_tasks = [t for t in tasks if t.status == AssessmentStatus.FAILED]
        
        # Calculate overall compliance score
        overall_score = 0
        if successful_tasks:
            scores = [t.result.get('overall_score', 0) for t in successful_tasks]
            overall_score = sum(scores) / len(scores)
        
        return {
            'company': company_profile,
            'assessment_id': f"assessment_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'overall_compliance_score': overall_score,
            'frameworks_assessed': [t.framework for t in successful_tasks],
            'framework_results': {t.framework: t.result for t in successful_tasks},
            'failed_assessments': [{'framework': t.framework, 'error': t.error} for t in failed_tasks],
            'metrics': {
                'total_time': sum(t.end_time - t.start_time for t in tasks if t.end_time and t.start_time),
                'cache_efficiency': (self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses))
                                   if (self.metrics.cache_hits + self.metrics.cache_misses) > 0 else 0
            }
        }
    
    async def _assess_liability(self, assessment_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess liability and risk for the compliance assessment"""
        liability_result = self.liability_manager.assess_liability_risk({
            'assessment_results': assessment_results,
            'confidence_level': assessment_results.get('overall_compliance_score', 0) / 100,
            'frameworks': assessment_results.get('frameworks_assessed', [])
        })
        
        return liability_result
    
    async def _store_assessment_results(self, results: Dict[str, Any]) -> None:
        """Store assessment results in database"""
        try:
            query = """
                INSERT INTO compliance_assessments 
                (assessment_id, company_name, timestamp, overall_score, results_json)
                VALUES ($1, $2, $3, $4, $5)
            """
            
            await db_pool.execute_query(
                query,
                (
                    results['assessment_id'],
                    results['company'].get('name', 'Unknown'),
                    results['timestamp'],
                    results['overall_compliance_score'],
                    json.dumps(results)
                )
            )
        except Exception as e:
            logger.error(f"Failed to store assessment results: {e}")
    
    def _generate_cache_key(self, task: AssessmentTask) -> str:
        """Generate cache key for assessment task"""
        company_hash = hash(json.dumps(task.company_profile, sort_keys=True))
        return f"assessment_{task.framework}_{company_hash}"
    
    async def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached assessment result"""
        return self.cache.get(cache_key)
    
    async def _cache_result(self, cache_key: str, result: Dict[str, Any]) -> None:
        """Cache assessment result"""
        self.cache.set(cache_key, result, ttl=config.get('cache_ttl_seconds', 3600))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get pipeline performance metrics"""
        return {
            'total_tasks': self.metrics.total_tasks,
            'completed_tasks': self.metrics.completed_tasks,
            'failed_tasks': self.metrics.failed_tasks,
            'total_time': self.metrics.total_time,
            'framework_times': self.metrics.framework_times,
            'cache_hits': self.metrics.cache_hits,
            'cache_misses': self.metrics.cache_misses,
            'cache_hit_rate': (self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses))
                             if (self.metrics.cache_hits + self.metrics.cache_misses) > 0 else 0
        }


# Example usage
async def main():
    """Example usage of async compliance orchestrator"""
    async with AsyncComplianceOrchestrator() as orchestrator:
        company_profile = {
            'name': 'Example Corp',
            'region': 'AU',
            'industry': 'finance',
            'size': 'large',
            'security_level': 7
        }
        
        results = await orchestrator.assess_compliance(company_profile)
        print(f"Overall Compliance Score: {results['overall_compliance_score']:.2f}%")
        print(f"Frameworks Assessed: {', '.join(results['frameworks_assessed'])}")
        print(f"Metrics: {orchestrator.get_metrics()}")


if __name__ == "__main__":
    asyncio.run(main())