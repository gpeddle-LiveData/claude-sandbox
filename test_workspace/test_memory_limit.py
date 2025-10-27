#!/usr/bin/env python3
"""Simple memory allocation test to verify Docker memory limits."""

import sys
import time

def allocate_memory_mb(megabytes):
    """Allocate specified megabytes of memory."""
    print(f"Attempting to allocate {megabytes}MB...")
    try:
        # Allocate and actually use the memory (not just reserve it)
        data = bytearray(megabytes * 1024 * 1024)
        # Write to the memory to ensure it's actually allocated
        for i in range(0, len(data), 1024 * 1024):
            data[i] = 1
        print(f"✅ Successfully allocated {megabytes}MB")
        return data
    except MemoryError as e:
        print(f"❌ MemoryError at {megabytes}MB: {e}")
        raise
    except Exception as e:
        print(f"❌ Error at {megabytes}MB: {type(e).__name__}: {e}")
        raise

def main():
    """Test memory allocation in steps."""
    print("Memory Allocation Test")
    print("=" * 60)
    print("Testing Docker memory limit enforcement...")
    print("Expected limit: 4GB (4096MB)")
    print("=" * 60)
    print()

    allocations = []
    step_size = 500  # Allocate in 500MB chunks

    try:
        for i in range(1, 20):  # Try up to 10GB
            mb = i * step_size
            data = allocate_memory_mb(step_size)
            allocations.append(data)

            total_mb = len(allocations) * step_size
            print(f"  Total allocated: {total_mb}MB ({total_mb/1024:.2f}GB)")

            # If we've exceeded 4GB, this is a problem
            if total_mb > 4096:
                print(f"\n⚠️  WARNING: Allocated {total_mb}MB, exceeding 4GB limit!")

            time.sleep(0.1)  # Brief pause between allocations

    except MemoryError:
        total_mb = len(allocations) * step_size
        print(f"\n✅ Memory limit enforced at {total_mb}MB")
        return 0
    except KeyboardInterrupt:
        print("\n⏸️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

    total_mb = len(allocations) * step_size
    print(f"\n❌ PROBLEM: Successfully allocated {total_mb}MB without hitting limit!")
    print("Memory limits may not be properly enforced.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
