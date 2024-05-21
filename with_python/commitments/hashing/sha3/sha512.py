from .utils import sha3_hash

RATE = 576


def hash(message: bytes):
    return sha3_hash(message, RATE)


# TEST USING TEST VECTORS
