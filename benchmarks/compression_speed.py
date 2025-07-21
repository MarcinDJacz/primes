import time
import os
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

from primes.benchmarks.utils import generate_timestamp_filename
from primes.file_manager import SieveFileManager
from primes.coordinator import PrimeCoordinator


def compress_wrapper(file: str):
    return SieveFileManager.compress_file(file)

def benchmark_compression_single(files_paths: list[str]) -> tuple[str, float]:
    start = time.time()
    for file in files_paths:
        SieveFileManager.compress_file(file)
    end = time.time()
    elapsed = end - start
    size_original = os.path.getsize(files_paths[0]) / (1024 * 1024)
    size_compressed = os.path.getsize(files_paths[0] + '.gz') / (1024 * 1024)
    result = f"Compression of {len(files_paths)} files.\n"
    result += f"   {'Single compression time:':35}{elapsed:.3f} s\n"
    result += f"   {'Original size of first file:':35}{size_original:.2f} MB\n"
    result += f"   {'Compressed size of first file:':35}{size_compressed:.2f} MB\n"
    result += f"   {'Compression ratio:':35}{(size_compressed / size_original):.2f}\n"

    print(result)
    return result, elapsed

def benchmark_compression_parallel(files_paths: list[str]) -> [str, float]:
    start = time.time()
    with ProcessPoolExecutor() as executor:
        list(executor.map(SieveFileManager.compress_file, files_paths))
    end = time.time()
    elapsed = end - start
    result = f"   {'Parallel compression time:':35}{elapsed:.3f} s.\n"
    print(result)
    return result, elapsed

if __name__ == "__main__":
    # initial data
    coordinator = PrimeCoordinator()
    coordinator.create_files(2, 12)

    test_files = [f"bits_file{x}.bin" for x in range(2, 13)]

    print("Benchmark single file compression:")
    test1, single_time = benchmark_compression_single(test_files)

    print("\nBenchmark parallel file compression:")
    test2, parallel_time = benchmark_compression_parallel(test_files)
    ratio = parallel_time / single_time
    percent_faster = (1 - ratio) * 100

    #filename = datetime.now().strftime("benchmark_%Y-%m-%d_%H-%M-%S.txt")
    filename = generate_timestamp_filename("benchmark_compression_speed")
    with open(filename, "w") as f:
        f.write(f"{test1}\n{test2}")
        f.write(f"   {'Parallel/Single ratio:':35}{ratio:.3f}\n")
        f.write(f"   About {percent_faster:.2f}% faster.")

    for file in test_files:
        if "file1." not in file:
            os.remove(file)
        os.remove(f"{file}.gz")

    print("End of benchmark.")

