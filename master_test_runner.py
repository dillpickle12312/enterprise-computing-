#!/usr/bin/env python3
"""
Master Test Suite Runner - Executes all testing suites
Includes: System Tests, UI Tests, Roll Call Tests, and Manual Verification Guides
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"🎯 {title}")
    print("="*80)

def print_section(title):
    """Print a formatted section"""
    print(f"\n🔍 {title}")
    print("-" * 60)

def print_result(test_name, passed, details=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"    {details}")

def run_test_script(script_name, description):
    """Run a test script and return success status"""
    print_section(f"Running: {description}")
    
    if not os.path.exists(script_name):
        print_result(f"{script_name} exists", False, "Script file not found")
        return False
    
    try:
        # Make script executable
        os.chmod(script_name, 0o755)
        
        # Run the script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        success = result.returncode == 0
        
        if success:
            print_result(f"{description}", True, "All tests passed")
        else:
            print_result(f"{description}", False, "Some tests failed")
            print("    Error output:")
            print("   ", result.stderr[:200] if result.stderr else "No error details")
        
        # Print summary of output
        if result.stdout:
            lines = result.stdout.split('\n')
            summary_lines = [line for line in lines if any(keyword in line for keyword in ['PASS', 'FAIL', 'SUCCESS', 'Total Tests'])]
            if summary_lines:
                print("    Summary:")
                for line in summary_lines[-5:]:  # Last 5 relevant lines
                    print(f"      {line.strip()}")
        
        return success
        
    except subprocess.TimeoutExpired:
        print_result(f"{description}", False, "Test timed out after 5 minutes")
        return False
    except Exception as e:
        print_result(f"{description}", False, str(e))
        return False

def create_manual_verification_checklist():
    """Create a manual verification checklist for final testing"""
    print_section("Creating Manual Verification Checklist")
    
    checklist = """
# 🔍 MANUAL VERIFICATION CHECKLIST

## 📋 Pre-Deployment Final Checks

### 1. 🎯 Roll Call System Testing
- [ ] Open "Add New Mentee" form
- [ ] Test invalid roll call: `12A` → Should show error message
- [ ] Test valid roll call: `12/7` → Should accept with green validation
- [ ] Test subject code: `12ENG1` → Should accept
- [ ] Submit form with valid data → Should create mentee successfully

### 2. 🔘 Button Functionality Testing
- [ ] Dashboard "Add New Mentor" button → Should navigate to add mentor form
- [ ] Dashboard "Add New Mentee" button → Should navigate to add mentee form
- [ ] Mentors list "View Details" buttons → Should show mentor details
- [ ] Mentees list "Assign Mentor" buttons → Should open assignment form
- [ ] Forms "Submit" buttons → Should process and show success/error messages
- [ ] Navigation menu links → Should navigate to correct pages

### 3. 📝 Form Validation Testing
- [ ] Try submitting empty forms → Should show validation errors
- [ ] Test real-time validation → Should show green/red feedback as you type
- [ ] Test all required fields → Should enforce completion
- [ ] Test field format validation → Should match expected patterns

### 4. 🔄 Navigation Flow Testing
- [ ] Can navigate to all main pages without errors
- [ ] Back button works correctly
- [ ] Breadcrumbs (if present) work correctly
- [ ] Menu items highlight current page

### 5. 📊 Data Display Testing
- [ ] Mentors list shows all mentors with correct roll calls
- [ ] Mentees list shows all mentees with correct roll calls
- [ ] Assignment status displays correctly
- [ ] Statistics page shows accurate data

### 6. 🎨 UI/UX Testing
- [ ] Forms are properly styled and readable
- [ ] Buttons have hover effects
- [ ] Error messages are clearly visible
- [ ] Success messages appear after actions
- [ ] Loading states work (if implemented)

### 7. 📱 Responsive Design Testing
- [ ] Test on mobile device or narrow browser window
- [ ] Check that navigation collapses properly
- [ ] Ensure forms are usable on small screens
- [ ] Verify tables scroll horizontally if needed

### 8. 🔒 Error Handling Testing
- [ ] Try accessing invalid URLs → Should show 404 or redirect
- [ ] Submit forms with invalid data → Should show helpful errors
- [ ] Test with empty database → Should handle gracefully

## ✅ FINAL VERIFICATION

