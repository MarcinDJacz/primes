from primes.main import Sieve
import pytest
import os


@pytest.fixture(scope="session")
def sieve():
    MySieve = Sieve()
    return MySieve

@pytest.fixture(scope="session")
def cleanup_files_session():
    created_files = []
    yield created_files
    print("Deleting files...")
    for f in created_files:
        if os.path.exists(f):
            os.remove(f)
