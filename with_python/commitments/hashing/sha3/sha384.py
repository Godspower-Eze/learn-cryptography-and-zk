from .utils import sha3_hash

RATE = 832


def hash(message: bytes):
    return sha3_hash(message, RATE)
