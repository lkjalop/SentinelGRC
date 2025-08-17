"""
Token Optimization & Cost Management Engine
==========================================
Minimizes API costs while maintaining quality for enterprise SaaS deployment.
Implements intelligent caching, token compression, and cost tracking.
"""

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CostTier(Enum):
    """API cost tiers for different services"""
    FREE = "free"
    BASIC = "basic"  
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

@dataclass
class TokenUsage:
    """Track token usage across different services"""
    service: str
    tokens_used: int
    cost_usd: float
    timestamp: datetime
    cache_hit: bool = False
    compression_ratio: float = 1.0

@dataclass
class CostBudget:
    """Monthly cost budgets for different services"""
    groq_monthly_limit: float = 0.0  # Free tier
    openai_monthly_limit: float = 20.0
    anthropic_monthly_limit: float = 20.0
    total_monthly_limit: float = 50.0

class TokenOptimizationEngine:
    """
    Optimizes API token usage and minimizes costs for enterprise deployment.
    Implements multiple cost reduction strategies.
    """
    
    def __init__(self, cost_budget: CostBudget = None):
        self.cost_budget = cost_budget or CostBudget()
        self.usage_history: List[TokenUsage] = []
        self.query_cache: Dict[str, Any] = {}
        self.cache_stats = {"hits": 0, "misses": 0}
        self.cost_tracking = {
            "daily": {},
            "monthly": {},
            "total": 0.0
        }
        
    def optimize_compliance_query(self, 
                                 query_text: str, 
                                 framework: str,
                                 industry: str) -> Dict[str, Any]:
        """
        Optimize compliance queries using multiple cost reduction strategies
        """
        
        # 1. Generate cache key
        cache_key = self._generate_cache_key(query_text, framework, industry)
        
        # 2. Check intelligent cache
        cached_result = self._check_intelligent_cache(cache_key)
        if cached_result:
            self.cache_stats["hits"] += 1
            return {
                "response": cached_result,
                "token_cost": 0,
                "cache_hit": True,
                "optimization_applied": "cache_hit"
            }
        
        self.cache_stats["misses"] += 1
        
        # 3. Apply query compression techniques
        compressed_query = self._compress_query(query_text, framework, industry)
        
        # 4. Select optimal API based on cost/quality
        selected_api = self._select_optimal_api(compressed_query)
        
        # 5. Execute with cost tracking
        result = self._execute_optimized_query(
            compressed_query, 
            selected_api,
            cache_key
        )
        
        return result
    
    def _generate_cache_key(self, query_text: str, framework: str, industry: str) -> str:
        """Generate intelligent cache key for compliance queries"""
        
        # Normalize inputs to improve cache hit rates
        normalized_query = self._normalize_compliance_text(query_text)
        
        # Create composite key
        cache_input = f"{normalized_query}|{framework}|{industry}"
        
        # Use SHA-256 for secure, consistent hashing
        return hashlib.sha256(cache_input.encode()).hexdigest()[:16]
    
    def _normalize_compliance_text(self, text: str) -> str:
        """Normalize compliance text to improve cache hit rates"""
        
        # Remove company-specific information that doesn't affect compliance logic
        normalization_rules = [
            (r'\\b[A-Z][a-z]+ (?:Corp|Inc|Ltd|Pty|LLC)\\b', '[COMPANY]'),
            (r'\\b\\d{1,3}(?:,\\d{3})*\\b', '[NUMBER]'),
            (r'\\b\\d{4}-\\d{2}-\\d{2}\\b', '[DATE]'),
            (r'\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b', '[EMAIL]'),
            (r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b', '[IP_ADDRESS]')
        ]
        
        normalized = text.lower().strip()
        
        # Apply normalization rules
        import re
        for pattern, replacement in normalization_rules:
            normalized = re.sub(pattern, replacement, normalized)
        
        return normalized
    
    def _check_intelligent_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Check cache with intelligent expiration based on content type"""
        
        if cache_key not in self.query_cache:
            return None
        
        cached_entry = self.query_cache[cache_key]
        cached_time = cached_entry.get("timestamp")
        content_type = cached_entry.get("content_type", "general")
        
        # Different TTL based on content type
        ttl_hours = {
            "regulatory_text": 24 * 7,  # Weekly for regulatory content
            "framework_mapping": 24 * 30,  # Monthly for framework relationships  
            "threat_intelligence": 24,  # Daily for threat data
            "general": 24 * 3  # 3 days for general queries
        }
        
        expiry_time = cached_time + timedelta(hours=ttl_hours.get(content_type, 72))
        
        if datetime.now() < expiry_time:
            return cached_entry["response"]
        else:
            # Remove expired entry
            del self.query_cache[cache_key]
            return None
    
    def _compress_query(self, query_text: str, framework: str, industry: str) -> Dict[str, Any]:
        """Apply intelligent query compression to reduce token usage"""
        
        # Template-based compression for common compliance patterns
        compression_templates = {
            "gap_analysis": {
                "template": "Analyze {framework} compliance gaps for {industry} company with controls: {controls}",
                "token_reduction": 0.60  # 60% token reduction
            },
            "risk_assessment": {
                "template": "Assess {framework} risks for {industry}: {risk_areas}",
                "token_reduction": 0.55
            },
            "control_mapping": {
                "template": "Map {source_framework} to {target_framework} controls: {controls}",
                "token_reduction": 0.70
            }
        }
        
        # Detect query pattern and apply appropriate compression
        query_pattern = self._detect_query_pattern(query_text)
        
        if query_pattern in compression_templates:
            template = compression_templates[query_pattern]
            compressed_text = self._apply_template_compression(
                query_text, template["template"], framework, industry
            )
            token_reduction = template["token_reduction"]
        else:
            # Fallback: generic text compression
            compressed_text = self._apply_generic_compression(query_text)
            token_reduction = 0.30
        
        return {
            "original_text": query_text,
            "compressed_text": compressed_text,
            "compression_ratio": token_reduction,
            "estimated_tokens": len(compressed_text.split()) * 1.3  # Rough token estimate
        }
    
    def _detect_query_pattern(self, query_text: str) -> str:
        """Detect the type of compliance query for optimal compression"""
        
        patterns = {
            "gap_analysis": ["gap", "missing", "deficient", "lacking"],
            "risk_assessment": ["risk", "threat", "vulnerability", "impact"],
            "control_mapping": ["mapping", "equivalent", "corresponds", "relates"]
        }
        
        query_lower = query_text.lower()
        
        for pattern_type, keywords in patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                return pattern_type
        
        return "general"
    
    def _select_optimal_api(self, compressed_query: Dict[str, Any]) -> Dict[str, Any]:
        """Select the most cost-effective API for the query type"""
        
        estimated_tokens = compressed_query["estimated_tokens"]
        
        # API cost analysis (per 1K tokens)
        api_costs = {
            "groq": {"cost_per_1k": 0.0, "limit_daily": 14400, "quality": 8},
            "openai_gpt3": {"cost_per_1k": 0.002, "limit_daily": None, "quality": 9},
            "anthropic": {"cost_per_1k": 0.015, "limit_daily": None, "quality": 10}
        }
        
        # Check current usage against limits
        current_usage = self._get_current_daily_usage()
        
        # Select API based on cost/quality optimization
        if (estimated_tokens <= 1000 and 
            current_usage.get("groq", 0) < api_costs["groq"]["limit_daily"]):
            return {"provider": "groq", "model": "mixtral-8x7b-32768"}
        
        elif estimated_tokens <= 2000:
            return {"provider": "openai", "model": "gpt-3.5-turbo"}
        
        else:
            # For complex queries, use higher quality but more expensive API
            return {"provider": "anthropic", "model": "claude-3-haiku"}
    
    def _execute_optimized_query(self, 
                                compressed_query: Dict[str, Any],
                                api_config: Dict[str, Any],
                                cache_key: str) -> Dict[str, Any]:
        """Execute query with cost tracking and caching"""
        
        # Simulate API call (in real implementation, this would call actual APIs)
        estimated_cost = self._calculate_estimated_cost(
            compressed_query["estimated_tokens"],
            api_config["provider"]
        )
        
        # Mock response for demonstration
        mock_response = {
            "analysis": f"Mock compliance analysis for {api_config['provider']}",
            "confidence": 0.85,
            "recommendations": ["Mock recommendation 1", "Mock recommendation 2"]
        }
        
        # Cache the result
        self.query_cache[cache_key] = {
            "response": mock_response,
            "timestamp": datetime.now(),
            "content_type": "general",
            "cost": estimated_cost
        }
        
        # Track usage
        usage = TokenUsage(
            service=api_config["provider"],
            tokens_used=int(compressed_query["estimated_tokens"]),
            cost_usd=estimated_cost,
            timestamp=datetime.now(),
            cache_hit=False,
            compression_ratio=compressed_query["compression_ratio"]
        )
        
        self.usage_history.append(usage)
        self._update_cost_tracking(estimated_cost)
        
        return {
            "response": mock_response,
            "token_cost": estimated_cost,
            "tokens_used": int(compressed_query["estimated_tokens"]),
            "cache_hit": False,
            "optimization_applied": f"compression_{compressed_query['compression_ratio']:.2f}",
            "provider": api_config["provider"]
        }
    
    def _calculate_estimated_cost(self, tokens: float, provider: str) -> float:
        """Calculate estimated cost for token usage"""
        
        cost_per_1k = {
            "groq": 0.0,
            "openai": 0.002,
            "anthropic": 0.015
        }
        
        return (tokens / 1000) * cost_per_1k.get(provider, 0.01)
    
    def _get_current_daily_usage(self) -> Dict[str, int]:
        """Get current daily usage by provider"""
        today = datetime.now().date()
        
        daily_usage = {}
        for usage in self.usage_history:
            if usage.timestamp.date() == today:
                daily_usage[usage.service] = daily_usage.get(usage.service, 0) + usage.tokens_used
        
        return daily_usage
    
    def _update_cost_tracking(self, cost: float):
        """Update cost tracking metrics"""
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        
        # Daily tracking
        if today not in self.cost_tracking["daily"]:
            self.cost_tracking["daily"][today] = 0.0
        self.cost_tracking["daily"][today] += cost
        
        # Monthly tracking
        if month not in self.cost_tracking["monthly"]:
            self.cost_tracking["monthly"][month] = 0.0
        self.cost_tracking["monthly"][month] += cost
        
        # Total tracking
        self.cost_tracking["total"] += cost
    
    def get_cost_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive cost analysis report"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        current_month = datetime.now().strftime("%Y-%m")
        
        daily_cost = self.cost_tracking["daily"].get(today, 0.0)
        monthly_cost = self.cost_tracking["monthly"].get(current_month, 0.0)
        
        # Calculate efficiency metrics
        total_queries = len(self.usage_history)
        cache_hit_rate = (self.cache_stats["hits"] / 
                         (self.cache_stats["hits"] + self.cache_stats["misses"])) * 100
        
        avg_compression = sum(usage.compression_ratio for usage in self.usage_history) / max(total_queries, 1)
        
        return {
            "cost_summary": {
                "daily_cost": daily_cost,
                "monthly_cost": monthly_cost, 
                "total_cost": self.cost_tracking["total"],
                "budget_remaining": self.cost_budget.total_monthly_limit - monthly_cost
            },
            "efficiency_metrics": {
                "cache_hit_rate": cache_hit_rate,
                "total_queries": total_queries,
                "avg_compression_ratio": avg_compression,
                "cost_per_query": self.cost_tracking["total"] / max(total_queries, 1)
            },
            "optimization_savings": {
                "estimated_savings_pct": (cache_hit_rate + (avg_compression * 100)) / 2,
                "tokens_saved": sum(usage.tokens_used * usage.compression_ratio 
                                  for usage in self.usage_history)
            }
        }
    
    def _apply_template_compression(self, query_text: str, template: str, 
                                  framework: str, industry: str) -> str:
        """Apply template-based compression for common patterns"""
        # Simplified implementation - extract key components and fit to template
        return template.format(framework=framework, industry=industry, 
                             controls="[extracted_controls]")
    
    def _apply_generic_compression(self, query_text: str) -> str:
        """Apply generic text compression techniques"""
        # Remove redundant words, use abbreviations, etc.
        # Simplified implementation
        return " ".join(query_text.split()[:100])  # Limit to 100 words

# Export for main application
def create_token_optimizer(budget: CostBudget = None) -> TokenOptimizationEngine:
    """Factory function to create token optimizer"""
    return TokenOptimizationEngine(budget)

if __name__ == "__main__":
    # Test token optimization
    optimizer = TokenOptimizationEngine()
    
    # Test query optimization
    result = optimizer.optimize_compliance_query(
        query_text="Analyze Essential 8 compliance gaps for our healthcare company",
        framework="Essential 8",
        industry="healthcare"
    )
    
    print("Optimization Result:")
    print(f"Cache Hit: {result['cache_hit']}")
    print(f"Token Cost: ${result['token_cost']:.4f}")
    print(f"Optimization: {result['optimization_applied']}")
    
    # Test cost analysis
    cost_analysis = optimizer.get_cost_analysis()
    print(f"\\nCache Hit Rate: {cost_analysis['efficiency_metrics']['cache_hit_rate']:.2f}%")
    print(f"Total Cost: ${cost_analysis['cost_summary']['total_cost']:.4f}")