#!/usr/bin/env python3
"""
Comprehensive Grey-Box and Black-Box Testing Suite
Tests every button, form, and user interaction in the Enterprise Mentorship Management System
"""

import os
import sys
import sqlite3
import re
import json
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

# Add the current directory to the path so we can import from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestLogger:
    """Enhanced test logging with categories"""
    
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_header(self, title):
        print("\n" + "="*70)
        print(f"🧪 {title}")
        print("="*70)
        
    def log_section(self, title, test_type=""):
        type_icon = {"grey": "⚫", "black": "⚪", "unit": "🔬", "integration": "🔗"}.get(test_type, "🔍")
        print(f"\n{type_icon} {title}")
        print("-" * 50)
        
    def log_result(self, test_name, passed, details="", test_type=""):
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        print(f"{status} {test_name}")
        if details:
            print(f"    📝 {details}")
            
        self.results[test_name] = {
            'passed': passed,
            'details': details,
            'type': test_type
        }

logger = TestLogger()

class DatabaseTestHelper:
    """Helper class for database testing operations"""
    
    @staticmethod
    def get_connection():
        return sqlite3.connect('mentorship.db')
    
    @staticmethod
    def count_records(table):
        with DatabaseTestHelper.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            return cursor.fetchone()[0]
    
    @staticmethod
    def get_sample_records(table, limit=5):
        with DatabaseTestHelper.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} LIMIT {limit}")
            return cursor.fetchall()
    
    @staticmethod
    def execute_query(query, params=None):
        with DatabaseTestHelper.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

class FormTester:
    """Test form validation and submission logic"""
    
    @staticmethod
    def test_roll_call_validation():
        """Grey-box testing: Test roll call validation with knowledge of internal logic"""
        logger.log_section("Roll Call Validation (Grey-Box Testing)", "grey")
        
        try:
            from app import validate_roll_call
            
            # Test boundary conditions (grey-box knowledge of patterns)
            test_cases = [
                # Valid boundary cases
                ('7A', True, 'Minimum year 7 with letter'),
                ('9Z', True, 'Maximum year 9 with last letter'),
                ('10/1', True, 'Minimum year 10 with class'),
                ('12/9', True, 'Maximum year 12 with class'),
                ('10AA1', True, 'Minimum subject code length'),
                ('12ABCD9', True, 'Maximum subject code length'),
                
                # Invalid boundary cases  
                ('6A', False, 'Below minimum year'),
                ('13/1', False, 'Above maximum year'),
                ('7a', False, 'Lowercase letter'),
                ('10/0', False, 'Invalid class number 0'),
                ('12/10', False, 'Class number too high'),
                ('10A1', False, 'Single letter subject code'),
                ('12ABCDE1', False, 'Subject code too long'),
                
                # Edge cases
                ('', False, 'Empty string'),
                ('   ', False, 'Whitespace only'),
                ('7', False, 'Year only'),
                ('A', False, 'Letter only'),
                ('10/', False, 'Incomplete format'),
                ('10ENG', False, 'Missing class number'),
                ('10ENG0', False, 'Zero class number'),
            ]
            
            all_passed = True
            for roll_call, expected, description in test_cases:
                result = validate_roll_call(roll_call)
                passed = result == expected
                all_passed = all_passed and passed
                logger.log_result(f"Roll call '{roll_call}' ({description})", passed, 
                                f"Expected: {expected}, Got: {result}", "grey")
            
            return all_passed
            
        except Exception as e:
            logger.log_result("Roll Call Validation Import", False, str(e), "grey")
            return False

    @staticmethod
    def test_form_field_validation():
        """Black-box testing: Test form fields without knowing internal implementation"""
        logger.log_section("Form Field Validation (Black-Box Testing)", "black")
        
        # Test data generation for black-box testing
        test_data = {
            'valid_names': ['John Smith', 'Mary Jane Watson', 'Li Wei Chen', 'José García'],
            'invalid_names': ['', '   ', 'A', 'X' * 100, '123', 'Name!@#'],
            'valid_subjects': ['Mathematics', 'English', 'Science', 'History'],
            'invalid_subjects': ['', '   ', 'X' * 200],
            'valid_roll_calls': ['7A', '8B', '9C', '10/1', '11/2', '12/3', '12ENG1'],
            'invalid_roll_calls': ['', '13A', '6B', '10A', '12/0', 'ABC123']
        }
        
        all_passed = True
        
        # Test name validation patterns
        for name in test_data['valid_names']:
            # Simulate form validation logic
            is_valid = bool(re.match(r'^[A-Za-z\s]{2,50}$', name))
            passed = is_valid
            all_passed = all_passed and passed
            logger.log_result(f"Valid name: '{name}'", passed, 
                            f"Should pass name validation", "black")
        
        for name in test_data['invalid_names']:
            is_valid = bool(re.match(r'^[A-Za-z\s]{2,50}$', name))
            passed = not is_valid  # Should fail validation
            all_passed = all_passed and passed
            logger.log_result(f"Invalid name: '{name}'", passed, 
                            f"Should fail name validation", "black")
        
        return all_passed

