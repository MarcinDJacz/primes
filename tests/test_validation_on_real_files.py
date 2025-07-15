import random
import pytest

from primes.utils import bit_file_to_array_of_primes, is_prime
from primes.main import Sieve


'''
use: pytest tests/ -n auto
'''


@pytest.fixture(scope="module")
def sieve():
    MySieve = Sieve()
    return MySieve


@pytest.fixture()
def primes_from_file():
    def _loader(file_number: int):
        return bit_file_to_array_of_primes(file_number)
    return _loader


@pytest.mark.parametrize("file_number", [1, 2, 3, 4, 5])
def test_file_has_only_primes_1_percent_check(file_number: int, primes_from_file):
    data = bit_file_to_array_of_primes(file_number)
    size = len(data) - 1
    print(f"numbers of primes checking: {size//10000}")
    for number in range(size//10000): # 0.01 %
        random_index = random.randint(1, size)
    results = [is_prime(data[random.randint(1, size)]) for _ in range(size//100)]
    results.extend([is_prime(data[x]) for x in range(5)])
    results.extend([is_prime(data[-x]) for x in range(1, 5)])
    assert all(results) == True

#5 passed in 328.16s (0:05:28)
#5 passed in 70.04s (0:01:10) pytest tests/ -n auto
