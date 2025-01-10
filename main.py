import math
import datetime
import time
from bitarray import bitarray
from multiprocessing import Pool
from multiprocessing import Process, Array
from defs import is_prime, More_Legible, Order_of_magnitude, Read_Bits, BitFileToArrayOfPrimes, \
    How_much_bin_files_in_directory, Zip_file

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
    global timed
    """
    1 file created in aproximatly 0.17s(from 16s earlier) with size 11,9 MB (110Mb earlier)
    """
    def __init__(self, part=1):
        self.primes = []
        self.limes = []
        self.file_name = 'bits_file'
        self.LEN = 100_000_000
        self.files_number = 0
        # does basic bits_file1.bin exist, if doesn't - create
        try:
            self.primes.extend(BitFileToArrayOfPrimes(1, self.LEN))
            self.files_number += 1
        except:
            print("No basic file. Generating...")
            self.Generate()
            print("Basic file loaded correctly.")
            self.primes.extend(BitFileToArrayOfPrimes(1, self.LEN))
            self.files_number += 1
        finally:
            print(f"File nr1 loaded and added to primes. Last prime is: {self.primes[-1]}")
        self.Max_range()
        print(f"{len(self.primes)} primes loaded.")
        print("Last prime number: ", self.primes[-1])
        files, files_in_order = How_much_bin_files_in_directory()

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

    # 1000000000000000199999999 #kwadrylion

    #@timed
    def Check_is_prime_better(self, number):
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

    def Check_is_prime_very_long_numbers(self, number):
        # initial conditions
        if number == 2 or number == 3:
            return True
        elif number % 2 == 0:
            return False

        aim_file_number = math.ceil((number ** (1 / 2)) / (self.LEN * 2))
        print(f'{aim_file_number} of files needed')
        square = int(number ** (1 / 2))
        for file in range(1, aim_file_number):
            self.primes.clear()
            self.primes.extend(BitFileToArrayOfPrimes(file, self.LEN))
            print(f'File nr {file} loaded')

            for prime in self.primes:
                if number % prime == 0:
                    return False
        # last file
        self.primes.clear()
        self.primes.extend(BitFileToArrayOfPrimes(aim_file_number, self.LEN))
        x = 1
        actual_number = self.primes[x]
        while actual_number < square:
            if number % actual_number == 0:
                return False
            x += 1
            actual_number = self.primes[x]
        return True

    def random_test_files(self, froom, too): #doesnt work yet
        p = Pool(10)
        result = p.map(self.random_test_one_file, range(froom, too))
        p.close()
        for x in result:
            print(x)

    @timed
    def random_test_one_file(self, nr, how_many=100):
        import random
        a = BitFileToArrayOfPrimes(nr)
        for x in range(how_many):
            random_index = random.randint(1, len(a) - 1)
            if self.Check_is_prime_better(a[random_index]) == False:
                print(f'Error in file nr {nr}. Found: {a[random_index]} in file.')
                return a[random_index]
                break
        for x in range(1, 4):
            if self.Check_is_prime_better(a[len(a) - x]) == False or self.Check_is_prime_better(a[x]) == False:
                print(f'Error in file nr {nr}. Found: {a[random_index]} in file.')
                return a[len(a) - x]
                break
        substring = 'File nr ' + str(nr) + ' OK. Last prime number: ' + More_Legible(a[-1])
        return substring

    def Max_range(self):
        act_range = self.primes[-1] ** 2
        print(f'Maximum range: {More_Legible(act_range)} -> {Order_of_magnitude(act_range)} ')
    @timed
    def Find_the_biggest_in_range(self, x_start):  # DO CALKOWITEJ POPRAWY
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
                    f'The biggest prime in this range is {More_Legible(number)} ({Order_of_magnitude(number)})  found in {(time2 - time1)}')
                print('Checking, if is prime number')

                file = open('The_biggests.txt', 'a')
                file.write(
                    "The biggest prime in range: " + str(More_Legible((x_start - 1) * self.LEN * 2)) + " to " + str(
                        More_Legible(x_start * self.LEN * 2)) + " is " + str(More_Legible(number)) + " -> " + str(
                        Order_of_magnitude(number)) + ". Found in " + str(time2 - time1) + '\n')
                file.close()
                return number

    def Max_range_from(self, file_number):
        try:
            temp = BitFileToArrayOfPrimes(str(file_number))
        except:
            print('This file doesnt exist. Creating...')
            self.Create_file(file_number)
            temp = BitFileToArrayOfPrimes(str(file_number))
        finally:
            pass

        max_file = int(temp[-1] ** 2 / self.LEN / 2)
        max_file_text = 'Max file number: ' + str(More_Legible(max_file))
        size = "Size of all files: " + str(int(12_200 * max_file / 1024 / 1024)) + " GB"
        return temp[-1], More_Legible(temp[-1] ** 2), Order_of_magnitude(temp[-1] ** 2), max_file_text, size

    @timed
    def Generate(self):

        temp_tab = (self.LEN) * bitarray('0')
        temp_tab[:1] = 1
        index = 2

        square_range = math.ceil(math.sqrt(self.LEN * 2)) + 1
        while index < square_range:
            act_number = index * 2 - 1  # id 2 = 3, id 3 = 5, ...
            if temp_tab[index] == 0:
                self.primes.append(act_number)
                cross_out_index = index + act_number  # 2 + 3 = 5 -> [0,1,3,5,7,(9),11
                temp_tab[cross_out_index: self.LEN: act_number] = 1
            index += 1

        temp_tab = temp_tab[:self.LEN]

        file_name = self.file_name + '1.bin'
        with open(file_name, 'wb') as fh:
            temp_tab.tofile(fh)
        self.random_test_one_file_basic(1)

    def Add_to_primes(self, from_x, to_y):
        for x in range(from_x, to_y):
            self.primes.extend(BitFileToArrayOfPrimes(x, self.LEN))
            x += 1
            print(f'File nr {x - 1} loaded')
        self.Max_range()

    @timed
    def Make_files_multip_single_mode(self, from_x, to_y):
        x_times = to_y - from_x
        for x in range(from_x, to_y):
            (MySieve.Create_file(x))


    @timed
    def Make_files_multip_thread(self, from_x, to_y):  # doesn't work yet
        from multiprocessing.pool import ThreadPool
        files = [n for n in range(from_x, to_y)]
        with ThreadPool(12) as pool:
            wyn = pool.map(self.Create_file, (files))
        return wyn

    @timed
    def Make_files_multiprocessing(self, from_x, to_y): # doesn't work yet
        x_times = to_y - from_x
        from itertools import product
        pliki = [n for n in range(from_x, to_y)]
        with Pool(12) as pool:
            wyn = pool.starmap(self.Create_file, product(pliki))

    def Create_file(self, file_number, info=False):
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
            temp_tab[index] = 1
            temp_tab[index: self.LEN: find_tag_number] = 1  # cala wykreslanka
            primes_counter += 1
            find_tag_number = self.primes[primes_counter]  # REFERENCE TO self.primes - multi !

        # SAVING BIT FILES
        temp_tab = temp_tab[:self.LEN]
        file_name = self.file_name + str(file_number) + '.bin'

        with open(file_name, 'wb') as fh:  #
            temp_tab.tofile(fh)  #

        time2 = datetime.datetime.now()
        if info:
            print(f'File number: {file_number} created in {(time2 - time1)}')
        self.files_number += 1
        return logs

if __name__ == "__main__":
    MySieve = Sieve()
    MySieve.Make_files_multip_single_mode(2, 12)
    for x in range(1,6):
        print(MySieve.random_test_one_file(x))

