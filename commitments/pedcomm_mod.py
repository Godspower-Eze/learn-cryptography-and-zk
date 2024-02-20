"""
A commitment scheme is a technique for committing to values to be verified at a later time.

It's like an sealed envelope. You put a value inside and send to a verifier. The verifier shouldn't be able to see what
is contained inside (hiding) and at the time of opening the verifier showed to able to ascertain with all certainty
that the values contained hasn't been tampered with (binding).

hiding and binding are important properties of any commitment scheme.

Hashing is a common type of commitment. A Pedersen Commitment is also a type of commitment scheme.

There many different variation of a Pedersen Commitments. In this implementation, we would work on the most
common type which has to do with modular exponentiation. Others include using elliptic curve cryptography and using Inner Product Argument as the verification mechanism.

The strength of Pedersen commitments lies in the discrete log problem.

A unique property of Pedersen Commitments is its homomorphic property which simply means that the commitment of the addtion of
two messages m1 and m2 is equal to the multiplication of there individual commitments. That is,
    commit(m1) * commit(m2) = commit(m1 + m2)

A Pedersen Commitment can also be used as a Vector Commitment Scheme.

Vector Commitments Scheme are used to describe commitments that are perform on a set of values rather than a single value. Examples include Merkle Tries
and Polynomial Commitments(./polynomials/basic_polynomial_comm_using_mod)
"""

import random

from utils.number_theory import generate_random_prime


class Ped_Mod:

    """
    Steps:
        Verifier:
            Setup:
                1. Generate a large prime `q`
                2. Pick a generator `g` (a number in [1, q - 1])
                3. Pick a random number `s` in [1, q - 1] and compute `h` = ((g ** s) mod q)
                4. The values q, g and h are sent to the prover

            Opening:
                1. The prover sends the commitment `c`, message `m_i` and the random number `r_i`
                2. The verifier computes c_i = ((g ** m_i)(h ** r_i) mod q)
                3. If c is equal to c_i then the message is valid else it's not.
                4. Note: The message and the random number are denoted `m_i` and `r_i` respectively because of cases where
                   the prover is a malicious prover and (m, r) would not be equal to (m_i, r_i)

        Prover:
            1. message `m` in [1, q - 1]
            2. Pick a random number `r` in [1, q - 1]
            3. To get the commitment, compute `c` = ((g ** m)(h ** r) mod q)
            4. The commitment `c`, the message `m` and the random number `r` is sent to the verifier for opening
    """

    q = None
    g = None
    h = None

    def __init__(self, p) -> None:
        q = generate_random_prime(1, p)
        g = random.randrange(1, q - 1)
        s = random.randrange(1, q - 1)
        h = (g ** s) % q

        self.q = q
        self.g = g
        self.h = h

    def commit(self, m: int, q: int, g: int, h: int) -> (int, int, int):
        r = random.randrange(1, q - 1)
        c = ((g ** m) * (h ** r)) % q
        return (c, m, r)

    def open(self, m_i: int, c: int, *r_i) -> bool:
        sum = 0
        for i in r_i:
            sum += i

        c_i = ((self.g ** m_i) * (self.h ** sum)) % self.q
        return c == c_i

    def mul_comm(self, *c):
        mul = 1
        for j in c:
            mul *= j

        c_s = mul % self.q
        return c_s


# USAGE

# SETUP
p = 0xffff

ped_mod = Ped_Mod(p)

q = ped_mod.q
g = ped_mod.g  # generator
h = ped_mod.h

# CREATING A COMMITMENT

m = 500  # message
c, m, r = ped_mod.commit(m, q, g, h)

# VERIFYING A COMMITMENT

status = ped_mod.open(m, c, r)
assert (status)

# SHOWING THE HOMOMORPHIC PROPERTY OF PEDERSEN COMMITMENT

m1 = 100  # message 1
m2 = 200  # message 2
m3 = 200  # message 3
m4 = 200  # message 4
m5 = 200  # message 5

c1, m_1, r_1 = ped_mod.commit(m1, q, g, h)
c2, m_2, r_2 = ped_mod.commit(m2, q, g, h)
c3, m_3, r_3 = ped_mod.commit(m3, q, g, h)
c4, m_4, r_4 = ped_mod.commit(m4, q, g, h)
c5, m_5, r_5 = ped_mod.commit(m5, q, g, h)

comms_mul = ped_mod.mul_comm(c1, c2, c3, c4, c5)
m6 = m1 + m2 + m3 + m4 + m5

status = ped_mod.open(m6, comms_mul, r_1, r_2, r_3, r_4, r_5)
assert (status)
