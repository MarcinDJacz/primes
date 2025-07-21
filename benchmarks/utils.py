from datetime import datetime
import os


def generate_timestamp_filename(prefix: str, ext: str = "txt", folder: str = "results") -> str:
    """
    Generate a filename with timestamp.
    Example: benchmark_something_2025-07-21_15-42-00.txt
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}_{now}.{ext}"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)