#!/usr/bin/env python3
"""
Simple launcher script for Mentorship System
Run this after setting up the virtual environment with setup.sh
"""
import os
import sys

def main():
    print("="*60)
    print("🎓 MENTORSHIP MANAGEMENT SYSTEM")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, 'venv')
    
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found!")
        print("Please run: ./setup.sh")
        sys.exit(1)
    
    print("✅ Starting application...")
    print("🛑 Press Ctrl+C to stop the server")
    print("="*60)
    
    # Change to script directory and activate venv
    os.chdir(script_dir)
    
    # Simple approach - just run with current Python if venv is activated
    if 'VIRTUAL_ENV' in os.environ:
        # Already in virtual environment
        from app import app, init_db
        init_db()
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Please activate the virtual environment first:")
        print("  source venv/bin/activate")
        print("  python run_online.py")

if __name__ == '__main__':
    main()
