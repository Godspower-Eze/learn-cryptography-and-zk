class CeaserCipher:

  num_of_shifts = None
  letters = [
    "", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
  ]

  def __init__(self, _num_of_shifts: int):
    if _num_of_shifts == 0:
      raise Exception
    self.num_of_shifts = _num_of_shifts

  def encrypt(self, word: str) -> str:
    word_as_lower_case = word.lower()
    new_word = ''
    for letter in word_as_lower_case:
      index = self.letters.index(letter)
      shift_value = index + self.num_of_shifts
      while shift_value > 26:
        shift_value = shift_value - 26
      new_index = shift_value
      letter_at_index = self.letters[new_index]
      new_word += letter_at_index
    return new_word

  def decrypt(self, cipherText: str) -> str:
    new_word = ''
    for letter in cipherText:
      index = self.letters.index(letter)
      unshift_value = index - self.num_of_shifts
      if unshift_value < 1:
        new_index = unshift_value + 26
      else:
        new_index = unshift_value
      letter_at_index = self.letters[new_index]
      new_word += letter_at_index
    return new_word

  def encrypt_sentence(self, sentence: str) -> str:
    words = sentence.split(" ")
    new_sentence = ''
    for word in words:
      new_sentence += self.encrypt(word) + " "
    return new_sentence

  def decrypt_sentence(self, encrypted_sentence: str) -> str:
    words = encrypted_sentence.split(" ")
    new_sentence = ''
    for word in words:
      new_sentence += self.decrypt(word) + " "
    return new_sentence


