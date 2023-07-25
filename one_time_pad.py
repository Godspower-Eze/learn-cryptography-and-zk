"""
One-time pad is a more secure form of caesar cipher and polyalphabetic cipher. 

Instead of shifting by a constant or by a repeating set of numbers, each number is generated randomly.

The weakness of ceasar cipher and polyalphabetic cipher lies in the frequency of letters even when encrypted.

One time pad solves that using random number to shift letters thereby uniformly distributing the frequency without 
creating patterns.

Also, the key space (possible encryption values) increases making brute force attacks harder. For example, using the
caesar cipher; shifting a word by a number means that we just need to try to unshift from 0 to 26 to get all possible
values. But, for one-time pad each word has an different and random number between 0 and 26 so if the word is a 4-letter word,
there are 26 ^ 4 possible values.
"""
from random import randint


class One_Time_Pad:

    """
    STEPS:
        1. Generate a list of random numbers the length of the word to be encrypted.
        2. Shift every letter of the word by the number mapped to them to get a cipher text. 
           E.g love -> [21, 15, 14, 13] -> [(l, 21), (o, 15), (v, 14), (e, 13)]
        3. Reverse the process to get the original word
    """

    letters = ["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ]

    def generate_numbers(self, length: int) -> list[int]:
        random_numbers = []
        for i in range(length):
            random_number = randint(1, 26)
            random_numbers.append(random_number)
        return random_numbers
    
    def _shift(self, _letter: str, _num_of_shifts: int):
        if _num_of_shifts > 26:
            raise Exception("Invalid number of shifts")
        
        index = self.letters.index(_letter)
        new_index = index + _num_of_shifts
        if new_index > 26:
            new_index = new_index - 26
        return self.letters[new_index]
    
    def _unshift(self, _letter: str, _num_of_shifts: int):
        if _num_of_shifts > 26:
            raise Exception("Invalid number of shifts")
        
        index = self.letters.index(_letter)
        new_index = index - _num_of_shifts
        if new_index < 1:
            new_index = new_index + 26
        return self.letters[new_index]
    
    def encrypt(self, word: str, random_numbers: list) -> str:
        if len(word) != len(random_numbers):
            raise Exception("invalid length")
        
        new_word = ""
        for (letter, random_number) in zip(word, random_numbers):
            new_letter = self._shift(letter, random_number)
            new_word += new_letter
        return new_word
    
    def decrypt(self, encrypted_word: str, random_numbers: list) -> str:
        if len(encrypted_word) != len(random_numbers):
            raise Exception("invalid length")
        
        new_word = ""
        for (letter, random_number) in zip(encrypted_word, random_numbers):
            new_letter = self._unshift(letter, random_number)
            new_word += new_letter
        return new_word