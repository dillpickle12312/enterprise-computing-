#!/usr/bin/env python3
"""
Simple test to isolate the Year 7-9 roll call validation issue
"""
import re

def validate_roll_call_backend(roll_call):
    """Backend validation (from app.py)"""
    if not roll_call or len(roll_call.strip()) < 2:
        return False

    roll_call = roll_call.strip().upper()
    
    # Pattern 1: Years 10-12 with class numbers (10/1, 11/2, 12/7)
    pattern1 = r'^1[0-2]\/[1-9]$'
    
    # Pattern 2: Years 7-9 with single letter (7A, 8B, 9C)
    pattern2 = r'^[7-9][A-Z]$'
    
    # Pattern 3: Subject codes (12ENG1, 11MAT2, 10SCI3)
    pattern3 = r'^1[0-2][A-Z]{2,4}[1-9]$'
    
    return bool(re.match(pattern1, roll_call) or 
                re.match(pattern2, roll_call) or 
                re.match(pattern3, roll_call))

def validate_roll_call_frontend_html(roll_call):
    """Frontend HTML pattern validation"""
    # From add_mentee.html: pattern="(1[0-2]\/[1-9]|[7-9][A-Z]|1[0-2][A-Z]{2,4}[1-9])"
    pattern = r'^(1[0-2]\/[1-9]|[7-9][A-Z]|1[0-2][A-Z]{2,4}[1-9])$'
    return bool(re.match(pattern, roll_call.strip().upper()))

def validate_roll_call_frontend_js(roll_call):
    """Frontend JavaScript validation"""
    # From add_mentee.html: /^(1[0-2]\/[1-9]|[7-9][A-Z]|1[0-2][A-Z]{2,4}[1-9])$/
    pattern = r'^(1[0-2]\/[1-9]|[7-9][A-Z]|1[0-2][A-Z]{2,4}[1-9])$'
    return bool(re.match(pattern, roll_call.strip().upper()))

print("🔍 TESTING YEAR 7-9 VALIDATION ACROSS ALL LAYERS")
print("=" * 60)

# Test cases that user reported as not working
test_cases = [
    "7A",
    "8B", 
    "9C",
    "7a",    # lowercase
    "8b",    # lowercase
    "9c",    # lowercase
    " 7A ",  # with spaces
    " 8B ",  # with spaces
    " 9C ",  # with spaces
]

print(f"{'Test Case':<10} | {'Backend':<8} | {'HTML':<8} | {'JavaScript':<10} | {'Status'}")
print("-" * 60)

all_pass = True
for case in test_cases:
    backend = validate_roll_call_backend(case)
    html = validate_roll_call_frontend_html(case)
    js = validate_roll_call_frontend_js(case)
    
    status = "✅ PASS" if (backend and html and js) else "❌ FAIL"
    if not (backend and html and js):
        all_pass = False
    
    print(f"'{case}':<10} | {str(backend):<8} | {str(html):<8} | {str(js):<10} | {status}")

print("\n" + "=" * 60)
if all_pass:
    print("🎉 ALL YEAR 7-9 VALIDATIONS ARE WORKING CORRECTLY!")
else:
    print("❌ SOME VALIDATIONS ARE FAILING - NEEDS INVESTIGATION")

# Test Years 10-12 for comparison
print(f"\n🔍 TESTING YEAR 10-12 VALIDATION (for comparison)")
print("-" * 60)

year_10_12_cases = ["10/1", "11/2", "12/7", " 12/7 "]

print(f"{'Test Case':<10} | {'Backend':<8} | {'HTML':<8} | {'JavaScript':<10} | {'Status'}")
print("-" * 60)

for case in year_10_12_cases:
    backend = validate_roll_call_backend(case)
    html = validate_roll_call_frontend_html(case)
    js = validate_roll_call_frontend_js(case)
    
    status = "✅ PASS" if (backend and html and js) else "❌ FAIL"
    
    print(f"'{case}':<10} | {str(backend):<8} | {str(html):<8} | {str(js):<10} | {status}")

print(f"\n📋 REGEX PATTERNS COMPARISON:")
print("Backend Pattern 2 (7-9): ^[7-9][A-Z]$")
print("Frontend Pattern:        ^(1[0-2]\\/[1-9]|[7-9][A-Z]|1[0-2][A-Z]{2,4}[1-9])$")
print("\n🌐 To test on Render: Try entering '7A', '8B', '9C' in the mentee form")
