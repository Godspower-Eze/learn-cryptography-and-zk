"""
Elliptic Curve Diffie-Hellman is more secure type of Diffie-Hellman.

Recall that the security of Diffie-Hellman lies in the fact that given m ** e mod n = c, it's hard to find `e` for
a sufficiently large `n` and we called this the discrete logarithm problem. Well, elliptic curves gives us another 
form of a discrete logarithm problem.

For an elliptic curve over a finite field in the form y**2 mod p = (x**3 + ax + b) mod p. 
Given a base point (generator) with symbol G: (x, y) on the curve, if the base point is added by itself `z` times and resulting in a new point A = zG.

It turns out that finding `z` when A and G is known is a harder discrete logarithm problem with an even lesser value of `n.`

Every cryptographic elliptic curve has public parameters (domain parameters) and in this implementation we would be using the secp256k1 curve used in Bitcoin.
It's domain parameters are listed below:

    curve: y**2 = x**3 + 7
    p: 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    a: 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
    b: 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    G: (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
    n: 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    h: 0x1

    `p` is the prime of the curve and it would used as the modulus.
    `a` and `b` are constants
    `G` is the base point, generator and the starting point. It is the point on the curve where other points would be generated from.
        Either by addition or scalar multiplication.
    `n` is the order of the subgroup of Integers mod p. That is, the number of valid points in the curve when 
        the equation mod p (y**2 mod p = (x**3 + ax + b) mod p) is  used to check each point on the curve.
    `h` is the ratio of number of the points on the curve and n which is ideally 1.
"""

import collections
import random

from utils import gcd_by_eea

class ECDH:

    """
    Steps:
        1. Choose a elliptic curve. E.g secp256k1, curve25519
        2. Every curve has known domain parameters
    """

    curve = None
    point_at_infinity = "♾️"

    def __init__(self, curve) -> None:
        self.curve = curve

    def is_on_curve(self, point: tuple[int, int]):

        """
        We check if a point is on the curve using the condition:

        y**2 mod p == (x**3 + ax + b) mod p
        """
        
        if point == self.point_at_infinity:
            return self.point_at_infinity
        
        x, y = point
        return (y ** 2) % self.curve.p == ((x ** 3) + (self.curve.a * x) + self.curve.b) % self.curve.p


    def slope_for_point_addition(self, x1: int, x2: int, y1: int, y2: int):

        """
        To get the slope when solving for point addition:
            s = ((y2 - y1)/(x2 - x1)) mod p

        But, to avoid getting decimal values, we would do this instead:
            s = (((y2 - y1) mod p)) * (((x2 - x1) ** -1) mod p) mod p

            We basically converted the divisor to it's multiplicative inverse mod p
            multiplied it by the dividend mod p
        """

        dividend = (y2 - y1) % self.curve.p
        divisor = (x2 - x1) % self.curve.p
        mi = gcd_by_eea(divisor, self.curve.p)[-1][8] # multiplicative inverse mod p
        return (dividend * mi) % self.curve.p
    
    def slope_for_point_doubling(self, x1: int, y1: int):

        """
        To get the slope when solving for point doubling:
            s = ((3 * (x1 ** 2) + a)/2y1) mod p

        But, to avoid getting decimal values just like above, we would do this instead:
            s = (((3 * (x1 ** 2) + a) mod p) * ((2y1) ** -1) mod p) mod p
        """

        dividend = ((3 * (x1 ** 2)) + self.curve.a) % curve.p
        divisor = (2 * y1) % self.curve.p
        mi = gcd_by_eea(divisor, self.curve.p)[-1][8] # multiplicative inverse mod p
        return (dividend * mi) % self.curve.p


    def point_addition(self, a: tuple[int, int]| str, b: tuple[int, int] | str):

        x1 = a[0]
        x2 = b[0]
        y1 = a[1]
        y2 = b[1]
        
        if x1 == x2 and y1 != y2:

            """
            if x1 is equal to x2 and y1 and y2 are, then line between point `a` and point `b` 
            would be a vertical line heading towards infinity so we would return
            infinity as the new point
            """

            return self.point_at_infinity
        

        """
        The infinity point is the identity element of the elliptic curve group so 
        computing an addition operation on a point and the infinity returns the point.

        That is, (point `a` + infinity point = `a`)
        """

        if a == self.point_at_infinity and b != self.point_at_infinity:
            return b
        
        if b == self.point_at_infinity and a != self.point_at_infinity:
            return a
        
        if a == self.point_at_infinity and b == self.point_at_infinity:
            return self.point_at_infinity
        
        if x1 == x2:
            slope = self.slope_for_point_doubling(x1, y1)
        else:
            slope = self.slope_for_point_addition(x1, x2, y1, y2)

        x3 = ((slope ** 2) - a[0] - b[0]) % self.curve.p
        y3 = (slope * (x1 - x3) - y1) % self.curve.p
        new_point = (x3, y3)
        return new_point
    
    def scalar_multiplication(self, z: int, point: tuple[int, int]| str):
        
        """
        A=zG computed using the double and add algorithm (https://www.youtube.com/watch?v=5ITRACsmCvQ). 
        Where z is the multiple and G is the `point` argument
        """

        if z % self.curve.n == 0 or point == self.point_at_infinity:
            return self.point_at_infinity
        
        z = z % self.curve.n

        result = self.point_at_infinity
        addend = point

        while z:

            if z & 1:
                # Add
                result = self.point_addition(result, addend)
            # Double
            addend = self.point_addition(addend, addend)

            z >>= 1

        return result
    
    def generate_key_pair(self) -> (int, int):

        """
        Generates a random private-public key pair
        """

        private_key = random.randrange(1, self.curve.p)
        public_key = self.scalar_multiplication(private_key, self.curve.g)
        return (private_key, public_key)
            


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

ecdh = ECDH(curve)

## Alice Generates key pair and shares public key with bob
alice_private_key, alice_public_key = ecdh.generate_key_pair()

## Bob Generates key pair and shares public key with alice
bob_private_key, bob_public_key = ecdh.generate_key_pair()

## Alice computes the scalar multiplication of her private key and Bob's public key to get a shared secret
alice_shared_secret = ecdh.scalar_multiplication(alice_private_key, bob_public_key)

## Bob computes the scalar multiplication of his private key and Alice's public key to get a shared secret
bob_shared_secret = ecdh.scalar_multiplication(bob_private_key, alice_public_key)

## The both shared secret should be equal
assert(alice_shared_secret == bob_shared_secret)