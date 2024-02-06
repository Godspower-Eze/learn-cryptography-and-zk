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

    k1 = 0x5A827999 # (0 <= t <= 19)

    k2 = 0x6ED9EBA1 # (20 <= t <= 39)

    k3 = 0x8F1BBCDC # (40 <= t <= 59)

    k4 = 0xCA62C1D6 # (60 <= t <= 79)

    ## Initialization Vector
    
    h0 = 0x67452301

    h1 =  0xEFCDAB89

    h2 =  0x98BADCFE

    h3 = 0x10325476

    h4 =  0xC3D2E1F0

    def f1(self, b: int, c: int, d: int) -> int:
        # (0 <= t <= 19)
        return (b & c) | ((~b) & d)

    def f2(self, b: int, c: int, d: int) -> int:
        # (20 <= t <= 39)
        return b ^ c ^ d

    def f3(self, b: int, c: int, d: int) -> int:
        # (40 <= t <= 59)
        return (b & c) | (b & d) | (c & d)

    def f4(self, b: int, c: int, d: int) -> int:
        # (60 <= t <= 79)
        return self.f2(b, c, d)

    @staticmethod
    def rotate(n: int, b: int) -> int:
        return ((n << b) | (n >> 32 - b)) & MAX_32_BIT_VALUE

    def pad(self, message: bytes) -> bytes:
        length = len(message)
        padding = b"\x80" + b"\x00" * ((self.block_size - 1) - (length + BITS_PER_BYTE) % self.block_size)
        padded_message = message + padding + struct.pack(">Q", 8 * length)
        return padded_message
    
    def split_into_blocks(self, padded_message: bytes) -> List[bytes]:
        return [padded_message[i : i + self.block_size] for i in range(0, len(padded_message), self.block_size)]
    
    def expand_block(self, block: bytes) -> List[int]:
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, self.rounds):
            w[i] = self.rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)
        return w
    
    def digest(self, message: bytes):
        padded_data = self.pad(message)
        blocks = self.split_into_blocks(padded_data)
        for block in blocks:
            expanded_block = self.expand_block(block)
            a, b, c, d, e = self.h0, self.h1, self.h2, self.h3, self.h4
            for i in range(self.rounds):
                if 0 <= i <= 19:
                    f = self.f1(b, c, d)
                    k = self.k1
                elif 20 <= i <= 39:
                    f = self.f2(b, c, d)
                    k = self.k2
                elif 40 <= i <= 59:
                    f = self.f3(b, c, d)
                    k = self.k3
                elif 60 <= i <= 79:
                    f = self.f4(b, c, d)
                    k = self.k4
                a, b, c, d, e = (
                    (self.rotate(a, 5) + f + e + k + expanded_block[i]) & MAX_32_BIT_VALUE,
                    a,
                    self.rotate(b, 30),
                    c,
                    d
                )
            self.h0 += a & MAX_32_BIT_VALUE
            self.h1 += b & MAX_32_BIT_VALUE
            self.h2 += c & MAX_32_BIT_VALUE
            self.h3 += d & MAX_32_BIT_VALUE
            self.h4 += e & MAX_32_BIT_VALUE
        return ("{:08x}" * 5).format(*(self.h0, self.h1, self.h2, self.h3, self.h4))
        


sha = SHA_1()
message = bytes("abc", "utf-8")
digest = sha.digest(message)
print(digest)
