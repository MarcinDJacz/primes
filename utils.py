import datetime
import bitarray
import random
from multiprocessing import Pool
import zipfile

LEN = 100_000_000  # 111546435#


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


def bit_file_to_array_of_primes(nr=1, dlugosc=LEN, base_name="bits_file"):
    file_name = base_name + str(nr) + '.bin'
    tab = []
    # time1 = datetime.datetime.now()
    a = bitarray.bitarray()
    with open(file_name, 'rb') as fh:
        a.fromfile(fh)
        # x = int(file_name[9:-4]) - 1
    x = nr - 1
    x = x * 2 * dlugosc  #

    # only for file nr 1
    if nr == 1:
        temp = -1
    else:
        temp = 1

    for z in range(len(a)):
        if a[z] == 0:  # is prime
            tab.append((x + 2 * z + temp))  #

    # time2 = datetime.datetime.now()
    # print(' in: ', (time2-time1))
    if nr == 1:
        return (tab[1:])  # delete "1"
    return tab


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


def zip_file(file_number):  # add optional delete original file + unziping function

    compression = zipfile.ZIP_DEFLATED
    file_name1 = 'zip_bits_file' + str(file_number) + '.zip'

    zf = zipfile.ZipFile(file_name1, mode='w')
    file_name = 'bits_file' + str(file_number) + '.bin'
    try:
        zf.write(file_name, compress_type=compression)
    finally:
        zf.close()


def unzip_file(file_number):
    pass
