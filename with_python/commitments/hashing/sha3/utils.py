from bitarray import bitarray


def pad(message: bytes) -> bitarray:
    """
    According to the spec(FIPS PUB 202), section 5.1,
        j = (- m - 2) mod x
        padding = 1 concat 0 ^ j concat 1

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

    length = len(a)
    j = (-(length) - 2) % 16
    a.append(1)
    zeros = [0 for _ in range(0, j)]
    a.extend(zeros)
    a.append(1)
    return a


def one_d_to_three_d():
    pass


def three_d_to_one_d():
    pass


message = bytes.fromhex("aebcdf")
padded_message = pad(message)
print(len(padded_message))
