import platform
import time
import os
import sys

def get_uptime_seconds():
    system = platform.system()
    try:
        if system == "Linux":
            with open('/proc/uptime', 'r') as f:
                return float(f.readline().split()[0])
        elif system == "Darwin":
            # macOS: use sysctl kern.boottime
            import subprocess
            output = subprocess.check_output(['sysctl', '-n', 'kern.boottime'], text=True)
            import re
            m = re.search(r'sec = (\d+)', output)
            if m:
                boot_time = int(m.group(1))
                return time.time() - boot_time
        elif system == "Windows":
            import ctypes
            import ctypes.wintypes
            class Uptime(ctypes.Structure):
                _fields_ = [("IdleTime", ctypes.wintypes.LARGE_INTEGER),
                            ("KernelTime", ctypes.wintypes.LARGE_INTEGER),
                            ("UserTime", ctypes.wintypes.LARGE_INTEGER)]
            lib = ctypes.windll.kernel32
            GetTickCount64 = getattr(lib, 'GetTickCount64', None)
            if GetTickCount64:
                return GetTickCount64() / 1000.0
            else:
                return lib.GetTickCount() / 1000.0
    except Exception as e:
        print(f"Error retrieving uptime: {e}", file=sys.stderr)
    return None

def format_uptime(seconds):
    if seconds is None:
        return "Uptime could not be determined."
    mins, sec = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    parts = []
    if days > 0: parts.append(f"{days}d")
    if hrs > 0 or days > 0: parts.append(f"{hrs}h")
    if mins > 0 or hrs > 0 or days > 0: parts.append(f"{mins}m")
    parts.append(f"{sec}s")
    return " ".join(parts)

def print_system_uptime():
    uptime = get_uptime_seconds()
    print("System uptime:", format_uptime(uptime))

if __name__ == "__main__":
    print_system_uptime()
