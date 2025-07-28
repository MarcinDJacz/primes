import math
import bisect
from concurrent.futures import ProcessPoolExecutor
from primes.prime_calculator import SieveCalculation
from primes.file_manager import SieveFileManager
from primes.utils import timed


class PrimeCoordinator:
    def __init__(self, length_per_file: int = 100_000_000):
        self.LEN = length_per_file
        self.file_manager = SieveFileManager(length_per_file, )
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
        self.calculator.primes = self.full_primes.copy()
        print(f"{len(self.full_primes)} primes loaded.")
        print("Last prime number: ", self.full_primes[-1])

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

    def load_primes_from_files(self, start_file: int, end_file: int) -> None:
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

    def trim_primes_for_file(self, max_file_number: int) -> None:
        """
            Trims the list of primes to include only those necessary for generating
            bit arrays up to the given file number.

            The cutoff is determined as sqrt((max_file_number + 1) * LEN), since primes
            larger than that are not needed for sieving numbers in the given range.
            This helps optimize memory usage during file generation.

            Args:
                max_file_number (int): The highest file number to be generated,
                determining the upper bound for required primes.
        """
        limit = int(math.sqrt((max_file_number + 1) * self.LEN))
        cutoff_index = bisect.bisect_right(self.calculator.primes, limit)
        self.calculator.primes = self.calculator.primes[:cutoff_index]

    def create_one_file(self, file_number: int) -> None:
        """
        Create one specify file.
        :param file_number:
        """
        data = self.calculator.create_file(file_number)
        self.file_manager.save(file_number, data)

    @timed
    def create_files(self, start_file: int, end_file: int) -> None:
        """
        Create range of files, in single-thread.
        :param start_file: first file
        :param end_file: last file
        """
        max_number = (end_file + 1) * self.LEN * 2
        limit = int(pow(max_number, 1/2)) + 1
        index_limit = bisect.bisect_right(self.full_primes, limit)
        self.calculator.primes = self.full_primes[:index_limit]
        print(f"Primes cut to {len(self.calculator.primes)} primes.")
        #single thread
        for file in range(start_file, end_file + 1):
            data = self.calculator.create_file(file)
            self.file_manager.save(file, data)

    # def compute_file(self, file_number, primes_snapshot):
    #     local_calculator = SieveCalculation(self.LEN)
    #     local_calculator.primes = primes_snapshot.copy()
    #     data = self.calculator.create_file(file_number)
    #     return file_number, data
    #
    # @timed
    # def create_files_parallel(self, start_file, end_file):
    #     files = list(range(start_file, end_file + 1))
    #     primes_snapshot = self.full_primes
    #
    #     # with multiprocessing.Pool() as pool:
    #     #     args = [(file, primes_snapshot) for file in files]
    #     #     results = pool.starmap(self.create_file_parallel, args)
    #     file_numbers = range(start_file, end_file + 1)
    #     with ProcessPoolExecutor() as executor:
    #         results = list(executor.map(self.compute_file, file_numbers))
    #
    #     for file_number, data in results:
    #         self.file_manager.save(file_number, data)

    @timed
    def compress_file(self, file: str) -> None:
        self.file_manager.compress_file(file)

    @timed
    def decompress_file(self, file: str) -> None:
        self.file_manager.decompress_file(file)


if __name__ == "__main__":
    Sieve = PrimeCoordinator()
    """
    bechmarks and results       -> benchmakrs directory
    tests                       -> tests directory
    performance observations    -> docs directory
    
    TO DO:
        - create_files_parallel with bigger packages
    """