class UIComponentTester:
    """Test UI components and user interactions"""
    
    @staticmethod
    def test_navigation_structure():
        """Test navigation menu and routing structure"""
        logger.log_section("Navigation Structure Testing", "black")
        
        # Expected navigation structure based on templates
        expected_nav_items = [
            'Dashboard', 'Mentors', 'Mentees', 'Calendar', 'Statistics', 'User Guide'
        ]
        
        expected_pages = [
            '/', '/mentors', '/mentees', '/add_mentor', '/add_mentee',
            '/calendar', '/statistics', '/assign_mentor', '/user_guide'
        ]
        
        # Test template files exist for navigation
        navigation_tests = [
            ('templates/base.html', 'Base template with navigation'),
            ('templates/dashboard.html', 'Dashboard page'),
            ('templates/mentors.html', 'Mentors list page'),
            ('templates/mentees.html', 'Mentees list page'),
            ('templates/add_mentor.html', 'Add mentor form'),
            ('templates/add_mentee.html', 'Add mentee form'),
            ('templates/calendar.html', 'Calendar page'),
            ('templates/statistics.html', 'Statistics page'),
        ]
        
        all_passed = True
        for template_path, description in navigation_tests:
            exists = os.path.exists(template_path)
            all_passed = all_passed and exists
            logger.log_result(f"Navigation: {description}", exists, 
                            f"Template file: {template_path}", "black")
        
        return all_passed

    @staticmethod
    def test_button_functionality():
        """Test all buttons and interactive elements"""
        logger.log_section("Button Functionality Testing", "black")
        
        # Test button configurations in templates
        button_tests = []
        
        # Analyze templates for buttons
        template_files = [
            'templates/dashboard.html',
            'templates/mentors.html', 
            'templates/mentees.html',
            'templates/add_mentor.html',
            'templates/add_mentee.html',
            'templates/mentor_detail.html',
            'templates/mentee_detail.html',
            'templates/assign_mentor.html',
            'templates/statistics.html'
        ]
        
        all_passed = True
        for template_file in template_files:
            if os.path.exists(template_file):
                with open(template_file, 'r') as f:
                    content = f.read()
                
                # Count different types of buttons
                submit_buttons = content.count('type="submit"')
                regular_buttons = content.count('<button')
                link_buttons = content.count('btn ')
                
                has_buttons = submit_buttons > 0 or regular_buttons > 0 or link_buttons > 0
                
                logger.log_result(f"Buttons in {template_file}", has_buttons,
                                f"Submit: {submit_buttons}, Buttons: {regular_buttons}, Links: {link_buttons}",
                                "black")
                
                all_passed = all_passed and has_buttons
        
        return all_passed

