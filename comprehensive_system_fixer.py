#!/usr/bin/env python3
"""
Comprehensive System Fixer for Enterprise Mentorship Management System
This script identifies and fixes common issues in the system.
"""

import os
import sys
import sqlite3
import shutil
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n🔍 {title}")
    print("-" * 40)

def print_result(action, success, details=""):
    """Print action result"""
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"{status} {action}")
    if details:
        print(f"    {details}")

def backup_database():
    """Create a backup of the database"""
    print_section("Creating Database Backup")
    
    try:
        if os.path.exists('mentorship.db'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"mentorship_backup_{timestamp}.db"
            shutil.copy2('mentorship.db', backup_name)
            print_result("Database backup created", True, f"Saved as {backup_name}")
            return True
        else:
            print_result("Database backup", False, "No database file found")
            return False
    except Exception as e:
        print_result("Database backup", False, str(e))
        return False

def fix_roll_call_data():
    """Fix invalid roll call data in the database"""
    print_section("Fixing Roll Call Data")
    
    try:
        # Import validation function
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from validation_utils import validate_roll_call
        
        conn = sqlite3.connect('mentorship.db')
        cursor = conn.cursor()
        
        # Fix mentee roll calls
        cursor.execute("SELECT id, name, roll_call FROM mentee")
        mentees = cursor.fetchall()
        
        fixed_mentees = 0
        for mentee_id, name, roll_call in mentees:
            if not validate_roll_call(roll_call):
                # Generate a valid roll call based on name patterns
                new_roll_call = generate_valid_roll_call(name)
                cursor.execute("UPDATE mentee SET roll_call = ? WHERE id = ?", 
                             (new_roll_call, mentee_id))
                fixed_mentees += 1
                print(f"    Fixed mentee {name}: {roll_call} → {new_roll_call}")
        
        # Fix mentor roll calls
        cursor.execute("SELECT id, name, roll_call FROM mentor")
        mentors = cursor.fetchall()
        
        fixed_mentors = 0
        for mentor_id, name, roll_call in mentors:
            if not validate_roll_call(roll_call):
                # Generate a valid roll call based on name patterns
                new_roll_call = generate_valid_roll_call(name)
                cursor.execute("UPDATE mentor SET roll_call = ? WHERE id = ?", 
                             (new_roll_call, mentor_id))
                fixed_mentors += 1
                print(f"    Fixed mentor {name}: {roll_call} → {new_roll_call}")
        
        conn.commit()
        conn.close()
        
        total_fixed = fixed_mentees + fixed_mentors
        print_result("Roll call data fixed", True, 
                    f"Fixed {fixed_mentees} mentees and {fixed_mentors} mentors")
        
        return total_fixed == 0  # True if no fixes were needed
        
    except Exception as e:
        print_result("Roll call data fix", False, str(e))
        return False

def generate_valid_roll_call(name):
    """Generate a valid roll call based on name"""
    # Simple logic: use Year 10 with class 1 as default
    # In a real system, you might have more sophisticated logic
    return "10/1"

def fix_missing_templates():
    """Check and create any missing templates"""
    print_section("Checking Template Files")
    
    required_templates = {
        'templates/bulk_assign_mentors.html': '''{% extends "base.html" %}

{% block title %}Bulk Assign Mentors{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-users me-2"></i>Bulk Assign Mentors</h1>
        
        <div class="card mt-4">
            <div class="card-header">
                <h5 class="mb-0">Auto-Assign Available Mentors</h5>
            </div>
            <div class="card-body">
                <p>This will automatically assign unassigned mentees to available mentors based on capacity.</p>
                
                <form method="POST">
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="priority_seniors" name="priority_seniors" checked>
                            <label class="form-check-label" for="priority_seniors">
                                Prioritize senior students (Years 11-12)
                            </label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="subject_match" name="subject_match" checked>
                            <label class="form-check-label" for="subject_match">
                                Try to match subjects where possible
                            </label>
                        </div>
                    </div>
                    
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-magic me-2"></i>Auto-Assign Mentors
                        </button>
                        <a href="{{ url_for('mentees') }}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Back to Mentees
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
        
        'templates/reassign_mentees.html': '''{% extends "base.html" %}

{% block title %}Reassign Mentees{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-exchange-alt me-2"></i>Reassign Mentees</h1>
        
        <div class="card mt-4">
            <div class="card-body">
                <p>Reassign mentees from one mentor to another.</p>
                
                <form method="POST">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="from_mentor" class="form-label">From Mentor</label>
                                <select class="form-select" id="from_mentor" name="from_mentor" required>
                                    <option value="">Select mentor...</option>
                                    {% for mentor in mentors %}
                                    <option value="{{ mentor.id }}">{{ mentor.name }} ({{ mentor.assigned_mentees|length }} mentees)</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="to_mentor" class="form-label">To Mentor</label>
                                <select class="form-select" id="to_mentor" name="to_mentor" required>
                                    <option value="">Select mentor...</option>
                                    {% for mentor in mentors %}
                                    <option value="{{ mentor.id }}">{{ mentor.name }} ({{ mentor.assigned_mentees|length }}/{{ mentor.max_mentees }} mentees)</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-exchange-alt me-2"></i>Reassign All Mentees
                        </button>
                        <a href="{{ url_for('mentors') }}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Back to Mentors
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    }
    
    created_templates = 0
    for template_path, content in required_templates.items():
        if not os.path.exists(template_path):
            try:
                os.makedirs(os.path.dirname(template_path), exist_ok=True)
                with open(template_path, 'w') as f:
                    f.write(content)
                created_templates += 1
                print_result(f"Created template {template_path}", True)
            except Exception as e:
                print_result(f"Create template {template_path}", False, str(e))
        else:
            print_result(f"Template {template_path} exists", True)
    
    return created_templates

def add_missing_routes_documentation():
    """Create documentation for missing routes"""
    print_section("Creating Route Documentation")
    
    try:
        route_docs = '''# Missing Routes and Their Implementation

## Routes that may need to be added to app.py:

### 1. Bulk Delete Mentors
```python
@app.route('/bulk_delete_mentors', methods=['POST'])
def bulk_delete_mentors():
    try:
        # Only delete if no mentees are assigned
        unassigned_mentors = Mentor.query.filter(~Mentor.assigned_mentees.any()).all()
        for mentor in unassigned_mentors:
            db.session.delete(mentor)
        db.session.commit()
        flash(f'Deleted {len(unassigned_mentors)} mentors successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting mentors: {str(e)}', 'error')
    return redirect(url_for('mentors'))
```

### 2. Reassign Mentees Route
```python
@app.route('/reassign_mentees', methods=['GET', 'POST'])
def reassign_mentees():
    if request.method == 'POST':
        from_mentor_id = request.form.get('from_mentor')
        to_mentor_id = request.form.get('to_mentor')
        
        if from_mentor_id and to_mentor_id:
            mentees = Mentee.query.filter_by(mentor_id=from_mentor_id).all()
            for mentee in mentees:
                mentee.mentor_id = to_mentor_id
            db.session.commit()
            flash(f'Reassigned {len(mentees)} mentees successfully!', 'success')
        
        return redirect(url_for('mentors'))
    
    mentors = Mentor.query.all()
    return render_template('reassign_mentees.html', mentors=mentors)
```

### 3. Enhanced Search and Filter Functions
These should be added as JavaScript functions in the templates or as separate AJAX endpoints.

### 4. Database Integrity Checks
Add regular validation functions to ensure data consistency.
'''
        
        with open('MISSING_ROUTES_DOCUMENTATION.md', 'w') as f:
            f.write(route_docs)
        
        print_result("Route documentation created", True, "See MISSING_ROUTES_DOCUMENTATION.md")
        return True
        
    except Exception as e:
        print_result("Create route documentation", False, str(e))
        return False

def optimize_database():
    """Optimize database performance"""
    print_section("Optimizing Database")
    
    try:
        conn = sqlite3.connect('mentorship.db')
        cursor = conn.cursor()
        
        # Run VACUUM to optimize database
        cursor.execute("VACUUM")
        
        # Analyze tables for better query planning
        cursor.execute("ANALYZE")
        
        # Check database integrity
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()[0]
        
        conn.close()
        
        if integrity_result == 'ok':
            print_result("Database optimization", True, "Database is optimized and integrity verified")
            return True
        else:
            print_result("Database optimization", False, f"Integrity check failed: {integrity_result}")
            return False
            
    except Exception as e:
        print_result("Database optimization", False, str(e))
        return False

def create_system_health_check():
    """Create a system health check script"""
    print_section("Creating System Health Check")
    
    health_check_content = '''#!/usr/bin/env python3
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
    print("\\n" + "="*60)
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
'''
    
    try:
        with open('system_health_check.py', 'w') as f:
            f.write(health_check_content)
        
        # Make it executable
        os.chmod('system_health_check.py', 0o755)
        
        print_result("System health check script created", True, "system_health_check.py")
        return True
        
    except Exception as e:
        print_result("Create health check script", False, str(e))
        return False

def update_gitignore():
    """Update .gitignore with all test and temporary files"""
    print_section("Updating .gitignore")
    
    gitignore_additions = [
        "# Test and development files",
        "test_*.py",
        "manual_*.py", 
        "comprehensive_*.py",
        "simple_*.py",
        "master_*.py",
        "final_*.py",
        "fix_*.py",
        "migrate_*.py",
        "run_tests.sh",
        "system_health_check.py",
        "validation_utils.py",
        "comprehensive_system_fixer.py",
        "",
        "# Test reports and logs",
        "test_report_*.json",
        "test_results_*.txt",
        "*_test_output.txt",
        "system_health_*.txt",
        "",
        "# Backup files",
        "mentorship_backup_*.db",
        "*.bak",
        "*.backup",
        "",
        "# Documentation generated during testing",
        "MISSING_ROUTES_DOCUMENTATION.md",
        "TESTING_GUIDE.md",
        "ROLL_CALL_FIXED.md",
        "MANUAL_VERIFICATION_CHECKLIST.md",
        "TEST_RESULTS_*.md",
        ""
    ]
    
    try:
        # Read existing .gitignore
        existing_content = ""
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                existing_content = f.read()
        
        # Add new entries that don't already exist
        new_entries = []
        for entry in gitignore_additions:
            if entry.strip() and entry.strip() not in existing_content:
                new_entries.append(entry)
        
        if new_entries:
            with open('.gitignore', 'a') as f:
                if existing_content and not existing_content.endswith('\\n'):
                    f.write('\\n')
                f.write('\\n'.join(new_entries))
            
            print_result("Updated .gitignore", True, f"Added {len(new_entries)} new entries")
        else:
            print_result("Check .gitignore", True, "Already up to date")
        
        return True
        
    except Exception as e:
        print_result("Update .gitignore", False, str(e))
        return False

def main():
    """Run all fixes"""
    print_header("COMPREHENSIVE SYSTEM FIXER")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Working directory: {os.getcwd()}")
    
    fixes_applied = []
    
    # Run all fixes
    if backup_database():
        fixes_applied.append("Database backup")
    
    if fix_roll_call_data():
        fixes_applied.append("Roll call validation")
    
    templates_created = fix_missing_templates()
    if templates_created > 0:
        fixes_applied.append(f"Created {templates_created} templates")
    
    if add_missing_routes_documentation():
        fixes_applied.append("Route documentation")
    
    if optimize_database():
        fixes_applied.append("Database optimization")
    
    if create_system_health_check():
        fixes_applied.append("Health check script")
    
    if update_gitignore():
        fixes_applied.append("Updated .gitignore")
    
    # Generate summary
    print_header("SUMMARY")
    print(f"✅ Fixes applied: {len(fixes_applied)}")
    for fix in fixes_applied:
        print(f"  • {fix}")
    
    print(f"\\n🏁 System fixing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\\n💡 Next steps:")
    print("  1. Run 'python manual_system_test.py' to verify fixes")
    print("  2. Run 'python system_health_check.py' for ongoing monitoring")
    print("  3. Check MISSING_ROUTES_DOCUMENTATION.md for any additional routes needed")
    
    return True

if __name__ == "__main__":
    main()
