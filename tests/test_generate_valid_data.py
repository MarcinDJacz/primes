import pytest
import random
import os
import datetime


@pytest.mark.parametrize("file_number", [3, 6, 21])
def test_generate_valid_data_with_generator(file_number: int, sieve):
    data_with_classic_method = sieve.calculator.create_file(file_number)

    data = sieve.file_manager.read_bits(1)
    data_with_generator = sieve.calculator.create_file_generator(file_number, data)

    assert data_with_classic_method == data_with_generator

@pytest.mark.parametrize("file_number", [2, 5, 20])
def test_generate_valid_data(file_number: int, sieve, cleanup_files_session):
    sieve.create_one_file(file_number)
    file_name = f"bits_file{file_number}.bin"
    data = sieve.file_manager.bit_file_to_array_of_primes(file_number)
    size = len(data) - 1
    division_factor = size // 100_000  # 0.001 %
    print(f"numbers of primes checking: {division_factor} / {size}")

    results = [sieve.calculator.is_prime_basic(data[random.randint(1, size)]) for _ in range(division_factor)]
    results.extend([sieve.calculator.is_prime_basic(data[x]) for x in range(5)])
    results.extend([sieve.calculator.is_prime_basic(data[-x]) for x in range(1, 5)])
    assert all(results) == True

    cleanup_files_session.append(file_name)

def test_create_and_check_distant_file(cleanup_files_session, sieve):
    file_number = 199_999_000
    sieve.create_one_file(file_number)
    data = sieve.file_manager.bit_file_to_array_of_primes(file_number)
    file_name = f"bits_file{file_number}.bin"
    assert os.path.exists(file_name)

    results = []
    results.extend([sieve.calculator.is_prime_basic(data[x]) for x in range(5)])
    results.extend([sieve.calculator.is_prime_basic(data[-x]) for x in range(1, 5)])
    assert all(results) == True

    cleanup_files_session.append(file_name)

@pytest.mark.parametrize("file_number", [100, 150_000_000])
def test_optimized_method_faster_than_basic_method(file_number: int, cleanup_files_session, sieve):
    #file_number = 150_000_000
    sieve.create_one_file(file_number)
    file_name = f"bits_file{file_number}.bin"
    data = sieve.file_manager.bit_file_to_array_of_primes(file_number)
    t1 = datetime.datetime.now()
    results_basic = [sieve.calculator.is_prime_basic(data[x]) for x in range(5)]
    t2 = datetime.datetime.now()
    results_optimized = [sieve.calculator.is_prime_optimized(data[x]) for x in range(5)]
    t3 = datetime.datetime.now()
    assert results_optimized == results_basic
    assert (t3 - t2) < (t2 - t1)
    print(f"optimized: {t3 - t2}, basic: {t2 - t1}")
    cleanup_files_session.append(file_name)
