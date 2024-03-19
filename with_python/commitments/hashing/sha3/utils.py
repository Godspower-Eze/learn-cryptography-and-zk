from bitarray import bitarray


def pad(message: bytes) -> bitarray:
    a = bitarray()
    a.frombytes(message)
    a.bytereverse()
    a.extend([0, 1])
    a.append(1)
    print(len(a))
    return a


def one_d_to_three_d():
    pass


def three_d_to_one_d():
    pass


message = bytes.fromhex("aebcdf")
padded_message = pad(message)
print(padded_message)
