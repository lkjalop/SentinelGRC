"""
Compliance Data Scraper for Australian Regulatory Sources
==========================================================
Automatically collects and updates compliance information from official sources
to keep the knowledge base current with regulatory changes.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
import httpx
import schedule
import time
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapedContent:
    """Structure for scraped compliance content"""
    source: str
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    scraped_at: datetime
    content_hash: str

class ComplianceDataScraper:
    """
    Scrapes Australian compliance sources for agent knowledge.
    Designed to run as a background service updating the knowledge base.
    """
    
    def __init__(self, knowledge_graph=None, cache_dir="./compliance_cache"):
        self.sources = {
            "essential8": {
                "url": "https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/essential-eight",
                "type": "framework",
                "frequency": "weekly"
            },
            "privacy": {
                "url": "https://www.oaic.gov.au/privacy/australian-privacy-principles",
                "type": "regulation",
                "frequency": "monthly"
            },
            "apra": {
                "url": "https://www.apra.gov.au/information-security",
                "type": "standard",
                "frequency": "monthly"
            },
            "acsc_advisories": {
                "url": "https://www.cyber.gov.au/about-us/view-all-content/advisories",
                "type": "threat_intel",
                "frequency": "daily"
            },
            "soci_act": {
                "url": "https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/security-of-critical-infrastructure",
                "type": "regulation",
                "frequency": "monthly"
            }
        }
        
        self.knowledge_graph = knowledge_graph
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Track last scrape times
        self.last_scrape_file = self.cache_dir / "last_scrape.json"
        self.last_scrape_times = self.load_last_scrape_times()
        
    def load_last_scrape_times(self) -> Dict[str, str]:
        """Load last scrape timestamps from cache"""
        if self.last_scrape_file.exists():
            with open(self.last_scrape_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_last_scrape_time(self, source: str):
        """Save last scrape timestamp"""
        self.last_scrape_times[source] = datetime.now().isoformat()
        with open(self.last_scrape_file, 'w') as f:
            json.dump(self.last_scrape_times, f)
    
    async def scrape_essential8_updates(self) -> Optional[ScrapedContent]:
        """
        Weekly scrape for Essential 8 changes.
        Extracts maturity levels, control descriptions, and implementation guidance.
        """
        logger.info("Scraping Essential 8 updates...")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(self.sources["essential8"]["url"])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract maturity model sections
                maturity_data = []
                
                # Look for maturity level sections (adjust selectors based on actual HTML)
                maturity_sections = soup.find_all(['div', 'section'], 
                                                 class_=['maturity-level', 'content-block'])
                
                for section in maturity_sections:
                    # Extract control information
                    title = section.find(['h2', 'h3'])
                    description = section.find(['p', 'div'], class_='description')
                    
                    if title:
                        maturity_data.append({
                            'title': title.get_text(strip=True),
                            'description': description.get_text(strip=True) if description else '',
                            'html': str(section)
                        })
                
                # Extract Essential 8 controls
                controls = self.extract_essential8_controls(soup)
                
                content = ScrapedContent(
                    source="essential8",
                    url=self.sources["essential8"]["url"],
                    title="Essential 8 Maturity Model",
                    content=json.dumps({
                        'maturity_levels': maturity_data,
                        'controls': controls,
                        'last_updated': datetime.now().isoformat()
                    }),
                    metadata={
                        'framework': 'Essential 8',
                        'publisher': 'ACSC',
                        'version': self.extract_version(soup)
                    },
                    scraped_at=datetime.now(),
                    content_hash=self.generate_content_hash(str(maturity_data))
                )
                
                # Store in knowledge graph if available
                if self.knowledge_graph:
                    await self.update_knowledge_graph(content)
                
                # Cache locally
                self.save_to_cache(content)
                
                self.save_last_scrape_time("essential8")
                logger.info("Essential 8 scraping completed successfully")
                
                return content
                
        except Exception as e:
            logger.error(f"Error scraping Essential 8: {e}")
            return None
    
    def extract_essential8_controls(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract the 8 essential controls from the page"""
        controls = []
        
        # Common patterns for finding controls
        control_keywords = [
            "Application control",
            "Patch applications", 
            "Configure Microsoft Office",
            "User application hardening",
            "Restrict administrative privileges",
            "Patch operating systems",
            "Multi-factor authentication",
            "Regular backups"
        ]
        
        for keyword in control_keywords:
            # Find elements containing control keywords
            elements = soup.find_all(text=lambda text: keyword.lower() in text.lower() if text else False)
            
            for element in elements[:1]:  # Take first match
                parent = element.parent
                if parent:
                    controls.append({
                        'name': keyword,
                        'description': parent.get_text(strip=True)[:500]  # Limit description length
                    })
        
        return controls
    
    async def scrape_privacy_act_updates(self) -> Optional[ScrapedContent]:
        """
        Monthly scrape for Privacy Act and APP updates.
        Focuses on Australian Privacy Principles and recent guidance.
        """
        logger.info("Scraping Privacy Act updates...")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(self.sources["privacy"]["url"])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract APP principles
                principles = []
                
                # Look for APP sections (typically numbered 1-13)
                app_sections = soup.find_all(['div', 'section'], 
                                            class_=['principle', 'app-principle', 'content'])
                
                for section in app_sections:
                    title = section.find(['h2', 'h3'])
                    if title and 'APP' in title.get_text():
                        principles.append({
                            'principle': title.get_text(strip=True),
                            'content': section.get_text(strip=True)[:1000],
                            'requirements': self.extract_requirements(section)
                        })
                
                content = ScrapedContent(
                    source="privacy",
                    url=self.sources["privacy"]["url"],
                    title="Australian Privacy Principles",
                    content=json.dumps({
                        'principles': principles,
                        'total_principles': len(principles),
                        'last_updated': datetime.now().isoformat()
                    }),
                    metadata={
                        'regulation': 'Privacy Act 1988',
                        'publisher': 'OAIC',
                        'jurisdiction': 'Australia'
                    },
                    scraped_at=datetime.now(),
                    content_hash=self.generate_content_hash(str(principles))
                )
                
                if self.knowledge_graph:
                    await self.update_knowledge_graph(content)
                
                self.save_to_cache(content)
                self.save_last_scrape_time("privacy")
                
                logger.info(f"Privacy Act scraping completed - found {len(principles)} principles")
                return content
                
        except Exception as e:
            logger.error(f"Error scraping Privacy Act: {e}")
            return None
    
    async def scrape_apra_cps234(self) -> Optional[ScrapedContent]:
        """
        Scrape APRA CPS 234 Information Security requirements.
        Critical for financial services compliance.
        """
        logger.info("Scraping APRA CPS 234...")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(self.sources["apra"]["url"])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract CPS 234 specific requirements
                requirements = {
                    'information_security': [],
                    'incident_management': [],
                    'testing_and_assurance': []
                }
                
                # Look for CPS 234 content
                cps_sections = soup.find_all(text=lambda text: 'CPS 234' in text if text else False)
                
                for text_element in cps_sections:
                    parent = text_element.parent
                    if parent:
                        content_text = parent.get_text(strip=True)
                        
                        if 'incident' in content_text.lower():
                            requirements['incident_management'].append(content_text[:500])
                        elif 'test' in content_text.lower() or 'assurance' in content_text.lower():
                            requirements['testing_and_assurance'].append(content_text[:500])
                        else:
                            requirements['information_security'].append(content_text[:500])
                
                content = ScrapedContent(
                    source="apra",
                    url=self.sources["apra"]["url"],
                    title="APRA CPS 234 Information Security",
                    content=json.dumps(requirements),
                    metadata={
                        'standard': 'CPS 234',
                        'publisher': 'APRA',
                        'sector': 'Financial Services'
                    },
                    scraped_at=datetime.now(),
                    content_hash=self.generate_content_hash(str(requirements))
                )
                
                if self.knowledge_graph:
                    await self.update_knowledge_graph(content)
                
                self.save_to_cache(content)
                self.save_last_scrape_time("apra")
                
                logger.info("APRA CPS 234 scraping completed")
                return content
                
        except Exception as e:
            logger.error(f"Error scraping APRA CPS 234: {e}")
            return None
    
    async def scrape_threat_intelligence(self) -> Optional[List[ScrapedContent]]:
        """
        Daily ACSC threat advisory scraping.
        Extracts current threats, vulnerabilities, and mitigation advice.
        """
        logger.info("Scraping ACSC threat advisories...")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(self.sources["acsc_advisories"]["url"])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                advisories = []
                
                # Look for advisory listings
                advisory_items = soup.find_all(['article', 'div'], class_=['advisory', 'alert', 'item'])
                
                for item in advisory_items[:10]:  # Latest 10 advisories
                    title = item.find(['h2', 'h3', 'a'])
                    date = item.find(['time', 'span'], class_=['date', 'published'])
                    severity = item.find(['span', 'div'], class_=['severity', 'level'])
                    
                    if title:
                        advisory = {
                            'title': title.get_text(strip=True),
                            'date': date.get_text(strip=True) if date else '',
                            'severity': severity.get_text(strip=True) if severity else 'Unknown',
                            'summary': item.get_text(strip=True)[:500]
                        }
                        advisories.append(advisory)
                
                content = ScrapedContent(
                    source="acsc_advisories",
                    url=self.sources["acsc_advisories"]["url"],
                    title="ACSC Threat Advisories",
                    content=json.dumps(advisories),
                    metadata={
                        'type': 'threat_intelligence',
                        'publisher': 'ACSC',
                        'advisory_count': len(advisories)
                    },
                    scraped_at=datetime.now(),
                    content_hash=self.generate_content_hash(str(advisories))
                )
                
                if self.knowledge_graph:
                    await self.update_knowledge_graph(content)
                
                self.save_to_cache(content)
                self.save_last_scrape_time("acsc_advisories")
                
                logger.info(f"Threat intelligence scraping completed - found {len(advisories)} advisories")
                return [content]
                
        except Exception as e:
            logger.error(f"Error scraping threat intelligence: {e}")
            return None
    
    def extract_requirements(self, section) -> List[str]:
        """Extract specific requirements from a section"""
        requirements = []
        
        # Look for list items which often contain requirements
        list_items = section.find_all(['li', 'ul', 'ol'])
        for item in list_items[:5]:  # Limit to prevent huge lists
            text = item.get_text(strip=True)
            if len(text) > 20:  # Filter out trivial items
                requirements.append(text[:200])
        
        return requirements
    
    def extract_version(self, soup: BeautifulSoup) -> str:
        """Extract version information if available"""
        version_patterns = ['version', 'v.', 'revision', 'updated']
        
        for pattern in version_patterns:
            version_elem = soup.find(text=lambda text: pattern in text.lower() if text else False)
            if version_elem:
                return version_elem.strip()[:50]
        
        return "Unknown"
    
    def generate_content_hash(self, content: str) -> str:
        """Generate hash to detect content changes"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()
    
    async def update_knowledge_graph(self, content: ScrapedContent):
        """
        Update the knowledge graph with scraped content.
        This integrates with your existing ComplianceKnowledgeGraph.
        """
        if not self.knowledge_graph:
            logger.warning("Knowledge graph not configured")
            return
        
        try:
            # Add to knowledge graph based on content type
            if content.source == "essential8":
                # Update Essential 8 controls in graph
                data = json.loads(content.content)
                for control in data.get('controls', []):
                    # This would integrate with your existing graph structure
                    logger.info(f"Updating knowledge graph with control: {control.get('name')}")
            
            elif content.source == "privacy":
                # Update Privacy Act requirements
                data = json.loads(content.content)
                for principle in data.get('principles', []):
                    logger.info(f"Updating knowledge graph with APP: {principle.get('principle')}")
            
            # Add more integration logic as needed
            
        except Exception as e:
            logger.error(f"Error updating knowledge graph: {e}")
    
    def save_to_cache(self, content: ScrapedContent):
        """Save scraped content to local cache"""
        cache_file = self.cache_dir / f"{content.source}_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(cache_file, 'w') as f:
            json.dump({
                'source': content.source,
                'url': content.url,
                'title': content.title,
                'content': content.content,
                'metadata': content.metadata,
                'scraped_at': content.scraped_at.isoformat(),
                'content_hash': content.content_hash
            }, f, indent=2)
        
        logger.info(f"Cached content to {cache_file}")
    
    def schedule_scraping(self):
        """
        Production scraping schedule.
        Runs different sources at appropriate intervals.
        """
        # Daily tasks
        schedule.every().day.at("02:00").do(
            lambda: asyncio.run(self.scrape_threat_intelligence())
        )
        
        # Weekly tasks
        schedule.every().monday.at("03:00").do(
            lambda: asyncio.run(self.scrape_essential8_updates())
        )
        
        # Monthly tasks
        schedule.every(30).days.at("04:00").do(
            lambda: asyncio.run(self.scrape_privacy_act_updates())
        )
        schedule.every(30).days.at("04:30").do(
            lambda: asyncio.run(self.scrape_apra_cps234())
        )
        
        logger.info("Scraping schedule configured")
    
    def run_scheduler(self):
        """Run the scheduler in production"""
        self.schedule_scraping()
        
        logger.info("Starting compliance data scraper scheduler...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    async def run_all_scrapers(self):
        """
        Run all scrapers once (useful for initial population or testing).
        """
        logger.info("Running all scrapers...")
        
        tasks = [
            self.scrape_essential8_updates(),
            self.scrape_privacy_act_updates(),
            self.scrape_apra_cps234(),
            self.scrape_threat_intelligence()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = sum(1 for r in results if r and not isinstance(r, Exception))
        logger.info(f"Scraping completed: {successful}/{len(tasks)} successful")
        
        return results


# Example usage and testing
if __name__ == "__main__":
    # For testing - run all scrapers once
    scraper = ComplianceDataScraper()
    
    # Run all scrapers
    asyncio.run(scraper.run_all_scrapers())
    
    # For production - uncomment to run on schedule
    # scraper.run_scheduler()