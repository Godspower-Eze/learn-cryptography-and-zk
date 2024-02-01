"""
A word: 32-bit(4 bytes) string

A block: 512-bit(64) string
"""

from utils.operations import and_bytes, or_bytes, xor_bytes, not_bytes

class SHA_1:

    k1 = bytes.fromhex('5A827999') # (0 <= t <= 19)

    k2 = bytes.fromhex('6ED9EBA1') # (20 <= t <= 39)

    k3 = bytes.fromhex('8F1BBCDC') # (40 <= t <= 59)

    k4 = bytes.fromhex('CA62C1D6') # (60 <= t <= 79)
    
    def f1(self, b: bytes, c: bytes, d:bytes):
        # (0 <= t <= 19)
        return or_bytes(and_bytes(b, c), and_bytes(not_bytes(b), d))

    def f2(self, b: bytes, c: bytes, d:bytes):
        # (20 <= t <= 39)
        return xor_bytes(xor_bytes(b, c), d)

    def f3(self, b: bytes, c: bytes, d:bytes):
        # (40 <= t <= 59)
        return or_bytes(or_bytes(and_bytes(b, c), and_bytes(b, d)), and_bytes(c, d))

    def f4z(self, b: bytes, c: bytes, d:bytes):
        # (60 <= t <= 79)
        return xor_bytes(xor_bytes(b, c), d)