import psutil
import os
import time
from datetime import datetime
from project_root.primes.coordinator import PrimeCoordinator
from utils import generate_timestamp_filename, header


header = header()
process = psutil.Process(os.getpid())

def get_mem_usage_mb():
    return process.memory_info().rss / (1024 * 1024)  # in MB

def benchmark_size_of_memory_and_time(Sieve) -> str:
    result = ""

    size1 = get_mem_usage_mb()
    t1 = time.time()
    primes_list = Sieve.file_manager.bit_file_to_array_of_primes(1)
    t2 = time.time()
    size2 = get_mem_usage_mb()
    list_duration = t2 - t1
    list_memory = size2 - size1

    result += f"[List load]\n"
    result += f"   Time: {list_duration:.3f} s\n"
    result += f"   Memory used: {list_memory:.2f} MB\n\n"

    # Clear memory
    primes_list = []

    size3 = get_mem_usage_mb()
    t3 = time.time()
    bits = Sieve.file_manager.read_bits(1)
    for _ in Sieve.calculator.prime_generator_from_bits(bits, 1):
        pass
    t4 = time.time()
    size4 = get_mem_usage_mb()
    gen_duration = t4 - t3
    gen_memory = size4 - size3

    result += f"[Generator traversal]\n"
    result += f"   Time: {gen_duration:.3f} s\n"
    result += f"   Memory used: {gen_memory:.2f} MB\n\n"

    # Time and memory savings
    time_diff = list_duration - gen_duration
    memory_diff = list_memory - gen_memory

    time_ratio = (gen_duration / list_duration) if list_duration else 0
    memory_ratio = (gen_memory / list_memory) if list_memory else 0

    result += "[Comparison]\n"
    result += f"   Generator is {100 * (1 - time_ratio):.2f}% faster\n" if list_duration else ""
    result += f"   Generator uses {100 * (1 - memory_ratio):.2f}% less memory\n" if list_memory else ""

    result += f"\nRaw differences:\n"
    result += f"   Time saved: {time_diff:.3f} s\n"
    result += f"   Memory saved: {memory_diff:.2f} MB\n"

    return result


if __name__ == '__main__':
    Sieve = PrimeCoordinator()
    benchmark_result = benchmark_size_of_memory_and_time(Sieve)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("results", exist_ok=True)
    #filename = f"results/benchmark_load_data_vs_generator_{now}.txt"
    filename = generate_timestamp_filename("benchmark_load_data_vs_generator")
    with open(filename, "w") as f:
        f.write(header)
        f.write(benchmark_result)

    print(f"Benchmark results saved to: {filename}")
