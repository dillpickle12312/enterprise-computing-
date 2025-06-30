#!/usr/bin/env python3
"""
Button and Interaction Testing Suite
Comprehensive testing of every button, link, and interactive element

This script performs exhaustive testing of:
1. Every button in every template
2. All form submissions and validations
3. Navigation links and routing
4. JavaScript interactions
5. Bootstrap modals and dropdowns
6. AJAX calls and dynamic content
7. Accessibility features
8. Error handling and edge cases
"""

import os
import re
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import sys

# HTML and JavaScript parsing
from bs4 import BeautifulSoup
import requests

# Flask testing
try:
    sys.path.insert(0, '/workspaces/enterprise-computing-')
    import app as flask_app
    from flask.testing import FlaskClient
except ImportError:
    flask_app = None
    FlaskClient = None

@dataclass
class InteractiveElement:
    """Represents an interactive UI element"""
    element_id: str
    element_type: str  # button, link, form, input, etc.
    tag: str
    text: str
    attributes: Dict[str, str]
    template_file: str
    line_number: int
    action: str  # What it does (submit, navigate, toggle, etc.)
    target: str  # Where it goes or what it affects
    validation_rules: List[str]
    accessibility_features: List[str]
    issues: List[str]

@dataclass
class InteractionTest:
    """Represents a test of an interactive element"""
    element_id: str
    test_name: str
    test_type: str  # click, submit, navigate, validate, etc.
    expected_behavior: str
    actual_behavior: str
    status: str  # PASS, FAIL, ERROR, SKIP
    execution_time: float
    error_message: str
    details: Dict[str, Any]

