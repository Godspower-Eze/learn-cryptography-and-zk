from .utils import sha3_hash

RATE = 1088


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
        "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532",
        "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
        "41c0dba2a9d6240849100376a8235e2c82e1b9998a999e21db32dd97496d3376",
        "916f6061fe879741ca6469b43971dfdb28b1a32dc36cb3254e812be27aad1d18",
        "5c8875ae474a3634ba4fd55ec85bffd661f32aca75c6d699d0cdcb6c115891c1",
    ]
    for m, d in zip(messages, digests):
        digest = hash(m)
        assert (digest == d)
