"""
This file check not unexected code run 
"""

import re

def Validator(code: str) -> tuple[bool, str]:
    dangerous_patterns = [
        r'import\s+os', r'import\s+subprocess', r'import\s+sys',
        r'__import__', r'eval\(', r'exec\(', r'open\(',
        r'file\(', r'input\(', r'raw_input\('
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return False, f"Potentially unsafe code detected: {pattern}"
    
    return True, "Code appears safe"