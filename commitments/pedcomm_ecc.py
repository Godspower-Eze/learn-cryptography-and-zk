"""
This is an implementation of Pedersen Commitments using Elliptic Curves Operations

Check out implementations of Pedersen Commitments using Modular Exponentiation (./pedcomm_mod.py) and Elliptic Curve Cryptography (./utils/ecc.py)
"""

import random
import collections

from utils.ecc import ECC


class Ped_ECC(ECC):

    """
    Steps:
        Verifier:
            Setup:
                1. Get the order of the curve `q`
                2. Get the generator of the curve `g`
                3. Pick a random number `s` in [1, q - 1] and compute h = scalar_multiplication(s, g)
                4. The values q, g and h are sent to the prover
            
            Opening:
                1. The prover sends the commitment `c`, message `m_i` and the random number `r_i`
                2. The verifier computes `c_i` = point_addition(scalar_multiplication(m_i, g), scalar_multiplication(r_i, h))
                3. If c is equal to c_i then the message is valid else it's not.
                4. Note: The message and the random number are denoted `m_i` and `r_i` respectively because of cases where
                   the prover is a malicious prover and (m, r) would not be equal to (m_i, r_i)

        Prover:
            1. message `m` in [1, q - 1]
            2. Pick a random number `r` in [1, q - 1]
            3. To get the commitment, compute `c` = point_addition(scalar_multiplication(m, g), scalar_multiplication(r, h))
            4. The commitment `c`, the message `m` and the random number `r` is sent to the verifier for opening
    """
    
    def __init__(self, curve) -> None:
        super().__init__(curve)
        g = self.curve.g
        s = random.randrange(1, self.curve.n - 1)
        h = self.scalar_multiplication(s, g)

        self.q = self.curve.n
        self.g = g
        self.h = h

    def commit(self, m: int, q: int, g: tuple[int, int], h: tuple[int, int]) -> (int, int, int):
        r = random.randrange(1, q - 1)
        ag = self.scalar_multiplication(m, g)
        ah = self.scalar_multiplication(r, h)
        c = self.point_addition(ag, ah)
        return (c, m, r)
    
    def open(self, m_i: int, c: int, *r_i) -> bool :
        sum = 0
        for i in r_i:
            sum +=i

        ag_i = self.scalar_multiplication(m_i, g)
        ah_i = self.scalar_multiplication(sum, h)
        c_i = self.point_addition(ag_i, ah_i)
        return c == c_i
    
    def add_comm(self, *c):
        sum = self.point_at_infinity
        for j in c:
            sum = self.point_addition(sum, j)
        c_s = sum
        return c_s



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



## USAGE

# SETUP

ped_ecc = Ped_ECC(curve)

q = ped_ecc.q
g = ped_ecc.g # generator
h = ped_ecc.h

## CREATING A COMMITMENT

m = 500 # message
c, m, r = ped_ecc.commit(m, q, g, h)

## VERIFYING A COMMITMENT

status = ped_ecc.open(m, c, r)
assert(status)

#### SHOWING THE HOMOMORPHIC PROPERTY OF PEDERSEN COMMITMENT

m1 = 100 # message 1
m2 = 200 # message 2
m3 = 200 # message 3
m4 = 200 # message 4
m5 = 200 # message 5

c1, m_1, r_1 = ped_ecc.commit(m1, q, g, h)
c2, m_2, r_2 = ped_ecc.commit(m2, q, g, h)
c3, m_3, r_3 = ped_ecc.commit(m3, q, g, h)
c4, m_4, r_4 = ped_ecc.commit(m4, q, g, h)
c5, m_5, r_5 = ped_ecc.commit(m5, q, g, h)

comms_add = ped_ecc.add_comm(c1, c2, c3, c4, c5)
m6 = m1 + m2 + m3 + m4 + m5

status = ped_ecc.open(m6, comms_add, r_1, r_2, r_3, r_4, r_5)
assert(status)