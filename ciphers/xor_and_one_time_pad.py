"""
This is an implementation of One Time Pad Implemented here(./one_time_pad) using the XOR bitwise operation 
rather than using addition and subtraction of shift number.

Why XOR?
    https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/xor-and-the-one-time-pad
"""

from random import randint

import ciphers.one_time_pad as one_time_pad

class XOR_One_Time_Pad(one_time_pad.One_Time_Pad):

    """
    STEPS:
        1. Generate a list of random numbers the length of the word to be encrypted.
        2. Convert every letter of the word to be encrypted to number according the their place in the letters of the alphabet. 
           E.g a -> 1, z -> 26 
        3. Perform XOR on the number from the list of random numbers and the numbers gotten from the Step 2. 
           E.g random numbers = [23, 14, 11, 16], letter_conversions = [22, 12, 9, 1], xors = [(23 XOR 22), (14 XOR 12), (11 XOR 9), (16 XOR 1)]
        4. Shift each letter by the result of the XOR operation
        5. Perform xor on the random numbers and original xor values to decrypt
    """

    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ]

    def generate_numbers(self, length: int) -> list[int]:
        random_numbers = []
        for i in range(length):
            random_number = randint(0, 25)
            random_numbers.append(random_number)
        return random_numbers

    def letter_to_number(self, word: str) -> list[int]:
        numbers = []
        for letter in word.lower().strip():
            index = self.letters.index(letter)
            numbers.append(index)
        return numbers
    
    def _xor(self, letter_numbers: list[int], random_numbers: list[int]):
        if len(letter_numbers) != len(random_numbers):
            raise Exception("Invalid length")
        numbers = []
        for (letter_number, random_number) in zip(letter_numbers, random_numbers):
            numbers.append(letter_number ^ random_number)
        return numbers
    
    def _shift(self, _num_of_shifts: int) -> str:
        new_index = _num_of_shifts % 26
        return self.letters[new_index]
    
    def encrypt(self, word: str, random_numbers: list[int]) -> str:
        if len(word) != len(random_numbers):
            raise Exception("invalid length")
        
        letter_numbers = self.letter_to_number(word)
        xor_numbers = self._xor(letter_numbers, random_numbers)

        print("Encrypted:", f"Letter numbers: {letter_numbers}", f"Random numbers: {random_numbers}", f"XOR numbers: {xor_numbers}")

        new_word = ""
        for number in xor_numbers:
            new_letter = self._shift(number)
            new_word += new_letter
        return new_word
    
    def decrypt(self, random_numbers: list[int], original_xor_numbers: list[int]) -> str:
        if len(random_numbers) != len(random_numbers):
            raise Exception("invalid length")

        xor_numbers = self._xor(random_numbers, original_xor_numbers)

        new_word = ""
        for number in xor_numbers:
            new_letter = self._shift(number)
            new_word += new_letter
        return new_word
    