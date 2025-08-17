"""
Memory Monitoring Utility for Sentinel GRC
==========================================

Zero-cost memory monitoring to prevent memory leaks in production.
Provides enterprise-grade memory management without additional dependencies.
"""

import psutil
import gc
from typing import Dict, Any, List
from datetime import datetime
from .core_types import SharedKnowledgeGraphManager

class MemoryMonitor:
    """
    Enterprise memory monitoring for compliance assessment platform.
    Tracks memory usage and provides automatic cleanup recommendations.
    """
    
    def __init__(self):
        self.baseline_memory = self.get_process_memory()
        self.peak_memory = self.baseline_memory
        self.monitoring_start = datetime.now()
    
    def get_process_memory(self) -> Dict[str, float]:
        """Get current process memory usage in MB"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / (1024 * 1024),  # Resident Set Size
            "vms_mb": memory_info.vms / (1024 * 1024),  # Virtual Memory Size
            "percent": process.memory_percent()
        }
    
    def get_system_memory(self) -> Dict[str, float]:
        """Get system-wide memory statistics"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": memory.total / (1024**3),
            "available_gb": memory.available / (1024**3),
            "used_percent": memory.percent
        }
    
    def check_agents_memory(self, agents: List[Any]) -> Dict[str, Any]:
        """Check memory usage of all compliance agents"""
        agent_stats = []
        total_confidence_entries = 0
        total_decision_entries = 0
        
        for agent in agents:
            if hasattr(agent, 'get_memory_usage'):
                stats = agent.get_memory_usage()
                agent_stats.append(stats)
                total_confidence_entries += stats.get('confidence_history_size', 0)
                total_decision_entries += stats.get('decision_log_size', 0)
        
        return {
            "agent_count": len(agents),
            "agent_stats": agent_stats,
            "total_confidence_entries": total_confidence_entries,
            "total_decision_entries": total_decision_entries,
            "average_confidence_per_agent": total_confidence_entries / len(agents) if agents else 0,
            "average_decisions_per_agent": total_decision_entries / len(agents) if agents else 0
        }
    
    def get_knowledge_graph_stats(self) -> Dict[str, Any]:
        """Get shared knowledge graph statistics"""
        return {
            "total_frameworks": len(SharedKnowledgeGraphManager._instances),
            "frameworks": list(SharedKnowledgeGraphManager._instances.keys()),
            "total_access_count": sum(
                instance.get("access_count", 0) 
                for instance in SharedKnowledgeGraphManager._instances.values()
            ),
            "framework_details": {
                framework: {
                    "access_count": instance.get("access_count", 0),
                    "created_at": instance.get("created_at", "unknown")
                }
                for framework, instance in SharedKnowledgeGraphManager._instances.items()
            }
        }
    
    def force_garbage_collection(self) -> Dict[str, Any]:
        """Force garbage collection and return statistics"""
        before_memory = self.get_process_memory()
        
        # Force full garbage collection
        collected = gc.collect()
        
        after_memory = self.get_process_memory()
        
        memory_freed = before_memory["rss_mb"] - after_memory["rss_mb"]
        
        return {
            "objects_collected": collected,
            "memory_freed_mb": memory_freed,
            "before_memory_mb": before_memory["rss_mb"],
            "after_memory_mb": after_memory["rss_mb"],
            "gc_stats": gc.get_stats()
        }
    
    def cleanup_unused_resources(self, max_idle_hours: int = 24) -> Dict[str, Any]:
        """Clean up unused resources and return cleanup statistics"""
        before_kg_count = len(SharedKnowledgeGraphManager._instances)
        
        # Cleanup unused knowledge graphs
        SharedKnowledgeGraphManager.cleanup_unused(max_idle_hours)
        
        after_kg_count = len(SharedKnowledgeGraphManager._instances)
        
        # Force garbage collection after cleanup
        gc_stats = self.force_garbage_collection()
        
        return {
            "knowledge_graphs_cleaned": before_kg_count - after_kg_count,
            "remaining_knowledge_graphs": after_kg_count,
            "garbage_collection": gc_stats
        }
    
    def get_comprehensive_report(self, agents: List[Any] = None) -> Dict[str, Any]:
        """Get comprehensive memory usage report"""
        current_memory = self.get_process_memory()
        system_memory = self.get_system_memory()
        
        # Update peak memory
        if current_memory["rss_mb"] > self.peak_memory["rss_mb"]:
            self.peak_memory = current_memory
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "monitoring_duration_hours": (datetime.now() - self.monitoring_start).total_seconds() / 3600,
            "process_memory": current_memory,
            "system_memory": system_memory,
            "memory_growth": {
                "current_rss_mb": current_memory["rss_mb"],
                "baseline_rss_mb": self.baseline_memory["rss_mb"],
                "growth_mb": current_memory["rss_mb"] - self.baseline_memory["rss_mb"],
                "peak_rss_mb": self.peak_memory["rss_mb"]
            },
            "knowledge_graph_stats": self.get_knowledge_graph_stats()
        }
        
        if agents:
            report["agent_memory_stats"] = self.check_agents_memory(agents)
        
        return report
    
    def get_optimization_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Get memory optimization recommendations based on usage patterns"""
        recommendations = []
        
        memory_growth = report["memory_growth"]["growth_mb"]
        if memory_growth > 100:  # More than 100MB growth
            recommendations.append(
                f"High memory growth detected ({memory_growth:.1f}MB). Consider running cleanup_unused_resources()."
            )
        
        if report["system_memory"]["used_percent"] > 80:
            recommendations.append(
                "System memory usage is high (>80%). Consider reducing concurrent agent instances."
            )
        
        kg_stats = report["knowledge_graph_stats"]
        if kg_stats["total_frameworks"] > 10:
            recommendations.append(
                f"Large number of knowledge graph instances ({kg_stats['total_frameworks']}). Consider cleanup."
            )
        
        if "agent_memory_stats" in report:
            agent_stats = report["agent_memory_stats"]
            if agent_stats["average_confidence_per_agent"] > 80:
                recommendations.append(
                    "High confidence history per agent. Bounded collections are working but consider shorter retention."
                )
        
        if not recommendations:
            recommendations.append("Memory usage looks healthy. No optimization needed.")
        
        return recommendations

# Example usage function
def demonstrate_memory_monitoring():
    """Demonstrate the memory monitoring capabilities"""
    monitor = MemoryMonitor()
    
    print("=== Sentinel GRC Memory Monitoring Demo ===")
    print()
    
    # Create some agents
    from australian_compliance_agents import PrivacyActAgent
    agents = [PrivacyActAgent() for _ in range(3)]
    
    # Simulate some usage
    for agent in agents:
        for i in range(50):
            agent.metrics.add_confidence_score(0.7 + i * 0.001)
            agent.log_decision(f"Test decision {i}", "Test reasoning", 0.7)
    
    # Generate comprehensive report
    report = monitor.get_comprehensive_report(agents)
    recommendations = monitor.get_optimization_recommendations(report)
    
    print("Memory Usage Report:")
    print(f"  Process Memory: {report['process_memory']['rss_mb']:.1f}MB")
    print(f"  Memory Growth: {report['memory_growth']['growth_mb']:.1f}MB")
    print(f"  Knowledge Graphs: {report['knowledge_graph_stats']['total_frameworks']}")
    
    if "agent_memory_stats" in report:
        agent_stats = report["agent_memory_stats"]
        print(f"  Agents: {agent_stats['agent_count']}")
        print(f"  Avg Confidence Entries/Agent: {agent_stats['average_confidence_per_agent']:.1f}")
    
    print()
    print("Optimization Recommendations:")
    for rec in recommendations:
        print(f"  • {rec}")
    
    # Test cleanup
    print()
    print("Testing cleanup...")
    cleanup_stats = monitor.cleanup_unused_resources()
    print(f"  Objects collected: {cleanup_stats['garbage_collection']['objects_collected']}")
    print(f"  Memory freed: {cleanup_stats['garbage_collection']['memory_freed_mb']:.1f}MB")
    
    # Cleanup agents
    for agent in agents:
        agent.cleanup()
    
    print()
    print("=== Memory Monitoring Demo Complete ===")

if __name__ == "__main__":
    demonstrate_memory_monitoring()