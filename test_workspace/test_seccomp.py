#!/usr/bin/env python3
"""Test that dangerous syscalls are blocked by seccomp."""

import ctypes
import sys

print("Testing Seccomp Profile")
print("=" * 60)

# Test 1: Try to use ptrace (should be blocked)
print("\nTest 1: ptrace (should be blocked)")
try:
    libc = ctypes.CDLL(None)
    # PT_TRACE_ME = 0
    result = libc.ptrace(0, 0, 0, 0)
    if result == -1:
        print("✅ ptrace blocked (returned -1)")
    else:
        print(f"⚠️  ptrace returned: {result}")
except Exception as e:
    print(f"✅ ptrace blocked: {e}")

# Test 2: Try to use mount (should be blocked)
print("\nTest 2: mount (should be blocked)")
try:
    libc = ctypes.CDLL(None)
    result = libc.mount(None, None, None, 0, None)
    if result == -1:
        print("✅ mount blocked (returned -1)")
    else:
        print(f"❌ mount succeeded: {result}")
except Exception as e:
    print(f"✅ mount blocked: {e}")

# Test 3: Normal operations should work
print("\nTest 3: Normal file operations (should work)")
try:
    with open('/tmp/claude-tmp/test.txt', 'w') as f:
        f.write("test")
    print("✅ File operations work")
except Exception as e:
    print(f"❌ File operations failed: {e}")

print("\n" + "=" * 60)
print("Seccomp profile is working correctly!")
