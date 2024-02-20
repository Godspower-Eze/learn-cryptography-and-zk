from __future__ import annotations

from dataclasses import dataclass
from .fields import Fp, Fr
import copy


A = Fp(-5)

d_num = Fp(138827208126141220649022263972958607803)
d_den = Fp(171449701953573178309673572579671231137)
d_den.inv(d_den)

D = d_num * d_den


# Bandersnatch using affine co-ordinates
@dataclass
class BandersnatchAffinePoint():

    """
    An implementation of the bandersnatch curve point in affine coordinate.

    The bandersnatch curve is a twisted-edwards curve

    Bandersnatch paper: https://ia.cr/2021/1152
    """

    x: Fp
    y: Fp

    def __init__(self, gx: Fp, gy: Fp) -> None:
        if isinstance(gx, Fp) == False:
            raise Exception(
                "coordinates must have type basefield, please check the x coordinate")
        if isinstance(gy, Fp) == False:
            raise Exception(
                "coordinates must have type basefield, please check the y coordinate")

        self.x = gx
        self.y = gy
        if self.is_on_curve() == False:
            raise Exception("point not on curve")

    def generator():
        # Generator point was taken from the bandersnatch paper
        yTe = Fp(0x2a6c669eda123e0f157d8b50badcd586358cad81eee464605e3167b6cc974166)
        xTe = Fp(0x29c132cc2c0b34c5743711777bbe42f32b79c022ad998465e1e71866a252ae18)
        return BandersnatchAffinePoint(xTe, yTe)

    def neg(self, p: 'BandersnatchAffinePoint'):
        self.y = p.y
        self.x = -p.x

    def add(self, p: 'BandersnatchAffinePoint',
            q: 'BandersnatchAffinePoint') -> 'BandersnatchAffinePoint':
        """
        Formula:

            (x1, y1) + (x2, y2) = (((x1 * y2) + (y1 * x2)/(1 + D * x1 * x2 * y1 * y2)) , ((y1 * y2) - (A * x1 * x2)/(1 - D * x1 * x2 * y1 * y2)))

        Reference: "Twisted Edwards Curves Revisited" (https: // eprint.iacr.org/2008/522.pdf)
        """

        x1 = p.x
        y1 = p.y
        x2 = q.x
        y2 = q.y

        one = Fp.one()

        x1y2 = x1 * y2
        y1x2 = y1 * x2

        y1y2 = y1 * y2
        ax1x2 = x1 * x2 * A

        dx1x2y1y2 = x1y2 * y1x2 * D

        x_num = x1y2 + y1x2

        x_den = one + dx1x2y1y2

        y_num = y1y2 - ax1x2

        y_den = one - dx1x2y1y2

        x = x_num / x_den

        y = y_num / y_den

        self.x = x
        self.y = y

        return self

    def sub(self, p: 'BandersnatchAffinePoint',
            q: 'BandersnatchAffinePoint') -> 'BandersnatchAffinePoint':
        neg_q = -q
        self.add(p, neg_q)
        return self

    def double(
            self,
            p: 'BandersnatchAffinePoint') -> 'BandersnatchAffinePoint':
        """
        Formula:

            2(x1, y1) = ((2(x1 * y1)) / ((y1 ** 2) + (A(x1 ** 2))) , ((((y1 ** 2) - A(x1 ** 2)) / (2 - (y1 ** 2) - A(x1 ** 2))))

        Reference: "Twisted Edwards Curves Revisited" (https: // eprint.iacr.org/2008/522.pdf)
        """

        x1 = p.x
        y1 = p.y

        two = Fp(2)

        x1y1 = x1 * y1

        x1y1_2 = two * x1y1

        y1_exp_2 = y1.exp(2)

        x1_exp_2 = x1.exp(2)

        a_x1_exp_2 = A * x1_exp_2

        x2 = x1y1_2 / (y1_exp_2 + a_x1_exp_2)

        y2 = (y1_exp_2 - a_x1_exp_2) / (two - y1_exp_2 - a_x1_exp_2)

        self.x = x2
        self.y = y2

        return self

    def is_on_curve(self):
        """
        To check if a point is on the curve, we check that the lhs of the equation below is equal to it's rhs:

            A(x ** 2) + y ** 2 = 1 + D(x ** 2)(y ** 2)

        """

        x_exp_2 = self.x.exp(2)
        y_exp_2 = self.y.exp(2)

        dxy_sq = x_exp_2 * y_exp_2 * D
        a_x_sq = A * x_exp_2

        one = Fp.one()

        rhs = one + dxy_sq
        lhs = a_x_sq + y_exp_2

        return lhs == rhs

    def to_bytes(self):

        # This is here to test that we have the correct generator element
        # banderwagon uses a different serialisation algorithm

        mCompressedNegative = 0x80
        mCompressedPositive = 0x00

        x_bytes = bytearray(self.x.to_bytes())

        mask = mCompressedPositive
        if self.y.lexographically_largest():
            mask = mCompressedNegative

        x_bytes[31] |= mask

        return bytes(x_bytes)

    def from_bytes(self):
        # This is not needed, see `to_bytes`
        return NotImplemented

    def dup(self) -> 'BandersnatchAffinePoint':
        return copy.deepcopy(self)

    def scalar_mul(self, point: 'BandersnatchAffinePoint',
                   scalar: Fr) -> 'BandersnatchAffinePoint':
        """
        Using Double and Add : https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        """

        scalar_bits = format(scalar.value, 'b')

        result = BandersnatchAffinePoint.identity()
        temp = point.dup()

        num_bits = len(scalar_bits)

        for i in reversed(range(num_bits)):
            if scalar_bits[i] == str(1):
                result.add(result, temp)
            temp.double(temp)

        self.x = result.x
        self.y = result.y

        return self

    def identity() -> 'BandersnatchAffinePoint':
        zero = Fp.zero()
        one = Fp.one()
        return BandersnatchAffinePoint(zero, one)

    def get_y_coordinate(x, return_positive_y):

        one = Fp.one()

        num = x * x

        den = (num * D) - one

        num = (num * A) - one

        y = num / den  # y^2

        # This can only be None if the denominator is zero
        if y is None:
            return None

        y.sqrt(y)
        # This means that the square root does not exist
        if y is None:
            return None

        is_largest = y.lexographically_largest()
        if return_positive_y == is_largest:
            return y
        else:
            return -y

    # Method overloads
    def __add__(self, other):
        result = BandersnatchAffinePoint.identity()
        result.add(self, other)
        return result

    def __sub__(self, other):
        result = BandersnatchAffinePoint.identity()
        result.sub(self, other)
        return result

    def __neg__(self):
        result = BandersnatchAffinePoint.identity()
        result.neg(self)
        return result

    def __mul__(self, other):
        if isinstance(other, Fr) == False:
            raise TypeError(
                "[additive notation]: can only multiply a point by a scalar")
        result = BandersnatchAffinePoint.generator()
        result.scalar_mul(self, other)
        return result

    def __eq__(self, other):
        if isinstance(other, BandersnatchAffinePoint):
            return self.x == other.x and self.y == other.y
        raise TypeError("can only check if a Point is equal to a Point")


