import datetime
import math
import bisect
import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from primes.prime_calculator import SieveCalculation
from primes.file_manager import SieveFileManager
from primes.utils import timed
from multiprocessing import Pool


class PrimeCoordinator:
    def __init__(self, length_per_file: int = 100_000_000):
        self.LEN = length_per_file
        self.file_manager = SieveFileManager(length_per_file)
        self.calculator = SieveCalculation(length_per_file)
        self.full_primes = []
        try:
            self.full_primes = self.file_manager.bit_file_to_array_of_primes(1)
        except FileNotFoundError:
            print("No basic file. Generating...")
            initial_data = self.calculator.generate_initial_data()
            self.file_manager.save(1, initial_data)
            self.full_primes = self.file_manager.bit_file_to_array_of_primes(1)
            print("Basic file created and loaded correctly.")
        finally:
            print(f"File nr1 loaded and added to primes. Last prime is: {self.full_primes[-1]}")


        #print(self.full_primes[:20])
        #self.actual_range, self.max_file = self.calculator.max_range()
        print(f"{len(self.full_primes)} primes loaded.")
        print("Last prime number: ", self.full_primes[-1])
        #self.calculator.primes = self.full_primes[:27832]
    def get_max_range_from_file(self, file_number: int) -> tuple[int, str, str]:
        """
        Retrieve prime numbers from the specified file and calculate the maximum
        file range along with additional info based on those primes.

        :param file_number: The number of the file to read primes from.
        :return: A tuple containing:
            - the maximum file number that can be generated (int),
            - the order of magnitude of the maximum range (str),
            - a human-readable string describing the estimated disk space usage (str).
        """
        primes = self.file_manager.bit_file_to_array_of_primes(file_number)
        return self.calculator.get_max_range_from_primes(primes)

    def load_primes_from_files(self, start_file: int, end_file: int):
        """
        Loads prime numbers from bit files in the range [start_file, end_file)
        and extends the internal prime list with them.

        :param start_file: Starting file number (inclusive)
        :param end_file: Ending file number (exclusive)
        """
        for file_number in range(start_file, end_file):
            self.full_primes.extend(self.file_manager.bit_file_to_array_of_primes(file_number))
            print(f"File nr {file_number} loaded")
        print("Last prime number: ", self.full_primes[-1])
        #self.calculator.max_range()

    def trim_primes_for_file(self, max_file_number: int):
        limit = int(math.sqrt((max_file_number + 1) * self.LEN))
        cutoff_index = bisect.bisect_right(self.calculator.primes, limit)
        self.calculator.primes = self.calculator.primes[:cutoff_index]

    @timed
    def create_files(self, start_file, end_file: int):
        max_number = (end_file + 1) * self.LEN * 2
        limit = int(pow(max_number, 1/2)) + 1
        index_limit = bisect.bisect_right(self.full_primes, limit)
        self.calculator.primes = self.full_primes[:index_limit]
        #self.calculator.primes = self.full_primes
        print(f"Primes cut to {len(self.calculator.primes)} primes.")
        #single thread
        for file in range(start_file, end_file + 1):
            data = self.calculator.create_file(file)
            self.file_manager.save(file, data)

    def compute_file(self, file_number, primes_snapshot):
        local_calculator = SieveCalculation(self.LEN)
        local_calculator.primes = primes_snapshot.copy()
        data = self.calculator.create_file(file_number)
        return file_number, data

    @timed
    def create_files_parallel(self, start_file, end_file):
        files = list(range(start_file, end_file + 1))
        primes_snapshot = self.full_primes  # lub ograniczona lista

        # with multiprocessing.Pool() as pool:
        #     # przekazujemy jako krotki argumentów file_number i primes_snapshot
        #     args = [(file, primes_snapshot) for file in files]
        #     results = pool.starmap(self.create_file_parallel, args)
        file_numbers = range(start_file, end_file + 1)
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(self.compute_file, file_numbers))

        for file_number, data in results:
            self.file_manager.save(file_number, data)

    @timed
    def compress_file(self, file):
        self.file_manager.compress_file(file)

    @timed
    def decompress_file(self, file):
        self.file_manager.decompress_file(file)
@timed
def aaa():
    tab = []
    for prime in Sieve.calculator.prime_generator_from_bits(bits, 1):
        tab.append(prime)
    return tab

if __name__ == "__main__":
    Sieve = PrimeCoordinator()
    print(Sieve.full_primes[:10])
    bits = Sieve.file_manager.read_bits(1)
    a = Sieve.file_manager.bit_file_to_array_of_primes(1)
    b = aaa()
    print(a==b)
    print(a[:10])
    print(a[-1])
    print(b[:10])
    print(b[-1])

    a= input('koniec')
    # Sieve.create_files(2, 3)


    #Sieve.load_primes_from_files(10, 19)

    #Sieve.create_files(10, 20)
    #Sieve.create_files_parallel(10, 20)

# import os
#
# for x in range(10):
#     start_file = x * 500 + 2
#     end_file = x * 500 + 21
#     Sieve.create_files(start_file, end_file)
#     for file_num in range(start_file, end_file + 1):
#         if file_num == 1:
#             continue
#         file_name = f"bits_file{file_num}.bin"  # dostosuj do faktycznej nazwy pliku
#         try:
#             os.remove(file_name)
#             #print(f"Deleted {file_name}")
#         except FileNotFoundError:
#             print(f"{file_name} not found, skipping delete.")
