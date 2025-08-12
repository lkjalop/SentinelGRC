"""
Sentinel GRC Setup Script
=========================
Install dependencies and initialize the system for first-time users.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def check_package(package):
    """Check if a package is already installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def setup_dependencies():
    """Install required dependencies"""
    
    print("🔧 Setting up Sentinel GRC dependencies...")
    print("=" * 50)
    
    # Core dependencies
    dependencies = [
        "streamlit",
        "groq", 
        "supabase",
        "pandas",
        "numpy",
        "networkx",
        "scikit-learn",
        "asyncio",
        "aiohttp",
        "beautifulsoup4",
        "cryptography"
    ]
    
    installed = 0
    failed = 0
    
    for dep in dependencies:
        package_name = dep.split("==")[0]  # Handle version specifications
        
        if check_package(package_name):
            print(f"✅ {package_name} already installed")
            installed += 1
        else:
            print(f"📦 Installing {package_name}...")
            if install_package(dep):
                installed += 1
            else:
                failed += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"✅ Installed/Available: {installed}")
    print(f"❌ Failed: {failed}")
    
    return failed == 0

def create_environment_file():
    """Create .env file with configuration templates"""
    
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    env_content = """# Sentinel GRC Configuration
# ==========================

# Groq API Configuration (for enhanced AI analysis)
GROQ_API_KEY=your_groq_api_key_here

# Supabase Configuration (for data persistence)
SUPABASE_URL=https://rqbfzjpbfykenqozcnyj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxYmZ6anBiZnlrZW5xb3pjbnlqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4OTczMzcsImV4cCI6MjA3MDQ3MzMzN30.mFQW-lT6m9zGAgBanp1UeU9UBQuom9BUgXLwzKp2pdc

# System Configuration
DEBUG=false
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env configuration file")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")

def create_requirements_txt():
    """Create requirements.txt file"""
    
    requirements = """streamlit>=1.28.0
groq>=0.4.0
supabase>=2.0.0
pandas>=1.5.0
numpy>=1.24.0
networkx>=3.0
scikit-learn>=1.3.0
aiohttp>=3.8.0
beautifulsoup4>=4.12.0
cryptography>=41.0.0
"""
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        print("✅ Created requirements.txt")
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")

def test_system():
    """Test core system components"""
    
    print("\n🧪 Testing system components...")
    print("=" * 40)
    
    # Test Groq connection
    try:
        from test_groq_simple import test_groq_api
        if test_groq_api():
            print("✅ Groq API test passed")
        else:
            print("⚠️ Groq API not configured (optional)")
    except Exception as e:
        print(f"⚠️ Groq API test failed: {e}")
    
    # Test Supabase connection
    try:
        from supabase_integration import setup_supabase_env
        if setup_supabase_env():
            print("✅ Supabase connection test passed")
        else:
            print("⚠️ Supabase connection failed (optional)")
    except Exception as e:
        print(f"⚠️ Supabase test failed: {e}")
    
    # Test core system
    try:
        from unified_orchestrator import SentinelGRC
        sentinel = SentinelGRC(enable_sidecars=False, enable_groq=False)
        status = sentinel.get_status()
        print(f"✅ Core system initialized with {len(status.get('core_agents', []))} agents")
    except Exception as e:
        print(f"❌ Core system test failed: {e}")
        return False
    
    return True

def show_next_steps():
    """Show next steps to the user"""
    
    print("\n🚀 Setup Complete!")
    print("=" * 30)
    print("\nNext steps:")
    print("1. 📝 Edit .env file with your API keys (optional)")
    print("2. 🌐 Run the demo: streamlit run streamlit_demo.py")
    print("3. 📊 Access dashboard and assessment tools")
    print("\nOptional enhancements:")
    print("• Get free Groq API key: https://console.groq.com/keys")
    print("• Configure Supabase database for data persistence")
    print("• Run data scrapers to populate knowledge base")
    
    print("\n🔗 Quick start command:")
    print("streamlit run streamlit_demo.py")

def main():
    """Main setup function"""
    
    print("🛡️ Sentinel GRC Setup")
    print("=" * 30)
    print("Australian Compliance Assessment Platform")
    print("Setting up your GRC environment...\n")
    
    # Create files
    create_requirements_txt()
    create_environment_file()
    
    # Install dependencies
    if not setup_dependencies():
        print("\n❌ Dependency installation failed!")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Test system
    if not test_system():
        print("\n❌ System test failed!")
        return False
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed - please check error messages above")
        sys.exit(1)