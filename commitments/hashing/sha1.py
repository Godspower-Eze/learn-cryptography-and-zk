"""
A word: 32-bit(4 bytes) string

A block: 512-bit(64) string
"""

import struct
from typing import List

from utils.operations import and_bytes, or_bytes, xor_bytes, not_bytes


BITS_PER_BYTE = 8

MAX_32_BIT_VALUE = 0xFFFFFFFF

class SHA_1:

    rounds = 80

    block_size = 64 # in bytes

    k1 = bytes.fromhex('5A827999') # (0 <= t <= 19)

    k2 = bytes.fromhex('6ED9EBA1') # (20 <= t <= 39)

    k3 = bytes.fromhex('8F1BBCDC') # (40 <= t <= 59)

    k4 = bytes.fromhex('CA62C1D6') # (60 <= t <= 79)

    ## Initialization Values
    
    h0 = bytes.fromhex('67452301')

    h1 =  bytes.fromhex('EFCDAB89')

    h2 =  bytes.fromhex('98BADCFE')

    h3 = bytes.fromhex('10325476')

    h4 =  bytes.fromhex('C3D2E1F0')

    @staticmethod
    def rotate(n: int, b: int):
        return ((n << b) | (n >> 32 - b)) & MAX_32_BIT_VALUE

    def pad(self, message: bytes) -> bytes:
        length = len(message)
        padding = b"\x80" + b"\x00" * ((self.block_size - 1) - (length + BITS_PER_BYTE) % self.block_size)
        padded_message = message + padding + struct.pack(">Q", 8 * length)
        return padded_message
    
    def split_into_blocks(self, padded_message: bytes) -> List[bytes]:
        return [padded_message[i : i + self.block_size] for i in range(0, len(padded_message), self.block_size)]
    
    def expand_block(self, block: bytes):
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, self.rounds):
            w[i] = self.rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)
        return w
    
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



sha = SHA_1()
message = bytes.fromhex("ffff")
padded_value = sha.pad(message)
blocks = sha.split_into_blocks(padded_value)
for block in blocks:
    w = sha.expand_block(block)
    print(w)