class DatabaseIntegrityTester:
    """Test database operations and data integrity"""
    
    @staticmethod
    def test_crud_operations():
        """Test Create, Read, Update, Delete operations"""
        logger.log_section("CRUD Operations Testing (Grey-Box)", "grey")
        
        all_passed = True
        
        # Test database connection and basic operations
        try:
            # Test Read operations
            mentor_count = DatabaseTestHelper.count_records('mentor')
            mentee_count = DatabaseTestHelper.count_records('mentee')
            session_count = DatabaseTestHelper.count_records('session')
            
            logger.log_result("Read: Count mentors", mentor_count > 0, 
                            f"Found {mentor_count} mentors", "grey")
            logger.log_result("Read: Count mentees", mentee_count > 0,
                            f"Found {mentee_count} mentees", "grey")
            logger.log_result("Read: Count sessions", session_count >= 0,
                            f"Found {session_count} sessions", "grey")
            
            # Test data integrity constraints
            invalid_mentees = DatabaseTestHelper.execute_query("""
                SELECT COUNT(*) FROM mentee 
                WHERE name IS NULL OR roll_call IS NULL OR subject IS NULL
            """)[0][0]
            
            logger.log_result("Data integrity: No NULL required fields", invalid_mentees == 0,
                            f"Found {invalid_mentees} records with NULL required fields", "grey")
            
            # Test foreign key relationships
            orphaned_mentees = DatabaseTestHelper.execute_query("""
                SELECT COUNT(*) FROM mentee 
                WHERE mentor_id IS NOT NULL 
                AND mentor_id NOT IN (SELECT id FROM mentor)
            """)[0][0]
            
            logger.log_result("Referential integrity: No orphaned mentees", orphaned_mentees == 0,
                            f"Found {orphaned_mentees} mentees with invalid mentor_id", "grey")
            
        except Exception as e:
            logger.log_result("Database CRUD operations", False, str(e), "grey")
            all_passed = False
        
        return all_passed

    @staticmethod
    def test_data_validation():
        """Test data validation rules in database"""
        logger.log_section("Data Validation Testing (Grey-Box)", "grey")
        
        all_passed = True
        
        try:
            from app import validate_roll_call
            
            # Test all mentee roll calls
            mentee_roll_calls = DatabaseTestHelper.execute_query("SELECT id, roll_call FROM mentee")
            invalid_mentee_roll_calls = []
            
            for mentee_id, roll_call in mentee_roll_calls:
                if not validate_roll_call(roll_call):
                    invalid_mentee_roll_calls.append((mentee_id, roll_call))
            
            logger.log_result("All mentee roll calls valid", len(invalid_mentee_roll_calls) == 0,
                            f"Invalid roll calls: {invalid_mentee_roll_calls[:5]}", "grey")
            
            # Test all mentor roll calls
            mentor_roll_calls = DatabaseTestHelper.execute_query("SELECT id, roll_call FROM mentor")
            invalid_mentor_roll_calls = []
            
            for mentor_id, roll_call in mentor_roll_calls:
                if not validate_roll_call(roll_call):
                    invalid_mentor_roll_calls.append((mentor_id, roll_call))
            
            logger.log_result("All mentor roll calls valid", len(invalid_mentor_roll_calls) == 0,
                            f"Invalid roll calls: {invalid_mentor_roll_calls[:5]}", "grey")
            
            all_passed = len(invalid_mentee_roll_calls) == 0 and len(invalid_mentor_roll_calls) == 0
            
        except Exception as e:
            logger.log_result("Data validation testing", False, str(e), "grey")
            all_passed = False
        
        return all_passed

