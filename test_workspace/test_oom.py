#!/usr/bin/env python3
"""Test OOM killer by allocating memory in large chunks."""

import sys

print("Testing OOM killer...")
print("Attempting to allocate 6GB in one large chunk...")
print("Expected: Process should be killed by OOM killer")
print()

try:
    # Try to allocate 6GB all at once
    size_bytes = 6 * 1024 * 1024 * 1024
    print(f"Allocating {size_bytes:,} bytes (6GB)...")

    data = bytearray(size_bytes)

    # Touch the memory to ensure it's actually allocated
    print("Writing to allocated memory...")
    for i in range(0, len(data), 1024 * 1024 * 1024):  # Every GB
        data[i] = 1
        print(f"  Touched byte at {i:,}")

    print("❌ PROBLEM: Successfully allocated 6GB!")
    sys.exit(1)

except MemoryError as e:
    print(f"✅ MemoryError caught: {e}")
    sys.exit(0)
except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
    sys.exit(1)
