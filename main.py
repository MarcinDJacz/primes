import math
import datetime
import time
from bitarray import bitarray
from multiprocessing import Pool
from multiprocessing import Process, Array
from defs import is_prime, Read, More_Legible, Order_of_magnitude

class Sieve():
    def __init__(self,part=1):
        self.primes = []
        self.LEN = 100_000_000        
        #does basic file1.txt exist, if doesn't - create
        try:
            self.primes.extend(Read('file1.txt'))            
        except:
            print("No basic file. Generating...")
            self.Generate()
        finally:
            print("Basic file loaded correctly.")
            
        #read other files, if exists
        answ1 = input("Load the remaining number of files? Y/N").upper()
        if answ1 == 'Y':
            try:
                i = 2
                while i < 100:                
                    file_name = 'file' + str(i) + '.txt'
                    self.primes.extend(Read(file_name))                
                    i += 1
            except:
                pass
            finally:
                print(f"{i-1} files loaded.")
                print("No more files to read")
                
                if i < 10:
                    print("At least 10 files recommended. Approximately 1Gb space needed.")
                    answ2 = input('Do you want to create it now? Y/N')
                    if answ2.upper() == 'Y':
                        self.Make_files_multip(i,11)
                        answ3 = input(f"Do you want to add this files to variable Primes now? Y/N")
                        if answ3.upper() == 'Y':
                            self.Add_to_primes(i,11)
        self.Max_range()

    def If_is_prime(self, number = 0, arr = []):
        if number != 0:
            print(is_prime(number))
            return 0
        elif len(arr) > 0:
            for num in arr:
                if is_prime(num) == False:
                    print(num)
            return 0
        
    def Repeat(self,x_times,from_x,to_y):
        difference = to_y - from_x
        for x in range(x_times):
            self.Make_files_multip(from_x, to_y)            
            time.sleep(1)
            from_x = to_y
            to_y += difference
            
    def Max_range(self):
        act_range = self.primes[-1]**2
        print(f'Maximum range: {More_Legible(act_range)} -> {Order_of_magnitude(act_range)} ')
        
    def Generate(self):
        file = open('file1.txt', 'w')
        time1 = datetime.datetime.now()
        
        temp_tab = self.LEN * bitarray('0')
        temp_tab[0]=1#0
        temp_tab[1]=1#1 -after, only odd numbers
        index = 2
        self.primes = [2]
        while index < self.LEN:
            act_number = index * 2 - 1 #id 2 = 3, id 3 = 5, ...
            if temp_tab[index] == 0:
                self.primes.append(act_number) 
                file.write(str(act_number)+' ')
                cross_out_index = index + act_number #2 + 3 = 5 -> [0,1,3,5,7,(9),11
                temp_tab[cross_out_index : self.LEN : act_number] = 1
                '''#the same, but x2 faster than:
                while cross_out_index < self.LEN:
                    temp_tab[cross_out_index] = 1
                    cross_out_index += act_number'''
            index += 1

        file.close()
        time2 = datetime.datetime.now()
        print("Basic file generated in: ", (time2 - time1))
    def Add_to_primes(self,  from_x, to_y):
        for x in range(from_x, to_y):            
                file_name = 'file' + str(x) + '.txt'
                self.primes.extend(Read(file_name))
                x += 1
        self.Max_range()
    def Make_files_multip(self, from_x, to_y):
        x_times = to_y - from_x 

        p = Pool(10)
        time1 = datetime.datetime.now()
        p.map(self.Create_file, range(from_x , to_y))
        p.close()
        time2 = datetime.datetime.now()
        print(f"{(x_times)} files created in: ---{(time2-time1)}---")
        
    def Check_file(self, nr):
        file = 'file' + str(nr) + '.txt'
        temp = Read(file)
        for x in range(len(temp)):
            is_prime(temp[x])
        temp = []
                
    def Create_file(self,file_number):
        time1 = datetime.datetime.now()
        number_of_primes = 0
        file_name = 'file' + str(file_number) + '.txt'
        file = open(file_name, 'w')
        last_element = (file_number-1) *(self.LEN)   
        square_range = math.floor(math.sqrt((last_element*2) + (self.LEN*2)) + 1)
 
        if square_range <= self.LEN:
            temp_tab = (self.LEN) * bitarray('0')# min size of bitarrey = LEN
        else:
            temp_tab = (square_range) * bitarray('0') 

        primes_counter = 0
        find_tag_number = self.primes[primes_counter]
        
        #FIND AND TAG
        while find_tag_number <= square_range:
            #missing elements on beginning
            missing = (last_element - ((find_tag_number-1)//2)) % find_tag_number
            if missing == 0:
                index = 0
                temp_tab[0]=1
            index = find_tag_number - missing
            temp_tab[index] = 1
            
            temp_tab[index : self.LEN : find_tag_number] = 1
            ''''' #the same, but x2 faster than:
            while index < self.LEN:
                temp_tab[index] = 1
                index += find_tag_number '''        
            primes_counter += 1
            find_tag_number = self.primes[primes_counter]
            
        #FINDING PRIMES FROM ASHES
        number = 0
        
        for x in range(self.LEN):
            if temp_tab[x] == 0:                
                number_of_primes += 1
                number = last_element*2+(x*2)+1
                file.write(str(number)+' ')

        file.close()
        time2 = datetime.datetime.now()
        print(f'File number: {file_number} created in {(time2-time1)}')
        print(f'{number_of_primes} primes found.')
        print(f'Last primes in block: {number}')

        
if __name__ == "__main__":

    MySieve = Sieve()
    print(f"{len(MySieve.primes)} primes loaded.")
    print("Last prime number: " , MySieve.primes[-1])
