"""
Launch the Sentinel GRC Web Server
=================================

Simple launcher script to start the web interface.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

# Now import and run the web server
try:
    from src.api.web_server import app
    import uvicorn
    
    print("=" * 60)
    print("🚀 LAUNCHING SENTINEL GRC WEB INTERFACE")
    print("=" * 60)
    print("📊 Dashboard URL: http://localhost:8000")
    print("🛡️ Compliance Mode: http://localhost:8000/compliance-dashboard.html")
    print("⚡ DevOps Mode: http://localhost:8000/devops-dashboard.html")
    print("📋 Executive Dashboard: http://localhost:8000/executive-dashboard.html")
    print("=" * 60)
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing missing dependencies...")
    os.system("pip install fastapi uvicorn")
    print("Please run this script again.")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("Please check the logs above for details.")