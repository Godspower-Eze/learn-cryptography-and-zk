"""
HMAC(hash-based MAC) is a type of MAC(message authentication code) that uses hash functions.

A MAC is used for message authentication. It confirms the authenticity of a message and the sender of the message i.e, 
the message hasn't been modified and the sender hasn't been compromised.

HMAC achieves this using hash functions. 
"""
import hashlib

class HMAC_SHA_256:

    block_size = 64
    opad = bytes.fromhex("5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c")
    ipad = bytes.fromhex("36363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636")

    def __init__(self, secret_key: str, message: str) -> None:
        self.secret_key = bytes(secret_key, 'utf-8')
        self.derived_key = self.derive_key(self.secret_key)
        self.message = bytes(message, 'utf-8')

    def derive_key(self, key: bytes):
        if len(key) > self.block_size:
            m = hashlib.sha256()
            m.update(key)
            hashed_key = m.digest()
            return hashed_key.rjust(self.block_size, b'\0')
        else:
            return key.rjust(self.block_size, b'\0')
        
    def xor_bytes(self, bytes1: bytes, bytes2: bytes):
        return bytes(x ^ y for x, y in zip(bytes1, bytes2))
    
    def compute(self):
        s1 = self.xor_bytes(self.derived_key, self.opad)
        s2 = self.xor_bytes(self.derived_key, self.ipad)
        h1 = hashlib.sha256()
        h1.update(s2)
        h1.update(self.message)
        hash_s2_m = h1.digest().rjust(self.block_size, b'\0')
        h2 = hashlib.sha256()
        h2.update(s1)
        h2.update(hash_s2_m)
        return h2.digest()


        


hmac = HMAC_SHA_256("key", "The quick brown fox jumps over the lazy dog")
authentication_tag = hmac.compute()
print(authentication_tag.hex())

