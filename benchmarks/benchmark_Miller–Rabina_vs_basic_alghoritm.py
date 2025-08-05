import time
import os
from project_root.benchmarks.utils import generate_timestamp_filename
from project_root.primes.coordinator import PrimeCoordinator


def benchmark_Miller_Rabin_vs_basic_algorithms(rang: int, number: int):
    sieve = PrimeCoordinator()
    sieve.create_one_file(number)
    data = sieve.file_manager.bit_file_to_array_of_primes(number)
    #basic
    t1 = time.time()
    results_1 = [sieve.calculator.is_prime_basic(data[x]) for x in range(rang)]
    t2 = time.time()
    results_2 = [sieve.calculator.is_prime_optimized(data[x]) for x in range(rang)]
    t3 = time.time()
    results_3 = [sieve.calculator.is_prime_miller_rabin(x) for x in range(rang)]
    t4 = time.time()
    text = f"Results for checking {rang} primes in file number: {number}.\n"
    text += f"  {'Basic algorithm:':35}{t2-t1:.3f} s\n"
    text += f"  {'Optimized algorithm:':35}{t3-t2:.3f} s\n"
    text += f"  {'Miller-Rabin algorithm:':35}{t4-t3:.3f} s\n"
    text += f"  {'results_2=results_1:':35}{results_2==results_1} \n"
    text += f"  {'results_2=results_3:':35}{results_2==results_3} \n"

    filename = generate_timestamp_filename("benchmark_Miller_Rabin_vs_basic_algorithms")
    with open(filename, "w") as f:
        f.write(text)

    file = f"bits_file{number}.bin"
    os.remove(file)


if __name__ == "__main__":
    #benchmark_Miller_Rabin_vs_basic_algorithms(100_000, 10)
    benchmark_Miller_Rabin_vs_basic_algorithms(1_000, 100_000)