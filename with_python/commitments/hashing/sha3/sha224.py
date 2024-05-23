from .utils import sha3_hash

RATE = 1152


def hash(message: bytes):
    return sha3_hash(message, RATE)


# TEST USING TEST VECTORS(https://www.di-mgt.com.au/sha_testvectors.html)
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
        "e642824c3f8cf24ad09234ee7d3c766fc9a3a5168d0c94ad73b46fdf",
        "6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7",
        "8a24108b154ada21c9fd5574494479ba5c7e7ab76ef264ead0fcce33",
        "543e6868e1666c1a643630df77367ae5a62a85070a51c14cbf665cbc",
        "d69335b93325192e516a912e6d19a15cb51c6ed5c15243e7a7fd653c",
    ]
    for m, d in zip(messages, digests):
        digest = hash(m)
        assert (digest == d)