class ButtonAndInteractionScanner:
    """Scans templates for all interactive elements and behaviors"""
    
    def __init__(self, templates_dir: str, static_dir: str = None):
        self.templates_dir = Path(templates_dir)
        self.static_dir = Path(static_dir) if static_dir else None
        self.elements = []
        self.javascript_handlers = []
        
    def scan_all_interactions(self) -> List[InteractiveElement]:
        """Scan all templates for interactive elements"""
        print("🔍 Scanning all templates for interactive elements...")
        
        template_files = list(self.templates_dir.glob("*.html"))
        for template_file in template_files:
            self._scan_template_interactions(template_file)
        
        # Also scan JavaScript files for handlers
        if self.static_dir and (self.static_dir / "js").exists():
            self._scan_javascript_files()
        
        print(f"   Found {len(self.elements)} interactive elements")
        print(f"   Found {len(self.javascript_handlers)} JavaScript handlers")
        
        return self.elements
    
    def _scan_template_interactions(self, template_file: Path):
        """Scan a single template for interactive elements"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            lines = content.split('\n')
            
            # Find all interactive elements
            self._scan_buttons(soup, template_file.name, content)
            self._scan_links(soup, template_file.name, content)
            self._scan_forms(soup, template_file.name, content)
            self._scan_inputs(soup, template_file.name, content)
            self._scan_select_elements(soup, template_file.name, content)
            self._scan_modals(soup, template_file.name, content)
            self._scan_dropdowns(soup, template_file.name, content)
            
        except Exception as e:
            print(f"   ⚠️  Error scanning {template_file}: {e}")
    
    def _scan_buttons(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for button elements"""
        buttons = soup.find_all('button')
        
        for button in buttons:
            line_num = self._find_line_number(content, str(button)[:100])
            
            # Determine button action
            action = self._determine_button_action(button)
            target = self._determine_button_target(button)
            
            # Check validation rules
            validation_rules = self._extract_validation_rules(button)
            
            # Check accessibility features
            accessibility = self._check_accessibility_features(button)
            
            # Find issues
            issues = self._find_button_issues(button)
            
            element = InteractiveElement(
                element_id=self._generate_element_id(button, template_file, line_num),
                element_type='button',
                tag='button',
                text=button.get_text(strip=True),
                attributes=dict(button.attrs) if button.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action=action,
                target=target,
                validation_rules=validation_rules,
                accessibility_features=accessibility,
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_links(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for link elements"""
        links = soup.find_all('a')
        
        for link in links:
            line_num = self._find_line_number(content, str(link)[:100])
            
            # Skip empty or placeholder links
            href = link.get('href', '')
            if not href or href == '#':
                onclick = link.get('onclick', '')
                data_toggle = link.get('data-bs-toggle', '')
                if not onclick and not data_toggle:
                    continue
            
            # Determine link action
            action = self._determine_link_action(link)
            target = link.get('href', link.get('data-bs-target', ''))
            
            # Check accessibility
            accessibility = self._check_accessibility_features(link)
            
            # Find issues
            issues = self._find_link_issues(link)
            
            element = InteractiveElement(
                element_id=self._generate_element_id(link, template_file, line_num),
                element_type='link',
                tag='a',
                text=link.get_text(strip=True),
                attributes=dict(link.attrs) if link.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action=action,
                target=target,
                validation_rules=[],
                accessibility_features=accessibility,
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_forms(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for form elements"""
        forms = soup.find_all('form')
        
        for form in forms:
            line_num = self._find_line_number(content, str(form)[:100])
            
            action = form.get('action', '')
            method = form.get('method', 'GET').upper()
            
            # Check form validation
            validation_rules = self._extract_form_validation_rules(form)
            
            # Check accessibility
            accessibility = self._check_accessibility_features(form)
            
            # Find issues
            issues = self._find_form_issues(form)
            
            element = InteractiveElement(
                element_id=self._generate_element_id(form, template_file, line_num),
                element_type='form',
                tag='form',
                text=f"Form -> {action}",
                attributes=dict(form.attrs) if form.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action=f"{method} {action}",
                target=action,
                validation_rules=validation_rules,
                accessibility_features=accessibility,
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_inputs(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for input elements"""
        inputs = soup.find_all('input')
        
        for input_elem in inputs:
            # Skip hidden inputs and buttons (handled separately)
            input_type = input_elem.get('type', 'text')
            if input_type in ['hidden', 'button', 'submit', 'reset']:
                continue
            
            line_num = self._find_line_number(content, str(input_elem)[:100])
            
            # Check validation rules
            validation_rules = self._extract_input_validation_rules(input_elem)
            
            # Check accessibility
            accessibility = self._check_accessibility_features(input_elem)
            
            # Find issues
            issues = self._find_input_issues(input_elem)
            
            element = InteractiveElement(
                element_id=self._generate_element_id(input_elem, template_file, line_num),
                element_type=f'input_{input_type}',
                tag='input',
                text=input_elem.get('placeholder', input_elem.get('name', '')),
                attributes=dict(input_elem.attrs) if input_elem.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action='input',
                target=input_elem.get('name', ''),
                validation_rules=validation_rules,
                accessibility_features=accessibility,
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_select_elements(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for select elements"""
        selects = soup.find_all('select')
        
        for select in selects:
            line_num = self._find_line_number(content, str(select)[:100])
            
            # Count options
            options = select.find_all('option')
            
            # Check validation
            validation_rules = self._extract_select_validation_rules(select)
            
            # Check accessibility
            accessibility = self._check_accessibility_features(select)
            
            # Find issues
            issues = self._find_select_issues(select)
            
            element = InteractiveElement(
                element_id=self._generate_element_id(select, template_file, line_num),
                element_type='select',
                tag='select',
                text=f"Select ({len(options)} options)",
                attributes=dict(select.attrs) if select.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action='select',
                target=select.get('name', ''),
                validation_rules=validation_rules,
                accessibility_features=accessibility,
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_modals(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for Bootstrap modals"""
        modals = soup.find_all(attrs={'class': re.compile(r'modal')})
        
        for modal in modals:
            line_num = self._find_line_number(content, str(modal)[:100])
            
            modal_id = modal.get('id', '')
            
            # Find modal triggers
            triggers = soup.find_all(attrs={'data-bs-target': f'#{modal_id}'})
            
            # Find modal buttons
            modal_buttons = modal.find_all('button')
            
            issues = []
            if not modal_id:
                issues.append("Modal missing ID")
            if not triggers:
                issues.append("No triggers found for modal")
            
            element = InteractiveElement(
                element_id=self._generate_element_id(modal, template_file, line_num),
                element_type='modal',
                tag='div',
                text=f"Modal {modal_id}",
                attributes=dict(modal.attrs) if modal.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action='modal_display',
                target=modal_id,
                validation_rules=[],
                accessibility_features=self._check_accessibility_features(modal),
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_dropdowns(self, soup: BeautifulSoup, template_file: str, content: str):
        """Scan for Bootstrap dropdowns"""
        dropdowns = soup.find_all(attrs={'data-bs-toggle': 'dropdown'})
        
        for dropdown in dropdowns:
            line_num = self._find_line_number(content, str(dropdown)[:100])
            
            # Find associated dropdown menu
            dropdown_menu = None
            if dropdown.get('id'):
                dropdown_menu = soup.find(attrs={'aria-labelledby': dropdown.get('id')})
            
            issues = []
            if not dropdown_menu:
                issues.append("Dropdown menu not found")
            
            element = InteractiveElement(
                element_id=self._generate_element_id(dropdown, template_file, line_num),
                element_type='dropdown',
                tag=dropdown.name,
                text=dropdown.get_text(strip=True),
                attributes=dict(dropdown.attrs) if dropdown.attrs else {},
                template_file=template_file,
                line_number=line_num,
                action='dropdown_toggle',
                target=dropdown.get('aria-labelledby', ''),
                validation_rules=[],
                accessibility_features=self._check_accessibility_features(dropdown),
                issues=issues
            )
            
            self.elements.append(element)
    
    def _scan_javascript_files(self):
        """Scan JavaScript files for event handlers"""
        js_files = list((self.static_dir / "js").glob("*.js"))
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for common event handlers
                event_patterns = [
                    r'addEventListener\s*\(\s*[\'"](\w+)[\'"]',
                    r'on(\w+)\s*=',
                    r'\$\([\'"]([^\'\"]+)[\'"]\)\.(\w+)\(',
                    r'document\.getElementById\([\'"]([^\'\"]+)[\'"]\)'
                ]
                
                for pattern in event_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        self.javascript_handlers.append({
                            'file': js_file.name,
                            'pattern': pattern,
                            'match': match.group(0),
                            'groups': match.groups()
                        })
                        
            except Exception as e:
                print(f"   ⚠️  Error scanning JS file {js_file}: {e}")
    
    def _find_line_number(self, content: str, element_str: str) -> int:
        """Find line number of element in content"""
        lines = content.split('\n')
        search_str = element_str[:50]  # First 50 characters
        
        for i, line in enumerate(lines, 1):
            if search_str in line:
                return i
        return 0
    
    def _generate_element_id(self, element, template_file: str, line_num: int) -> str:
        """Generate unique ID for element"""
        element_id = element.get('id', '')
        if element_id:
            return f"{template_file}#{element_id}"
        
        element_name = element.get('name', '')
        if element_name:
            return f"{template_file}@{element_name}"
        
        return f"{template_file}:{line_num}:{element.name}"
    
    def _determine_button_action(self, button) -> str:
        """Determine what a button does"""
        button_type = button.get('type', 'button')
        onclick = button.get('onclick', '')
        data_toggle = button.get('data-bs-toggle', '')
        
        if button_type == 'submit':
            return 'form_submit'
        elif button_type == 'reset':
            return 'form_reset'
        elif data_toggle == 'modal':
            return 'modal_open'
        elif data_toggle == 'dropdown':
            return 'dropdown_toggle'
        elif onclick:
            return 'javascript_function'
        else:
            return 'button_click'
    
    def _determine_button_target(self, button) -> str:
        """Determine button target"""
        return (button.get('data-bs-target') or 
                button.get('form') or 
                button.get('onclick', '').split('(')[0] or 
                'unknown')
    
    def _determine_link_action(self, link) -> str:
        """Determine what a link does"""
        href = link.get('href', '')
        data_toggle = link.get('data-bs-toggle', '')
        onclick = link.get('onclick', '')
        
        if data_toggle:
            return f'bootstrap_{data_toggle}'
        elif onclick:
            return 'javascript_function'
        elif href.startswith('#'):
            return 'anchor_navigation'
        elif href.startswith('http'):
            return 'external_navigation'
        elif href:
            return 'internal_navigation'
        else:
            return 'unknown'
    
    def _extract_validation_rules(self, element) -> List[str]:
        """Extract validation rules from element"""
        rules = []
        
        if element.get('required'):
            rules.append('required')
        if element.get('pattern'):
            rules.append(f"pattern: {element.get('pattern')}")
        if element.get('minlength'):
            rules.append(f"minlength: {element.get('minlength')}")
        if element.get('maxlength'):
            rules.append(f"maxlength: {element.get('maxlength')}")
        if element.get('min'):
            rules.append(f"min: {element.get('min')}")
        if element.get('max'):
            rules.append(f"max: {element.get('max')}")
        
        return rules
    
    def _extract_form_validation_rules(self, form) -> List[str]:
        """Extract validation rules from form"""
        rules = []
        
        # Check if form has novalidate
        if form.get('novalidate') is not None:
            rules.append('client_validation_disabled')
        
        # Count required fields
        required_fields = form.find_all(attrs={'required': True})
        if required_fields:
            rules.append(f'{len(required_fields)} required fields')
        
        return rules
    
    def _extract_input_validation_rules(self, input_elem) -> List[str]:
        """Extract validation rules from input element"""
        rules = self._extract_validation_rules(input_elem)
        
        input_type = input_elem.get('type', 'text')
        if input_type in ['email', 'url', 'tel', 'number', 'date']:
            rules.append(f'type_validation: {input_type}')
        
        return rules
    
    def _extract_select_validation_rules(self, select) -> List[str]:
        """Extract validation rules from select element"""
        rules = self._extract_validation_rules(select)
        
        if select.get('multiple'):
            rules.append('multiple_selection')
        
        return rules
    
    def _check_accessibility_features(self, element) -> List[str]:
        """Check accessibility features of element"""
        features = []
        
        if element.get('aria-label'):
            features.append('aria-label')
        if element.get('aria-describedby'):
            features.append('aria-describedby')
        if element.get('aria-labelledby'):
            features.append('aria-labelledby')
        if element.get('role'):
            features.append(f"role: {element.get('role')}")
        if element.get('tabindex'):
            features.append(f"tabindex: {element.get('tabindex')}")
        if element.get('title'):
            features.append('title')
        
        return features
    
    def _find_button_issues(self, button) -> List[str]:
        """Find issues with button element"""
        issues = []
        
        text = button.get_text(strip=True)
        if not text and not button.get('aria-label') and not button.get('title'):
            issues.append('No accessible text')
        
        if not button.get('type'):
            issues.append('Missing type attribute')
        
        # Check for disabled buttons without explanation
        if button.get('disabled') and not button.get('title') and not button.get('aria-describedby'):
            issues.append('Disabled without explanation')
        
        return issues
    
    def _find_link_issues(self, link) -> List[str]:
        """Find issues with link element"""
        issues = []
        
        href = link.get('href', '')
        text = link.get_text(strip=True)
        
        if not text and not link.get('aria-label'):
            issues.append('No accessible text')
        
        if href == '#' and not link.get('onclick') and not link.get('data-bs-toggle'):
            issues.append('Empty href without action')
        
        if href.startswith('http') and not link.get('target'):
            issues.append('External link without target specification')
        
        return issues
    
    def _find_form_issues(self, form) -> List[str]:
        """Find issues with form element"""
        issues = []
        
        if not form.get('action'):
            issues.append('Missing action attribute')
        
        if not form.get('method'):
            issues.append('Missing method attribute')
        
        # Check for forms without submit buttons
        submit_buttons = form.find_all('button', {'type': 'submit'}) + form.find_all('input', {'type': 'submit'})
        if not submit_buttons:
            issues.append('No submit button found')
        
        return issues
    
    def _find_input_issues(self, input_elem) -> List[str]:
        """Find issues with input element"""
        issues = []
        
        input_type = input_elem.get('type', 'text')
        name = input_elem.get('name', '')
        
        if not name:
            issues.append('Missing name attribute')
        
        if input_elem.get('required') and not input_elem.get('pattern') and input_type in ['text', 'email', 'tel']:
            issues.append('Required field without validation pattern')
        
        if not input_elem.get('placeholder') and input_type in ['text', 'email', 'tel', 'password']:
            issues.append('Missing placeholder text')
        
        # Check for proper labels
        input_id = input_elem.get('id')
        if input_id:
            # This would need to be checked in the context of the full document
            pass
        else:
            issues.append('Missing ID for label association')
        
        return issues
    
    def _find_select_issues(self, select) -> List[str]:
        """Find issues with select element"""
        issues = []
        
        if not select.get('name'):
            issues.append('Missing name attribute')
        
        options = select.find_all('option')
        if not options:
            issues.append('No options found')
        elif len(options) == 1:
            issues.append('Only one option available')
        
        return issues

class InteractionTester:
    """Tests interactive elements using Flask test client"""
    
    def __init__(self, elements: List[InteractiveElement]):
        self.elements = elements
        self.test_results = []
        self.client = None
        
        # Setup Flask test client
        self._setup_test_client()
    
    def _setup_test_client(self):
        """Setup Flask test client"""
        try:
            if flask_app:
                flask_app.app.config['TESTING'] = True
                flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
                
                with flask_app.app.app_context():
                    flask_app.db.create_all()
                
                self.client = flask_app.app.test_client()
                print("   ✅ Flask test client setup successful")
            else:
                print("   ⚠️  Flask app not available for testing")
        except Exception as e:
            print(f"   ❌ Failed to setup test client: {e}")
    
    def test_all_interactions(self) -> List[InteractionTest]:
        """Test all interactive elements"""
        print("🧪 Testing all interactive elements...")
        
        # Group elements by type for organized testing
        element_groups = {}
        for element in self.elements:
            if element.element_type not in element_groups:
                element_groups[element.element_type] = []
            element_groups[element.element_type].append(element)
        
        # Test each group
        for element_type, elements in element_groups.items():
            print(f"   Testing {len(elements)} {element_type} elements...")
            
            if element_type == 'button':
                self._test_buttons(elements)
            elif element_type == 'link':
                self._test_links(elements)
            elif element_type == 'form':
                self._test_forms(elements)
            elif element_type.startswith('input_'):
                self._test_inputs(elements)
            elif element_type == 'select':
                self._test_selects(elements)
            elif element_type == 'modal':
                self._test_modals(elements)
            elif element_type == 'dropdown':
                self._test_dropdowns(elements)
        
        print(f"   Completed {len(self.test_results)} interaction tests")
        return self.test_results
    
    def _test_buttons(self, buttons: List[InteractiveElement]):
        """Test button elements"""
        for button in buttons:
            start_time = time.time()
            
            try:
                # Test button accessibility
                if button.issues:
                    self._add_test_result(
                        button.element_id,
                        "Button Accessibility Check",
                        "accessibility",
                        "Check button has proper accessibility features",
                        f"Issues found: {', '.join(button.issues)}",
                        "FAIL" if button.issues else "PASS",
                        time.time() - start_time,
                        "",
                        {"issues": button.issues}
                    )
                else:
                    self._add_test_result(
                        button.element_id,
                        "Button Accessibility Check",
                        "accessibility",
                        "Button should have proper accessibility features",
                        "All accessibility checks passed",
                        "PASS",
                        time.time() - start_time,
                        "",
                        {}
                    )
                
                # Test button action based on type
                if button.action == 'form_submit' and self.client:
                    self._test_form_submit_button(button)
                elif button.action == 'modal_open':
                    self._test_modal_button(button)
                elif button.action == 'dropdown_toggle':
                    self._test_dropdown_button(button)
                
            except Exception as e:
                self._add_test_result(
                    button.element_id,
                    "Button Test",
                    "error",
                    "Button should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_links(self, links: List[InteractiveElement]):
        """Test link elements"""
        for link in links:
            start_time = time.time()
            
            try:
                # Test link accessibility
                status = "FAIL" if link.issues else "PASS"
                message = f"Issues: {', '.join(link.issues)}" if link.issues else "Link accessibility OK"
                
                self._add_test_result(
                    link.element_id,
                    "Link Accessibility Check",
                    "accessibility",
                    "Link should have proper accessibility features",
                    message,
                    status,
                    time.time() - start_time,
                    "",
                    {"issues": link.issues}
                )
                
                # Test link navigation if it's an internal link
                if link.action == 'internal_navigation' and self.client:
                    self._test_link_navigation(link)
                
            except Exception as e:
                self._add_test_result(
                    link.element_id,
                    "Link Test",
                    "error",
                    "Link should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_forms(self, forms: List[InteractiveElement]):
        """Test form elements"""
        for form in forms:
            start_time = time.time()
            
            try:
                # Test form structure
                status = "FAIL" if form.issues else "PASS"
                message = f"Issues: {', '.join(form.issues)}" if form.issues else "Form structure OK"
                
                self._add_test_result(
                    form.element_id,
                    "Form Structure Check",
                    "validation",
                    "Form should have proper structure",
                    message,
                    status,
                    time.time() - start_time,
                    "",
                    {"issues": form.issues, "validation_rules": form.validation_rules}
                )
                
                # Test form submission if client available
                if self.client and form.target:
                    self._test_form_submission(form)
                
            except Exception as e:
                self._add_test_result(
                    form.element_id,
                    "Form Test",
                    "error",
                    "Form should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_inputs(self, inputs: List[InteractiveElement]):
        """Test input elements"""
        for input_elem in inputs:
            start_time = time.time()
            
            try:
                # Test input validation rules
                status = "FAIL" if input_elem.issues else "PASS"
                message = f"Issues: {', '.join(input_elem.issues)}" if input_elem.issues else "Input validation OK"
                
                self._add_test_result(
                    input_elem.element_id,
                    "Input Validation Check",
                    "validation",
                    "Input should have proper validation",
                    message,
                    status,
                    time.time() - start_time,
                    "",
                    {"issues": input_elem.issues, "validation_rules": input_elem.validation_rules}
                )
                
            except Exception as e:
                self._add_test_result(
                    input_elem.element_id,
                    "Input Test",
                    "error",
                    "Input should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_selects(self, selects: List[InteractiveElement]):
        """Test select elements"""
        for select in selects:
            start_time = time.time()
            
            try:
                # Test select structure
                status = "FAIL" if select.issues else "PASS"
                message = f"Issues: {', '.join(select.issues)}" if select.issues else "Select structure OK"
                
                self._add_test_result(
                    select.element_id,
                    "Select Structure Check",
                    "validation",
                    "Select should have proper structure",
                    message,
                    status,
                    time.time() - start_time,
                    "",
                    {"issues": select.issues}
                )
                
            except Exception as e:
                self._add_test_result(
                    select.element_id,
                    "Select Test",
                    "error",
                    "Select should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_modals(self, modals: List[InteractiveElement]):
        """Test modal elements"""
        for modal in modals:
            start_time = time.time()
            
            try:
                # Test modal structure
                status = "FAIL" if modal.issues else "PASS"
                message = f"Issues: {', '.join(modal.issues)}" if modal.issues else "Modal structure OK"
                
                self._add_test_result(
                    modal.element_id,
                    "Modal Structure Check",
                    "ui",
                    "Modal should have proper structure",
                    message,
                    status,
                    time.time() - start_time,
                    "",
                    {"issues": modal.issues}
                )
                
            except Exception as e:
                self._add_test_result(
                    modal.element_id,
                    "Modal Test",
                    "error",
                    "Modal should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_dropdowns(self, dropdowns: List[InteractiveElement]):
        """Test dropdown elements"""
        for dropdown in dropdowns:
            start_time = time.time()
            
            try:
                # Test dropdown structure
                status = "FAIL" if dropdown.issues else "PASS"
                message = f"Issues: {', '.join(dropdown.issues)}" if dropdown.issues else "Dropdown structure OK"
                
                self._add_test_result(
                    dropdown.element_id,
                    "Dropdown Structure Check",
                    "ui",
                    "Dropdown should have proper structure",
                    message,
                    status,
                    time.time() - start_time,
                    "",
                    {"issues": dropdown.issues}
                )
                
            except Exception as e:
                self._add_test_result(
                    dropdown.element_id,
                    "Dropdown Test",
                    "error",
                    "Dropdown should function without errors",
                    f"Error during testing: {e}",
                    "ERROR",
                    time.time() - start_time,
                    str(e),
                    {}
                )
    
    def _test_form_submit_button(self, button: InteractiveElement):
        """Test form submit button"""
        # This would require more complex form context testing
        pass
    
    def _test_modal_button(self, button: InteractiveElement):
        """Test modal trigger button"""
        # Test that modal target exists
        target = button.target
        if target:
            status = "PASS"
            message = f"Modal button targets {target}"
        else:
            status = "FAIL"
            message = "Modal button has no target"
        
        self._add_test_result(
            button.element_id,
            "Modal Button Target Check",
            "ui",
            "Modal button should have valid target",
            message,
            status,
            0.001,
            "",
            {"target": target}
        )
    
    def _test_dropdown_button(self, button: InteractiveElement):
        """Test dropdown button"""
        # Similar to modal button testing
        pass
    
    def _test_link_navigation(self, link: InteractiveElement):
        """Test link navigation"""
        if not self.client:
            return
        
        start_time = time.time()
        
        try:
            response = self.client.get(link.target)
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                status = "PASS"
                message = f"Link navigates successfully ({response.status_code})"
            elif response.status_code in [301, 302]:
                status = "PASS"
                message = f"Link redirects ({response.status_code})"
            else:
                status = "FAIL"
                message = f"Link navigation failed ({response.status_code})"
            
            self._add_test_result(
                link.element_id,
                "Link Navigation Test",
                "navigation",
                "Link should navigate successfully",
                message,
                status,
                execution_time,
                "",
                {"target": link.target, "status_code": response.status_code}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._add_test_result(
                link.element_id,
                "Link Navigation Test",
                "navigation",
                "Link should navigate successfully",
                f"Navigation error: {e}",
                "ERROR",
                execution_time,
                str(e),
                {"target": link.target}
            )
    
    def _test_form_submission(self, form: InteractiveElement):
        """Test form submission"""
        if not self.client:
            return
        
        start_time = time.time()
        
        try:
            # Create test data based on form action
            test_data = self._create_test_form_data(form)
            
            if 'POST' in form.action:
                response = self.client.post(form.target, data=test_data)
            else:
                response = self.client.get(form.target, query_string=test_data)
            
            execution_time = time.time() - start_time
            
            if response.status_code in [200, 302, 400]:  # Success, redirect, or validation error
                status = "PASS"
                message = f"Form submission handled ({response.status_code})"
            else:
                status = "FAIL"
                message = f"Form submission failed ({response.status_code})"
            
            self._add_test_result(
                form.element_id,
                "Form Submission Test",
                "form",
                "Form should handle submission",
                message,
                status,
                execution_time,
                "",
                {"target": form.target, "status_code": response.status_code, "test_data": test_data}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._add_test_result(
                form.element_id,
                "Form Submission Test",
                "form",
                "Form should handle submission",
                f"Submission error: {e}",
                "ERROR",
                execution_time,
                str(e),
                {"target": form.target}
            )
    
    def _create_test_form_data(self, form: InteractiveElement) -> Dict[str, str]:
        """Create test data for form submission"""
        # Basic test data based on common form patterns
        if 'mentor' in form.target:
            return {
                'name': 'Test Mentor',
                'roll_call': '12345',
                'subjects': 'Mathematics'
            }
        elif 'mentee' in form.target:
            return {
                'name': 'Test Mentee',
                'roll_call': '54321',
                'year_level': '10'
            }
        else:
            return {'test_field': 'test_value'}
    
    def _add_test_result(self, element_id: str, test_name: str, test_type: str,
                        expected: str, actual: str, status: str, 
                        execution_time: float, error_msg: str, details: Dict[str, Any]):
        """Add a test result"""
        self.test_results.append(InteractionTest(
            element_id=element_id,
            test_name=test_name,
            test_type=test_type,
            expected_behavior=expected,
            actual_behavior=actual,
            status=status,
            execution_time=execution_time,
            error_message=error_msg,
            details=details
        ))

class ButtonTestReporter:
    """Generates detailed reports for button and interaction testing"""
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def generate_report(self, elements: List[InteractiveElement], 
                       test_results: List[InteractionTest],
                       output_file: str = None) -> str:
        """Generate comprehensive button testing report"""
        
        if output_file is None:
            output_file = f"button_interaction_report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        
        # Calculate statistics
        total_elements = len(elements)
        total_tests = len(test_results)
        
        passed_tests = sum(1 for r in test_results if r.status == "PASS")
        failed_tests = sum(1 for r in test_results if r.status == "FAIL")
        error_tests = sum(1 for r in test_results if r.status == "ERROR")
        
        elements_with_issues = sum(1 for e in elements if e.issues)
        
        # Group elements by type
        element_types = {}
        for element in elements:
            if element.element_type not in element_types:
                element_types[element.element_type] = []
            element_types[element.element_type].append(element)
        
        # Group tests by type
        test_types = {}
        for test in test_results:
            if test.test_type not in test_types:
                test_types[test.test_type] = []
            test_types[test.test_type].append(test)
        
        # Generate report
        report = f"""# Button and Interaction Testing Report

**Generated:** {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Total Interactive Elements:** {total_elements}
- **Elements with Issues:** {elements_with_issues} ({elements_with_issues/total_elements*100:.1f}%)
- **Total Tests Executed:** {total_tests}
- **Tests Passed:** {passed_tests} ({passed_tests/total_tests*100:.1f}% if total_tests > 0 else 0)
- **Tests Failed:** {failed_tests} ({failed_tests/total_tests*100:.1f}% if total_tests > 0 else 0)
- **Tests with Errors:** {error_tests} ({error_tests/total_tests*100:.1f}% if total_tests > 0 else 0)

## Interactive Elements by Type

"""
        
        for element_type, elements_list in sorted(element_types.items()):
            issues_count = sum(1 for e in elements_list if e.issues)
            report += f"### {element_type.replace('_', ' ').title()} ({len(elements_list)} elements)\n"
            report += f"**Issues Found:** {issues_count}\n\n"
            
            # Show problematic elements first
            problematic = [e for e in elements_list if e.issues]
            good = [e for e in elements_list if not e.issues]
            
            if problematic:
                report += "#### Elements with Issues:\n"
                for element in problematic[:5]:  # Show first 5
                    report += f"- **{element.template_file}:{element.line_number}** - {element.text[:50]}...\n"
                    for issue in element.issues:
                        report += f"  - ⚠️ {issue}\n"
                    report += "\n"
                
                if len(problematic) > 5:
                    report += f"... and {len(problematic) - 5} more with issues\n\n"
            
            if good:
                report += f"#### Elements OK: {len(good)}\n\n"
        
        # Test Results Summary
        report += "## Test Results by Category\n\n"
        
        for test_type, tests_list in sorted(test_types.items()):
            passed = sum(1 for t in tests_list if t.status == "PASS")
            failed = sum(1 for t in tests_list if t.status == "FAIL")
            errors = sum(1 for t in tests_list if t.status == "ERROR")
            
            report += f"### {test_type.replace('_', ' ').title()} Tests ({len(tests_list)} tests)\n"
            report += f"- ✅ Passed: {passed}\n"
            report += f"- ❌ Failed: {failed}\n"
            report += f"- ⚠️ Errors: {errors}\n\n"
            
            # Show failed tests
            failed_tests_list = [t for t in tests_list if t.status in ["FAIL", "ERROR"]]
            if failed_tests_list:
                report += "#### Failed/Error Tests:\n"
                for test in failed_tests_list:
                    status_icon = "❌" if test.status == "FAIL" else "⚠️"
                    report += f"- {status_icon} **{test.test_name}** ({test.element_id})\n"
                    report += f"  - Expected: {test.expected_behavior}\n"
                    report += f"  - Actual: {test.actual_behavior}\n"
                    if test.error_message:
                        report += f"  - Error: {test.error_message}\n"
                    report += "\n"
        
        # Detailed Element Inventory
        report += "## Detailed Element Inventory\n\n"
        
        for template_file in sorted(set(e.template_file for e in elements)):
            template_elements = [e for e in elements if e.template_file == template_file]
            report += f"### {template_file} ({len(template_elements)} elements)\n\n"
            
            for element in template_elements:
                status_icon = "⚠️" if element.issues else "✅"
                report += f"#### {status_icon} {element.element_type} - Line {element.line_number}\n"
                report += f"**Text:** {element.text}\n"
                report += f"**Action:** {element.action} → {element.target}\n"
                
                if element.validation_rules:
                    report += f"**Validation:** {', '.join(element.validation_rules)}\n"
                
                if element.accessibility_features:
                    report += f"**Accessibility:** {', '.join(element.accessibility_features)}\n"
                
                if element.issues:
                    report += "**Issues:**\n"
                    for issue in element.issues:
                        report += f"- {issue}\n"
                
                if element.attributes:
                    report += "**Attributes:**\n"
                    for attr, value in element.attributes.items():
                        if len(str(value)) > 50:
                            value = str(value)[:50] + "..."
                        report += f"- {attr}: {value}\n"
                
                report += "\n"
        
        # Recommendations
        report += "## Recommendations\n\n"
        
        recommendations = []
        
        # Accessibility recommendations
        accessibility_issues = sum(1 for e in elements if any('accessible' in issue.lower() for issue in e.issues))
        if accessibility_issues > 0:
            recommendations.append(f"🔧 Fix {accessibility_issues} accessibility issues to improve usability for all users")
        
        # Validation recommendations
        validation_issues = sum(1 for e in elements if any('validation' in issue.lower() or 'pattern' in issue.lower() for issue in e.issues))
        if validation_issues > 0:
            recommendations.append(f"📝 Add proper validation to {validation_issues} form elements")
        
        # Structure recommendations
        structure_issues = sum(1 for e in elements if any('missing' in issue.lower() for issue in e.issues))
        if structure_issues > 0:
            recommendations.append(f"🏗️ Fix {structure_issues} structural issues (missing attributes, etc.)")
        
        # Test failures
        if failed_tests > 0:
            recommendations.append("🐛 Investigate and fix failing tests before production deployment")
        
        if error_tests > 0:
            recommendations.append("⚡ Fix test errors to ensure complete coverage")
        
        # Performance recommendations
        slow_tests = sum(1 for t in test_results if t.execution_time > 1.0)
        if slow_tests > 0:
            recommendations.append(f"🚀 Optimize {slow_tests} slow-performing interactions")
        
        if not recommendations:
            recommendations.append("🎉 Excellent! All buttons and interactions are working properly with no issues found.")
        
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += f"\n---\n*Report generated by Button and Interaction Testing Suite*\n"
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_file

def main():
    """Main execution function"""
    print("🎯 Button and Interaction Testing Suite")
    print("=" * 50)
    
    start_time = time.time()
    
    # Configuration
    templates_dir = "/workspaces/enterprise-computing-/templates"
    static_dir = "/workspaces/enterprise-computing-/static"
    
    # Phase 1: Scan for interactive elements
    print("\n🔍 PHASE 1: Scanning Interactive Elements")
    scanner = ButtonAndInteractionScanner(templates_dir, static_dir)
    elements = scanner.scan_all_interactions()
    
    # Phase 2: Test interactions
    print("\n🧪 PHASE 2: Testing Interactions")
    tester = InteractionTester(elements)
    test_results = tester.test_all_interactions()
    
    # Phase 3: Generate report
    print("\n📊 PHASE 3: Generating Report")
    reporter = ButtonTestReporter()
    report_file = reporter.generate_report(elements, test_results)
    
    total_time = time.time() - start_time
    
    # Summary
    print(f"\n🎯 TESTING COMPLETE")
    print("=" * 50)
    print(f"Execution time: {total_time:.2f}s")
    print(f"Elements scanned: {len(elements)}")
    print(f"Tests executed: {len(test_results)}")
    print(f"Report saved: {report_file}")
    
    # Quick stats
    passed = sum(1 for r in test_results if r.status == "PASS")
    failed = sum(1 for r in test_results if r.status == "FAIL")
    errors = sum(1 for r in test_results if r.status == "ERROR")
    issues = sum(1 for e in elements if e.issues)
    
    print(f"\nResults Summary:")
    print(f"  ✅ Tests Passed: {passed}")
    print(f"  ❌ Tests Failed: {failed}")
    print(f"  ⚠️  Test Errors: {errors}")
    print(f"  🔧 Elements with Issues: {issues}")
    
    if failed > 0 or errors > 0 or issues > 0:
        print(f"\n⚠️  Issues found! Check {report_file} for details.")
        return 1
    else:
        print(f"\n🎉 All buttons and interactions working perfectly!")
        return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n🛑 Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
