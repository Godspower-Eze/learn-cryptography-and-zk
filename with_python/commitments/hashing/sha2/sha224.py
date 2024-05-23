from .sha256 import SHA_256


class SHA_224(SHA_256):

    h0 = 0xc1059ed8
    h1 = 0x367cd507
    h2 = 0x3070dd17
    h3 = 0xf70e5939
    h4 = 0xffc00b31
    h5 = 0x68581511
    h6 = 0x64f98fa7
    h7 = 0xbefa4fa4

    def digest(self, message: bytes):
        super().digest(message)
        return ("{:08x}" * 7).format(*
                                     (self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6))


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
        "23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7",
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f",
        "75388b16512776cc5dba5da1fd890150b0c6455cb4f58b1952522525",
        "c97ca9a559850ce97a04a96def6d99a9e0e0e2ab14e6b8df265fc0b3",
        "20794655980c91d8bbb4c1ea97618a4bf03f42581948b2ee4ee7ad67",
    ]
    for m, d in zip(messages, digests):
        sha2_224 = SHA_224()
        digest = sha2_224.digest(m)
        assert (digest == d)
