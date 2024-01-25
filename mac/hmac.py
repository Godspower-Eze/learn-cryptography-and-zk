"""
HMAC(hash-based MAC) is a type of MAC(message authentication code) that uses hash functions.

A MAC is used for message authentication. It confirms the authenticity of a message and the sender of the message i.e, 
the message hasn't been modified and the sender hasn't been compromised.

HMAC achieves this using hash functions. 
"""
import hashlib

class HMAC:

    block_size = 64
    opad = bytes.fromhex("5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c")
    ipad = bytes.fromhex("36363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636")

    def __init__(self, hash_algorithm, secret_key: str, message: str) -> None:
        self.secret_key = bytes.fromhex(secret_key)
        self.derived_key = self.derive_key(self.secret_key)
        self.message = bytes.fromhex(message)

    def derive_key(self, key: bytes):
        if len(key) > self.block_size:
            m = hashlib.sha256()
            m.update(key)
            hashed_key = m.digest()
            return hashed_key.rjust(self.block_size, b'\x00')
        elif len(key) < self.block_size:
            # key.rjust(self.block_size, b'\x00')
            # key + b'\x00' * (self.block_size-len(key))
            return key.ljust(self.block_size, b'\x00')
        else:
            return key
        
    def xor_bytes(self, bytes1: bytes, bytes2: bytes):
        return bytes(x ^ y for x, y in zip(bytes1, bytes2))
    
    def compute(self):
        s1 = self.xor_bytes(self.derived_key, self.ipad)
        s1_and_m = s1 + self.message
        h1 = hashlib.sha256()
        h1.update(s1_and_m)
        hash_s1_m = h1.digest()
        s2 = self.xor_bytes(self.derived_key, self.opad)
        hash_s1_m_s2 = s2 + hash_s1_m
        h2 = hashlib.sha256()
        h2.update(hash_s1_m_s2)
        return h2.digest()

## Source: https://en.wikipedia.org/wiki/HMAC#Definition
    
hash_algorithms = [
    {"algorithm": hashlib.sha256(),
     "block_size": 64}
]
        
## TEST VECTORS: 
## Source: https://datatracker.ietf.org/doc/html/rfc4231#section-4



## Test Case 1
    
