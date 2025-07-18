import math
import bisect
from primes.prime_calculator import SieveCalculation
from primes.file_manager import SieveFileManager
from utils import timed

class PrimeCoordinator:
    def __init__(self, length_per_file: int = 100_000_000):
        self.LEN = length_per_file
        self.file_manager = SieveFileManager(length_per_file)
        self.calculator = SieveCalculation(length_per_file)
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
        self.calculator.primes = self.full_primes[:27832]
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
        #print(f"end file: {end_file}")

        #print(f"last prime: {self.full_primes[-1]}")
        limit = int(pow(max_number, 1/2)) + 1
        #print(f"Max number: {limit}")
        index_limit = bisect.bisect_right(self.full_primes, limit)
        #print(f"limit index found in: {index_limit}")
        '''
        20 files (10 -> 19)
        create_files ran for 0:00:15.656483 ns
        create_files ran for 0:00:15.464452 ns  vs
        1.23% difference
  
        20 files (1000 -> 1019)
        create_files ran for 0:00:20.944686 ns  vs
        create_files ran for 0:00:19.047710 ns
        9.06% difference
        
        20 files (10_000 -> 10_019)
        create_files ran for 0:00:21.093284 ns  vs
        create_files ran for 0:00:20.809433 ns
        1.35% difference
        '''
        #self.calculator.primes = self.full_primes[:index_limit]
        #self.calculator.primes = self.full_primes
        print(f"Primes cut to {len(self.calculator.primes)} primes.")
        #print(f"last primes in calc: {self.calculator.primes[-1]}")
        #single thread
        for file in range(start_file, end_file + 1):
            data = self.calculator.create_file(file)
            self.file_manager.save(file, data)

        #print(f"{end_file + 1 - start_file} files created.")


Sieve = PrimeCoordinator()
#Sieve.load_primes_from_files(10, 19)

#Sieve.create_files(5000, 5019)
import os

for x in range(2):
    start_file = x * 500 + 1
    end_file = x * 500 + 20
    Sieve.create_files(start_file, end_file)
    for file_num in range(start_file, end_file + 1):
        if file_num == 1:
            continue
        file_name = f"bits_file{file_num}.bin"  # dostosuj do faktycznej nazwy pliku
        try:
            os.remove(file_name)
            #print(f"Deleted {file_name}")
        except FileNotFoundError:
            print(f"{file_name} not found, skipping delete.")
