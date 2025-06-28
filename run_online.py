#!/usr/bin/env python3
"""
Launcher script for Mentorship System
This script starts the Flask application for online hosting
"""
import os
import sys
import subprocess
import threading
import time
import webbrowser

def check_virtual_env():
    """Check if virtual environment exists and create if needed"""
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    if not os.path.exists(venv_path):
        print("🔧 Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
            print("✅ Virtual environment created successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            sys.exit(1)
    
    # Check if packages are installed
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
    
    # Install requirements if needed
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        print("🔧 Installing/updating requirements...")
        pip_executable = os.path.join(venv_path, 'bin', 'pip')
        if os.name == 'nt':  # Windows
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')
        
        try:
            subprocess.check_call([pip_executable, 'install', '-r', requirements_path])
            print("✅ Requirements installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install requirements: {e}")
            sys.exit(1)
    
    return venv_path

def import_app_modules():
    """Import app modules after ensuring dependencies are available"""
    try:
        from app import app, init_db
        return app, init_db
    except ImportError as e:
        print(f"❌ Failed to import app modules: {e}")
        print("Make sure all dependencies are installed.")
        sys.exit(1)

def main():
    """Main launcher function"""
    print("="*60)
    print("🎓 MENTORSHIP MANAGEMENT SYSTEM")
    print("="*60)
    
    # Check and setup virtual environment
    venv_path = check_virtual_env()
    
    # Import app modules after dependencies are ready
    app, init_db = import_app_modules()
    
    print("🔧 Initializing database...")
    
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    print("🌐 Starting web server...")
    
    # Get port from environment or use 5000
    port = int(os.environ.get('PORT', '5000'))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"✅ Server starting on {host}:{port}")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Check if running in Codespace
    if os.environ.get('CODESPACE_NAME'):
        codespace_url = f"https://{os.environ.get('CODESPACE_NAME')}-{port}.{os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN', 'preview.app.github.dev')}"
        print(f"🌍 Codespace URL: {codespace_url}")
        
        # Auto-open browser in Codespace after short delay
        def open_browser():
            time.sleep(3)
            print(f"🌐 Opening browser to: {codespace_url}")
            webbrowser.open(codespace_url)
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
    else:
        # For local development
        local_url = f"http://localhost:{port}"
        print(f"🏠 Local URL: {local_url}")
        
        # Auto-open browser for local development after short delay
        def open_browser():
            time.sleep(3)
            print(f"🌐 Opening browser to: {local_url}")
            webbrowser.open(local_url)
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
    
    print("="*60)
    
    try:
        app.run(
            host=host,
            port=port,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
