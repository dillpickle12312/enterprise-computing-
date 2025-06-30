#!/usr/bin/env python3
"""
Standalone validation utilities for testing without Flask dependencies.
This module contains validation functions that can be imported independently.
"""

import re

def validate_roll_call(roll_call):
    """
    Validate roll call format based on the Enterprise Mentorship System requirements.
    
    Supported formats:
    1. Years 10-12: 10/1, 11/2, 12/7 (Year/Class format)
    2. Years 7-9: 7A, 8B, 9C (YearLetter format)
    3. Subject codes: 12ENG1, 11MAT2, 10SCI3 (YearSubjectNumber format)
    
    Args:
        roll_call (str): The roll call string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not roll_call or not isinstance(roll_call, str):
        return False
    
    # Convert to uppercase and strip whitespace
    roll_call = roll_call.strip().upper()
    
    # Pattern 1: Years 10-12 with class numbers (10/1, 11/2, 12/7)
    pattern1 = r'^1[0-2]\/[1-9]$'
    
    # Pattern 2: Years 7-9 with single letter (7A, 8B, 9C)
    pattern2 = r'^[7-9][A-Z]$'
    
    # Pattern 3: Subject codes (12ENG1, 11MAT2, 10SCI3)
    pattern3 = r'^1[0-2][A-Z]{2,4}[1-9]$'
    
    return (re.match(pattern1, roll_call) or 
            re.match(pattern2, roll_call) or 
            re.match(pattern3, roll_call)) is not None

def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid phone format, False otherwise
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's all digits and appropriate length
    return cleaned.isdigit() and 8 <= len(cleaned) <= 15

def validate_name(name):
    """
    Validate name format.
    
    Args:
        name (str): Name to validate
        
    Returns:
        bool: True if valid name, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    # Name should contain only letters, spaces, hyphens, apostrophes
    # and be between 2 and 50 characters
    pattern = r"^[a-zA-Z\s\-']{2,50}$"
    return re.match(pattern, name.strip()) is not None

# Test functions for validation
def test_roll_call_validation():
    """Test the roll call validation with comprehensive test cases."""
    test_cases = [
        # Valid formats - Years 10-12 with class numbers
        ('10/1', True, 'Year 10 class 1'),
        ('11/2', True, 'Year 11 class 2'),
        ('12/7', True, 'Year 12 class 7'),
        ('12/9', True, 'Year 12 class 9'),
        
        # Valid formats - Years 7-9 with letters
        ('7A', True, 'Year 7 class A'),
        ('8B', True, 'Year 8 class B'),
        ('9C', True, 'Year 9 class C'),
        ('9Z', True, 'Year 9 class Z'),
        
        # Valid formats - Subject codes
        ('10ENG1', True, 'Year 10 English 1'),
        ('11MAT2', True, 'Year 11 Math 2'),
        ('12SCI3', True, 'Year 12 Science 3'),
        ('12HIST1', True, 'Year 12 History 1'),
        ('10CHEM9', True, 'Year 10 Chemistry 9'),
        ('12PHYS4', True, 'Year 12 Physics 4'),
        
        # Invalid formats
        ('13/1', False, 'Invalid year (too high)'),
        ('6A', False, 'Invalid year (too low)'),
        ('12/0', False, 'Invalid class (zero)'),
        ('11/', False, 'Incomplete format'),
        ('AB12', False, 'Invalid format'),
        ('', False, 'Empty string'),
        ('12ENG0', False, 'Invalid class (zero)'),
        ('12ENG', False, 'Missing class number'),
        ('12A', False, 'Invalid Year 12 format'),
        ('10B', False, 'Invalid Year 10 format'),
        ('9/1', False, 'Invalid format for year 9'),
        ('7/1', False, 'Invalid format for year 7'),
        ('12eng1', False, 'Lowercase subject code'),
        ('121ENG1', False, 'Invalid year format'),
        ('12E1', False, 'Subject code too short'),
        ('12ENGLISH1', False, 'Subject code too long'),
    ]
    
    all_passed = True
    for roll_call, expected, description in test_cases:
        result = validate_roll_call(roll_call)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} Roll call '{roll_call}' ({description}) - Expected: {expected}, Got: {result}")
    
    return all_passed

if __name__ == "__main__":
    print("Testing roll call validation...")
    test_roll_call_validation()
