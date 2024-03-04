from ..constants import SHA3_BITS


class SHA_224:

    output_length = 28  # in bytes

    capacity = output_length * 2  # in bytes

    rate = SHA3_BITS - (capacity)  # in bytes

    def pad(self, message: bytes):
        length = len(message)
        space = self.rate - (length % self.rate)
        print(space)


sha_224 = SHA_224()
message = b"abcdefghijklmnopqrstuvwxtuvwxyz"
padded_message = sha_224.pad(message)
