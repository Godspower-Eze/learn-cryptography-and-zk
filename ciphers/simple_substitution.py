"""
This is an implementation of a simple substitution cipher.

This cipher involves replacing each letter of the alphabet uniquely with another letter in the alphabet.

It can also be broken using `frequency analysis`.
"""
from random import sample
from typing import Dict

class SimpleSubstitution_Cipher:

    """
    Steps
        1. Generate a random sequence of letters whereby each letter occurs once
        2. Map this sequence to an ordered sequence of letters in the alphabet. E.g [a, b, c] = [y, x, w] = [(a,y), (b,x), (c,w)]
    """

    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def generate_random_letters(self) -> list[str]:
        random_numbers = sample(range(0, 26), 26)
        letters: list[str] = []
        for i in random_numbers:
            letters.append(self.letters[i])
        return letters
    
    def assign(self, random_letters: list[str]) -> Dict[str, str]:
        letter_mapping: Dict[str, str] = {}
        for (i, v) in zip(self.letters, random_letters):
            letter_mapping[i] = v
        return letter_mapping
    
    def encrypt(self, word: str, letter_mapping: Dict[str, str]) -> str:
        new_word = ''
        for letter in word:
            new_word += letter_mapping[letter]
        return new_word
    
    def decrypt(self, word: str, letter_mapping: Dict[str, str]) -> str:
        reverse_mapping: Dict[str, str] = {}
        for (value, key) in zip(letter_mapping.values(), letter_mapping.keys()):
            reverse_mapping[value] = key
        new_word = ''
        for letter in word:
            new_word += reverse_mapping[letter]
        return new_word

    