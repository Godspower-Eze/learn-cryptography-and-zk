"""
This is an adaption of Trusted Setup using Mod (./basic_trusted_setup_mod.py) using Elliptic Curve Cryptography

Check out Trusted Setup using Mod (./basic_trusted_setup_mod.py) for detailed explanations
"""

import collections

from utils.ecc import ECC
from utils.number_theory import generate_random_prime


class TrustedSetup_ECC(ECC):

    d = None  # degree
    g = None  # generator
    # values of encrypted exponents of x and encrypted exponents of x times a
    # computed by the first party
    base_crs: (list[int], list[int]) = None

    def __init__(self, curve, d: int, x: int, a: int) -> None:
        super().__init__(curve)
        self.d = d
        self.g = curve.g
        encrypted_values_of_f = [
            self.scalar_multiplication(
                x ** i,
                self.g) for i in range(
                0,
                d + 1)]
        encrypted_values_of_f_times_a = [
            self.scalar_multiplication(
                (x ** i) * a,
                self.g) for i in range(
                0,
                d + 1)]
        self.base_crs = (encrypted_values_of_f, encrypted_values_of_f_times_a)

    def compute_crs(self, x: int, a: int, crs: (
            list[int], list[int])) -> (list[int], list[int]):
        assert len(crs[0]) == self.d + 1, "wrong degree"
        assert len(crs[1]) == self.d + 1, "wrong degree"

        encrypted_values_of_f = crs[0]
        encrypted_values_of_f_times_a = crs[1]

        crs = ([self.scalar_multiplication(x, i) for i in encrypted_values_of_f], [
               self.scalar_multiplication(a, i) for i in encrypted_values_of_f_times_a])
        return crs


# USAGE

# Secret of First Participant
x = generate_random_prime(1, 0xffff)
a = generate_random_prime(1, 0xffff)

# Public
d = 3
g = 5

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

# Set the domain parameters specific to the curve

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

trusted_setup = TrustedSetup_ECC(curve, d, x, a)
crs = trusted_setup.base_crs

partipants = 10

for i in range(0, partipants):
    x = generate_random_prime(1, 0xffff)
    a = generate_random_prime(1, 0xffff)
    crs = trusted_setup.compute_crs(x, a, crs)

print("Common Reference String:", crs)