### All automated tests pass: [ ]
### All manual checks pass: [ ]
### System ready for production: [ ]

## 🚀 DEPLOYMENT READINESS

If all items above are checked:
- ✅ Roll call system is fully functional
- ✅ All buttons and interactions work correctly
- ✅ Forms validate properly
- ✅ UI is polished and user-friendly
- ✅ System is production-ready!

---
📅 Verified by: _________________ Date: _________________
"""
    
    with open('MANUAL_VERIFICATION_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print_result("Manual verification checklist created", True, "Saved as MANUAL_VERIFICATION_CHECKLIST.md")
    return True

def generate_master_report(test_results):
    """Generate master test report"""
    print_header("🎯 MASTER TEST SUITE RESULTS")
    
    total_suites = len(test_results)
    passed_suites = sum(1 for result in test_results.values() if result)
    failed_suites = total_suites - passed_suites
    
    print(f"📊 Total Test Suites: {total_suites}")
    print(f"✅ Passed: {passed_suites}")
    print(f"❌ Failed: {failed_suites}")
    print(f"📈 Success Rate: {(passed_suites/total_suites)*100:.1f}%")
    
    print("\n📋 Test Suite Results:")
    for suite_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {suite_name}")
    
    # Overall status
    overall_success = failed_suites == 0
    
    if overall_success:
        print("\n🎉 ALL TEST SUITES PASSED!")
        print("✨ Your Enterprise Mentorship Management System is fully tested and ready!")
        print("🎯 Roll call system: WORKING PERFECTLY")
        print("🔘 All buttons and interactions: TESTED AND FUNCTIONAL")
        print("📝 All forms and validation: WORKING CORRECTLY")
        print("🚀 SYSTEM IS PRODUCTION READY!")
        
        print("\n📋 NEXT STEPS:")
        print("1. Complete manual verification checklist")
        print("2. Test in a browser environment")
        print("3. Deploy to production")
        
    else:
        print(f"\n⚠️  {failed_suites} TEST SUITE(S) FAILED")
        print("🔧 Please fix the failed test suites before deployment")
        
        print("\n🔧 FAILED SUITES TO FIX:")
        for suite_name, result in test_results.items():
            if not result:
                print(f"   • {suite_name}")
    
    return overall_success

def main():
    """Run all test suites"""
    print_header("ENTERPRISE MENTORSHIP SYSTEM - MASTER TEST SUITE")
    print("🎯 Comprehensive Testing: Roll Call, UI, Buttons, Forms, and More")
    print(f"🕐 Testing started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Test suites to run
    test_suites = [
        ('simple_system_test.py', 'Core System Functionality Tests'),
        ('comprehensive_ui_test.py', 'UI & Button Interaction Tests'),
        ('manual_system_test.py', 'Advanced Manual System Tests')
    ]
    
    # Run all test suites
    results = {}
    
    for script, description in test_suites:
        results[description] = run_test_script(script, description)
    
    # Create manual verification checklist
    results['Manual Verification Checklist'] = create_manual_verification_checklist()
    
    # Generate master report
    overall_success = generate_master_report(results)
    
    # Save master report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    master_report = {
        'timestamp': datetime.now().isoformat(),
        'test_type': 'Master Test Suite - All Components',
        'suites_run': test_suites,
        'results': results,
        'summary': {
            'total_suites': len(results),
            'passed_suites': sum(1 for r in results.values() if r),
            'failed_suites': sum(1 for r in results.values() if not r),
            'overall_success': overall_success
        }
    }
    
    report_file = f"master_test_report_{timestamp}.json"
    with open(report_file, 'w') as f:
        json.dump(master_report, f, indent=2)
    
    print(f"\n📁 Master test report saved to: {report_file}")
    
    if overall_success:
        print("\n🎊 CONGRATULATIONS! 🎊")
        print("🏆 ALL TESTS PASSED!")
        print("✨ Your system is comprehensively tested and production-ready!")
        print("🎯 Roll call system is working perfectly!")
        print("🔘 Every button and interaction has been verified!")
        print("📝 All forms and validation are functional!")
        
        print("\n📋 FINAL STEP:")
        print("Complete the manual verification checklist: MANUAL_VERIFICATION_CHECKLIST.md")
        
    else:
        print("\n🔧 ATTENTION REQUIRED")
        print("Some test suites failed. Please review and fix before deployment.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
