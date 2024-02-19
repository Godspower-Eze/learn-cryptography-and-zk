"""
SHA-1(Secure Hashing Algorithm 1) is a type of hash function based on Merkle-Damgard Construction.

It takes an arbitrary length input and returns a 160-bit(20 byte) value.

Merkle-Damgard Construction is a method of building collision-resistant cryptographic hash functions from
collision resistant one-way compression functions.s
"""

import struct
from typing import List


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
        w = list(struct.unpack(">16L", block)) + [0] * self.block_size
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
            self.h0 = self.h0 + a & MAX_32_BIT_VALUE
            self.h1 = self.h1 + b & MAX_32_BIT_VALUE
            self.h2 = self.h2 + c & MAX_32_BIT_VALUE
            self.h3 = self.h3 + d & MAX_32_BIT_VALUE
            self.h4 = self.h4 + e & MAX_32_BIT_VALUE
        return ("{:08x}" * 5).format(*(self.h0, self.h1, self.h2, self.h3, self.h4))
        

sha = SHA_1()
messages = [
    bytes("abc", "utf-8"),
    bytes("", "utf-8"),
    bytes("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "utf-8"),
    bytes("abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu", "utf-8"),
    bytes("a" * 1_000_000, "utf-8"), 
    # bytes("abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno" * 16_777_216, "utf-8") TOO SLOW
]
digests = [
    "a9993e364706816aba3e25717850c26c9cd0d89d",
    "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "84983e441c3bd26ebaae4aa1f95129e5e54670f1",
    "a49b2446a02c645bf419f995b67091253a04a259",
    "34aa973cd4c4daa4f61eeb2bdbad27316534016f",
    # "7789f0c9ef7bfc40d93311143dfbe69e2017f592" TOO SLOW
]
for m, d in zip(messages, digests):
    sha = SHA_1()
    digest = sha.digest(m)
    assert(digest == d)

