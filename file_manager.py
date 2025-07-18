
import bitarray

class SieveFileManager:
    def __init__(self, length_per_file: int):
        self.LEN = length_per_file
        self.file_name = 'bits_file'

    def save(self, file_number: int, data):
        file_name = self.file_name + str(file_number) + '.bin'
        with open(file_name, 'wb') as fh:
            data.tofile(fh)

    def bit_file_to_array_of_primes(self, nr):
        file_name = self.file_name + str(nr) + '.bin'
        tab = []
        a = bitarray.bitarray()
        with open(file_name, 'rb') as fh:
            a.fromfile(fh)
        x = nr - 1
        x = x * 2 * self.LEN

        # only for file nr 1
        if nr == 1:
            temp = -1
        else:
            temp = 1

        for z in range(len(a)):
            if a[z] == 0:  # is prime
                tab.append((x + 2 * z + temp))
        if nr == 1:
            return (tab[1:])  # delete "1"
        return tab