from bitarray import bitarray
import numpy as np

from ..constants import W

X_AXIS = 5
Y_AXIS = 5
Z_AXIS = 64


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
    out = np.zeros((X_AXIS, Y_AXIS, Z_AXIS), dtype=int)
    for x in range(X_AXIS):
        for y in range(Y_AXIS):
            for z in range(Z_AXIS):
                out[x][y][z] = bits[W*(5*y + x) + z]
                print([x, y, z])
    return out


def three_d_to_one_d(bits_box: np.ndarray) -> bitarray:
    """
    implemented according to the spec(FIPS PUB 202), section 3.1.3
    """
    out = np.zeros(1600, dtype=int)  # Initialize empty array of size 1600
    for x in range(X_AXIS):
        for y in range(Y_AXIS):
            for z in range(Z_AXIS):
                out[Z_AXIS*(5*y+x)+z] = bits_box[x][y][z]
    return bitarray(out.tolist())


def theta(bits_box: np.ndarray):
    """
    implemented according to the spec(FIPS PUB 202), section 3.2.1
    """

    def c_of_x_and_y(bits_box, x, z):
        # C[x,z] = A[x, 0 , z] ⊕ A[x, 1, z] ⊕ A[x, 2, z] ⊕ A[x, 3, z] ⊕ A[x, 4, z].
        a = bits_box[x, 0, z] ^ bits_box[x, 1,
                                         z] ^ bits_box[x, 2, z] ^ bits_box[x, 3, z] ^ bits_box[x, 4, z]
        return a

    out = np.zeros((5, 5, 64), dtype=int)
    for x in range(X_AXIS):
        for y in range(Y_AXIS):
            for z in range(Z_AXIS):
                # D[x,z] = C[(x - 1) mod 5, z] ⊕ C[(x+1) mod 5, (z – 1) mod w]
                d = c_of_x_and_y((x - 1) %
                                 5, z) ^ c_of_x_and_y((x + 1) % 5, (z - 1) % W)
                # A′[x, y, z] = A[x, y, z] ⊕ D[x, z].
                out[x, y, z] = bits_box[x, y, z] ^ d
    return out


message = bytes.fromhex("aebcdf")
padded_message = pad(message, 1600)
d = one_d_to_three_d(padded_message)
e = three_d_to_one_d(d)
after_theta = theta(d)
print(after_theta)
