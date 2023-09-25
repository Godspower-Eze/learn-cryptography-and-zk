"""
In our implementations of a Basic Polynomial Commitments; using Modular Exponentiation (./basic_polynomial_comm_using_mod.py) and
using Elliptic Curve Cryptography(./basic_polynomial_comm_using_ecc.py) we had a setup phase where the verifier computed the encrypted values 
to be used by the prover.

There's a problem with this. We have to trust the verifier. In a situation where the proof by the prover would be used 
by multiple verifiers, then it's flawed.

The idea is that the secrets been used in creating the encrypted values would be discarded after the setup but is it possible to
confirm this? I doubt.

How do we solve this?

    Instead of depending on one party to produce the encrypted values, we depend on multiple parties and this process is called
    the `Trusted Setup`.

    Instead of us trusting one party to throw away their secret, we can have multiple parties participate and for it be truly secure
    only one party has to discard their secrets and this pretty normal in distributed systems like the blockchain.

    The final encrypted values gotten in this process is called the Common Reference String (CRS). 
    You might also hear another variation of this called a Structured Reference String (SRS).

How does this work?

    We are building on the concepts explained in Basic Polynomial Commitments; using Modular Exponentiation (./basic_polynomial_comm_using_mod.py).
    Check it out for clarity.

    Steps:

        1. Pick a generator `g` from a cryptographic group

        2. Pick a random value `x` and another random value `a` 

        3. Computes encrypted exponents of x: [((g ** (x ** 0)) mod n), ((g ** (x ** 1)) mod n), ..., ((g ** (x ** d)) mod n)] and 
           the encrypted exponents of x times a: [((g ** (x ** 0) * a) mod n), ((g ** (x ** 1) * a) mod n), ..., ((g ** (x ** d) * a) mod n)]. 
           For brevity, we will represent the encrypted exponents of x as `g ** x_i` and encrypted exponents of x times a as `g ** (x_i * a)`

        4. Discards `x` and `a` and sends the encrypted values to the next party.

        5. The next party picks a random value `x_2` and another random value `a_2` and computes `(g ** x_i) ** x_2` and `(g ** x_i) ** (x_2 * a_2`

        6. The continues till all participant have `slapped` their values of `x` and `a` on the encrypted values.

    This is implemented below.

Can we integrate this to our Polynomial Commitment or create a Polynomial Commitment that does?

    The short answer is YES.

    The long answer is NO because in our implementation, the `setup` takes the secrets `x` and `a` and it need for verification 
    and for us to implement one that supports trusted setup we need to use cryptographic pairings. We would be dealing with strictly encrypted values and there's a 
    limitation on the operations you can perform on encrypted values using modular operations (same for the elliptic curve implementation).

    I would come back to this when I understand pairings 🤞🏾
"""

import random

from .basic_polynomial_comm_using_mod import PolyComm_Mod
from utils.number_theory import generate_random_prime


class TrustedSetup_Mod:

    d = None # degree
    g = None # generator
    n = None # modulus
    base_crs: (list[int], list[int]) = None # values of encrypted exponents of x and encrypted exponents of x times a computed by the first party

    def __init__(self, g: int, d: int, n: int, x: int, a: int) -> None:
        self.d = d
        self.g = g
        self.n = n
        encrypted_values_of_f = [pow(self.g, x ** i, self.n) for i in range(0, d + 1)]
        encrypted_values_of_f_times_a = [pow(self.g, (x ** i) * a, self.n) for i in range(0, d + 1)]
        self.base_crs = (encrypted_values_of_f, encrypted_values_of_f_times_a)

    def compute_crs(self, x: int, a: int, crs: (list[int], list[int])) -> (list[int], list[int]):
        assert len(crs[0])  == self.d + 1, "wrong degree"
        assert len(crs[1])  == self.d + 1, "wrong degree"

        encrypted_values_of_f = crs[0]
        encrypted_values_of_f_times_a = crs[1]

        crs = ([pow(i, x, self.n) for i in encrypted_values_of_f], [pow(i, a, self.n) for i in encrypted_values_of_f_times_a])
        return crs


#### USAGE

## Secret of First Participant
x = generate_random_prime(1, 0xffff)
a = generate_random_prime(1, 0xffff)

## Public
d = 3
g = 5
n = 11

trusted_setup = TrustedSetup_Mod(g, d, n, x, a)
crs = trusted_setup.base_crs

partipants = 100

for i in range(0, partipants):
    x = generate_random_prime(1, 0xffff)
    a = generate_random_prime(1, 0xffff)
    crs = trusted_setup.compute_crs(x, a, crs)

print("Common Reference String:", crs)


