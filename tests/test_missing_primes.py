import pytest
import random
import os
import datetime


def test_no_missing_primes_between_files(sieve, cleanup_files_session):
    sieve.create_one_file(2)
    sieve.create_one_file(3)
    data_1 = sieve.file_manager.bit_file_to_array_of_primes(2)
    data_2 = sieve.file_manager.bit_file_to_array_of_primes(3)

    start_number = data_1[-1] + 2
    end_number = data_2[0] + 2

    missing_primes = [x for x in range(start_number, end_number)
                      if sieve.calculator.is_prime_basic(x)]
    if missing_primes:
        print(missing_primes)

    cleanup_files_session.append("bits_file2.bin")
    cleanup_files_session.append("bits_file3.bin")

    assert len(missing_primes) == 0

def test_only_primes_all_numbers_in_file(sieve):
    data = sieve.file_manager.bit_file_to_array_of_primes(2)
    test = [sieve.calculator.is_prime_optimized(data[random.randint(0, len(data) - 1)])
    for _ in range(len(data) - 1)]
    # estimate 18 minutes
    test.extend([sieve.calculator.is_prime_optimized(data[x]) for x in range(5)])
    test.extend([sieve.calculator.is_prime_optimized(data[-x]) for x in range(1, 6)])
    assert all(test) == True

def test_not_missing_files_inside(sieve):
    data = sieve.file_manager.bit_file_to_array_of_primes(2)
    results = [sieve.calculator.is_prime_basic(x) for x in range(data[0],data[0] + 1_000_000, 2) if x not in data]
    #estimate 6h - all
    # fits 100_000 - 15s
    assert all(results) == False
