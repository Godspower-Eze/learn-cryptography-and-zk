"""
Elliptic Curve Diffie-Hellman is more secure type of Diffie-Hellman using Elliptic Curves

Check out `utils/ecc.py` for more
"""

import collections

from utils.ecc import ECC

# USAGE

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

ecdh = ECC(curve)

# Alice Generates key pair and shares public key with bob
alice_private_key, alice_public_key = ecdh.generate_key_pair()

# Bob Generates key pair and shares public key with alice
bob_private_key, bob_public_key = ecdh.generate_key_pair()

# Alice computes the scalar multiplication of her private key and Bob's
# public key to get a shared secret
alice_shared_secret = ecdh.scalar_multiplication(
    alice_private_key, bob_public_key)

# Bob computes the scalar multiplication of his private key and Alice's
# public key to get a shared secret
bob_shared_secret = ecdh.scalar_multiplication(
    bob_private_key, alice_public_key)

# The both shared secret should be equal
assert (alice_shared_secret == bob_shared_secret)
