#!/usr/bin/env python3
"""
System Health Check for Enterprise Mentorship Management System
Run this script regularly to check system health.
"""

import os
import sqlite3
from datetime import datetime
import sys

def health_check():
    """Perform comprehensive system health check"""
    print(f"🏥 System Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    issues = []
    
    # Check database
    if not os.path.exists('mentorship.db'):
        issues.append("❌ Database file missing")
    else:
        try:
            conn = sqlite3.connect('mentorship.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mentor")
            mentor_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM mentee")
            mentee_count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ Database: {mentor_count} mentors, {mentee_count} mentees")
        except Exception as e:
            issues.append(f"❌ Database error: {e}")
    
    # Check templates
    required_templates = [
        'templates/base.html',
        'templates/dashboard.html',
        'templates/mentors.html',
        'templates/mentees.html',
        'templates/add_mentor.html',
        'templates/add_mentee.html'
    ]
    
    missing_templates = [t for t in required_templates if not os.path.exists(t)]
    if missing_templates:
        issues.append(f"❌ Missing templates: {missing_templates}")
    else:
        print(f"✅ All {len(required_templates)} core templates present")
    
    # Check static files
    required_static = ['static/css/style.css', 'static/js/main.js']
    missing_static = [s for s in required_static if not os.path.exists(s)]
    if missing_static:
        issues.append(f"❌ Missing static files: {missing_static}")
    else:
        print("✅ Static files present")
    
    # Check configuration
    config_files = ['requirements.txt', 'Procfile', 'runtime.txt']
    missing_config = [c for c in config_files if not os.path.exists(c)]
    if missing_config:
        issues.append(f"⚠️  Missing config files: {missing_config}")
    else:
        print("✅ Configuration files present")
    
    # Summary
    print("\n" + "="*60)
    if issues:
        print(f"❌ {len(issues)} ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ SYSTEM HEALTHY - No issues found")
        return True

if __name__ == "__main__":
    healthy = health_check()
    sys.exit(0 if healthy else 1)
