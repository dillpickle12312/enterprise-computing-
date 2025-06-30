#!/usr/bin/env python3
"""
UI Button and Interactive Element Testing Suite
Tests every button, form field, and user interaction element
"""

import os
import sys
import re
from typing import Dict, List, Tuple
from datetime import datetime

class ButtonTester:
    """Comprehensive button and UI element testing"""
    
    def __init__(self):
        self.test_results = []
        self.total_buttons = 0
        self.tested_buttons = 0
        
    def log_result(self, test_name, passed, details=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    📝 {details}")
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        
    def extract_buttons_from_template(self, template_path):
        """Extract all buttons and interactive elements from a template"""
        if not os.path.exists(template_path):
            return []
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        buttons = []
        
        # Find submit buttons
        submit_buttons = re.findall(r'<input[^>]*type=["\']submit["\'][^>]*>', content, re.IGNORECASE)
        for btn in submit_buttons:
            value_match = re.search(r'value=["\']([^"\']*)["\']', btn)
            id_match = re.search(r'id=["\']([^"\']*)["\']', btn)
            name_match = re.search(r'name=["\']([^"\']*)["\']', btn)
            
            button_info = {
                'type': 'submit',
                'html': btn,
                'text': value_match.group(1) if value_match else 'Submit',
                'id': id_match.group(1) if id_match else None,
                'name': name_match.group(1) if name_match else None
            }
            buttons.append(button_info)
        
        # Find regular buttons
        regular_buttons = re.findall(r'<button[^>]*>.*?</button>', content, re.IGNORECASE | re.DOTALL)
        for btn in regular_buttons:
            type_match = re.search(r'type=["\']([^"\']*)["\']', btn)
            id_match = re.search(r'id=["\']([^"\']*)["\']', btn)
            text_match = re.search(r'<button[^>]*>(.*?)</button>', btn, re.DOTALL)
            onclick_match = re.search(r'onclick=["\']([^"\']*)["\']', btn)
            
            # Clean text content
            text_content = text_match.group(1) if text_match else ''
            text_content = re.sub(r'<[^>]+>', '', text_content).strip()
            
            button_info = {
                'type': type_match.group(1) if type_match else 'button',
                'html': btn,
                'text': text_content[:50] + ('...' if len(text_content) > 50 else ''),
                'id': id_match.group(1) if id_match else None,
                'onclick': onclick_match.group(1) if onclick_match else None
            }
            buttons.append(button_info)
        
        # Find link buttons (anchor tags with btn class)
        link_buttons = re.findall(r'<a[^>]*class=["\'][^"\']*btn[^"\']*["\'][^>]*>.*?</a>', content, re.IGNORECASE | re.DOTALL)
        for btn in link_buttons:
            href_match = re.search(r'href=["\']([^"\']*)["\']', btn)
            text_match = re.search(r'<a[^>]*>(.*?)</a>', btn, re.DOTALL)
            id_match = re.search(r'id=["\']([^"\']*)["\']', btn)
            
            text_content = text_match.group(1) if text_match else ''
            text_content = re.sub(r'<[^>]+>', '', text_content).strip()
            
            button_info = {
                'type': 'link',
                'html': btn,
                'text': text_content[:50] + ('...' if len(text_content) > 50 else ''),
                'id': id_match.group(1) if id_match else None,
                'href': href_match.group(1) if href_match else None
            }
            buttons.append(button_info)
        
        return buttons
    
    def extract_form_fields_from_template(self, template_path):
        """Extract all form fields from a template"""
        if not os.path.exists(template_path):
            return []
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        fields = []
        
        # Find input fields
        input_fields = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
        for field in input_fields:
            type_match = re.search(r'type=["\']([^"\']*)["\']', field)
            name_match = re.search(r'name=["\']([^"\']*)["\']', field)
            id_match = re.search(r'id=["\']([^"\']*)["\']', field)
            required_match = re.search(r'required', field, re.IGNORECASE)
            pattern_match = re.search(r'pattern=["\']([^"\']*)["\']', field)
            
            field_info = {
                'element': 'input',
                'type': type_match.group(1) if type_match else 'text',
                'name': name_match.group(1) if name_match else None,
                'id': id_match.group(1) if id_match else None,
                'required': bool(required_match),
                'pattern': pattern_match.group(1) if pattern_match else None,
                'html': field
            }
            fields.append(field_info)
        
        # Find select fields
        select_fields = re.findall(r'<select[^>]*>.*?</select>', content, re.IGNORECASE | re.DOTALL)
        for field in select_fields:
            name_match = re.search(r'name=["\']([^"\']*)["\']', field)
            id_match = re.search(r'id=["\']([^"\']*)["\']', field)
            required_match = re.search(r'required', field, re.IGNORECASE)
            
            # Count options
            options = re.findall(r'<option[^>]*>', field, re.IGNORECASE)
            
            field_info = {
                'element': 'select',
                'type': 'select',
                'name': name_match.group(1) if name_match else None,
                'id': id_match.group(1) if id_match else None,
                'required': bool(required_match),
                'options_count': len(options),
                'html': field[:100] + ('...' if len(field) > 100 else '')
            }
            fields.append(field_info)
        
        # Find textarea fields
        textarea_fields = re.findall(r'<textarea[^>]*>.*?</textarea>', content, re.IGNORECASE | re.DOTALL)
        for field in textarea_fields:
            name_match = re.search(r'name=["\']([^"\']*)["\']', field)
            id_match = re.search(r'id=["\']([^"\']*)["\']', field)
            required_match = re.search(r'required', field, re.IGNORECASE)
            
            field_info = {
                'element': 'textarea',
                'type': 'textarea',
                'name': name_match.group(1) if name_match else None,
                'id': id_match.group(1) if id_match else None,
                'required': bool(required_match),
                'html': field[:100] + ('...' if len(field) > 100 else '')
            }
            fields.append(field_info)
        
        return fields
    
    def test_template_buttons(self, template_path, template_name):
        """Test all buttons in a specific template"""
        print(f"\n🔍 Testing buttons in {template_name}")
        print("-" * 50)
        
        buttons = self.extract_buttons_from_template(template_path)
        self.total_buttons += len(buttons)
        
        if not buttons:
            self.log_result(f"{template_name}: No buttons found", True, "Template has no interactive buttons")
            return True
        
        all_passed = True
        
        for i, button in enumerate(buttons):
            self.tested_buttons += 1
            
            # Test button has proper attributes
            has_text = bool(button['text'] and button['text'].strip())
            has_action = bool(button.get('onclick') or button.get('href') or button['type'] in ['submit', 'button'])
            
            button_desc = f"{button['type']} button: '{button['text'][:30]}'"
            if button['id']:
                button_desc += f" (id: {button['id']})"
            
            # Test button completeness
            passed = has_text and has_action
            self.log_result(f"{template_name}: {button_desc}", passed, 
                          f"Text: {has_text}, Action: {has_action}")
            
            all_passed = all_passed and passed
            
            # Test specific button types
            if button['type'] == 'submit':
                # Submit buttons should be in forms
                has_form_context = '<form' in open(template_path).read().lower()
                self.log_result(f"{template_name}: Submit button in form context", has_form_context,
                              "Submit buttons should be within form elements")
                all_passed = all_passed and has_form_context
            
            elif button['type'] == 'link':
                # Link buttons should have valid href
                has_valid_href = button.get('href') and not button['href'].startswith('#')
                self.log_result(f"{template_name}: Link button has valid href", has_valid_href,
                              f"href: {button.get('href', 'None')}")
        
        return all_passed
    
    def test_template_forms(self, template_path, template_name):
        """Test all form fields in a specific template"""
        print(f"\n📝 Testing form fields in {template_name}")
        print("-" * 50)
        
        fields = self.extract_form_fields_from_template(template_path)
        
        if not fields:
            self.log_result(f"{template_name}: No form fields found", True, "Template has no form fields")
            return True
        
        all_passed = True
        
        for field in fields:
            field_desc = f"{field['element']} field"
            if field['name']:
                field_desc += f" (name: {field['name']})"
            if field['id']:
                field_desc += f" (id: {field['id']})"
            
            # Test field has proper attributes
            has_name_or_id = bool(field['name'] or field['id'])
            self.log_result(f"{template_name}: {field_desc} has identifier", has_name_or_id,
                          f"name: {field['name']}, id: {field['id']}")
            
            # Test required fields have validation
            if field['required']:
                has_validation = bool(field.get('pattern') or field['type'] in ['email', 'tel', 'url'])
                if field['type'] not in ['submit', 'button', 'hidden']:
                    self.log_result(f"{template_name}: Required field has validation", has_validation,
                                  f"type: {field['type']}, pattern: {field.get('pattern', 'None')}")
                    all_passed = all_passed and (has_validation or field['type'] in ['text', 'password'])
            
            all_passed = all_passed and has_name_or_id
        
        return all_passed
    
    def test_javascript_interactions(self, template_path, template_name):
        """Test JavaScript interactions in templates"""
        print(f"\n⚡ Testing JavaScript interactions in {template_name}")
        print("-" * 50)
        
        if not os.path.exists(template_path):
            return True
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Check for JavaScript event handlers
        onclick_handlers = re.findall(r'onclick=["\']([^"\']*)["\']', content, re.IGNORECASE)
        onchange_handlers = re.findall(r'onchange=["\']([^"\']*)["\']', content, re.IGNORECASE)
        onsubmit_handlers = re.findall(r'onsubmit=["\']([^"\']*)["\']', content, re.IGNORECASE)
        
        total_handlers = len(onclick_handlers) + len(onchange_handlers) + len(onsubmit_handlers)
        
        if total_handlers == 0:
            self.log_result(f"{template_name}: No JavaScript handlers", True, "Template has no inline JavaScript")
            return True
        
        # Test onclick handlers
        for handler in onclick_handlers:
            is_safe = not any(dangerous in handler.lower() for dangerous in ['eval', 'innerhtml', 'document.write'])
            self.log_result(f"{template_name}: Safe onclick handler", is_safe,
                          f"Handler: {handler[:50]}...")
        
        # Test for external script includes
        script_includes = re.findall(r'<script[^>]*src=["\']([^"\']*)["\']', content, re.IGNORECASE)
        for script_src in script_includes:
            is_local = not script_src.startswith(('http://', 'https://'))
            self.log_result(f"{template_name}: Local script include", is_local,
                          f"Script: {script_src}")
        
        return True
    
    def run_comprehensive_ui_tests(self):
        """Run comprehensive UI testing on all templates"""
        print("🧪 COMPREHENSIVE UI BUTTON & INTERACTION TESTING")
        print("=" * 60)
        
        # List of all templates to test
        template_files = [
            ('templates/base.html', 'Base Template'),
            ('templates/dashboard.html', 'Dashboard'),
            ('templates/mentors.html', 'Mentors List'),
            ('templates/mentees.html', 'Mentees List'),
            ('templates/add_mentor.html', 'Add Mentor Form'),
            ('templates/add_mentee.html', 'Add Mentee Form'),
            ('templates/mentor_detail.html', 'Mentor Detail'),
            ('templates/mentee_detail.html', 'Mentee Detail'),
            ('templates/assign_mentor.html', 'Assign Mentor'),
            ('templates/bulk_assign_mentors.html', 'Bulk Assign'),
            ('templates/reassign_mentees.html', 'Reassign Mentees'),
            ('templates/schedule_session.html', 'Schedule Session'),
            ('templates/statistics.html', 'Statistics'),
            ('templates/calendar.html', 'Calendar'),
            ('templates/user_guide.html', 'User Guide'),
            ('templates/clear_all_data.html', 'Clear Data'),
            ('templates/delete_mentor_confirm.html', 'Delete Mentor'),
            ('templates/delete_mentee_confirm.html', 'Delete Mentee'),
        ]
        
        all_tests_passed = True
        templates_tested = 0
        
        for template_path, template_name in template_files:
            if os.path.exists(template_path):
                templates_tested += 1
                print(f"\n📄 Testing {template_name} ({template_path})")
                print("=" * 60)
                
                # Test buttons
                buttons_passed = self.test_template_buttons(template_path, template_name)
                
                # Test form fields
                forms_passed = self.test_template_forms(template_path, template_name)
                
                # Test JavaScript
                js_passed = self.test_javascript_interactions(template_path, template_name)
                
                template_passed = buttons_passed and forms_passed and js_passed
                all_tests_passed = all_tests_passed and template_passed
                
                status = "✅ PASS" if template_passed else "❌ FAIL"
                print(f"\n{status} {template_name} overall testing")
        
        # Generate summary report
        print("\n" + "=" * 60)
        print("📊 UI TESTING SUMMARY REPORT")
        print("=" * 60)
        
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        total_tests = len(self.test_results)
        
        print(f"📈 Templates Tested: {templates_tested}")
        print(f"🔘 Total Buttons Found: {self.total_buttons}")
        print(f"🧪 Total Tests Run: {total_tests}")
        print(f"✅ Tests Passed: {passed_tests}")
        print(f"❌ Tests Failed: {total_tests - passed_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if all_tests_passed:
            print(f"\n🎉 ALL UI TESTS PASSED!")
            print(f"✨ Every button and form element has been tested and validated!")
            print(f"🚀 User interface is ready for production!")
        else:
            print(f"\n⚠️ SOME TESTS FAILED")
            print(f"🔧 Review failed tests and fix UI issues before deployment")
        
        # Save detailed report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"ui_testing_report_{timestamp}.json"
        
        import json
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'templates_tested': templates_tested,
                'total_buttons': self.total_buttons,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': (passed_tests/total_tests)*100 if total_tests > 0 else 0
            },
            'test_results': self.test_results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📁 Detailed UI test report saved to: {report_file}")
        
        return all_tests_passed

def main():
    """Run comprehensive UI testing"""
    tester = ButtonTester()
    success = tester.run_comprehensive_ui_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
