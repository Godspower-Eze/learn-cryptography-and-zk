import binascii
import struct

from .sha512 import SHA_512


class SHA_384(SHA_512):

    h0 = 0xcbbb9d5dc1059ed8
    h1 = 0x629a292a367cd507
    h2 = 0x9159015a3070dd17
    h3 = 0x152fecd8f70e5939
    h4 = 0x67332667ffc00b31
    h5 = 0x8eb44a8768581511
    h6 = 0xdb0c2e0d64f98fa7
    h7 = 0x47b5481dbefa4fa4

    def digest(self, message: bytes):
        super().digest(message)
        h = (self.h0, self.h1, self.h2, self.h3,
             self.h4, self.h5)
        return binascii.hexlify(
            b''.join(struct.pack('!Q', e) for e in h),
        ).decode('utf-8')


if __name__ == "__main__":
    messages = [
        bytes("abc", "utf-8"),
        bytes("", "utf-8"),
        bytes("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "utf-8"),
        bytes(
            "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
            "utf-8"),
        bytes("a" * 1_000_000, "utf-8"),
    ]
    digests = [
        "cb00753f45a35e8bb5a03d699ac65007272c32ab0eded1631a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7",
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b",
        "3391fdddfc8dc7393707a65b1b4709397cf8b1d162af05abfe8f450de5f36bc6b0455a8520bc4e6f5fe95b1fe3c8452b",
        "09330c33f71147e83d192fc782cd1b4753111b173b3b05d22fa08086e3b0f712fcc7c71a557e2db966c3e9fa91746039",
        "9d0e1809716474cb086e834e310a4a1ced149e9c00f248527972cec5704c2a5b07b8b3dc38ecc4ebae97ddd87f3d8985",
    ]
    for m, d in zip(messages, digests):
        sha2_384 = SHA_384()
        digest = sha2_384.digest(m)
        assert (digest == d)
