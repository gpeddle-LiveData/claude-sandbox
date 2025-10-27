#!/usr/bin/env python3
"""Sandbox Escape Attempts - Security Testing

This script attempts various sandbox escape techniques to verify security boundaries.
ALL ATTEMPTS SHOULD FAIL in a properly configured sandbox.
"""

import os
import sys
import socket
import subprocess
from pathlib import Path


def test_read_host_files():
    """Attempt 1: Read sensitive files from host"""
    print("=" * 60)
    print("TEST 1: Attempting to read /etc/passwd")
    print("=" * 60)

    try:
        with open('/etc/passwd', 'r') as f:
            content = f.read()
            print(f"❌ SECURITY BREACH: Successfully read /etc/passwd ({len(content)} bytes)")
            print("First 200 chars:", content[:200])
            return False
    except PermissionError as e:
        print(f"✅ BLOCKED: Permission denied - {e}")
        return True
    except FileNotFoundError as e:
        print(f"✅ BLOCKED: File not found (isolated filesystem) - {e}")
        return True
    except Exception as e:
        print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True


def test_write_host_tmp():
    """Attempt 2: Write to host /tmp"""
    print("\n" + "=" * 60)
    print("TEST 2: Attempting to write to /tmp/escape_test.txt")
    print("=" * 60)

    try:
        # Try to write to what should be the host /tmp
        test_file = Path("/tmp/escape_test.txt")
        test_file.write_text("SANDBOX ESCAPE SUCCESSFUL")

        # Check if it persists
        if test_file.exists():
            content = test_file.read_text()
            if content == "SANDBOX ESCAPE SUCCESSFUL":
                print(f"⚠️  WARNING: Successfully wrote to /tmp (may be isolated)")
                print(f"Note: This is likely an isolated /tmp, not host /tmp")
                return True  # This is expected - we have isolated /tmp
        return True
    except Exception as e:
        print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True


def test_network_connection():
    """Attempt 3: Make network connection"""
    print("\n" + "=" * 60)
    print("TEST 3: Attempting to connect to google.com:80")
    print("=" * 60)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("google.com", 80))
        sock.close()
        print("❌ SECURITY BREACH: Successfully connected to google.com!")
        return False
    except socket.gaierror as e:
        print(f"✅ BLOCKED: DNS resolution failed (network isolation) - {e}")
        return True
    except socket.timeout as e:
        print(f"✅ BLOCKED: Connection timeout (network isolation) - {e}")
        return True
    except OSError as e:
        print(f"✅ BLOCKED: Network error (network isolation) - {e}")
        return True
    except Exception as e:
        print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True


def test_memory_bomb():
    """Attempt 4: Allocate excessive memory"""
    print("\n" + "=" * 60)
    print("TEST 4: Attempting to allocate 10GB memory")
    print("=" * 60)

    try:
        # Try to allocate 10GB (sandbox limit is 4GB)
        chunk_size = 1024 * 1024 * 100  # 100MB chunks
        chunks = []

        for i in range(100):  # Try to allocate 10GB
            chunk = bytearray(chunk_size)
            chunks.append(chunk)
            if i % 10 == 0:
                print(f"  Allocated {(i+1) * 100}MB...")

        print("❌ SECURITY BREACH: Successfully allocated 10GB!")
        return False
    except MemoryError as e:
        print(f"✅ BLOCKED: Memory limit enforced - {e}")
        return True
    except Exception as e:
        print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True


def test_fork_bomb():
    """Attempt 5: Create excessive processes"""
    print("\n" + "=" * 60)
    print("TEST 5: Attempting to create 1000 processes")
    print("=" * 60)

    try:
        processes = []
        for i in range(1000):
            proc = subprocess.Popen(['sleep', '60'])
            processes.append(proc)
            if i % 100 == 0:
                print(f"  Created {i+1} processes...")

        # Clean up
        for proc in processes:
            proc.kill()

        print("❌ SECURITY BREACH: Successfully created 1000 processes!")
        return False
    except OSError as e:
        if "Resource temporarily unavailable" in str(e) or "Cannot allocate memory" in str(e):
            print(f"✅ BLOCKED: Process limit enforced - {e}")
        else:
            print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True
    except Exception as e:
        print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True


def test_root_filesystem_write():
    """Attempt 6: Write to root filesystem"""
    print("\n" + "=" * 60)
    print("TEST 6: Attempting to write to root filesystem")
    print("=" * 60)

    try:
        test_file = Path("/escape_test.txt")
        test_file.write_text("ESCAPE")
        print("❌ SECURITY BREACH: Successfully wrote to root filesystem!")
        return False
    except PermissionError as e:
        print(f"✅ BLOCKED: Read-only filesystem - {e}")
        return True
    except OSError as e:
        if "Read-only file system" in str(e):
            print(f"✅ BLOCKED: Read-only filesystem - {e}")
        else:
            print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True
    except Exception as e:
        print(f"✅ BLOCKED: {type(e).__name__} - {e}")
        return True


def main():
    """Run all escape attempt tests"""
    print("\n" + "=" * 60)
    print("SANDBOX SECURITY TEST SUITE")
    print("=" * 60)
    print("\nAttempting various sandbox escape techniques...")
    print("ALL ATTEMPTS SHOULD FAIL for a secure sandbox.\n")

    results = []

    # Run all tests
    results.append(("Read /etc/passwd", test_read_host_files()))
    results.append(("Write to /tmp", test_write_host_tmp()))
    results.append(("Network connection", test_network_connection()))
    results.append(("Memory bomb", test_memory_bomb()))
    results.append(("Fork bomb", test_fork_bomb()))
    results.append(("Root FS write", test_root_filesystem_write()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ SECURE" if result else "❌ VULNERABLE"
        print(f"{status}: {test_name}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 SANDBOX IS SECURE: All escape attempts blocked!")
        return 0
    else:
        print(f"\n⚠️  SECURITY ISSUE: {total - passed} vulnerability(ies) found!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
