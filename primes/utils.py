import datetime
import bitarray
import random
from multiprocessing import Pool
import zipfile
import os


LEN = 100_000_000  # 111546435#

def timed(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        res = func(*args, **kwargs)
        end = datetime.datetime.now()
        print(f"{func.__name__} "
              f"ran for {end - start} ns")
        return res
    return wrapper

def is_prime(p):
    # t1 = datetime.datetime.now()
    sq = int(p ** (1 / 2))
    if p % 2 == 0:
        return False
    for x in range(3, sq, 2):
        if p % x == 0:
            return False
    t2 = datetime.datetime.now()
    # print("Calculate in ", (datetime.datetime.now()-time1))
    return True


def read_bits(nr, base_name="bits_file"):
    file_name = base_name + str(nr) + '.bin'
    a = bitarray.bitarray()
    with open(file_name, 'rb') as fh:
        a.fromfile(fh)
    return a

def more_legible(number):
    real_range = str(number)
    dl = len(real_range) - 3
    while dl > 0:
        real_range = real_range[:dl] + '_' + real_range[dl:]
        dl -= 3
    return real_range


def order_of_magnitude(number):
    str_number = str(number)
    long = len(str_number)
    what = ''
    if long > 30:
        what = 'Quintilions or more!'
    elif long > 27:
        what = 'Quadrilliards'
    elif long > 24:
        what = 'Quadrillions'
    elif long > 21:
        what = 'Trylliards'
    elif long > 18:
        what = 'Tryllions'
    elif long > 15:
        what = 'Billiards'
    elif long > 12:
        what = 'Bilions'
    else:
        what = 'Miliards or less. Weakly...'
    return what


def how_much_bin_files_in_directory():
    files_count = 0
    import os
    files = os.listdir()
    for file in files:
        if file.endswith(".bin"):
            files_count += 1

    # is first file in directory and how much files are in order
    files_in_order_count = 0
    for x in range(1, files_count + 1):
        s = 'bits_file' + str(x) + '.bin'
        if s in files:
            files_in_order_count += 1
        else:
            break

    print(f"Found {files_count} files in main directory, {files_in_order_count} in order.")
    return files_count, files_in_order_count

def print_file_size_mb(file_path):

    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    print(f"Rozmiar pliku '{file_path}': {size_mb:.2f} MB")