#!/usr/bin/env python3
"""Check cgroup memory settings inside container."""

import os
from pathlib import Path

print("Checking cgroup memory configuration...")
print("=" * 60)

# Check cgroup version
cgroup_v1_path = Path("/sys/fs/cgroup/memory/memory.limit_in_bytes")
cgroup_v2_path = Path("/sys/fs/cgroup/memory.max")

if cgroup_v1_path.exists():
    print("Cgroup version: v1")
    limit = cgroup_v1_path.read_text().strip()
    limit_bytes = int(limit)
    limit_gb = limit_bytes / (1024**3)
    print(f"Memory limit: {limit} bytes ({limit_gb:.2f} GB)")
elif cgroup_v2_path.exists():
    print("Cgroup version: v2")
    limit = cgroup_v2_path.read_text().strip()
    if limit == "max":
        print(f"Memory limit: {limit} (unlimited)")
    else:
        limit_bytes = int(limit)
        limit_gb = limit_bytes / (1024**3)
        print(f"Memory limit: {limit} bytes ({limit_gb:.2f} GB)")
else:
    print("❌ Cannot find cgroup memory settings")
    print("Checking alternative locations...")

    # Try other common paths
    paths = [
        "/sys/fs/cgroup/memory.max",
        "/sys/fs/cgroup/memory.limit_in_bytes",
        "/proc/self/cgroup",
    ]

    for path_str in paths:
        path = Path(path_str)
        if path.exists():
            print(f"\n✓ Found: {path_str}")
            try:
                content = path.read_text()
                print(f"  Content: {content[:200]}")
            except Exception as e:
                print(f"  Error reading: {e}")

print("\n" + "=" * 60)
print("Checking /proc/meminfo...")
print("=" * 60)

meminfo = Path("/proc/meminfo")
if meminfo.exists():
    lines = meminfo.read_text().split('\n')[:5]
    for line in lines:
        print(line)
