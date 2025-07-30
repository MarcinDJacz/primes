from project_root.primes.coordinator import PrimeCoordinator
import pytest
import os


@pytest.fixture(scope="session")
def sieve():
    MySieve = PrimeCoordinator()
    return MySieve

@pytest.fixture(scope="session")
def cleanup_files_session():
    created_files = []
    yield created_files
    print(f"Deleting files {len(created_files)}...")
    for f in created_files:
        if os.path.exists(f):
            os.remove(f)
