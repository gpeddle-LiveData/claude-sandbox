#!/usr/bin/env python3
"""Test memory limits with incremental allocation and immediate writing."""

import sys
import gc

print("Incremental Memory Test with Immediate Write")
print("=" * 60)
print("Allocating memory in 256MB chunks, writing immediately")
print("Expected limit: 4GB")
print("=" * 60)
print()

chunks = []
chunk_size_mb = 256
total_mb = 0

try:
    for i in range(30):  # Try up to 7.5GB
        print(f"\nChunk {i+1}: Allocating {chunk_size_mb}MB...", end=" ", flush=True)

        # Allocate chunk
        chunk = bytearray(chunk_size_mb * 1024 * 1024)

        # IMMEDIATELY write to it to force actual allocation
        print("writing...", end=" ", flush=True)
        for j in range(0, len(chunk), 1024 * 1024):  # Every MB
            chunk[j] = (j % 256)

        chunks.append(chunk)
        total_mb += chunk_size_mb

        print(f"✓ Total: {total_mb}MB ({total_mb/1024:.2f}GB)")

        # Force garbage collection
        gc.collect()

        if total_mb > 4096:
            print(f"\n⚠️  WARNING: Exceeded 4GB limit! Currently at {total_mb}MB")

except MemoryError as e:
    print(f"\n\n✅ MemoryError at {total_mb}MB")
    print(f"   Limit enforced at approximately {total_mb/1024:.2f}GB")
    sys.exit(0)
except KeyboardInterrupt:
    print(f"\n\n⏸️  Interrupted at {total_mb}MB")
    sys.exit(1)
except Exception as e:
    print(f"\n\n❌ Unexpected error at {total_mb}MB: {type(e).__name__}: {e}")
    sys.exit(1)

print(f"\n\n❌ PROBLEM: Successfully allocated {total_mb}MB ({total_mb/1024:.2f}GB)")
print("Memory limit not properly enforced!")
sys.exit(1)
