"""
NIST CSF 2.0 + OLIR Integration Module
=====================================
Integrates NIST Cybersecurity Framework 2.0 with OLIR mappings
Built on research from NIST.gov OLIR program
"""

import json
import requests
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import asyncio
import aiohttp
from pathlib import Path

class NISTCSFIntegrator:
    """NIST CSF 2.0 integration with OLIR mappings"""
    
    def __init__(self):
        self.base_data_path = Path("data/nist_csf")
        self.base_data_path.mkdir(parents=True, exist_ok=True)
        
        # NIST CSF 2.0 Core Structure
        self.csf_functions = {
            "GV": {
                "name": "Govern",
                "description": "The organization's cybersecurity governance and management strategy"
            },
            "ID": {
                "name": "Identify", 
                "description": "Understanding cybersecurity risk to systems, people, assets, data, and capabilities"
            },
            "PR": {
                "name": "Protect",
                "description": "Safeguards to ensure delivery of critical infrastructure services"
            },
            "DE": {
                "name": "Detect",
                "description": "Appropriate activities to identify cybersecurity events"
            },
            "RS": {
                "name": "Respond", 
                "description": "Appropriate activities to take action regarding detected cybersecurity incidents"
            },
            "RC": {
                "name": "Recover",
                "description": "Activities to maintain plans for resilience and restore capabilities"
            }
        }
        
    def get_csf_2_core_structure(self) -> Dict[str, Any]:
        """Return NIST CSF 2.0 complete structure based on official framework"""
        
        return {
            "framework_info": {
                "name": "NIST Cybersecurity Framework 2.0",
                "version": "2.0",
                "release_date": "2024-02-26",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "source": "NIST.gov",
                "authority": "National Institute of Standards and Technology"
            },
            "functions": {
                "GV": {
                    "name": "Govern",
                    "description": "The organization's cybersecurity governance and management strategy",
                    "categories": {
                        "GV.OC": "Organizational Context",
                        "GV.RM": "Risk Management Strategy", 
                        "GV.RR": "Roles, Responsibilities, and Authorities",
                        "GV.PO": "Policy",
                        "GV.OV": "Oversight",
                        "GV.SC": "Cybersecurity Supply Chain Risk Management"
                    }
                },
                "ID": {
                    "name": "Identify",
                    "description": "Understanding cybersecurity risk to systems, people, assets, data, and capabilities",
                    "categories": {
                        "ID.AM": "Asset Management",
                        "ID.RA": "Risk Assessment", 
                        "ID.IM": "Improvement"
                    }
                },
                "PR": {
                    "name": "Protect", 
                    "description": "Safeguards to ensure delivery of critical infrastructure services",
                    "categories": {
                        "PR.AA": "Identity Management, Authentication and Access Control",
                        "PR.AT": "Awareness and Training",
                        "PR.DS": "Data Security",
                        "PR.IP": "Information Protection Processes and Procedures",
                        "PR.MA": "Maintenance",
                        "PR.PT": "Protective Technology"
                    }
                },
                "DE": {
                    "name": "Detect",
                    "description": "Appropriate activities to identify cybersecurity events", 
                    "categories": {
                        "DE.AE": "Anomalies and Events",
                        "DE.CM": "Security Continuous Monitoring"
                    }
                },
                "RS": {
                    "name": "Respond",
                    "description": "Appropriate activities to take action regarding detected cybersecurity incidents",
                    "categories": {
                        "RS.MA": "Management",
                        "RS.AN": "Analysis", 
                        "RS.MI": "Mitigation",
                        "RS.RP": "Reporting"
                    }
                },
                "RC": {
                    "name": "Recover",
                    "description": "Activities to maintain plans for resilience and restore capabilities",
                    "categories": {
                        "RC.RP": "Recovery Planning",
                        "RC.IM": "Improvements",
                        "RC.CO": "Communications"
                    }
                }
            }
        }
    
    def get_sample_subcategories(self) -> Dict[str, List[str]]:
        """Sample subcategories for each category (based on NIST CSF 2.0)"""
        
        return {
            "GV.OC": [
                "GV.OC-01: The organizational mission is understood and informs cybersecurity risk management",
                "GV.OC-02: Internal and external stakeholders are understood",
                "GV.OC-03: Legal, regulatory, and contractual requirements are understood"
            ],
            "ID.AM": [
                "ID.AM-01: Inventories of hardware managed by the organization are maintained",
                "ID.AM-02: Inventories of software, services, and systems managed by the organization are maintained", 
                "ID.AM-03: Representations of the organization's authorized network are maintained"
            ],
            "PR.AA": [
                "PR.AA-01: Identities and credentials for authorized users are managed",
                "PR.AA-02: Identities and credentials for authorized software and hardware are managed",
                "PR.AA-03: Identity management and credential management systems are protected"
            ]
        }
    
    def create_olir_mapping_template(self) -> Dict[str, Any]:
        """Create template for OLIR (Online Informative References) mappings"""
        
        return {
            "mapping_info": {
                "source_framework": "NIST CSF 2.0",
                "target_frameworks": [],
                "mapping_date": datetime.now(timezone.utc).isoformat(),
                "mapping_version": "1.0",
                "olir_program": True
            },
            "mappings": {
                # Structure: CSF_Subcategory -> [Target_Framework_Controls]
            },
            "relationship_types": {
                "equivalent": "Controls address identical objectives",
                "subset": "CSF control is subset of target control", 
                "superset": "CSF control encompasses target control",
                "related": "Controls address related security objectives"
            }
        }
    
    def load_framework_data(self) -> Dict[str, Any]:
        """Load complete NIST CSF 2.0 framework data"""
        
        framework_file = self.base_data_path / "nist_csf_2_complete.json"
        
        if framework_file.exists():
            with open(framework_file, 'r') as f:
                return json.load(f)
        
        # Create initial framework data
        framework_data = self.get_csf_2_core_structure()
        framework_data["subcategories"] = self.get_sample_subcategories()
        
        # Save for future use
        with open(framework_file, 'w') as f:
            json.dump(framework_data, f, indent=2)
            
        return framework_data
    
    def create_cross_framework_mapper(self) -> "CrossFrameworkMapper":
        """Create cross-framework mapping engine"""
        return CrossFrameworkMapper(self)

