#!/usr/bin/env python3
"""
🚀 AstralytiQ Full-Stack Startup Script
Starts both FastAPI backend and Streamlit frontend

Perfect for demonstrating full-stack capabilities to recruiters
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def print_banner():
    """Print startup banner."""
    print("""
    ⚡ AstralytiQ Enterprise Platform
    ================================
    
    🚀 Starting Full-Stack Application...
    
    Backend:  FastAPI + SQLite + JWT Auth
    Frontend: Streamlit + Real-time Integration
    
    Perfect for Campus Placement Demos!
    """)

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'streamlit', 'pydantic', 
        'bcrypt', 'python-jose', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        for package in missing_packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        
        print("✅ All dependencies installed!")
    else:
        print("✅ All dependencies satisfied!")

def start_backend():
    """Start FastAPI backend server."""
    print("\n🔧 Starting FastAPI Backend...")
    print("   URL: http://localhost:8081")
    print("   Docs: http://localhost:8081/docs")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return None
    
    # Start backend process
    try:
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start Streamlit frontend."""
    print("\n🎨 Starting Streamlit Frontend...")
    print("   URL: http://localhost:8501")
    
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app_with_backend.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def monitor_processes(backend_process, frontend_process):
    """Monitor both processes and restart if needed."""
    print("\n👀 Monitoring processes...")
    
    try:
        while True:
            time.sleep(5)
            
            # Check backend
            if backend_process and backend_process.poll() is not None:
                print("⚠️  Backend process died, restarting...")
                backend_process = start_backend()
            
            # Check frontend
            if frontend_process and frontend_process.poll() is not None:
                print("⚠️  Frontend process died, restarting...")
                frontend_process = start_frontend()
            
            if not backend_process and not frontend_process:
                print("❌ Both processes failed, exiting...")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            frontend_process.wait()
            print("✅ Frontend stopped")
        
        print("👋 Goodbye!")

def show_demo_info():
    """Show demo information for recruiters."""
    print("""
    🎯 DEMO INFORMATION FOR RECRUITERS
    ==================================
    
    📱 Frontend (Streamlit):
       URL: http://localhost:8501
       Features: Enterprise UI, Real-time Dashboard, Mobile Responsive
    
    🔧 Backend (FastAPI):
       URL: http://localhost:8081
       Docs: http://localhost:8081/docs
       Features: JWT Auth, REST APIs, SQLite Database
    
    🔐 Demo Credentials:
       Email: admin@astralytiq.com
       Password: admin123
    
    📊 Key Features to Demonstrate:
       ✅ Full-stack development (Frontend + Backend)
       ✅ JWT authentication and authorization
       ✅ Real-time API integration
       ✅ Database connectivity and operations
       ✅ Professional UI/UX with responsive design
       ✅ Auto-generated API documentation
       ✅ Production-ready error handling
       ✅ Enterprise-grade architecture
    
    🚀 Perfect for SDE and Data Engineering interviews!
    """)

def main():
    """Main startup function."""
    print_banner()
    
    # Check dependencies
    check_dependencies()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot start without backend. Exiting...")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Cannot start without frontend. Exiting...")
        if backend_process:
            backend_process.terminate()
        return
    
    # Show demo information
    show_demo_info()
    
    # Monitor processes
    monitor_processes(backend_process, frontend_process)

if __name__ == "__main__":
    main()