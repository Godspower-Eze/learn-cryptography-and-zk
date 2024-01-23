"""
HMAC(hash-based MAC) is a type of MAC(message authentication code) that uses hash functions.

A MAC is used for message authentication. It confirms the authenticity of a message and the sender of the message i.e, 
the message hasn't been modified and the sender hasn't been compromised.

HMAC achieves this using hash functions. 
"""

class HMAC_SHA_256:

    ipad = None
    opad = None

    def __init__(self, key: str, message: str) -> None:
        self.key = bytes.fromhex
        self.message = message

    def pad():
        pass


hmac = HMAC_SHA_256("God", "Help")