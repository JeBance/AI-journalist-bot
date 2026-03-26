#!/usr/bin/env python3
"""
Quick publish script with automatic Markdown V2 escaping.
"""

import sys
import re
from publisher import publish

def escape_markdown_v2(text):
    """Escape all Markdown V2 special characters."""
    # Order matters: escape backslash first
    special_chars = r'\_ * [ ] ( ) ~ ` > # + - = | { } . !'
    
    # Escape backslash first
    text = text.replace('\\', '\\\\')
    
    # Then escape other special chars
    for char in '_*[]()~`>#+-=|{}.!':
        text = text.replace(char, '\\' + char)
    
    return text

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quick_publish.py \"Your text\"")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    escaped = escape_markdown_v2(text)
    
    print("Escaped text:")
    print("-" * 40)
    print(escaped[:500] + "..." if len(escaped) > 500 else escaped)
    print("-" * 40)
    
    result = publish(escaped)
    
    if result["success"]:
        print(f"\n✅ Published! Message ID: {result['message_id']}")
    else:
        print(f"\n❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
