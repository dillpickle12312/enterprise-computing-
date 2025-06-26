#!/usr/bin/env python3
"""
Simple startup script for Render deployment
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app import app, init_db
    
    # Initialize database
    init_db()
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting on port {port}")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
