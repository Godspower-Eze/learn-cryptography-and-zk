from .utils import sha3_hash

RATE = 1088


def hash(message: bytes):
    return sha3_hash(message, RATE)
