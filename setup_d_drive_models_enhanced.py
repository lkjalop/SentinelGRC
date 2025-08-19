#!/usr/bin/env python3
"""
Enhanced D-Drive Model Setup with Financial Intelligence Integration
Downloads models to D drive and integrates recovery/penalty research
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

class EnhancedModelSetup:
    """Setup models on D drive with integrated financial intelligence"""
    
    def __init__(self):
        # D drive setup based on CLAUDE_OPTIMIZED.md Phase 2 plan
        self.d_drive_path = Path("D:/Docker/SentinelGRC/models")
        self.research_path = Path("D:/AI/New folder")
        
    def setup_d_drive_structure(self):
        """Create D drive directory structure for models"""
        print("Setting up D drive structure for models...")
        
        directories = [
            self.d_drive_path,
            self.d_drive_path / "llama",
            self.d_drive_path / "mistral", 
            self.d_drive_path / "bert-ner",
            self.d_drive_path / "embeddings",
            self.d_drive_path / "financial_intelligence"
        ]
        
        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {dir_path}")
    
    def download_models_script(self):
        """Generate script to download models using HuggingFace"""
        
        download_script = '''
import os
os.environ['HF_HOME'] = 'D:/Docker/SentinelGRC/models/huggingface'
os.environ['TRANSFORMERS_CACHE'] = 'D:/Docker/SentinelGRC/models/cache'

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

print("Downloading models to D drive...")

# 1. Llama 3.2 (smaller version for testing)
print("Downloading Llama 3.2...")
try:
    model_name = "meta-llama/Llama-3.2-1B"  # Start with 1B for testing
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    print(f"Llama 3.2 downloaded to: {os.environ['HF_HOME']}")
except Exception as e:
    print(f"Note: Llama requires authentication. Error: {e}")
    print("Alternative: Using TinyLlama for testing")
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("TinyLlama downloaded as alternative")

# 2. Mistral 7B
print("Downloading Mistral 7B...")
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
print(f"Mistral 7B downloaded to: {os.environ['HF_HOME']}")

# 3. BERT for NER (Evidence Detection)
print("Downloading BERT-NER...")
from transformers import pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")
print("BERT-NER downloaded")

# 4. Sentence embeddings for similarity
print("Downloading sentence embeddings...")
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('D:/Docker/SentinelGRC/models/embeddings/all-MiniLM-L6-v2')
print("Embeddings model downloaded")

print("All models downloaded to D drive successfully!")
print(f"Total size: Check D:/Docker/SentinelGRC/models/")
'''
        
        script_path = self.d_drive_path / "download_models.py"
        with open(script_path, 'w') as f:
            f.write(download_script)
        
        print(f"Download script created: {script_path}")
        return script_path
    
    def create_financial_intelligence_db(self):
        """Create database from recovery time and penalty research"""
        
        print("Creating financial intelligence database...")
        
        # Parse recovery time data
        recovery_data = {
            "downtime_costs": {
                "average_per_minute": "$5,600-9,000",
                "mega_tech_per_minute": "$373,606",
                "apple_per_minute": "$691,234"
            },
            "recovery_metrics": {
                "technical_controls": {
                    "automated_failover": "5-60 seconds",
                    "database_replication": "35 second RPO, 5 minute RTO",
                    "cloud_recovery": "sub-minute RTO"
                },
                "administrative_controls": {
                    "incident_activation": "15-60 minutes",
                    "staff_mobilization": "2-8 hours",
                    "full_recovery": "24-72 hours"
                },
                "physical_controls": {
                    "power_restoration": "4-48 hours",
                    "hvac_repairs": "8-72 hours",
                    "infrastructure_replacement": "7-30 days"
                }
            },
            "maturity_benefits": {
                "level_3_or_higher": "33-day faster threat identification",
                "level_5": "30-60 day detection vs 200+ days for level 1"
            }
        }
        
        # Parse regulatory penalty data
        penalty_data = {
            "total_penalties": "$7 billion documented",
            "gdpr": {
                "total": "€5.65 billion",
                "meta": "€1.2 billion",
                "amazon": "€746 million",
                "whatsapp": "€225 million"
            },
            "hipaa": {
                "anthem": "$16 million (largest)",
                "average_per_violation": "$141-$2,134,831"
            },
            "pci_dss": {
                "target": "$292 million total",
                "heartland": "$145 million",
                "monthly_fines": "$5,000-$100,000"
            },
            "cve_to_penalty": {
                "equifax_struts": "$700+ million for CVE-2017-5638",
                "tuckers_citrix": "£98,000 for CVE-2019-19781",
                "known_cve_unpatched": "Prima facie negligence"
            },
            "patch_timelines": {
                "critical_cvss_9_10": "14 days maximum",
                "high_cvss_7_9": "30 days maximum",
                "medium_cvss_4_7": "90 days maximum"
            },
            "auditor_quotes": {
                "kc_fikes": "Failure of new staff to follow protocols causes qualified opinions",
                "red_flags": ["No control ownership", "No defined scope", "Controls stopping operation"],
                "evidence_sampling": "10 of 100 samples tested against each control"
            }
        }
        
        # Save to D drive
        intelligence_db = {
            "recovery_analytics": recovery_data,
            "penalty_database": penalty_data,
            "integration_timestamp": "2025-08-19",
            "business_value": {
                "risk_reduction": "$3.81 million per breach with technical controls",
                "compliance_savings": "$1.76 million with incident response",
                "recovery_improvement": "50% faster with Zero Trust",
                "audit_cost_reduction": "40% with automation"
            }
        }
        
        db_path = self.d_drive_path / "financial_intelligence" / "intelligence_db.json"
        with open(db_path, 'w') as f:
            json.dump(intelligence_db, f, indent=2)
        
        print(f"Financial intelligence database created: {db_path}")
        return intelligence_db
    
    def create_agent_training_config(self):
        """Configure which agents to train with new data"""
        
        training_config = {
            "evidence_detector_agent": {
                "train_with": ["penalty_database", "auditor_quotes"],
                "focus": "Identify control failures that trigger penalties",
                "model": "bert-base-NER"
            },
            "apollo_reasoner_agent": {
                "train_with": ["recovery_analytics", "maturity_models"],
                "focus": "Calculate recovery times and business impact",
                "model": "mistral-7b"
            },
            "report_generator_agent": {
                "train_with": ["all_financial_data"],
                "focus": "Generate reports with real financial impact",
                "model": "llama-3.2"
            },
            "legal_compliance_agent": {
                "train_with": ["regulatory_penalties", "patch_timelines"],
                "focus": "Assess compliance risk in monetary terms",
                "model": "mistral-7b"
            },
            "interactive_chat_agent": {
                "train_with": ["auditor_quotes", "red_flags"],
                "focus": "Answer with auditor psychology insights",
                "model": "tinyllama"
            }
        }
        
        config_path = self.d_drive_path / "agent_training_config.json"
        with open(config_path, 'w') as f:
            json.dump(training_config, f, indent=2)
        
        print(f"Agent training configuration created: {config_path}")
        return training_config

if __name__ == "__main__":
    print("=" * 60)
    print("ENHANCED D-DRIVE MODEL SETUP WITH FINANCIAL INTELLIGENCE")
    print("=" * 60)
    
    setup = EnhancedModelSetup()
    
    # 1. Setup D drive structure
    setup.setup_d_drive_structure()
    
    # 2. Create download script
    script_path = setup.download_models_script()
    print(f"\nTo download models, run: python {script_path}")
    
    # 3. Create financial intelligence database
    intelligence_db = setup.create_financial_intelligence_db()
    print(f"\nFinancial intelligence integrated:")
    print(f"- Recovery costs: $5,600-9,000 per minute average")
    print(f"- Total penalties tracked: $7 billion")
    print(f"- Direct auditor quotes integrated")
    
    # 4. Configure agent training
    training_config = setup.create_agent_training_config()
    print(f"\nAgent training configured for:")
    for agent, config in training_config.items():
        print(f"- {agent}: {config['focus']}")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE! Next steps:")
    print("1. Run: python D:/Docker/SentinelGRC/models/download_models.py")
    print("2. Models will download to D drive (23GB+ space needed)")
    print("3. Financial intelligence ready for integration")
    print("4. Agents configured for training with new data")
    print("=" * 60)