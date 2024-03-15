from bitarray import bitarray


def pad(message: bytes) -> bitarray:
    a = bitarray()
    a.frombytes(message)
    return a


def one_d_to_three_d():
    pass


def three_d_to_one_d():
    pass


message = bytes.fromhex("aebcdf")
padded_message = pad(message)
print(padded_message)
