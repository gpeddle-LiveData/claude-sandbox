# gVisor Installation Guide

## Overview

gVisor provides VM-level security with container-level performance by intercepting all syscalls before they reach the host kernel.

## Platform Support

### Linux (Native Docker)

**Recommended:** Full gVisor support with excellent performance.

```bash
# Install gVisor
curl -fsSL https://gvisor.dev/archive.key | sudo gpg --dearmor -o /usr/share/keyrings/gvisor-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gvisor-archive-keyring.gpg] https://storage.googleapis.com/gvisor/releases release main" | sudo tee /etc/apt/sources.list.d/gvisor.list > /dev/null

sudo apt-get update
sudo apt-get install -y runsc

# Configure Docker
sudo runsc install
sudo systemctl restart docker

# Verify
docker run --rm --runtime=runsc hello-world
```

### macOS (Docker Desktop)

**Status:** Limited support - gVisor doesn't work directly with Docker Desktop on macOS due to the VM layer.

**Alternatives:**
1. Use Linux VM with native Docker (best gVisor support)
2. Use enhanced security features documented below
3. Accept runc with defense-in-depth approach

**Why it doesn't work:**
- Docker Desktop on macOS runs containers inside a Linux VM
- gVisor needs direct access to the host kernel
- The VM layer prevents proper gVisor integration

### Windows (Docker Desktop)

**Status:** Similar limitations to macOS - Docker Desktop uses WSL2 or Hyper-V VM.

**Alternatives:**
1. Use WSL2 with native Docker (better gVisor support)
2. Use enhanced security features documented below

## Alternative Security Measures (macOS/Windows)

When gVisor isn't available, use these defense-in-depth measures:

### 1. Seccomp Profiles

Create `seccomp-profile.json`:

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "accept", "accept4", "access", "arch_prctl", "bind", "brk",
        "capget", "capset", "chdir", "chmod", "chown", "chroot",
        "clock_getres", "clock_gettime", "clone", "close", "connect",
        "dup", "dup2", "dup3", "epoll_create", "epoll_create1",
        "epoll_ctl", "epoll_pwait", "epoll_wait", "execve", "exit",
        "exit_group", "fchdir", "fchmod", "fchmodat", "fchown",
        "fchownat", "fcntl", "fdatasync", "flock", "fork", "fstat",
        "fstatfs", "fsync", "ftruncate", "futex", "getcwd", "getdents",
        "getdents64", "getegid", "geteuid", "getgid", "getgroups",
        "getpeername", "getpgrp", "getpid", "getppid", "getpriority",
        "getrandom", "getresgid", "getresuid", "getrlimit", "getrusage",
        "getsid", "getsockname", "getsockopt", "gettid", "gettimeofday",
        "getuid", "getxattr", "ioctl", "kill", "lchown", "lgetxattr",
        "link", "linkat", "listen", "llistxattr", "lseek", "lstat",
        "madvise", "memfd_create", "mkdir", "mkdirat", "mknod",
        "mknodat", "mlock", "mlock2", "mlockall", "mmap", "mprotect",
        "mremap", "msync", "munlock", "munlockall", "munmap", "nanosleep",
        "newfstatat", "open", "openat", "pause", "pipe", "pipe2",
        "poll", "ppoll", "prctl", "pread64", "preadv", "preadv2",
        "prlimit64", "pselect6", "pwrite64", "pwritev", "pwritev2",
        "read", "readlink", "readlinkat", "readv", "recvfrom",
        "recvmmsg", "recvmsg", "rename", "renameat", "renameat2",
        "restart_syscall", "rmdir", "rt_sigaction", "rt_sigpending",
        "rt_sigprocmask", "rt_sigqueueinfo", "rt_sigreturn",
        "rt_sigsuspend", "rt_sigtimedwait", "rt_tgsigqueueinfo",
        "sched_getaffinity", "sched_setaffinity", "sched_yield",
        "select", "sendfile", "sendmmsg", "sendmsg", "sendto",
        "set_robust_list", "set_tid_address", "setgid", "setgroups",
        "setitimer", "setpgid", "setpriority", "setresgid", "setresuid",
        "setrlimit", "setsid", "setsockopt", "setuid", "shutdown",
        "sigaltstack", "socket", "socketpair", "stat", "statfs",
        "symlink", "symlinkat", "sync", "sync_file_range", "sysinfo",
        "tgkill", "time", "timer_create", "timer_delete",
        "timer_getoverrun", "timer_gettime", "timer_settime",
        "timerfd_create", "timerfd_gettime", "timerfd_settime",
        "times", "tkill", "truncate", "umask", "uname", "unlink",
        "unlinkat", "utime", "utimensat", "utimes", "vfork", "wait4",
        "waitid", "write", "writev"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

Usage:
```bash
docker run --security-opt seccomp=seccomp-profile.json ...
```

### 2. AppArmor Profile (Linux only)

Create `/etc/apparmor.d/docker-claude-sandbox`:

```
profile docker-claude-sandbox flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny access to host filesystem
  deny /proc/sys/** rw,
  deny /sys/kernel/security/** rw,

  # Allow container filesystem
  /workspace/** rw,
  /tmp/claude-tmp/** rw,

  # Deny network
  deny network,
}
```

### 3. Capability Dropping

Add to run-sandbox.sh:
```bash
--cap-drop=ALL \
--cap-add=CHOWN \
--cap-add=DAC_OVERRIDE \
--cap-add=SETGID \
--cap-add=SETUID \
```

### 4. No New Privileges

Add to run-sandbox.sh:
```bash
--security-opt=no-new-privileges:true
```

## Testing Security

Run Project 4.4 (Escape Attempts) to verify security:

```bash
./run-sandbox.sh sample-projects/4-complex/4.4-escape-attempts/workspace python3 escape_tests.py
```

All escape attempts should fail.

## Performance Impact

- **runc (default):** Baseline performance
- **runc + seccomp:** ~2-5% overhead
- **gVisor:** ~10-20% overhead (but much better security)

## Recommendations

**Production Linux:** Use gVisor + seccomp + AppArmor (defense-in-depth)
**Development macOS/Windows:** Use runc + seccomp + capability dropping
**High Security:** Consider Linux host with full gVisor support

## References

- [gVisor Documentation](https://gvisor.dev/docs/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Seccomp Profiles](https://docs.docker.com/engine/security/seccomp/)
