import struct
from typing import List

from ..constants import MAX_32_BIT_VALUE
from ..sha1 import SHA_1


class SHA_256(SHA_1):

    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    k = [
        0x428a2f98,
        0x71374491,
        0xb5c0fbcf,
        0xe9b5dba5,
        0x3956c25b,
        0x59f111f1,
        0x923f82a4,
        0xab1c5ed5,
        0xd807aa98,
        0x12835b01,
        0x243185be,
        0x550c7dc3,
        0x72be5d74,
        0x80deb1fe,
        0x9bdc06a7,
        0xc19bf174,
        0xe49b69c1,
        0xefbe4786,
        0x0fc19dc6,
        0x240ca1cc,
        0x2de92c6f,
        0x4a7484aa,
        0x5cb0a9dc,
        0x76f988da,
        0x983e5152,
        0xa831c66d,
        0xb00327c8,
        0xbf597fc7,
        0xc6e00bf3,
        0xd5a79147,
        0x06ca6351,
        0x14292967,
        0x27b70a85,
        0x2e1b2138,
        0x4d2c6dfc,
        0x53380d13,
        0x650a7354,
        0x766a0abb,
        0x81c2c92e,
        0x92722c85,
        0xa2bfe8a1,
        0xa81a664b,
        0xc24b8b70,
        0xc76c51a3,
        0xd192e819,
        0xd6990624,
        0xf40e3585,
        0x106aa070,
        0x19a4c116,
        0x1e376c08,
        0x2748774c,
        0x34b0bcb5,
        0x391c0cb3,
        0x4ed8aa4a,
        0x5b9cca4f,
        0x682e6ff3,
        0x748f82ee,
        0x78a5636f,
        0x84c87814,
        0x8cc70208,
        0x90befffa,
        0xa4506ceb,
        0xbef9a3f7,
        0xc67178f2]

    rounds = 64

    @staticmethod
    def right_rotate(n: int, b: int) -> int:
        return ((n >> b) | (n << 32 - b)) & MAX_32_BIT_VALUE

    def expand_block(self, block: bytes) -> List[int]:
        w = list(struct.unpack(">16L", block)) + [0] * (self.block_size - 16)
        for i in range(16, self.rounds):
            s0 = self.right_rotate(
                w[i-15], 7) ^ self.right_rotate(w[i-15], 18) ^ ((w[i-15] >> 3))
            s1 = self.right_rotate(
                w[i-2], 17) ^ self.right_rotate(w[i-2], 19) ^ ((w[i-2] >> 10))
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & MAX_32_BIT_VALUE
        return w

    def digest(self, message: bytes):
        padded_data = self.pad(message)
        blocks = self.split_into_blocks(padded_data)
        for block in blocks:
            w = self.expand_block(block)
            a, b, c, d, e, f, g, h = self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7
            for i in range(self.rounds):
                S1 = self.right_rotate(e, 6) ^ self.right_rotate(
                    e, 11) ^ self.right_rotate(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = h + S1 + ch + self.k[i] + w[i]
                S0 = self.right_rotate(a, 2) ^ self.right_rotate(
                    a, 13) ^ self.right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = S0 + maj

                h = g
                g = f
                f = e
                e = (d + temp1) & MAX_32_BIT_VALUE
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & MAX_32_BIT_VALUE

            self.h0 = self.h0 + a & MAX_32_BIT_VALUE
            self.h1 = self.h1 + b & MAX_32_BIT_VALUE
            self.h2 = self.h2 + c & MAX_32_BIT_VALUE
            self.h3 = self.h3 + d & MAX_32_BIT_VALUE
            self.h4 = self.h4 + e & MAX_32_BIT_VALUE
            self.h5 = self.h5 + f & MAX_32_BIT_VALUE
            self.h6 = self.h6 + g & MAX_32_BIT_VALUE
            self.h7 = self.h7 + h & MAX_32_BIT_VALUE
        return ("{:08x}" * 8).format(*
                                     (self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7))


sha2 = SHA_256()
message = b""
hash_of_message = sha2.digest(message)
print(hash_of_message)
