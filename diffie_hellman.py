"""
Diffie-hellman key exchange algorithm is cryptographic algorithm based on the discrete logarithm problem.

Given 3 ** e mod n = m. As the value of n gets larger it becomes increasingly hard to get the value of e that resulted in a known m. 
That's the discrete logarithm problem. For sufficiently large prime n, a super computer can't get the value of e.

This is why the Diffie-hellman key exchange is simple and powerful at the same time.
"""

class DHKE:

    """
    Steps:
        1. Choose a large prime `n`. The modulus
        2. Choose a generator g
        3. Share publicly
        4. The sender generates a private key using a good random number generator denoted as `a`
        5. The receiver generates a private key using a good random number generator denoted as `b`
        6. The sender computes g ** a mod n and sends publicly to the receiver. Denoted as A
        7. The receiver computes g ** b mod n and sends publicly to the sender. Denoted as B
        8. The sender computes B ** a mod n and arrives at a secret S_1
        9. The receiver computes A ** a mod n and arrives at a secret S_2
        10. S_1 and S_2 should be equal making it the shared secret
    """

    # Public values
    g: int # generator
    n: int # modulus

    # Private values
    a: int # sender private value
    b: int # receiver private value

    def __init__(self, generator: int, modulus: int) -> None:
        self.g = generator
        self.n = modulus

    def compute_public_key(self, private_key: int) -> int:
        return (self.g ** private_key) % self.n
    
    def compute_shared_secret(self, private_key: int, public_key: int) -> int:
        return (public_key ** private_key) % self.n
    
    
## USAGE(Note: for the sake of speed, I am using small prime numbers)
generator = 5
modulus = 99347

dfhe = DHKE(generator, modulus)

sender_private_key = 20551
receiver_private_key = 28663

sender_public_key = dfhe.compute_public_key(sender_private_key)
receiver_public_key = dfhe.compute_public_key(receiver_private_key)

sender_shared_secret = dfhe.compute_shared_secret(sender_private_key, receiver_public_key)
receiver_shared_secret = dfhe.compute_shared_secret(receiver_private_key, sender_public_key)

assert(sender_shared_secret == receiver_shared_secret)