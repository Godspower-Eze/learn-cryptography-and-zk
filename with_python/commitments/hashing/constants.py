BITS_PER_BYTE = 8
MAX_32_BIT_VALUE = 0xFFFFFFFF
MAX_64_BIT_VALUE = 0xFFFFFFFFFFFFFFFF

# SHA-3
L = 6  # possible values of l = {0, 1, 2, 3, 4, 5, 6} but 6 for SHA-3
W = 2 ** L
STATE_SIZE = 25 * W  # state size for SHA-3 which is 1600 bits
ROUNDS = 12 + (2 * L)
