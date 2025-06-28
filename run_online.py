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

#!/usr/bin/env python3
"""
Launcher script for Mentorship System
This script starts the Flask application for online hosting with proper environment setup
"""
import os
import sys
import subprocess
import threading
import time
import webbrowser

def main():
    """Main launcher function with virtual environment support"""
    print("="*60)
    print("🎓 MENTORSHIP MANAGEMENT SYSTEM")
    print("="*60)
    
    # Get current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, 'venv')
    
    # Check if virtual environment exists
    if os.path.exists(venv_path):
        print("✅ Virtual environment found!")
        
        # Use the virtual environment Python
        if os.name == 'nt':  # Windows
            python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:  # Unix/Linux/macOS
            python_executable = os.path.join(venv_path, 'bin', 'python')
        
        # Set environment variables for the Flask app
        env = os.environ.copy()
        env['PYTHONPATH'] = script_dir
        
        print("🌐 Starting Flask application...")
        print("🛑 Press Ctrl+C to stop the server")
        print("="*60)
        
        try:
            # Run the app using the virtual environment Python
            subprocess.run([python_executable, 'app.py'], 
                         cwd=script_dir, 
                         env=env)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Error running application: {e}")
            
    else:
        print("❌ Virtual environment not found!")
        print("Please run the following commands first:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        print("  python run_online.py")
        sys.exit(1)

if __name__ == '__main__':
    main()
    
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