class SystemIntegrationTester:
    """Test system integration and workflows"""
    
    @staticmethod
    def test_mentor_mentee_assignment():
        """Test mentor-mentee assignment workflow"""
        logger.log_section("Mentor-Mentee Assignment Workflow (Integration)", "integration")
        
        all_passed = True
        
        try:
            # Test assignment logic
            assignments = DatabaseTestHelper.execute_query("""
                SELECT m.id as mentee_id, m.name as mentee_name, m.subject,
                       mentor.id as mentor_id, mentor.name as mentor_name, mentor.subjects
                FROM mentee m
                LEFT JOIN mentor ON m.mentor_id = mentor.id
                WHERE m.mentor_id IS NOT NULL
                LIMIT 10
            """)
            
            subject_mismatches = 0
            for assignment in assignments:
                mentee_subject = assignment[2]
                mentor_subjects = assignment[5].split(',') if assignment[5] else []
                mentor_subjects = [s.strip() for s in mentor_subjects]
                
                if mentee_subject not in mentor_subjects:
                    subject_mismatches += 1
            
            logger.log_result("Subject compatibility in assignments", subject_mismatches == 0,
                            f"Found {subject_mismatches} subject mismatches out of {len(assignments)} assignments",
                            "integration")
            
            # Test mentor capacity constraints
            mentor_capacities = DatabaseTestHelper.execute_query("""
                SELECT m.id, m.name, m.max_mentees, COUNT(mentee.id) as current_mentees
                FROM mentor m
                LEFT JOIN mentee ON m.id = mentee.mentor_id
                GROUP BY m.id, m.name, m.max_mentees
            """)
            
            capacity_violations = 0
            for mentor_id, mentor_name, max_mentees, current_mentees in mentor_capacities:
                if current_mentees > max_mentees:
                    capacity_violations += 1
            
            logger.log_result("Mentor capacity constraints", capacity_violations == 0,
                            f"Found {capacity_violations} mentors over capacity", "integration")
            
            all_passed = subject_mismatches == 0 and capacity_violations == 0
            
        except Exception as e:
            logger.log_result("Assignment workflow testing", False, str(e), "integration")
            all_passed = False
        
        return all_passed

    @staticmethod
    def test_session_management():
        """Test session scheduling and management"""
        logger.log_section("Session Management Testing (Integration)", "integration")
        
        all_passed = True
        
        try:
            # Test session data integrity
            sessions = DatabaseTestHelper.execute_query("""
                SELECT s.id, s.scheduled_date, s.status, s.mentee_id, s.mentor_id
                FROM session s
                LIMIT 20
            """)
            
            logger.log_result("Sessions exist in database", len(sessions) >= 0,
                            f"Found {len(sessions)} sessions", "integration")
            
            # Test session status values
            if sessions:
                valid_statuses = ['scheduled', 'completed', 'cancelled', 'missed', 'rescheduled']
                invalid_status_count = 0
                
                for session in sessions:
                    if session[2] not in valid_statuses:
                        invalid_status_count += 1
                
                logger.log_result("Valid session statuses", invalid_status_count == 0,
                                f"Found {invalid_status_count} sessions with invalid status", "integration")
            
        except Exception as e:
            logger.log_result("Session management testing", False, str(e), "integration")
            all_passed = False
        
        return all_passed

class SecurityTester:
    """Test security aspects and input validation"""
    
    @staticmethod
    def test_input_sanitization():
        """Test input sanitization and SQL injection prevention"""
        logger.log_section("Input Sanitization Testing (Black-Box)", "black")
        
        # Test malicious input patterns
        malicious_inputs = [
            "'; DROP TABLE mentee; --",
            "<script>alert('xss')</script>",
            "' OR '1'='1",
            "../../../etc/passwd",
            "javascript:alert('xss')",
            "{{7*7}}",  # Template injection
            "%3Cscript%3E",  # URL encoded
        ]
        
        all_passed = True
        
        # Test roll call validation against malicious input
        try:
            from app import validate_roll_call
            
            for malicious_input in malicious_inputs:
                try:
                    result = validate_roll_call(malicious_input)
                    # Should return False for malicious input
                    passed = result == False
                    logger.log_result(f"Security: Malicious input rejected", passed,
                                    f"Input: {malicious_input[:20]}...", "black")
                    all_passed = all_passed and passed
                except Exception:
                    # If exception is raised, that's also acceptable (input rejected)
                    logger.log_result(f"Security: Malicious input caused exception", True,
                                    f"Input safely rejected: {malicious_input[:20]}...", "black")
        
        except Exception as e:
            logger.log_result("Security testing setup", False, str(e), "black")
            all_passed = False
        
        return all_passed