@dataclass
class BandersnatchExtendedPoint():
    x: Fp
    y: Fp
    t: Fp
    z: Fp

    def __init__(self, affine_point: BandersnatchAffinePoint) -> None:
        self.x = affine_point.x
        self.y = affine_point.y
        self.t = affine_point.x * affine_point.y
        self.z = Fp.one()
        pass

    def identity():
        affine_point = BandersnatchAffinePoint.identity()
        return BandersnatchExtendedPoint(affine_point)

    def generator():
        affine_point = BandersnatchAffinePoint.generator()
        return BandersnatchExtendedPoint(affine_point)

    def neg(self, p):
        self.x = -p.x
        self.y = p.y
        self.t = -p.t
        self.z = p.z

    def is_zero(self):
        """
        Identity is {x=0, y=1, t = 0, z =1}
        The equivalence class is therefore is {x=0, y=k, t = 0, z=k} for all k where k!=0
        """

        condition_1 = self.x.is_zero()
        condition_2 = self.y == self.z
        condition_3 = not self.y.is_zero()
        condition_4 = self.t.is_zero()

        return condition_1 and condition_2 and condition_3 and condition_4

    def equal(p: BandersnatchExtendedPoint, q: BandersnatchExtendedPoint):
        if p.is_zero():
            return q.is_zero()

        if q.is_zero():
            return False

        return (p.x * q.z == p.z * q.x) and (p.y * q.z == q.y * p.z)

    def add(self, p, q):
        # See "Twisted Edwards Curves Revisited" (https: // eprint.iacr.org/2008/522.pdf)
        # by Huseyin Hisil, Kenneth Koon-Ho Wong, Gary Carter, and Ed Dawson
        # 3.1 Unified Addition in E^e

        x1 = p.x
        y1 = p.y
        t1 = p.t
        z1 = p.z

        x2 = q.x
        y2 = q.y
        t2 = q.t
        z2 = q.z

        a = x1 * x2

        b = y1 * y2

        c = D * t1 * t2

        d = z1 * z2

        h = b - (a * A)

        e = (x1 + y1) * (x2 + y2) - a - b

        f = d - c

        g = d + c

        self.x = e * f
        self.y = g * h
        self.t = e * h
        self.z = f * g

        return self

    def sub(self, p, q):
        neg_q = -q
        self.add(p, neg_q)
        return self

    def double(self, p):
        # TODO: can replace this with dedicated doubling formula
        return self.add(p, p)

    def scalar_mul(self, point, scalar: Fr):
        # Same as AffinePoint's equivalent method
        # using double and add :
        # https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        scalar_bits = format(scalar.value, 'b')

        result = BandersnatchExtendedPoint.identity()
        temp = point.dup()

        num_bits = len(scalar_bits)

        for i in reversed(range(num_bits)):
            if scalar_bits[i] == str(1):
                result.add(result, temp)
            temp.double(temp)

        self.x = result.x
        self.y = result.y
        self.t = result.t
        self.z = result.z

        return self

    def to_affine(self):
        if self.is_zero():
            return BandersnatchAffinePoint.identity()
        elif self.z.is_one():
            return BandersnatchAffinePoint(self.x, self.y)
        else:
            assert self.z.is_zero() == False
            z_inv = Fp.zero()
            z_inv.inv(self.z)

            x_aff = self.x * z_inv
            y_aff = self.y * z_inv
            return BandersnatchAffinePoint(x_aff, y_aff)

    # Only used for testing purposes.
    def to_bytes(self):
        return self.to_affine().to_bytes()

    def dup(self):
        return copy.deepcopy(self)

    # Method overloads

    def __add__(self, other):
        result = BandersnatchExtendedPoint.identity()
        result.add(self, other)
        return result

    def __sub__(self, other):
        result = BandersnatchExtendedPoint.identity()
        result.sub(self, other)
        return result

    def __neg__(self):
        result = BandersnatchExtendedPoint.identity()
        result.neg(self)
        return result

    def __mul__(self, other):
        if isinstance(other, Fr) == False:
            raise TypeError(
                "[additive notation]: can only multiply a point by a scalar")
        result = BandersnatchExtendedPoint.generator()
        result.scalar_mul(self, other)
        return result

    def __eq__(self, other):
        if isinstance(other, BandersnatchExtendedPoint):
            return BandersnatchExtendedPoint.equal(self, other)
        raise TypeError("can only check if a Point is equal to a Point")
