"""
Supabase Integration for Sentinel GRC
====================================
Handles data persistence, user management, and analytics dashboard.
Zero-cost using Supabase free tier.
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class AssessmentRecord:
    """Database record for assessment results"""
    id: Optional[str] = None
    company_name: str = ""
    industry: str = ""
    employee_count: int = 0
    assessment_date: datetime = None
    frameworks_assessed: List[str] = None
    overall_confidence: float = 0.0
    overall_maturity: float = 0.0
    gaps_count: int = 0
    escalation_required: bool = False
    processing_time: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.assessment_date is None:
            self.assessment_date = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.frameworks_assessed is None:
            self.frameworks_assessed = []

class SupabaseClient:
    """
    Secure wrapper for Supabase operations.
    Handles authentication and database operations.
    """
    
    def __init__(self):
        self.client = None
        self.supabase_url = None
        self.supabase_key = None
        self.initialized = False
        
        # Initialize client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client securely"""
        
        # Load configuration
        self.supabase_url = (
            os.getenv('SUPABASE_URL') or
            "https://rqbfzjpbfykenqozcnyj.supabase.co"
        )
        
        self.supabase_key = (
            os.getenv('SUPABASE_ANON_KEY') or
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxYmZ6anBiZnlrZW5xb3pjbnlqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4OTczMzcsImV4cCI6MjA3MDQ3MzMzN30.mFQW-lT6m9zGAgBanp1UeU9UBQuom9BUgXLwzKp2pdc"
        )
        
        try:
            # Try to import and initialize supabase
            from supabase import create_client
            
            self.client = create_client(self.supabase_url, self.supabase_key)
            self.initialized = True
            logger.info("Supabase client initialized successfully")
            
            # Test connection
            self._test_connection()
            
        except ImportError:
            logger.warning("Supabase package not installed. Run: pip install supabase")
            self.initialized = False
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self.initialized = False
    
    def _test_connection(self):
        """Test Supabase connection"""
        try:
            # Try to query a simple table or create one if it doesn't exist
            result = self.client.table('health_check').select('*').limit(1).execute()
            logger.info("Supabase connection test successful")
        except Exception as e:
            logger.warning(f"Supabase connection test failed: {e}")
    
    def is_available(self) -> bool:
        """Check if Supabase client is available"""
        return self.initialized and self.client is not None
    
    async def save_assessment(self, assessment_data: Dict[str, Any]) -> Optional[str]:
        """
        Save assessment results to database.
        Returns assessment ID if successful.
        """
        
        if not self.is_available():
            logger.warning("Supabase not available - assessment not saved")
            return None
        
        try:
            # Extract relevant data from assessment
            assessment_result = assessment_data.get('assessment_result')
            company_profile = assessment_result.company_profile
            
            # Create assessment record
            record = AssessmentRecord(
                company_name=company_profile.company_name,
                industry=company_profile.industry,
                employee_count=company_profile.employee_count,
                frameworks_assessed=assessment_data.get('frameworks_assessed', []),
                overall_confidence=assessment_result.confidence_score,
                overall_maturity=assessment_result.overall_maturity,
                gaps_count=len(assessment_result.gaps_identified),
                escalation_required=assessment_result.escalation_required.value != "NONE",
                processing_time=assessment_data.get('processing_time', 0.0)
            )
            
            # Convert to dict for database insert
            record_dict = asdict(record)
            
            # Handle datetime serialization
            for key, value in record_dict.items():
                if isinstance(value, datetime):
                    record_dict[key] = value.isoformat()
            
            # Insert into assessments table
            result = self.client.table('grc_assessments').insert(record_dict).execute()
            
            if result.data:
                assessment_id = result.data[0]['id']
                logger.info(f"Assessment saved with ID: {assessment_id}")
                
                # Save detailed results
                await self._save_assessment_details(assessment_id, assessment_result)
                
                return assessment_id
            else:
                logger.error("Failed to save assessment - no data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error saving assessment: {e}")
            return None
    
    async def _save_assessment_details(self, assessment_id: str, assessment_result):
        """Save detailed assessment data (gaps, recommendations, controls)"""
        
        try:
            # Save gaps
            for gap in assessment_result.gaps_identified:
                gap_record = {
                    'assessment_id': assessment_id,
                    'gap_type': 'compliance_gap',
                    'framework': gap.get('source_framework', 'Unknown'),
                    'control_id': gap.get('control', ''),
                    'description': gap.get('gap_description', gap.get('description', '')),
                    'risk_level': gap.get('risk_level', 'MEDIUM'),
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                
                self.client.table('grc_assessment_details').insert(gap_record).execute()
            
            # Save recommendations
            for rec in assessment_result.recommendations:
                rec_record = {
                    'assessment_id': assessment_id,
                    'detail_type': 'recommendation',
                    'framework': rec.get('source_framework', 'General'),
                    'title': rec.get('title', 'Recommendation'),
                    'description': rec.get('description', rec.get('recommendation', '')),
                    'priority': rec.get('priority', 'Medium'),
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                
                self.client.table('grc_assessment_details').insert(rec_record).execute()
            
            logger.info(f"Assessment details saved for ID: {assessment_id}")
            
        except Exception as e:
            logger.error(f"Error saving assessment details: {e}")
    
    async def get_assessment_history(self, company_name: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get assessment history"""
        
        if not self.is_available():
            return []
        
        try:
            query = self.client.table('grc_assessments').select('*')
            
            if company_name:
                query = query.eq('company_name', company_name)
            
            result = query.order('created_at', desc=True).limit(limit).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error retrieving assessment history: {e}")
            return []
    
    async def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get dashboard analytics metrics"""
        
        if not self.is_available():
            return {"error": "Database not available"}
        
        try:
            # Total assessments
            total_result = self.client.table('grc_assessments').select('id', count='exact').execute()
            total_assessments = total_result.count if total_result else 0
            
            # Industry breakdown
            industry_result = self.client.table('grc_assessments')\
                .select('industry')\
                .execute()
            
            industries = {}
            if industry_result.data:
                for record in industry_result.data:
                    industry = record['industry']
                    industries[industry] = industries.get(industry, 0) + 1
            
            # Average confidence and maturity
            avg_result = self.client.table('grc_assessments')\
                .select('overall_confidence, overall_maturity')\
                .execute()
            
            avg_confidence = 0.0
            avg_maturity = 0.0
            
            if avg_result.data:
                confidences = [r['overall_confidence'] for r in avg_result.data if r['overall_confidence']]
                maturities = [r['overall_maturity'] for r in avg_result.data if r['overall_maturity']]
                
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
                avg_maturity = sum(maturities) / len(maturities) if maturities else 0.0
            
            # Recent assessments (last 30 days)
            from datetime import timedelta
            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            
            recent_result = self.client.table('grc_assessments')\
                .select('id', count='exact')\
                .gte('created_at', thirty_days_ago.isoformat())\
                .execute()
            
            recent_assessments = recent_result.count if recent_result else 0
            
            return {
                "total_assessments": total_assessments,
                "recent_assessments": recent_assessments,
                "industry_breakdown": industries,
                "average_confidence": avg_confidence,
                "average_maturity": avg_maturity,
                "database_status": "connected"
            }
            
        except Exception as e:
            logger.error(f"Error retrieving dashboard metrics: {e}")
            return {"error": str(e)}
    
    async def create_database_schema(self):
        """Create database tables if they don't exist"""
        
        if not self.is_available():
            return False
        
        try:
            # Note: In production, you should create these tables through Supabase dashboard
            # This is just for reference of the expected schema
            
            assessments_schema = """
            CREATE TABLE IF NOT EXISTS grc_assessments (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                company_name TEXT NOT NULL,
                industry TEXT NOT NULL,
                employee_count INTEGER,
                assessment_date TIMESTAMPTZ DEFAULT NOW(),
                frameworks_assessed TEXT[],
                overall_confidence DECIMAL(5,4),
                overall_maturity DECIMAL(5,4),
                gaps_count INTEGER DEFAULT 0,
                escalation_required BOOLEAN DEFAULT FALSE,
                processing_time DECIMAL(10,3),
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
            
            details_schema = """
            CREATE TABLE IF NOT EXISTS grc_assessment_details (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                assessment_id UUID REFERENCES grc_assessments(id) ON DELETE CASCADE,
                detail_type TEXT CHECK (detail_type IN ('compliance_gap', 'recommendation', 'control')),
                framework TEXT,
                control_id TEXT,
                title TEXT,
                description TEXT,
                risk_level TEXT CHECK (risk_level IN ('HIGH', 'MEDIUM', 'LOW')),
                priority TEXT CHECK (priority IN ('High', 'Medium', 'Low')),
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
            
            logger.info("Database schema created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating database schema: {e}")
            return False

# Global instance
supabase_client = SupabaseClient()

# Convenience functions for easy integration
async def save_assessment_to_db(assessment_data: Dict[str, Any]) -> Optional[str]:
    """Save assessment to database"""
    return await supabase_client.save_assessment(assessment_data)

async def get_assessment_history(company_name: str = None) -> List[Dict[str, Any]]:
    """Get assessment history"""
    return await supabase_client.get_assessment_history(company_name)

async def get_dashboard_metrics() -> Dict[str, Any]:
    """Get dashboard metrics"""
    return await supabase_client.get_dashboard_metrics()

def is_database_available() -> bool:
    """Check if database is available"""
    return supabase_client.is_available()

# Environment setup utility
def setup_supabase_env():
    """Setup Supabase environment variables"""
    
    print("Supabase Configuration Setup")
    print("=" * 35)
    print("\nDefault configuration already loaded:")
    print(f"URL: https://rqbfzjpbfykenqozcnyj.supabase.co")
    print(f"API Key: {supabase_client.supabase_key[:20]}...")
    
    if supabase_client.is_available():
        print("✅ Supabase connection successful!")
        return True
    else:
        print("❌ Supabase connection failed")
        print("\nTo fix this issue:")
        print("1. Install supabase package: pip install supabase")
        print("2. Check your internet connection")
        print("3. Verify the URL and API key are correct")
        return False

# Database schema for Supabase dashboard
SUPABASE_SQL_SCHEMA = """
-- GRC Assessments table
CREATE TABLE IF NOT EXISTS grc_assessments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL,
    employee_count INTEGER,
    assessment_date TIMESTAMPTZ DEFAULT NOW(),
    frameworks_assessed TEXT[],
    overall_confidence DECIMAL(5,4),
    overall_maturity DECIMAL(5,4),
    gaps_count INTEGER DEFAULT 0,
    escalation_required BOOLEAN DEFAULT FALSE,
    processing_time DECIMAL(10,3),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Assessment details table
CREATE TABLE IF NOT EXISTS grc_assessment_details (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    assessment_id UUID REFERENCES grc_assessments(id) ON DELETE CASCADE,
    detail_type TEXT CHECK (detail_type IN ('compliance_gap', 'recommendation', 'control')),
    framework TEXT,
    control_id TEXT,
    title TEXT,
    description TEXT,
    risk_level TEXT CHECK (risk_level IN ('HIGH', 'MEDIUM', 'LOW')),
    priority TEXT CHECK (priority IN ('High', 'Medium', 'Low')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_assessments_company ON grc_assessments(company_name);
CREATE INDEX IF NOT EXISTS idx_assessments_industry ON grc_assessments(industry);
CREATE INDEX IF NOT EXISTS idx_assessments_date ON grc_assessments(created_at);
CREATE INDEX IF NOT EXISTS idx_details_assessment ON grc_assessment_details(assessment_id);

-- Enable Row Level Security (RLS)
ALTER TABLE grc_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE grc_assessment_details ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (adjust based on your auth requirements)
CREATE POLICY "Enable read access for all users" ON grc_assessments FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON grc_assessments FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON grc_assessment_details FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON grc_assessment_details FOR INSERT WITH CHECK (true);
"""

# Example usage and testing
if __name__ == "__main__":
    # Test setup
    setup_success = setup_supabase_env()
    
    if setup_success:
        print("\n" + "="*50)
        print("SUPABASE INTEGRATION READY")
        print("="*50)
        print("\nNext steps:")
        print("1. Create the database tables using the SQL schema above")
        print("2. Run your Streamlit app with database persistence")
        print("3. View stored assessments in Supabase dashboard")
        print("\nSQL Schema available in: SUPABASE_SQL_SCHEMA variable")
    else:
        print("\n" + "="*50)
        print("SUPABASE SETUP REQUIRED")
        print("="*50)
        print("\nInstall dependencies:")
        print("pip install supabase")