"""
PDF Batch Processor for ISO27001 Compliance Documents
Handles API limitations by processing PDFs in controlled batches
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import PyPDF2
import pdfplumber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFBatchProcessor:
    """Processes multiple PDFs in batches to avoid API limitations"""
    
    def __init__(self, max_pages_per_batch: int = 95):
        """
        Initialize with conservative 95-page limit (under 100-page API limit)
        """
        self.max_pages_per_batch = max_pages_per_batch
        self.processed_content = {}
        self.batch_metadata = []
        
    def count_pdf_pages(self, pdf_path: str) -> int:
        """Count pages in a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            logger.error(f"Error counting pages in {pdf_path}: {e}")
            return 0
    
    def create_batches(self, pdf_directory: str) -> List[List[Dict[str, Any]]]:
        """
        Create optimized batches of PDFs that stay under page limit
        """
        pdf_files = sorted([f for f in os.listdir(pdf_directory) if f.endswith('.pdf')])
        
        # Get page counts for all PDFs
        pdf_info = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_directory, pdf_file)
            page_count = self.count_pdf_pages(pdf_path)
            pdf_info.append({
                'filename': pdf_file,
                'path': pdf_path,
                'pages': page_count
            })
            logger.info(f"📄 {pdf_file}: {page_count} pages")
        
        # Create batches
        batches = []
        current_batch = []
        current_pages = 0
        
        for pdf in pdf_info:
            if current_pages + pdf['pages'] > self.max_pages_per_batch:
                # Start new batch
                if current_batch:
                    batches.append(current_batch)
                current_batch = [pdf]
                current_pages = pdf['pages']
            else:
                current_batch.append(pdf)
                current_pages += pdf['pages']
        
        # Add final batch
        if current_batch:
            batches.append(current_batch)
        
        # Log batch information
        for i, batch in enumerate(batches, 1):
            total_pages = sum(pdf['pages'] for pdf in batch)
            files = [pdf['filename'] for pdf in batch]
            logger.info(f"📦 Batch {i}: {len(files)} files, {total_pages} pages")
            logger.info(f"   Files: {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")
        
        return batches
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF using pdfplumber"""
        try:
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return '\n'.join(text_content)
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            # Fallback to PyPDF2
            return self._extract_with_pypdf2(pdf_path)
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Fallback text extraction using PyPDF2"""
        try:
            text_content = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return '\n'.join(text_content)
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed for {pdf_path}: {e}")
            return ""
    
    def process_batch(self, batch: List[Dict[str, Any]], batch_num: int) -> Dict[str, Any]:
        """
        Process a single batch of PDFs
        """
        logger.info(f"🔄 Processing Batch {batch_num}...")
        
        batch_content = {
            'batch_number': batch_num,
            'timestamp': datetime.now().isoformat(),
            'files': [],
            'total_pages': sum(pdf['pages'] for pdf in batch),
            'extracted_content': {}
        }
        
        for pdf in batch:
            logger.info(f"  📖 Extracting: {pdf['filename']}")
            text_content = self.extract_text_from_pdf(pdf['path'])
            
            # Store extracted content
            batch_content['files'].append(pdf['filename'])
            batch_content['extracted_content'][pdf['filename']] = {
                'pages': pdf['pages'],
                'text_length': len(text_content),
                'content': text_content[:1000] + '...' if len(text_content) > 1000 else text_content,
                'full_content': text_content  # Store full content for processing
            }
            
            # Also store in main content dictionary
            self.processed_content[pdf['filename']] = text_content
        
        logger.info(f"✅ Batch {batch_num} processed successfully")
        return batch_content
    
    def process_all_pdfs(self, pdf_directory: str) -> Dict[str, Any]:
        """
        Main method to process all PDFs in directory
        """
        logger.info(f"🚀 Starting PDF batch processing for: {pdf_directory}")
        
        # Create batches
        batches = self.create_batches(pdf_directory)
        
        # Process each batch
        results = {
            'total_batches': len(batches),
            'timestamp': datetime.now().isoformat(),
            'directory': pdf_directory,
            'batches': []
        }
        
        for i, batch in enumerate(batches, 1):
            batch_result = self.process_batch(batch, i)
            results['batches'].append(batch_result)
            self.batch_metadata.append(batch_result)
        
        # Save extracted content to cache
        cache_file = Path(pdf_directory).parent / 'pdf_content_cache.json'
        self.save_cache(cache_file)
        
        logger.info(f"✨ Processing complete! {len(self.processed_content)} PDFs processed")
        return results
    
    def save_cache(self, cache_path: Path):
        """Save extracted content to cache file"""
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'content': {k: v[:5000] for k, v in self.processed_content.items()},  # Store preview
            'metadata': self.batch_metadata
        }
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Cache saved to: {cache_path}")
    
    def analyze_for_iso27001(self) -> Dict[str, Any]:
        """
        Analyze extracted content for ISO27001 compliance mapping
        """
        iso_controls = {
            'A.5': 'Information security policies',
            'A.6': 'Organization of information security',
            'A.8': 'Asset management',
            'A.10': 'Cryptography',
            'A.11': 'Physical and environmental security',
            'A.12': 'Operations security',
            'A.13': 'Communications security',
            'A.14': 'System acquisition, development and maintenance',
            'A.15': 'Supplier relationships',
            'A.16': 'Information security incident management',
            'A.17': 'Business continuity management',
            'A.18': 'Compliance'
        }
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'documents_analyzed': len(self.processed_content),
            'control_coverage': {},
            'policy_mapping': {}
        }
        
        # Map each document to ISO controls
        for filename, content in self.processed_content.items():
            content_lower = content.lower()
            covered_controls = []
            
            for control, description in iso_controls.items():
                # Simple keyword matching (can be enhanced with NLP)
                keywords = description.lower().split()
                if any(keyword in content_lower for keyword in keywords):
                    covered_controls.append(control)
            
            analysis['policy_mapping'][filename] = {
                'covered_controls': covered_controls,
                'primary_focus': covered_controls[0] if covered_controls else 'General'
            }
        
        # Calculate coverage statistics
        all_covered = set()
        for mapping in analysis['policy_mapping'].values():
            all_covered.update(mapping['covered_controls'])
        
        analysis['control_coverage'] = {
            'total_controls': len(iso_controls),
            'covered_controls': len(all_covered),
            'coverage_percentage': (len(all_covered) / len(iso_controls)) * 100,
            'covered_list': list(all_covered)
        }
        
        return analysis


# Example usage function
def process_brunel_pdfs():
    """Process Brunel ISO27001 PDFs"""
    processor = PDFBatchProcessor(max_pages_per_batch=95)
    
    # Process PDFs
    brunel_dir = r"D:\AI\New folder\Brunel"
    results = processor.process_all_pdfs(brunel_dir)
    
    # Analyze for ISO27001
    iso_analysis = processor.analyze_for_iso27001()
    
    # Save results
    output_path = Path(brunel_dir).parent / 'brunel_iso27001_analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'processing_results': results,
            'iso27001_analysis': iso_analysis
        }, f, indent=2)
    
    logger.info(f"📊 Analysis saved to: {output_path}")
    return processor, results, iso_analysis

if __name__ == "__main__":
    processor, results, analysis = process_brunel_pdfs()
    print(f"\n✅ Processed {len(processor.processed_content)} PDFs in {results['total_batches']} batches")
    print(f"📊 ISO27001 Coverage: {analysis['control_coverage']['coverage_percentage']:.1f}%")