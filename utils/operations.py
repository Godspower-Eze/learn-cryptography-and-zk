def not_bytes(a: bytes):
    return bytes(~x & 0xFF for x in a)


def and_bytes(a: bytes, b: bytes):
    return bytes(x & y for x, y in zip(a, b))


def or_bytes(a: bytes, b: bytes):
    return bytes(x | y for x, y in zip(a, b))


def xor_bytes(a: bytes, b: bytes):
    return bytes(x ^ y for x, y in zip(a, b))