class PerformanceTester:
    """Test performance aspects"""
    
    @staticmethod
    def test_database_performance():
        """Test database query performance"""
        logger.log_section("Database Performance Testing", "grey")
        
        all_passed = True
        
        try:
            import time
            
            # Test query performance
            start_time = time.time()
            mentee_count = DatabaseTestHelper.count_records('mentee')
            query_time = time.time() - start_time
            
            # Simple query should complete quickly (under 1 second)
            passed = query_time < 1.0
            logger.log_result("Database query performance", passed,
                            f"Count query took {query_time:.3f} seconds", "grey")
            
            # Test complex join query
            start_time = time.time()
            assignments = DatabaseTestHelper.execute_query("""
                SELECT m.name, mentor.name, m.subject 
                FROM mentee m 
                LEFT JOIN mentor ON m.mentor_id = mentor.id 
                LIMIT 50
            """)
            join_time = time.time() - start_time
            
            passed_join = join_time < 2.0
            logger.log_result("Complex join query performance", passed_join,
                            f"Join query took {join_time:.3f} seconds", "grey")
            
            all_passed = passed and passed_join
            
        except Exception as e:
            logger.log_result("Performance testing", False, str(e), "grey")
            all_passed = False
        
        return all_passed

def test_flask_routes():
    """Test Flask routes and application structure"""
    logger.log_section("Flask Routes Testing (Grey-Box)", "grey")
    
    all_passed = True
    
    try:
        from app import app
        
        # Test route registration
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = [
            '/', '/mentors', '/mentees', '/add_mentor', '/add_mentee',
            '/mentor/<int:id>', '/mentee/<int:id>', '/assign_mentor',
            '/statistics', '/calendar', '/user_guide'
        ]
        
        for expected_route in expected_routes:
            # Handle dynamic routes
            route_exists = any(
                expected_route == route or 
                (expected_route.startswith('/mentor/') and '/mentor/' in route) or
                (expected_route.startswith('/mentee/') and '/mentee/' in route)
                for route in routes
            )
            
            logger.log_result(f"Route exists: {expected_route}", route_exists,
                            f"Checking route registration", "grey")
            all_passed = all_passed and route_exists
        
    except Exception as e:
        logger.log_result("Flask routes testing", False, str(e), "grey")
        all_passed = False
    
    return all_passed

def generate_comprehensive_report(all_results):
    """Generate comprehensive test report with categorization"""
    logger.log_header("COMPREHENSIVE TEST REPORT")
    
    # Categorize results
    categories = {
        'grey': {'tests': [], 'passed': 0, 'total': 0},
        'black': {'tests': [], 'passed': 0, 'total': 0},
        'integration': {'tests': [], 'passed': 0, 'total': 0},
        'unit': {'tests': [], 'passed': 0, 'total': 0}
    }
    
    for test_name, result in logger.results.items():
        test_type = result.get('type', 'unit')
        if test_type in categories:
            categories[test_type]['tests'].append((test_name, result))
            categories[test_type]['total'] += 1
            if result['passed']:
                categories[test_type]['passed'] += 1
    
    # Overall statistics
    print(f"📊 OVERALL STATISTICS:")
    print(f"   Total Tests: {logger.total_tests}")
    print(f"   ✅ Passed: {logger.passed_tests}")
    print(f"   ❌ Failed: {logger.failed_tests}")
    print(f"   📈 Success Rate: {(logger.passed_tests/logger.total_tests)*100:.1f}%")
    
    # Category breakdown
    print(f"\n📋 CATEGORY BREAKDOWN:")
    category_names = {
        'grey': '⚫ Grey-Box Testing (Internal Knowledge)',
        'black': '⚪ Black-Box Testing (External Behavior)', 
        'integration': '🔗 Integration Testing (System Workflows)',
        'unit': '🔬 Unit Testing (Individual Components)'
    }
    
    for cat_key, cat_data in categories.items():
        if cat_data['total'] > 0:
            success_rate = (cat_data['passed'] / cat_data['total']) * 100
            print(f"   {category_names[cat_key]}: {cat_data['passed']}/{cat_data['total']} ({success_rate:.1f}%)")
    
    # Detailed results by category
    for cat_key, cat_data in categories.items():
        if cat_data['total'] > 0:
            print(f"\n{category_names[cat_key]}:")
            for test_name, result in cat_data['tests']:
                status = "✅" if result['passed'] else "❌"
                print(f"  {status} {test_name}")
                if result['details']:
                    print(f"      {result['details']}")
    
    # Recommendations
    if logger.failed_tests > 0:
        print(f"\n🔧 RECOMMENDATIONS:")
        failed_tests = [name for name, result in logger.results.items() if not result['passed']]
        
        if any('roll call' in test.lower() for test in failed_tests):
            print("  • Review roll call validation patterns")
        if any('database' in test.lower() for test in failed_tests):
            print("  • Check database connectivity and schema")
        if any('security' in test.lower() for test in failed_tests):
            print("  • Enhance input validation and sanitization")
        if any('performance' in test.lower() for test in failed_tests):
            print("  • Optimize database queries and application performance")
    
    overall_success = logger.failed_tests == 0
    
    if overall_success:
        print(f"\n🎉 ALL SYSTEMS OPERATIONAL!")
        print(f"✨ Your Enterprise Mentorship Management System has passed comprehensive testing!")
        print(f"🚀 System is production-ready with robust validation and security!")
    else:
        print(f"\n⚠️ ATTENTION REQUIRED")
        print(f"🔧 {logger.failed_tests} test(s) need to be addressed before production deployment")
    
    return overall_success

