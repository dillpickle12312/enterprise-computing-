#!/usr/bin/env python3
"""
Launcher script for Mentorship System
This script starts the Flask application for online hosting
"""
import os
import sys
import threading
import time
import webbrowser
from app import app, init_db

def main():
    """Main launcher function"""
    print("="*60)
    print("🎓 MENTORSHIP MANAGEMENT SYSTEM")
    print("="*60)
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
