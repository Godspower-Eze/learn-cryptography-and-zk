"""
Check out the ECDH implementation (./ecdh.py) to understand this section better.

ECDSA (Elliptic Curve Digital Signature Algorithm) is a type of digital signature algorithm. 

A digital signature is a signature that was cryptographically signed. Others are able to
verify without reasonable doubt that you are the signer without knowing the private key you
used in signing it.

ECDSA is a built on the power of Elliptic Curve Cryptography; its discrete logarithm problem precisely.

This is the used in the Bitcoin blockchain.
"""

import collections
import random

from ecc.ecdh import ECC, gcd_by_eea

class ECDSA(ECC):

    """
    Steps:
        To Sign:
            1. Choose a random integer between k, 1 <= k <= n - 1. Recall that `n` is order of the generator point `G`. See (./ecdh.py)

            2. Compute (x1, y1) = kG. That is, a scalar multiplication of k and the generator point `G`. We need only x1.
            
               Ideally, we would hash x1 and use a standard like ANSI X9.62 to convert it to an integer but for the sake of simplicity, 
               we will use it as is.

            3. Compute r = x1 mod n. If r is equals to 0, then we would have to restart the process.

            4. Compute the multiplicative inverse of k mod n. we would call it `kmi`

            5. We bring in our message `m`. The message should be known by the verifier
            
               Ideally, we should hash our message and convert to an integer because it's not practical to use the message as it is in the real world. 

               Messages could have arbitrary length and size so it might not be compatible with the domain parameters of the curve. 
               That's why it been hashed and converted to an integer.
               
               But, for the sake of simplicity we would use it as it is.

            6. Compute s = (kmi * (m + dr)) mod n. If s is 0 then go back to step 1. `d` is the signer's private key

            7. r ans s are the signature for the signer's message `m` and they are shared with the verifier along the signer's public key `q`

        To Verify:
            1. Verify that r and s are integers in the interval [1, n-1]

            2. Compute the multiplicative inverse of s mod n and we will call it `smi`

            3. Compute u = (m * smi) mod n and w = (r * smi) mod n

            4. Compute (x2, y2) = uG + wQ

            5. If (x2, y2) is equal to the `point at infinity`, then reject the signature. Otherwise,
               compute v = x2 mod n.
            
            6. If v == r, then the signature is valid
    """

    def generate_random_number(self) -> int:
        return random.randrange(1, self.curve.n - 1)
    
    """
    SIGNING
    """

    def compute_r(self, k: int) -> int:
        x1, _ = self.scalar_multiplication(k, self.curve.g)
        r = x1 % self.curve.n
        if r == 0:
            raise Exception("Invalid r value. Choose another random number")
        return r
    
    def compute_s(self, r:int, k: int, m: int, d: int) -> int:
        kmi = gcd_by_eea(k, self.curve.n)[-1][8] # multiplicative inverse mod n
        s = (kmi * (m + (d * r))) % self.curve.n
        if s == 0:
            raise Exception("Invalid s value. Choose another random number")
        return s
    
    """
    VERIFICATION
    """

    def verify(self, m: int, r: int, s: int, q: tuple[int, int]):

        if r not in range(1, self.curve.n) or s not in range(1, self.curve.n):
            return False
        
        smi = gcd_by_eea(s, self.curve.n)[-1][8] % self.curve.n # multiplicative inverse mod n
        u1 = (m * smi) % self.curve.n
        u2 = (r * smi) % self.curve.n
        y = self.point_addition(self.scalar_multiplication(u1, self.curve.g), self.scalar_multiplication(u2, q))
        if y == self.point_at_infinity:
            raise Exception("Invalid signature")
        x2 = y[0]
        v = x2 % self.curve.n
        return v == r

    
## USAGE

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

## Set the domain parameters specific to the curve

curve = EllipticCurve(
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    # Subgroup cofactor.
    h=1,
)

ecdsa = ECDSA(curve)

private_key, public_key = ecdsa.generate_key_pair()

message = 22

## Generate random number `k`
k = ecdsa.generate_random_number()

## Compute `r`
r = ecdsa.compute_r(k)

## Compute `s`
s = ecdsa.compute_s(r, k, message, private_key)

## Verify signature
verification_status = ecdsa.verify(message, r, s, public_key)
assert(verification_status)