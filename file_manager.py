import datetime
import bitarray
import os
import gzip
import shutil


class SieveFileManager:
    def __init__(self, length_per_file: int) -> None:
        self.LEN = length_per_file
        self.file_name = 'bits_file'

    def save(self, file_number: int, data) -> None:
        file_name = self.file_name + str(file_number) + '.bin'
        with open(file_name, 'wb') as fh:
            data.tofile(fh)

    def bit_file_to_array_of_primes(self, nr) -> list[int]:
        """
            Load a bitarray file and return a list of prime numbers.

            The file is expected to contain a bitarray where each bit represents
            whether a number (typically only odd numbers) is prime (1) or not (0),
            according to the sieve structure used during generation.

            Args:
                path (str): Path to the binary file containing the prime bitarray.

            Returns:
                list[int]: List of prime numbers decoded from the bitarray.
        """
        file_name = self.file_name + str(nr) + '.bin'
        array = []
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
                array.append((x + 2 * z + temp))
        if nr == 1:
            return (array[1:])  # delete "1"
        return array

    @staticmethod
    def compress_file(input_path: str,
                      output_path: str = None,
                      remove = False) -> None:
        """Compress file input_path to gzip and
         [optional] remove original file."""
        if output_path is None:
            output_path = input_path + ".gz"

        with open(input_path, 'rb') as f_in, gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"Compressed '{input_path}' to '{output_path}'.")

        if remove:
            os.remove(input_path)
            print(" and removed original.")

    @staticmethod
    def decompress_file(input_path: str, output_path: str = None) -> None:
        """Decompress gzip file input_path to output_path without removing gzip."""
        if output_path is None:
            if input_path.endswith(".gz"):
                output_path = input_path[:-3]
            else:
                raise ValueError("Output path must be specified if input is not .gz")
        with gzip.open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
            f_out.write(f_in.read())
        print(f"Decompressed '{input_path}' to '{output_path}'.")
