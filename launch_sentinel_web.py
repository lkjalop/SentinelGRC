#!/usr/bin/env python3
"""
Sentinel GRC Web Interface Launcher
===================================
Starts the new HTML/CSS/JavaScript two-door interface 
that replaces the Streamlit implementation.

This matches the IMPLEMENTATION_GUIDE.md specifications
and provides proper frontend-backend integration.
"""

import sys
import os
import webbrowser
import asyncio
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def banner():
    """Display startup banner"""
    print("=" * 80)
    print("🏢 SENTINEL GRC - ENTERPRISE COMPLIANCE PLATFORM")
    print("=" * 80)
    print("🔄 ARCHITECTURE: Two-Door Interface (DevOps + Compliance)")
    print("🎯 BACKEND: Python FastAPI + SentinelGRC Complete")
    print("🎨 FRONTEND: HTML/CSS/JavaScript (Implementation Guide Spec)")
    print("📊 FEATURES: Professional PDF, Expert Escalation, OWASP Security")
    print("=" * 80)
    print()

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    missing = []
    
    try:
        import fastapi
        print("  ✅ FastAPI available")
    except ImportError:
        missing.append("fastapi")
    
    try:
        import uvicorn
        print("  ✅ Uvicorn available")
    except ImportError:
        missing.append("uvicorn")
    
    try:
        import reportlab
        print("  ✅ ReportLab available (PDF generation)")
    except ImportError:
        missing.append("reportlab")
    
    try:
        from src.core.sentinel_grc_complete import SentinelGRC
        print("  ✅ SentinelGRC backend available")
    except ImportError as e:
        print(f"  ❌ SentinelGRC backend error: {e}")
        missing.append("sentinel-backend")
    
    try:
        from src.config.geographic_router import ComplianceRouter
        print("  ✅ Geographic router available")
    except ImportError:
        missing.append("geographic-router")
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install fastapi uvicorn reportlab")
        return False
    
    print("  ✅ All dependencies available")
    return True

def check_ui_files():
    """Check if UI files are present"""
    print("\n🎨 Checking UI files...")
    
    ui_path = Path(__file__).parent / "src" / "ui"
    
    files_to_check = [
        "sentinel_gateway.html",
        "css/sentinel.css", 
        "js/sentinel-gateway.js"
    ]
    
    missing_files = []
    
    for file_path in files_to_check:
        full_path = ui_path / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing UI files: {', '.join(missing_files)}")
        print("UI files should be in src/ui/ directory")
        return False
    
    print("  ✅ All UI files present")
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Sentinel GRC Web Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🎯 Two-door interface will load automatically")
    print("⚡ DevOps Mode: http://localhost:8000/devops-dashboard.html")
    print("📋 Compliance Mode: http://localhost:8000/compliance-dashboard.html")
    print("\n" + "=" * 80)
    print("🔧 DEVELOPER NOTES:")
    print("- Frontend: Modern HTML/CSS/JS (no Streamlit)")
    print("- Backend: Complete Python integration")
    print("- APIs: RESTful endpoints at /api/*")
    print("- PDF Generation: Professional compliance reports")
    print("- Security: OWASP frameworks integrated")
    print("=" * 80)
    
    # Start server
    import uvicorn
    from src.api.web_server import app
    
    # Auto-open browser
    def open_browser():
        time.sleep(2)  # Wait for server to start
        webbrowser.open("http://localhost:8000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

def main():
    """Main launcher function"""
    banner()
    
    # Check everything is ready
    if not check_dependencies():
        print("\n💡 SOLUTION: Run 'pip install fastapi uvicorn reportlab' to install missing dependencies")
        return 1
    
    if not check_ui_files():
        print("\n💡 SOLUTION: Make sure all UI files are present in src/ui/ directory")
        return 1
    
    print("\n✅ ALL SYSTEMS READY - LAUNCHING SENTINEL GRC WEB INTERFACE")
    print("📝 This replaces the old Streamlit interface with proper HTML/CSS/JS")
    print("🎯 Implements the two-door pattern from IMPLEMENTATION_GUIDE.md")
    
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Thank you for using Sentinel GRC!")
        return 0
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())