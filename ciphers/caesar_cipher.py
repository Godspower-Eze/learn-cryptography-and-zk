"""
Caesar Cipher(aka Substitution Cipher) is considered one of the first forms of cryptography.

It was used by Julius Caesar around 58BC.

It is built on the shifting letters in the alphabet by number known by the sender and receiver only.

It can be broken with a technique called `frequency analysis` and it's also easy to break using brute force because 

there would always be 25 possible encryption/decryption of every letter in the alphabet
"""

class CaesarCipher:

  """
  STEPS:
    1. Choose a secret number from 1 to 26
    2. Shift every letter of the word by that secret number to get a cipher text
    3. Reverse the process to get the original word
  """

  secret_number = None
  letters = [
    "", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
  ]

  def __init__(self, _secret_number: int):
    if _secret_number == 0 or _secret_number > 26:
      raise Exception(f"{_secret_number} is out of range")
    
    self.secret_number = _secret_number

  def encrypt(self, _word: str) -> str:
    word_as_lower_case = _word.lower()
    new_word = ''

    for letter in word_as_lower_case:
      index = self.letters.index(letter)
      shift_value = index + self.num_of_shifts
      if shift_value > 26:
        shift_value = shift_value - 26
      else:
        new_index = shift_value
      letter_at_index = self.letters[new_index]
      new_word += letter_at_index
    return new_word

  def decrypt(self, cipher_text: str) -> str:
    new_word = ''

    for letter in cipher_text:
      index = self.letters.index(letter)
      unshift_value = index - self.num_of_shifts
      if unshift_value < 1:
        new_index = unshift_value + 26
      else:
        new_index = unshift_value
      letter_at_index = self.letters[new_index]
      new_word += letter_at_index
    return new_word

  def encrypt_sentence(self, _sentence: str) -> str:
    words = _sentence.split(" ")
    new_sentence = ''

    for word in words:
      new_sentence += self.encrypt(word) + " "
    return new_sentence

  def decrypt_sentence(self, _encrypted_sentence: str) -> str:
    words = _encrypted_sentence.split(" ")
    new_sentence = ''

    for word in words:
      new_sentence += self.decrypt(word) + " "
    return new_sentence


