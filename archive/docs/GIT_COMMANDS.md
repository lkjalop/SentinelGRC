# Git Commands for Sentinel GRC Deployment
## Ready-to-Execute Commands

### 🚀 Initial Setup (Run these in order)

```bash
# 1. Initialize Git repository
git init

# 2. Add all files to staging
git add .

# 3. Create initial commit
git commit -m "feat: Initial Sentinel GRC platform with 72 controls across 10 frameworks

- Implement Essential 8, Privacy Act, APRA CPS 234, SOCI Act
- Add enterprise frameworks: HIPAA, PCI DSS, ISO 27001
- Neo4j knowledge graph with 155+ relationships  
- Streamlit UI with PDF report generation
- Groq AI enhancement with fallback systems
- Comprehensive demo data (10 companies, 5 scenarios)
- Basic security hardening and input validation
- Zero-cost deployment architecture

Current capabilities:
- 72 controls across 10 compliance frameworks
- Multi-agent assessment orchestration
- Cross-framework relationship mapping
- Professional PDF reporting
- Real-time threat analysis
- $250K platform value with $0 investment"

# 4. Connect to your GitHub repository
git remote add origin https://github.com/lkjalop/SentinelGRC.git

# 5. Push to GitHub (creates main branch)
git push -u origin main
```

### 🔄 Regular Updates (After changes)

```bash
# Check status
git status

# Add specific files
git add filename.py
# OR add all changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new framework support"
# OR
git commit -m "fix: Resolve Neo4j connection issue"
# OR  
git commit -m "docs: Update deployment guide"

# Push changes
git push
```

### 🏷️ Version Tags (For releases)

```bash
# Create version tag
git tag -a v1.0.0 -m "Release v1.0.0: Production-ready GRC platform
- 72 controls across 10 frameworks
- Neo4j knowledge graph integration
- PDF report generation
- Enterprise security hardening"

# Push tags
git push origin --tags

# List all tags
git tag -l
```

### 🌿 Branch Management (For features)

```bash
# Create and switch to feature branch
git checkout -b feature/api-endpoints

# Work on feature, then commit
git add .
git commit -m "feat: Add REST API endpoints for assessment"

# Switch back to main
git checkout main

# Merge feature branch
git merge feature/api-endpoints

# Delete feature branch
git branch -d feature/api-endpoints

# Push merged changes
git push
```

### 📦 Repository Structure Check

```bash
# Before pushing, verify these files exist:
ls -la

# Should see:
# .gitignore
# README.md  
# DEPLOYMENT_GUIDE.md
# requirements.txt
# streamlit_demo.py
# unified_orchestrator.py
# security_utils.py
# (and all other .py files)
```

### 🔧 Troubleshooting Commands

```bash
# If you get authentication errors:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# If you need to reset remote URL:
git remote set-url origin https://github.com/lkjalop/SentinelGRC.git

# If you need to force push (careful!):
git push --force-with-lease

# If you need to unstage files:
git reset HEAD filename.py

# If you need to see commit history:
git log --oneline

# If you need to see what changed:
git diff
```

### 📋 Pre-Push Checklist

```bash
# 1. Test the system works locally
streamlit run streamlit_demo.py

# 2. Check no sensitive data in commits
git log --oneline | head -5
# Look for any API keys or passwords in commit messages

# 3. Verify .gitignore working
git status
# Should not see .env, __pycache__, *.pyc files

# 4. Test imports work
python -c "import unified_orchestrator; print('Imports OK')"

# 5. Run security check
python security_utils.py
```

### 🚀 Streamlit Cloud Deployment

After pushing to GitHub:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub account
3. Select repository: `lkjalop/SentinelGRC`
4. Main file path: `streamlit_demo.py`
5. Click "Deploy"

Add secrets in Streamlit dashboard:
```toml
GROQ_API_KEY = "your_groq_key"
SUPABASE_URL = "your_supabase_url"  
SUPABASE_ANON_KEY = "your_supabase_key"
```

### 📊 Repository Statistics

```bash
# Count lines of code
find . -name "*.py" -exec wc -l {} + | tail -1

# Count number of files
find . -name "*.py" | wc -l

# See repository size
du -sh .

# Show commit authors
git shortlog -sn
```

### 🔄 Sync with Remote Changes

```bash
# Fetch latest changes
git fetch origin

# Merge remote changes
git pull origin main

# Or if you prefer rebase
git pull --rebase origin main
```

---

## 📝 Commit Message Conventions

Use these prefixes for clear commit history:

- `feat:` New feature
- `fix:` Bug fix  
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```bash
git commit -m "feat: Add NIST Cybersecurity Framework support"
git commit -m "fix: Resolve Neo4j connection timeout issue"
git commit -m "docs: Update README with new framework details"
git commit -m "refactor: Optimize agent orchestration performance"
```

---

## 🚨 Emergency Recovery

### If you need to start over:
```bash
# Remove git history
rm -rf .git

# Start fresh
git init
git add .
git commit -m "feat: Reset - Sentinel GRC platform v1.0"
git remote add origin https://github.com/lkjalop/SentinelGRC.git
git push -u origin main --force
```

### If you committed sensitive data:
```bash
# Remove file from history (dangerous!)
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch secrets.txt' --prune-empty --tag-name-filter cat -- --all

# Force push cleaned history
git push --force --all
```

---

**Ready to deploy? Run the Initial Setup commands above! 🚀**