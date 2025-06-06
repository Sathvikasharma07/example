import os
import platform
import subprocess

def print_system_uptime():
    """
    Prints the system uptime in a human-readable format.
    """
    system = platform.system()
    if system == "Windows":
        # Use 'net stats srv' and parse output
        try:
            output = subprocess.check_output("net stats srv", shell=True, text=True)
            for line in output.splitlines():
                if "Statistics since" in line:
                    print(f"System uptime: {line}")
                    break
        except Exception as e:
            print(f"Failed to get uptime on Windows: {e}")
    elif system == "Linux":
        # Use /proc/uptime
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                seconds = int(uptime_seconds % 60)
                print(f"System uptime: {hours}h {minutes}m {seconds}s")
        except Exception as e:
            print(f"Failed to get uptime on Linux: {e}")
    elif system == "Darwin":
        # Use 'uptime' command
        try:
            output = subprocess.check_output("uptime", shell=True, text=True)
            print(f"System uptime: {output.strip()}")
        except Exception as e:
            print(f"Failed to get uptime on macOS: {e}")
    else:
        print(f"Unsupported OS: {system}")

if __name__ == "__main__":
    print_system_uptime()
