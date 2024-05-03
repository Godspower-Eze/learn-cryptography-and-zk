import sys

from bitarray import bitarray
import numpy as np

from ..constants import X, Y, W, STATE_SIZE, MAX_64_BIT_VALUE, ROUNDS, ROUND_CONSTANTS

np.set_printoptions(threshold=sys.maxsize)


def bit_padding(message: bytes, rate: int) -> bitarray:
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


def byte_padding(message: bytes, rate: int) -> bytes:
    """
    According to the spec(FIPS PUB 202), section B.2,

        q = (x - 8) - (m % (x / 8))

        where:
            x is the rate

            m is the message length

        if q is 1, append `0x86` to the message

        if q is 2, append `0x0686` to the message

        if q is more than 2, 0x06, 0x00 * (q - 2) and 0x86 in this order.
    """
    length = len(message)
    rate_in_byte = (rate // 8)
    q = rate_in_byte - (length % rate_in_byte)
    if q == 1:
        return message + bytes.fromhex("86")
    elif q == 2:
        return message + bytes.fromhex("0680")
    else:
        x = q - 2
        zeros_bytes = bytes.fromhex("00") * x
        return message + bytes.fromhex("06") + zeros_bytes + bytes.fromhex("80")


def message_to_state_array(padded_message: bytes, rate: int) -> np.ndarray:
    """
    the goal of this function is to convert a message to a 5 x 5 array with 64-bit words.

    we achieve this by taking the message in groups of 8 bytes, combine it into a 64-bit word and add it to the array downwards.

    for example:

        - given an array: [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)]]
        - by downwards, we mean that we add the first word to index (0, 0), second to (1, 0), third to (0, 1), 
          fourth to (1, 1), fifth to (0, 2) and sixth to (1, 2)

    loop logic:
        - for the main loop, we loop through the length of the padded message
          and increment by block size(rate // 8) so that we deal with the
          message per block

        - for the inner loop, we loop through 17(rate // 64) so that we can work with
          every single byte in the block

        - inside the inner loop:

            - pre_index is the starting point and it helps us getting all 8 bytes in an iteration.
              the values are 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120 and 128 
              when the index of the main loop is 0. so, for example using 0, we 0 to 7 and using 8 we 8 to 15
              and so on. and, we achieve this using line 137 to 144

            - line 146 to 156 is the most interesting part of this function because it uses a bit trick to achieve
              bit concatenation and flipping.

              the goal is to concatenate a set of 8-bit in reverse.

              for example, say we wanted to do that for the message `abc`,

                - the values of a, b and c in ascii is 97, 98 and 99 respectively

                - 97 is 0110 0001, left-shift by 0; making it the same

                - 98 is 0110 0010, left-shift by 8; making it 25088 and 0110 0010 0000 0000 in binary

                - 99 is 0110 0011. left-shift by 16 making it 6488064 and 0110 0011 0000 0000 0000 0000 in binary

                - when we add 6488064, 25088 and 97 we have 6513249 which is 0110 0011 0110 0010 0110 0001 in binary!

                - this is the concatenation of 99, 98 and 97!

        - the next part handles the downwards movement making it sure it goes down per column as explained above.

    """

    out = np.zeros((X, Y), dtype=np.uint64)
    state_array = out.tolist()
    for i in range(0, len(padded_message), rate // 8):
        for j in range(0, rate // W):
            pre_index = i + j * 8

            first = pre_index + 0
            second = pre_index + 1
            third = pre_index + 2
            fourth = pre_index + 3
            fifth = pre_index + 4
            sixth = pre_index + 5
            seventh = pre_index + 6
            eighth = pre_index + 7

            first_byte = padded_message[first] << 0
            second_byte = padded_message[second] << 8
            third_byte = padded_message[third] << 16
            fourth_byte = padded_message[fourth] << 24
            fifth_byte = padded_message[fifth] << 32
            sixth_byte = padded_message[sixth] << 40
            seventh_byte = padded_message[seventh] << 48
            eighth_byte = padded_message[eighth] << 56

            combination = first_byte + second_byte + \
                third_byte + fourth_byte + fifth_byte + sixth_byte + seventh_byte + eighth_byte

            x = j % 5
            y = j // 5
            state_array[x][y] = state_array[x][y] ^ combination
    return state_array


def left_rotate(n: int, b: int) -> int:
    return ((n << b) | (n >> W - b)) & MAX_64_BIT_VALUE


def theta(state_array: np.ndarray):
    """
    implemented according to the spec(FIPS PUB 202), section 3.2.1
    """

    c = []
    d = []

    for i in range(5):
        c.append(state_array[i][0])
        for j in range(1, 5):
            c[i] = c[i] ^ state_array[i][j]

    for i in range(5):
        d.append(c[(i + 4) % 5] ^ left_rotate(c[(i + 1) % 5], 1))
        for j in range(5):
            state_array[i][j] = state_array[i][j] ^ d[i]

    return state_array


def rho_and_pi(state_array: np.ndarray):
    x, y = 1, 0

    current = state_array[x][y]
    for t in range(24):
        X, Y = y, (2 * x + 3 * y) % 5
        tmp = state_array[X][Y]
        state_array[X][Y] = left_rotate(
            current, ((((t + 1) * (t + 2)) // 2) % W))
        current = tmp
        x, y = X, Y

    return state_array


def chi(state_array: np.ndarray):

    for i in range(5):
        c = [state_array[j][i] for j in range(5)]
        for j in range(5):
            state_array[j][i] = c[j] ^ (~c[(j + 1) % 5] & c[(j + 2) % 5])

    return state_array


def keccak_f_1600(state_array):
    for r in range(ROUNDS):
        state_array = chi(rho_and_pi(theta(state_array)))
        state_array[0][0] = state_array[0][0] ^ ROUND_CONSTANTS[r]
    return state_array


RATE = 1088
message = bytes("abc", "utf-8")
padded_message = byte_padding(message, RATE)
state_array = message_to_state_array(padded_message, RATE)
state_array = keccak_f_1600(state_array)
print(state_array)
