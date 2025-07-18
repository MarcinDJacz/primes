import datetime
import inspect
import itertools
import math
import random
import threading
import time
from multiprocessing import Array, Pool, Process
from multiprocessing.pool import ThreadPool

from bitarray import bitarray

'''
Przerob to na 3 osobne klasy:
sieve(koordynator)
SieveCalculation (obliczenia)
SieveFileMenager ( odczyt i zapis plikow, generowanie ( bez obliczen))
metody testujace przenies do testow
'''



from primes.utils import (
    bit_file_to_array_of_primes,
    how_much_bin_files_in_directory,
    is_prime,
    more_legible,
    order_of_magnitude,
    read_bits
)



def timed(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        res = func(*args, **kwargs)
        end = datetime.datetime.now()
        print(f"{func.__name__} "
              f"ran for {end - start} ns")
        return res
    return wrapper

class Sieve():
    # global timed
    """
    1 file created in aproximatly 0.17s(from 16s earlier) with size 11,9 MB (110Mb earlier)
    """
    def __init__(self, part=1):
        self.primes = []
        #self.limes = []
        self.file_name = 'bits_file'#
        self.LEN = 100_000_000
        self.files_number = 0
        # does basic bits_file1.bin exist, if doesn't - create
        try:
            self.primes.extend(bit_file_to_array_of_primes(1, self.LEN))
            self.files_number += 1
        except:
            print("No basic file. Generating...")
            self.generate_initial_file()
            print("Basic file loaded correctly.")
            self.primes.extend(bit_file_to_array_of_primes(1, self.LEN))
            self.files_number += 1
        finally:
            print(f"File nr1 loaded and added to primes. Last prime is: {self.primes[-1]}")
        #self.primes = self.primes[:10000]
        self.max_range()
        print(f"{len(self.primes)} primes loaded.")
        print("Last prime number: ", self.primes[-1])
        #files, files_in_order = how_much_bin_files_in_directory()
        '''
        self.sqrts = []
        for x in range(100):  # potencial files
            self.sqrts.append(pow(int((x * self.LEN * 2) + self.LEN * 2), 1 / 2))
        x = 0
        for prime in self.primes:
            if x == len(self.sqrts) - 1:
                break
            if prime > self.sqrts[x]:
                self.limes.append(self.primes.index(prime))
                    x += 1
        '''
    # 1000000000000000199999999 #kwadrylion


    # def max_range(self): #jaki maksymalny nr pliku mozna wygenerowac z liczb aktualnie wczytanych
    #     act_range = self.primes[-1] ** 2
    #     max_file = act_range // 200_000_000 - 1
    #     print(f'Maximum range: {more_legible(act_range)} -> {order_of_magnitude(act_range)} ')
    #     print(f'__ Maximum file number possible to create is: {max_file}')
    @timed
    def find_max_in_range(self, x_start):  # DO CALKOWITEJ POPRAWY
        file_number = 1
        if len(self.primes) > 22157872:
            print(f'Cuttig primes to range in file1')
            self.primes = self.primes[0:22157871]
        else:
            print('Counting')

        last_element = (x_start - 1) * (self.LEN)
        square_range = math.floor(math.sqrt((last_element * 2) + (self.LEN * 2)) + 1)

        temp_tab = (self.LEN) * bitarray('0')
        primes_counter = 0
        how_much_primes_in_file = len(self.primes)

        find_tag_number = self.primes[primes_counter]
        # FIND AND TAG
        while find_tag_number <= square_range:

            # missing elements on beginning
            missing = (last_element - ((find_tag_number - 1) // 2)) % find_tag_number
            if missing == 0:
                index = 0
                temp_tab[0] = 1
            index = find_tag_number - missing
            try:
                temp_tab[index] = 1
            except IndexError:
                pass

            temp_tab[index: self.LEN: find_tag_number] = 1
            primes_counter += 1

            if primes_counter == how_much_primes_in_file:  # OutOfRange
                file_number += 1
                print(f'Resetting primes and load next file ({file_number})')
                self.primes = []

                how_much_primes_in_file = len(self.primes)
                primes_counter = 0

            find_tag_number = self.primes[primes_counter]

        # FINDING PRIMES FROM ASHES
        number = 0

        for x in range(self.LEN - 1, 0, -1):
            if temp_tab[x] == 0:
                number = last_element * 2 + (x * 2) + 1
                print(
                    f'The biggest prime in this range is {more_legible(number)} ({order_of_magnitude(number)})  found in {(time2 - time1)}')
                print('Checking, if is prime number')

                file = open('The_biggests.txt', 'a')
                file.write(
                    "The biggest prime in range: " + str(more_legible((x_start - 1) * self.LEN * 2)) + " to " + str(
                        more_legible(x_start * self.LEN * 2)) + " is " + str(more_legible(number)) + " -> " + str(
                        order_of_magnitude(number)) + ". Found in " + str(time2 - time1) + '\n')
                file.close()
                return number


    # def get_max_range_from(self, file_number): #jaki maksymalny nr pliku mozna wygenerowac z liczb DO podanego pliku wlacznie
    #     try:
    #         temp = bit_file_to_array_of_primes(str(file_number))
    #     except:
    #         print('This file doesnt exist. Creating...')
    #         self.create_file(file_number)
    #         temp = bit_file_to_array_of_primes(str(file_number))
    #     finally:
    #         pass
    #
    #     max_file = int(temp[-1] ** 2 / self.LEN / 2)
    #     max_file_text = 'Max file number: ' + str(more_legible(max_file))
    #     size = "Size of all files: " + str(int(12_200 * max_file / 1024 / 1024)) + " GB"
    #     return temp[-1], more_legible(temp[-1] ** 2), order_of_magnitude(temp[-1] ** 2), max_file_text, size

    # @timed
    # def generate_initial_file(self): #calculation
    #
    #     temp_tab = (self.LEN) * bitarray('0')
    #     temp_tab[:1] = 1
    #     index = 2
    #
    #     square_range = math.ceil(math.sqrt(self.LEN * 2)) + 1
    #     while index < square_range:
    #         act_number = index * 2 - 1  # id 2 = 3, id 3 = 5, ...
    #         if temp_tab[index] == 0:
    #             self.primes.append(act_number)
    #             cross_out_index = index + act_number  # 2 + 3 = 5 -> [0,1,3,5,7,(9),11
    #             temp_tab[cross_out_index: self.LEN: act_number] = 1
    #         index += 1
    #
    #     temp_tab = temp_tab[:self.LEN]
    #
    #     file_name = self.file_name + '1.bin'
    #     with open(file_name, 'wb') as fh:
    #         temp_tab.tofile(fh)
    #self.random_test_one_file(1)

    def add_to_primes_data(self, from_x, to_y): #menager
        for x in range(from_x, to_y):
            self.primes.extend(bit_file_to_array_of_primes(x, self.LEN))
            x += 1
            print(f'File nr {x - 1} loaded')
        self.max_range()

    @timed
    def generate_files_single_thread(self, from_x, to_y):#menager i rozdzial
        x_times = to_y - from_x
        for x in range(from_x, to_y):
            (MySieve.create_file(x))


    @timed
    def generate_files_threaded(self, from_x, to_y):  # doesn't work yet - menager
        files = [n for n in range(from_x, to_y)]
        with ThreadPool(12) as pool:
            wyn = pool.map(self.create_file, (files))
        return wyn

    @timed
    def generate_files_multiprocessing(self, from_x, to_y): # doesn't work yet menager
        x_times = to_y - from_x

        pliki = [n for n in range(from_x, to_y)]
        with Pool(10) as pool:
            wyn = pool.starmap(self.create_file, product(pliki))

    def create_file(self, file_number, info=False): #file menager rozdzial obliczen
        # for tests:
        logs = []
        time1 = datetime.datetime.now()

        number_of_primes = 0
        potencial_big_prime = file_number * self.LEN
        last_element = (file_number - 1) * (self.LEN)

        square_range = math.floor(math.sqrt(file_number * 2 * self.LEN)) + 1  # ???

        temp_tab = (self.LEN + self.primes[-1]) * bitarray('0')  # min size of bitarrey = LEN , + last prime

        primes_counter = 0
        find_tag_number = self.primes[primes_counter]


        # FIND AND TAG

        while find_tag_number <= square_range:
            # missing elements on beginning
            missing = (last_element - ((find_tag_number - 1) // 2)) % find_tag_number
            if missing == 0:
                index = 0
                temp_tab[0] = 1
            else:
                index = find_tag_number - missing
            temp_tab[index] = 1#?
            temp_tab[index: self.LEN: find_tag_number] = 1  # cala wykreslanka
            primes_counter += 1
            find_tag_number = self.primes[primes_counter]  # REFERENCE TO self.primes - multi !

        # SAVING BIT FILES
        temp_tab = temp_tab[:self.LEN]
        file_name = self.file_name + str(file_number) + '.bin'

        ### !!! niech funkcja zwraca tablice, a beda one zapisywane w osobnej metodzie / osobnym wątku
        self.save_file(file_name, temp_tab)
        '''t = threading.Thread(target = self.save_file, args=(file_name, temp_tab))
        t.start()
        t.join()
        '''
        time2 = datetime.datetime.now()
        if info:
            print(f'File number: {file_number} created in {(time2 - time1)}')
        self.files_number += 1
        return logs

    def save_file(self, file_name: str, temp_tab) -> None: #filemenager
        with open(file_name, 'wb') as fh:
            temp_tab.tofile(fh)

    def check_prime_optimiz(self, number):
        if self.primes[-1] ** 2 > number:
            if number == 2 or number == 3:
                return True
            elif number % 2 == 0:
                return False
            else:
                square = int(number ** (1 / 2))
                x = 1
                actual_number = self.primes[x]
                while actual_number < square:
                    if number % self.primes[x] == 0:
                        return False
                    x += 1
                    actual_number = self.primes[x]
                return True
        else:
            print('More primes in data needed.')


if __name__ == "__main__":
    # met = [name for name, func in inspect.getmembers(Sieve, predicate=inspect.isfunction)]
    # print(met)
    # a=input()

    MySieve = Sieve()
    #MySieve.random_test_one_file(1)
    #MySieve.create_file(1000)
    # MySieve.generate_files_single_thread(2, 6)
    #MySieve.add_to_primes_data(2, 3)
    #print(MySieve.primes[-1])
    #MySieve.generate_files_multiprocessing(2,12)

