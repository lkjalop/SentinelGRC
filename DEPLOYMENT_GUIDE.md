# Sentinel GRC Deployment Guide
## Production Deployment Options

### 🚀 Option 1: Streamlit Cloud (Recommended)

**Cost:** Free tier available  
**Time:** 10 minutes  
**Complexity:** Beginner-friendly

#### Prerequisites
- GitHub account
- Streamlit account (free)

#### Steps
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial Sentinel GRC deployment"
   git remote add origin https://github.com/lkjalop/SentinelGRC
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select repository: `lkjalop/SentinelGRC`
   - Main file: `streamlit_demo.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to app settings
   - Add secrets in TOML format:
   ```toml
   [secrets]
   GROQ_API_KEY = "your_groq_key_here"
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_ANON_KEY = "your_supabase_key"
   ```

4. **Custom Domain** (Optional)
   - Available in Streamlit Pro plan ($20/month)
   - Add CNAME record to your domain

**Result:** `https://yourusername-sentinel-grc.streamlit.app`

---

### 🌐 Option 2: Vercel (For Next Steps)

**Cost:** Free tier available  
**Time:** 20 minutes  
**Complexity:** Intermediate

#### Prerequisites
- Vercel account
- Node.js wrapper (we'll create)

#### Create Next.js Wrapper
```bash
npx create-next-app@latest sentinel-grc-web
cd sentinel-grc-web
npm install axios
```

#### Python API Endpoint
Create `api/assess.py` in your Vercel project:
```python
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add your Sentinel GRC files
sys.path.append('/var/task')

from unified_orchestrator import UnifiedSentinelGRC

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle assessment requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Process assessment
        sentinel = UnifiedSentinelGRC(enable_sidecars=False)
        result = sentinel.assess_company(**data)
        
        # Return results
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
```

---

### 🐳 Option 3: Docker Deployment

**Cost:** Infrastructure dependent  
**Time:** 30 minutes  
**Complexity:** Advanced

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "streamlit_demo.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'
services:
  sentinel-grc:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  neo4j:
    image: neo4j:5.13-community
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/Ag3nt-GRC
    volumes:
      - neo4j_data:/data
    restart: unless-stopped

volumes:
  neo4j_data:
```

#### Deploy Commands
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Update deployment
docker-compose pull && docker-compose up -d
```

---

### ☁️ Option 4: Cloud Platforms

#### AWS Deployment
- **Elastic Beanstalk**: Easy deployment, auto-scaling
- **ECS + Fargate**: Container-based, highly scalable
- **Lambda**: Serverless functions (API endpoints)

#### Azure Deployment
- **Container Instances**: Quick container deployment
- **App Service**: Platform-as-a-Service
- **Functions**: Serverless computing

#### Google Cloud Deployment
- **Cloud Run**: Serverless containers
- **App Engine**: Fully managed platform
- **Compute Engine**: Virtual machines

---

## 🔧 Configuration for Production

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Optional
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=Ag3nt-GRC

# Production Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false
```

### Security Headers
Add to your web server configuration:
```nginx
# Nginx example
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'";
```

### Database Setup
```sql
-- Supabase RLS policies
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only see their own assessments" ON assessments
  FOR ALL USING (auth.uid() = user_id);
```

---

## 📊 Monitoring and Maintenance

### Health Checks
```python
# Add to streamlit_demo.py
import streamlit as st

def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        from supabase_integration import test_connection
        db_status = test_connection()
        
        # Test Neo4j connection
        from neo4j_sentinel_integration import GraphEnhancedAssessment
        graph = GraphEnhancedAssessment()
        graph_status = graph.is_available()
        
        # Test Groq API
        from groq_integration_secure import test_groq_connection
        api_status = test_groq_connection()
        
        return {
            "status": "healthy" if all([db_status, graph_status, api_status]) else "degraded",
            "database": "up" if db_status else "down",
            "graph": "up" if graph_status else "down",
            "api": "up" if api_status else "down",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

### Logging Configuration
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sentinel_grc.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Backup Strategy
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)

# Backup Supabase data
pg_dump $DATABASE_URL > backups/supabase_$DATE.sql

# Backup Neo4j data
docker exec neo4j neo4j-admin dump --database=neo4j --to=/backups/neo4j_$DATE.dump

# Backup application files
tar -czf backups/app_$DATE.tar.gz *.py *.md *.json

echo "Backup completed: $DATE"
```

---

## 🚦 Performance Optimization

### Caching Strategy
```python
import streamlit as st
from functools import lru_cache

@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_assessment(company_data):
    """Cache assessment results"""
    return run_assessment(company_data)

@lru_cache(maxsize=100)
def cached_threat_analysis(industry):
    """Cache threat analysis by industry"""
    return analyze_industry_threats(industry)
```

### Database Optimization
```python
# Connection pooling
from supabase import create_client
import os

# Create connection pool
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY"),
    options={
        "pool_pre_ping": True,
        "pool_size": 20,
        "max_overflow": 30
    }
)
```

---

## 🔒 Security Checklist

### Pre-Deployment
- [ ] API keys in environment variables (not code)
- [ ] Input validation on all forms
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF tokens
- [ ] Rate limiting implemented
- [ ] HTTPS enforced
- [ ] Security headers configured

### Post-Deployment
- [ ] Monitor error rates
- [ ] Check security logs
- [ ] Update dependencies regularly
- [ ] Backup data regularly
- [ ] Test disaster recovery
- [ ] Security audit quarterly

---

## 📈 Scaling Strategy

### Performance Tiers

#### Tier 1: Basic (0-100 users/day)
- Single Streamlit instance
- Supabase free tier
- Basic monitoring

#### Tier 2: Growth (100-1000 users/day)
- Load balancer + multiple instances
- Supabase Pro tier
- Redis caching
- Monitoring dashboard

#### Tier 3: Scale (1000+ users/day)
- Container orchestration (K8s)
- Database clustering
- CDN for assets
- Advanced monitoring
- Auto-scaling

---

## 🎯 Quick Start Commands

### Streamlit Cloud
```bash
# 1. Push to GitHub
git init && git add . && git commit -m "Deploy Sentinel GRC"
git remote add origin https://github.com/lkjalop/SentinelGRC
git push -u origin main

# 2. Deploy at share.streamlit.io
# 3. Add secrets in dashboard
```

### Docker Local
```bash
# 1. Build and run
docker-compose up -d

# 2. Access at http://localhost:8501
# 3. Neo4j browser at http://localhost:7474
```

### Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export GROQ_API_KEY="your_key"

# 3. Run locally
streamlit run streamlit_demo.py
```

---

## 📞 Support and Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**Neo4j connection failed**
```bash
# Start Neo4j Desktop or Docker
docker run -p 7474:7474 -p 7687:7687 neo4j:5.13-community
```

**API rate limits**
```bash
# Check usage in API provider dashboard
# Implement caching to reduce requests
```

**Deployment failures**
- Check logs in platform dashboard
- Verify environment variables
- Ensure requirements.txt is complete

### Performance Issues
- Enable caching with `@st.cache_data`
- Use database connection pooling
- Implement lazy loading for large datasets
- Add CDN for static assets

---

*This deployment guide provides multiple paths from development to production. Start with Streamlit Cloud for quick deployment, then scale as needed.*