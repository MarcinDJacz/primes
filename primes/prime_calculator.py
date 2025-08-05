import math
import datetime
from bitarray import bitarray
from typing import Generator
from .utils import more_legible, order_of_magnitude
from sympy.ntheory.primetest import mr

class SieveCalculation:
    def __init__(self, length_per_file: int, primes: list[int] = None):
        self.LEN = length_per_file
        self.primes = primes or []


    def is_prime_basic(self, number) -> bool:
        """
        standard method for checking prime numbers
        :param number: the number being checked to see
         if it is a prime number
        :return: True if number is a prime number
        """
        sq = int(number ** (1 / 2))
        if number % 2 == 0:
            return False
        for x in range(3, sq, 2):
            if number % x == 0:
                return False
        return True

    def is_prime_optimized(self, number) -> bool:
        """
        better method for checking prime numbers
        :param number: the number being checked to see
         if it is a prime number
        :return: True if number is a prime number
        """
        if number == 2 or number == 3:
            return True
        if number < 2 or number % 2 == 0:
            return False

        if self.primes[-1] ** 2 > number:
            square = int(number ** 0.5)
            for prime in self.primes:
                if prime > square:
                    break
                if number % prime == 0:
                    return False
            return True
        else:
            print('More primes in data needed.')

    def is_prime_miller_rabin(self, number: int) -> bool:
        """
            Perform a Miller-Rabin primality test to check if a number is probably prime.

            Parameters:
                n (int): The number to test for primality.
                witnesses (list[int], optional): List of bases (witnesses) to test against.
                    If None, a default set of bases will be used to achieve high accuracy.

            Returns:
                bool: True if `n` is probably prime, False if `n` is definitely composite.

            Notes:
                - Miller-Rabin is a probabilistic primality test. It can falsely identify
                  some composite numbers as prime (false positives), but the chance of error
                  decreases exponentially with the number of chosen witnesses.
                - Selecting a proper set of witnesses can make the test deterministic
                  for numbers smaller than certain bounds.
                - For cryptographic or production use, consider running additional
                  deterministic tests or using libraries like `sympy` for 100% accuracy.
        """
        return mr(number, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def max_range(self) -> tuple[int, int]:
        """
        :return: tuple: maximum range and file number that can be generated
        from the loaded prime numbers
        """
        act_range = self.primes[-1] ** 2
        max_file = (act_range // 200_000_000) - 1
        print(f'Maximum range: {more_legible(act_range)} '
              f'-> {order_of_magnitude(act_range)} ')
        print(f'__ Maximum file number possible to create is:'
              f' {max_file}')
        return act_range, max_file

    def get_max_range_from_primes(self, primes: list[int]) -> tuple[int, str, str]:
        """
        Calculates the maximum file number and disk usage based on
         given primes.

        :param primes: List of primes (last prime used for max range)
        :return: Tuple of (max file number, magnitude, disk usage)
        """
        max_file = int(primes[-1] ** 2 / self.LEN / 2)
        disk_space = f"Size of all files: {int(12_200 * max_file / 1024 / 1024)} GB"
        return max_file, order_of_magnitude(primes[-1] ** 2), disk_space

    def generate_initial_data(self) -> bitarray:
        """
        Generates a bitarray representing prime numbers using the Sieve of Eratosthenes
        optimized for odd numbers only. This forms the initial dataset for the first file
        in the sequence.

        The resulting bitarray is of length `self.LEN`, representing numbers from 0 to 2 * LEN,
        where only odd numbers are considered to reduce memory usage and improve performance.
        The value at each index corresponds to whether the associated number is composite (1) or prime (0).

        This method also populates `self.primes` with the list of discovered prime numbers
        during the sieving process.

        Note: This method does not handle file saving — it only returns the computed bitarray.

        :return: A bitarray where 0 represents a prime number and 1 a composite number.
        """

        temp_tab = (self.LEN) * bitarray('0')
        temp_tab[:1] = 1
        index = 2

        square_range = math.ceil(math.sqrt(self.LEN * 2)) + 1
        while index < square_range:
            act_number = index * 2 - 1  # id 2 = 3, id 3 = 5, ...
            if temp_tab[index] == 0:
                self.primes.append(act_number)
                cross_out_index = index + act_number  # 2 + 3 = 5 -> [0,1,3,5,7,(9),11...]
                temp_tab[cross_out_index: self.LEN: act_number] = 1
            index += 1

        temp_tab = temp_tab[:self.LEN]
        return temp_tab

    def create_file(self, file_number) -> bitarray:
        """
            Creates a bitarray where prime numbers are marked as 1 and saves it to a binary file.
            Parameters:
                file_number (int): The identifier used in the generated file's name.
            Returns:
                bitarray: A bitarray with bits set to 1 for prime indices and 0 otherwise.
        """
        last_element = (file_number - 1) * (self.LEN)
        square_range = math.floor(math.sqrt(file_number * 2 * self.LEN)) + 1

        temp_tab = (self.LEN + self.primes[-1]) * bitarray('0')  # min size of bitarrey = LEN , + last prime
        if file_number == 1:
            temp_tab[0] = 1

        primes_counter = 0
        find_tag_number = self.primes[primes_counter]

        # FIND AND TAG
        while find_tag_number <= square_range:
            # missing elements on beginning
            missing = (last_element - ((find_tag_number - 1) // 2)) % find_tag_number
            if missing == 0:
                index = find_tag_number
            else:
                index = find_tag_number - missing

            temp_tab[index: self.LEN: find_tag_number] = 1  # all magic
            primes_counter += 1
            find_tag_number = self.primes[primes_counter]

        temp_tab = temp_tab[:self.LEN]
        return temp_tab

    def create_file_generator(self, file_number, data: bitarray) -> bitarray:
        """
           Creates a bitarray based on a generator, where prime numbers are marked as 1, and saves it to a binary file.
           Parameters:
               file_number (int): The identifier used in the generated file's name.
               data (bitarray): Input bitarray representing the prime generation source.
           Returns:
               bitarray: A bitarray with bits set to 1 for prime indices, generated from the provided data.
        """
        last_element = (file_number - 1) * (self.LEN)
        square_range = math.floor(math.sqrt(file_number * 2 * self.LEN)) + 1
        temp_tab = (self.LEN + self.primes[-1]) * bitarray('0')  # min size of bitarrey = LEN , + last prime

        if file_number == 1:
            temp_tab[0] = 1

        find_tag_number = 0
        prime_generator = self.prime_generator_from_bits(data, 1)
        # FIND AND TAG
        while find_tag_number <= square_range:
            try:
                find_tag_number = next(prime_generator)
            except StopIteration:
                break
            # missing elements on beginning
            missing = (last_element - ((find_tag_number - 1) // 2)) % find_tag_number
            if missing == 0:
                index = find_tag_number
            else:
                index = find_tag_number - missing
            temp_tab[index] = 1#?
            temp_tab[index: self.LEN: find_tag_number] = 1  # all magic

        temp_tab = temp_tab[:self.LEN]
        return temp_tab

    def prime_generator_from_bits(self, a: bitarray, nr: int) -> Generator[int, None, None]:
        """
            Yields prime numbers represented by bits in the given bitarray.
            Parameters:
                a (bitarray): Bitarray where 0 indicates a prime number at a specific position.
                nr (int): The chunk number used to calculate offset and starting value.
            Yields:
                int: Prime numbers corresponding to unset bits (0) in the bitarray.
        """
        x = (nr - 1) * 2 * self.LEN
        if nr == 1:
            offset = -1
        else:
            offset = 1

        for z, bit in enumerate(a):
            if bit == 0:
                val = x + 2 * z + offset
                if nr == 1 and val == 1:
                    continue
                yield val
