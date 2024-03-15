"""
The polyalphabetic cipher is a more secure technique than the caesar cipher.

Using brute force, It would take a longer time to break compared to the caesar cipher.

It can also be broken using `frequency analysis`.
"""


class PolyAlphabetic_Cipher:

    """
    STEPS:
        1. Choose a secret word and get it's equivalent in numbers. E.g Love -> 12 15 22 5
        2. Repeat this sequence of numbers across the word/words you want to encrypt mapping every letter to a number
        3. Shift every letter by the number mapped to it to get the cipher
    """

    secret_word = None
    letters = [
        "",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z"]

    def __init__(self, _secret_word: str) -> None:
        if len(_secret_word) == 0:
            raise Exception("Invalid secret word")

        self.secret_numbers = [
            self.letters.index(
                letter.lower()) for letter in _secret_word.lower()]

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

    def _partition_word(self, _length: int, _word: str,
                        _partitioned_words: list) -> list:
        if len(_word) == 0:
            return _partitioned_words

        word = _word[:_length]
        _partitioned_words.append(word)
        new_word = _word[_length:]
        return self._partition_word(_length, new_word, _partitioned_words)

    def encrypt(self, _word: str):
        len_of_secret_numbers = len(self.secret_numbers)
        partitioned_words = self._partition_word(
            len_of_secret_numbers, _word.lower(), [])

        letters_pair = []
        for part in partitioned_words:
            for letter, number in zip(part, self.secret_numbers):
                letters_pair.append((letter, number))

        cipher_word = ""
        for pair in letters_pair:
            cipher_letter = self._shift(pair[0], pair[1])
            cipher_word += cipher_letter

        return cipher_word

    def decrypt(self, _encrypted_word: str):
        len_of_secret_numbers = len(self.secret_numbers)
        partitioned_words = self._partition_word(
            len_of_secret_numbers, _encrypted_word.lower(), [])

        letters_pair = []
        for part in partitioned_words:
            for letter, number in zip(part, self.secret_numbers):
                letters_pair.append((letter, number))

        deciphered_word = ""
        for pair in letters_pair:
            deciphered_letter = self._unshift(pair[0], pair[1])
            deciphered_word += deciphered_letter

        return deciphered_word
