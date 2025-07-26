import pytest
import os


@pytest.mark.parametrize("file_number", [11, 12, 13, 14, 15])
def test_created_files_exists(file_number, cleanup_files_session, sieve):
    sieve.create_file(file_number)
    file_name = f"bits_file{file_number}.bin"
    cleanup_files_session.append(file_name)
    assert os.path.exists(file_name)
# 14.12s w singlu
# 23.10s w multi