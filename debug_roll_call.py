#!/usr/bin/env python3
"""
Debug script to test roll call validation patterns
"""
import re

def validate_roll_call(roll_call):
    """Validate roll call format for Australian schools"""
    if not roll_call or len(roll_call.strip()) < 2:
        return False

    roll_call = roll_call.strip().upper()
    
    # Pattern 1: Years 10-12 with class numbers (10/1, 11/2, 12/7)
    pattern1 = r'^1[0-2]\/[1-9]$'
    
    # Pattern 2: Years 7-9 with single letter (7A, 8B, 9C)
    pattern2 = r'^[7-9][A-Z]$'
    
    # Pattern 3: Subject codes (12ENG1, 11MAT2, 10SCI3)
    pattern3 = r'^1[0-2][A-Z]{2,4}[1-9]$'
    
    result1 = bool(re.match(pattern1, roll_call))
    result2 = bool(re.match(pattern2, roll_call))
    result3 = bool(re.match(pattern3, roll_call))
    
    print(f"Testing: '{roll_call}'")
    print(f"  Pattern 1 (10-12): {result1}")
    print(f"  Pattern 2 (7-9): {result2}")
    print(f"  Pattern 3 (subject): {result3}")
    print(f"  Final result: {result1 or result2 or result3}")
    print()
    
    return result1 or result2 or result3

# Test cases
test_cases = [
    "7A", "8B", "9C",  # Years 7-9
    "10/1", "11/2", "12/7",  # Years 10-12
    "12ENG1", "11MAT2",  # Subject codes
    "7a", "8b", "9c",  # Lowercase (should work after conversion)
    " 7A ", " 8B ",  # With spaces
    "6A", "13A", "7AA", "10A"  # Invalid cases
]

print("=== Roll Call Validation Test ===")
for test in test_cases:
    validate_roll_call(test)
