import random
import pytest
import os
from primes.utils import bit_file_to_array_of_primes, is_prime


'''
use: pytest -n auto
'''
@pytest.fixture()
def primes_from_file():
    def _loader(file_number: int):
        return bit_file_to_array_of_primes(file_number)
    return _loader

@pytest.mark.parametrize("file_number", [1, 2, 3, 4, 5])
def test_file_has_only_primes_00_1_percent_check(file_number: int, primes_from_file):
    data = bit_file_to_array_of_primes(file_number)
    size = len(data) - 1
    division_factor = size // 10_000 # 0.01 %
    print(f"numbers of primes checking: {division_factor} / {size}")
    results = [is_prime(data[random.randint(1, size)]) for _ in range(division_factor)]
    results.extend([is_prime(data[x]) for x in range(5)])
    results.extend([is_prime(data[-x]) for x in range(1, 5)])
    assert all(results) == True

# 5 passed in 28.66s
# 5 passed in 10.70s - pytest tests/ -n auto

@pytest.mark.parametrize("file_number", [100, 1000])
def test_big_file_has_only_primes_00_1_percent_check(file_number: int, primes_from_file, sieve):
    data = bit_file_to_array_of_primes(file_number)
    size = len(data) - 1
    division_factor = size // 10_000 # 0.01 %
    print(f"numbers of primes checking: {division_factor} / {size}")
    results = [sieve.check_prime_optimiz(data[random.randint(1, size)]) for _ in range(division_factor)]
    results.extend([sieve.check_prime_optimiz(data[x]) for x in range(5)])
    results.extend([sieve.check_prime_optimiz(data[-x]) for x in range(1, 5)])
    assert all(results) == True


def test_create_and_check_distant_file(sieve, cleanup_files_session):
    file_number = 199_999_000
    sieve.create_file(file_number)
    file_name = f"bits_file{file_number}.bin"
    data = bit_file_to_array_of_primes(file_number)

    assert os.path.exists(file_name)
    results = []
    results.extend([sieve.check_prime_optimiz(data[x]) for x in range(5)])
    results.extend([sieve.check_prime_optimiz(data[-x]) for x in range(1, 5)])
    assert all(results) == True

    # cleanup
    cleanup_files_session.append(file_name)