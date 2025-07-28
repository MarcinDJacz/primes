import os
import wmi
import platform
from datetime import datetime
from dotenv import load_dotenv


def generate_timestamp_filename(prefix: str, ext: str = "txt", folder: str = "results") -> str:
    """
    Generate a filename with timestamp.
    Example: benchmark_something_2025-07-21_15-42-00.txt
    """
    load_dotenv()
    machine = os.getenv("MACHINE", "UNKNOWN")

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}_{machine}_{now}.{ext}"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)

def header():
    c = wmi.WMI()
    cpu_name = c.Win32_Processor()[0].Name.strip()
    os_name = platform.system() + " " + platform.release()
    header = f"CPU: {cpu_name}, OS: {os_name}\n"
    print(header)
    return header
