#!/usr/bin/env python3
"""
Simple hello world script for sandbox testing.
"""
from datetime import datetime

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hello from the sandbox!")
    print(f"Current timestamp: {timestamp}")

if __name__ == "__main__":
    main()