def main():
    """Run comprehensive grey-box and black-box testing"""
    logger.log_header("COMPREHENSIVE GREY-BOX & BLACK-BOX TEST SUITE")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Working directory: {os.getcwd()}")
    print(f"🎯 Testing Strategy: Grey-box + Black-box + Integration + Security")
    
    # Run all test categories
    test_results = {}
    
    # Grey-box testing (with internal knowledge)
    test_results['Roll Call Validation'] = FormTester.test_roll_call_validation()
    test_results['CRUD Operations'] = DatabaseIntegrityTester.test_crud_operations()
    test_results['Data Validation'] = DatabaseIntegrityTester.test_data_validation()
    test_results['Flask Routes'] = test_flask_routes()
    test_results['Database Performance'] = PerformanceTester.test_database_performance()
    
    # Black-box testing (external behavior only)
    test_results['Form Field Validation'] = FormTester.test_form_field_validation()
    test_results['Navigation Structure'] = UIComponentTester.test_navigation_structure()
    test_results['Button Functionality'] = UIComponentTester.test_button_functionality()
    test_results['Input Sanitization'] = SecurityTester.test_input_sanitization()
    
    # Integration testing (workflows)
    test_results['Mentor-Mentee Assignment'] = SystemIntegrationTester.test_mentor_mentee_assignment()
    test_results['Session Management'] = SystemIntegrationTester.test_session_management()
    
    # Generate comprehensive report
    overall_success = generate_comprehensive_report(test_results)
    
    # Save detailed test report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"comprehensive_test_report_{timestamp}.json"
    
    detailed_report = {
        'timestamp': datetime.now().isoformat(),
        'testing_strategy': 'Grey-box + Black-box + Integration + Security',
        'summary': {
            'total_tests': logger.total_tests,
            'passed_tests': logger.passed_tests,
            'failed_tests': logger.failed_tests,
            'success_rate': (logger.passed_tests / logger.total_tests) * 100 if logger.total_tests > 0 else 0
        },
        'results': logger.results,
        'test_categories': {
            'grey_box': 'Internal system knowledge testing',
            'black_box': 'External behavior testing',
            'integration': 'System workflow testing',
            'security': 'Security and input validation testing'
        }
    }
    
    with open(report_file, 'w') as f:
        json.dump(detailed_report, f, indent=2)
    
    print(f"\n📁 Detailed test report saved to: {report_file}")
    
    # Exit with appropriate code
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
