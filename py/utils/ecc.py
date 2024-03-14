"""
Recall that the security of Diffie-Hellman lies in the fact that given m ** e mod n = c, it's hard to find `e` for
a sufficiently large `n` and we called this the discrete logarithm problem. Well, elliptic curves give us another
form of a discrete logarithm problem.

For an elliptic curve over a finite field in the form y**2 mod p = (x**3 + ax + b) mod p.
Given a base point (generator) with symbol G: (x, y) on the curve, if the base point is added by itself `z` times and resulting in a new point A = zG.

It turns out that finding `z` when A and G are known is a harder discrete logarithm problem with an even lesser value of `n.`

Every cryptographic elliptic curve has public parameters (domain parameters) and in this implementation, we would use the secp256k1 curve used in Bitcoin.
Its domain parameters are listed below:

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

    `n` is the order of the generator point `G`. That is the smallest positive integer such that nG equals to the identity element.
        The identity element of an elliptic curve is the point at infinity, a line that cuts only two points vertically.

        To verify this, perform a scalar multiplication (see below) of `n` and `G` you should get the point at infinity

        Research on `order of an element in a group` to learn more.

    `h` is the ratio of the number of points on the curve and n, ideally 1.
"""

import random

from .number_theory import gcd_by_eea


class ECC:

    """
    Steps:
        1. Choose an elliptic curve. E.g secp256k1, curve25519
        2. Alice generates key pair and shares the public key with Bob
        3. Bob generates key pair and shares the public key with Bob
        4. Alice performs a scalar multiplication using her private key and Bob's public key to get a secret key
        4. Bob performs a scalar multiplication using her private key and Alice's public key to the same secret key
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
        return (y ** 2) % self.curve.p == ((x ** 3) + \
                (self.curve.a * x) + self.curve.b) % self.curve.p

    def slope_for_point_addition(self, x1: int, x2: int, y1: int, y2: int):
        """
        To get the slope when solving for point addition:
            s = ((y2 - y1)/(x2 - x1)) mod p

        But, to avoid getting decimal values, we would do this instead:
            s = (((y2 - y1) mod p)) * (((x2 - x1) ** -1) mod p) mod p

            We converted the divisor to its multiplicative inverse mod p
            multiplied it by the dividend mod p
        """

        dividend = (y2 - y1) % self.curve.p
        divisor = (x2 - x1) % self.curve.p
        # multiplicative inverse mod p
        mi = gcd_by_eea(divisor, self.curve.p)[-1][8] % self.curve.p
        return (dividend * mi) % self.curve.p

    def slope_for_point_doubling(self, x1: int, y1: int):
        """
        To get the slope when solving for point doubling:
            s = ((3 * (x1 ** 2) + a)/2y1) mod p

        But, to avoid getting decimal values just like above, we would do this instead:
            s = (((3 * (x1 ** 2) + a) mod p) * ((2y1) ** -1) mod p) mod p
        """

        dividend = ((3 * (x1 ** 2)) + self.curve.a) % self.curve.p
        divisor = (2 * y1) % self.curve.p
        # multiplicative inverse mod p
        mi = gcd_by_eea(divisor, self.curve.p)[-1][8] % self.curve.p
        return (dividend * mi) % self.curve.p

    def point_addition(self, a: tuple[int, int]
                       | str, b: tuple[int, int] | str):

        assert self.is_on_curve(a)
        assert self.is_on_curve(b)

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
        assert self.is_on_curve(new_point)

        return new_point

    def scalar_multiplication(self, z: int, point: tuple[int, int] | str):
        """
        A=zG computed using the double and add algorithm (https://www.youtube.com/watch?v=5ITRACsmCvQ).
        Where z is the multiple and G is the `point` argument
        """

        assert self.is_on_curve(point)

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

        assert self.is_on_curve(result)

        return result

    def generate_key_pair(self) -> (int, int):
        """
        Generates a random private-public key pair
        """

        private_key = random.randrange(1, self.curve.n)
        public_key = self.scalar_multiplication(private_key, self.curve.g)
        return (private_key, public_key)
