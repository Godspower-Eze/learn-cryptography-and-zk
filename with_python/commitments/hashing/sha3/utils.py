from bitarray import bitarray
import numpy as np


def pad(message: bytes, rate: int) -> bitarray:
    """
    According to the spec(FIPS PUB 202), section 5.1,
        j = (- m - 2) mod x
        padding = 1 concat 0 ^ j concat 1

        where:
            - `m` is the length of the message (after the delimiter has been added)

            - `x` is the rate

    Full padding steps:

        1. convert byte message to bitarray

        2. reverse to use little-endian bit ordering per byte

        3. add the domain separation bit (delimiter) which is 01 (for SHA-3)

        4. compute the padding as specified above and add to the bitarray
    """
    a = bitarray()
    # convert byte to bitarray
    a.frombytes(message)
    # reverse bits
    a.bytereverse()
    # add domain separation bits
    a.extend([0, 1])

    #
    length = len(a)
    padding = []
    j = (-(length) - 2) % rate
    padding.append(1)
    zeros = [0 for _ in range(0, j)]
    padding.extend(zeros)
    padding.append(1)
    a.extend(padding)
    return a


def one_d_to_three_d(bits: bitarray) -> np.ndarray:
    """
    implemented according to the spec(FIPS PUB 202), section 3.1.2
    """
    out = np.zeros((5, 5, 64), dtype=int)
    for i in range(5):
        for j in range(5):
            for k in range(64):
                out[i][j][k] = bits[64*(5*j + i) + k]
    return out


def three_d_to_one_d(bits_box: np.ndarray) -> bitarray:
    """
    implemented according to the spec(FIPS PUB 202), section 3.1.3
    """
    out = np.zeros(1600, dtype=int)  # Initialize empty array of size 1600
    for i in range(5):
        for j in range(5):
            for k in range(64):
                out[64*(5*j+i)+k] = bits_box[i][j][k]
    return bitarray(out.tolist())


message = bytes.fromhex("aebcdf")
padded_message = pad(message, 1600)
d = one_d_to_three_d(padded_message)
e = three_d_to_one_d(d)