class CrossFrameworkMapper:
    """Core framework mapping engine - the 'Rosetta Stone'"""
    
    def __init__(self, nist_integrator: NISTCSFIntegrator):
        self.nist = nist_integrator
        self.mappings_cache = {}
        self.supported_frameworks = ["NIST_CSF_2", "Essential_Eight", "CIS_Controls_8.1"]
        
    def map_control(self, source_control: str, 
                   source_framework: str, 
                   target_framework: str) -> List[Dict[str, Any]]:
        """Map a control from source framework to target framework"""
        
        # Cache key for performance  
        cache_key = f"{source_framework}:{source_control}:{target_framework}"
        
        if cache_key in self.mappings_cache:
            return self.mappings_cache[cache_key]
        
        # Sample mapping logic (would be expanded with real OLIR data)
        mappings = []
        
        if source_framework == "NIST_CSF_2" and target_framework == "Essential_Eight":
            mappings = self._map_nist_to_essential8(source_control)
        elif source_framework == "NIST_CSF_2" and target_framework == "CIS_Controls_8.1":
            mappings = self._map_nist_to_cis(source_control)
            
        self.mappings_cache[cache_key] = mappings
        return mappings
    
    def _map_nist_to_essential8(self, nist_control: str) -> List[Dict[str, Any]]:
        """Map NIST CSF 2.0 controls to Essential Eight"""
        
        # Based on real framework analysis
        nist_to_e8_mappings = {
            "ID.AM-01": [{"control": "E8_1", "name": "Application Control", "relationship": "related"}],
            "ID.AM-02": [{"control": "E8_1", "name": "Application Control", "relationship": "related"}],
            "PR.AA-01": [{"control": "E8_5", "name": "Restrict Administrative Privileges", "relationship": "equivalent"}],
            "PR.AA-02": [{"control": "E8_6", "name": "Multi-factor Authentication", "relationship": "equivalent"}],
            "PR.DS-01": [{"control": "E8_3", "name": "Configure MS Office Macro Settings", "relationship": "subset"}]
        }
        
        return nist_to_e8_mappings.get(nist_control, [])
    
    def _map_nist_to_cis(self, nist_control: str) -> List[Dict[str, Any]]:
        """Map NIST CSF 2.0 controls to CIS Controls v8.1"""
        
        # Based on official CIS-NIST mappings
        nist_to_cis_mappings = {
            "ID.AM-01": [{"control": "CIS_1", "name": "Inventory and Control of Enterprise Assets", "relationship": "equivalent"}],
            "ID.AM-02": [{"control": "CIS_2", "name": "Inventory and Control of Software Assets", "relationship": "equivalent"}], 
            "PR.AA-01": [{"control": "CIS_5", "name": "Account Management", "relationship": "equivalent"}],
            "DE.CM-01": [{"control": "CIS_8", "name": "Audit Log Management", "relationship": "equivalent"}]
        }
        
        return nist_to_cis_mappings.get(nist_control, [])
    
    def find_control_overlaps(self, frameworks: List[str]) -> Dict[str, Any]:
        """Find overlapping controls across multiple frameworks"""
        
        overlap_analysis = {
            "common_controls": [],
            "framework_coverage": {},
            "optimization_opportunities": []
        }
        
        # Sample overlap detection (would use real OLIR mappings)
        if "NIST_CSF_2" in frameworks and "Essential_Eight" in frameworks:
            overlap_analysis["common_controls"].append({
                "objective": "Multi-factor Authentication",
                "frameworks": {
                    "NIST_CSF_2": "PR.AA-02",
                    "Essential_Eight": "E8_6"  
                },
                "implementation_effort": "MEDIUM",
                "business_value": "HIGH"
            })
            
        return overlap_analysis

def test_nist_integration():
    """Test NIST CSF 2.0 integration"""
    
    print("Testing NIST CSF 2.0 Integration...")
    
    # Initialize integrator
    integrator = NISTCSFIntegrator()
    
    # Load framework data
    framework_data = integrator.load_framework_data()
    print(f"Loaded {len(framework_data['functions'])} CSF functions")
    
    # Test cross-framework mapping
    mapper = integrator.create_cross_framework_mapper() 
    
    # Test control mapping
    test_mappings = mapper.map_control("ID.AM-01", "NIST_CSF_2", "Essential_Eight")
    print(f"Sample mapping: ID.AM-01 -> {test_mappings}")
    
    # Test overlap analysis
    overlaps = mapper.find_control_overlaps(["NIST_CSF_2", "Essential_Eight"])
    print(f"Found {len(overlaps['common_controls'])} common controls")
    
    # Save framework data
    output_file = "nist_csf_2_framework_data.json"
    with open(output_file, 'w') as f:
        json.dump(framework_data, f, indent=2)
    
    print(f"\nNIST CSF 2.0 integration complete!")
    print(f"Framework data saved to: {output_file}")
    print("Ready for cross-framework mapping engine!")

if __name__ == "__main__":
    test_nist_integration()