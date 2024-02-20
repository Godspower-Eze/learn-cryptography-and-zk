"""
Polynomial Commitments are increasingly being used in Modern Cryptography. Especially in zero knowledge cryptography

Why Polynomials?

    Polynomials have some unique properties that makes them suitable for vector commitment(see /pedcomm_mod.py) so instead of committing to a set of values,
    the values are converted into polynomials using interpolation and we commitment to the polynomials instead.

    The basic idea behind polynomial commitments is that a prover is trying to convince a verifier that they know a polynomial (a set of values) of a certain degree

What does it mean to know a polynomial?

    Given a polynomial:
        f(x) = (c_0 * (x ** 0)) + (c_1 * (x ** 1)) + .... + (c_d * (x ** d))

        where:
            `d` is the degree of the polynomial

            `c_i` is the coefficient of the polynomial

            `x` is the variable

    The knowledge of a polynomial simply means that you know the set of coefficients (c_i) of a polynomial of degree d

A Polynomial can also be represented as a product of its factors (roots). Like so:

    f(x) = (x - a_0)(x - a_1)....(x - a_n)

    For example:
        (x ** 3) - 3(x ** 2) + 2x = (x - 0)(x - 1)(x - 2)

    This can also be called the factorization or factorized form of the polynomial.

    Note that these factors are unique together and that's one the properties that makes it polynomials suitable for cryptography

Using the example above,

    (x - 1) and (x - 2) are cofactors of the polynomials. Hence:

        f(x) = (x ** 3) - 3(x ** 2) + 2x

        t(x) = (x - 1)(x - 2) (also called the target polynomial)

        h(x) = (x - 0)

        f(x) / t(x) = h(x)


Hence, if the prover wants to prove that indeed his polynomial has those roots without disclosing the polynomial itself,
he needs to prove that his polynomial f(x) is the multiplication of those cofactors t(x) and the polynomial h(x) i.e f(x) = t(x) * h(x)

Let's look at a simple polynomial commitment scheme:

    1. The verifier samples a random value x.

    2. Evaluates t(x)

    3. Gives x to the prover.

    4. The prover computes f(x)/t(x) using polynomial division to get h(x)

    5. The prover evaluates f(x) and h(x) and sends the values to the verifier

    6. If t(x) * h(x) is equal to f(x) the verifier can say the prover knows the polynomial

You immediately see the problem with the scheme above:

    1. x is public

    2. The prover can look for other ways to get f(x) and h(x) without using a polynomial

    3. The prover can use another polynomial entirely with a different degree and still convince the verifier

Let's fix the above protocol:

    Recall,

        1. (g ** x) * a = g ** (x * a)

        2. (g ** x) * (g ** a) = g ** (x + a)

        Using this, we can create a protocol where the prover is able to perform computation on encrypted values. For multiplication, the first and for
        addition the second is used.

        All multiplication and addition would be done in this form.

        See new protocol below

    Steps:

        Verifier:

            1. Pick a generator `g` from a cryptographic group (a group where discrete log is hard) and this group has a modulus `n`

            2. Pick a random value `x` and another random value `a`

            3. Instead of sending x to the prover, the verifier computes ((g ** (x ** 0)) mod n) up to ((g ** (x ** d)) mod n) and
            also ((g ** ((x ** 0) * a)) mod n) up to ((g ** ((x ** d) * a)) mod n)

            4. We now have the encrypted exponents of x: [((g ** (x ** 0)) mod n), ((g ** (x ** 1)) mod n), ..., ((g ** (x ** d)) mod n)] and
            the encrypted exponents of x times a: [((g ** (x ** 0) * a) mod n), ((g ** (x ** 1) * a) mod n), ..., ((g ** (x ** d) * a) mod n)].
            These would help us hide x and also check that right polynomial is used respectively. And, these are sent to the prover

            5. The verifier computes t(x) (unencrypted)

        Prover:

            1. Gets the encrypted values from the verifier (encrypted exponents of `x` and encrypted exponents of `x times a`)

            2. The prover computes `f(x)`/`t(x)` using polynomial division to get `h(x)`

            3. Uses the encrypted values to compute `f(x)`, `f(x) times a`, and `h(x)`. For brevity, let represent `f(x) times a` as `f(x)'`. Sends to the verifier

            Reminder: the prover doesn't know x and a

        Verifier:

            The verifier checks two things: the usage of the right polynomial and also the knowledge of the polynomial

            Check for correct polynomial:

                1. Computes `f(x) times a` and check that it's equal to the one sent by the prover by the prover `f(x)'`.

                2. If 1 is true, then the prover used the right polynomial

            Check for knowledge of polynomial:

                1. Check that `f(x)` is equal to `h(x)` * `t(*)`

                2. If 1 is true, then the prover used the right polynomial

    There are obviously improvements to this but this is enough to give fundamental information how polynomial commitments scheme work.

    This is implemented below.
"""

from numpy.polynomial.polynomial import polydiv

from utils.number_theory import generate_random_prime


class PolyComm_Mod:

    d = None  # degree
    g = None  # generator
    n = None  # modulus

    def __init__(self, d: int, g: int, n: int) -> None:
        self.d = d
        self.g = g
        self.n = n

    def __encrypted_product__(self, values: list[int]):
        assert len(values) == self.d + 1, "wrong degree"

        multiple = 1
        for i in values:
            multiple = (multiple * i) % self.n
        return multiple

    def __unencrypted_summation__(self, values: list[int]):
        assert len(values) == self.d + 1, "wrong degree"

        sum = 0
        for i in values:
            sum = (sum + i)
        return sum

    """
    VERIFIER
    """

    def setup(self,
              x: int,
              a: int,
              t_of_x: list[int]) -> (list[int],
                                     list[int],
                                     int):

        assert len(t_of_x) == self.d + 1, "wrong degree"

        # [((g ** (x ** 0)) mod n), ((g ** (x ** 1)) mod n), ..., ((g ** (x ** d)) mod n)]
        encrypted_terms = []

        for i in range(0, self.d + 1):
            value = pow(self.g, x ** i, self.n)
            encrypted_terms.append(value)

        # [((g ** (x ** 0) * a) mod n), ((g ** (x ** 1) * a) mod n), ..., ((g ** (x ** d) * a) mod n)]
        encrypted_terms_with_a = []
        for i in range(0, self.d + 1):
            value = pow(self.g, (x ** i) * a, self.n)
            encrypted_terms_with_a.append(value)

        t_at_x = []
        for i in range(0, self.d + 1):
            value = t_of_x[i] * (x ** i)
            t_at_x.append(value)

        eval_of_t_at_x = self.__unencrypted_summation__(t_at_x)

        return encrypted_terms, encrypted_terms_with_a, eval_of_t_at_x

    def check_polynomial(self, a: int, eval_of_f: int,
                         eval_of_f_prime: int) -> bool:
        return pow(eval_of_f, a, self.n) == eval_of_f_prime

    def check_knowledge_of_polynomial(
            self,
            eval_of_h: int,
            eval_of_t: int,
            eval_of_f: int) -> bool:
        return pow(eval_of_h, eval_of_t, self.n) == eval_of_f

    """
    PROVER
    """

    def evaluate(self,
                 encrypted_terms: list[int],
                 encrypted_terms_with_a: list[int],
                 f_of_x: list[int],
                 t_of_x: list[int]) -> (int,
                                        int,
                                        int):

        assert len(encrypted_terms) == self.d + 1, "wrong degree"
        assert len(encrypted_terms_with_a) == self.d + 1, "wrong degree"
        assert len(f_of_x) == self.d + 1, "wrong degree"
        assert len(t_of_x) == self.d + 1, "wrong degree"

        # f(x) / t(x) using polynomial division
        quotient, _ = polydiv(f_of_x, t_of_x)
        # Convert from numpy.float to float
        quotient = [float(i) for i in quotient]
        len_of_quotient = len(quotient)

        # Padding the quotient array to be of length `d`

        if len_of_quotient != self.d:
            diff = self.d - len_of_quotient
            padding = [0.0 for _ in range(0, diff + 1)]
            quotient = quotient + padding
        h_of_x = quotient

        evals_of_f = [pow(i, j, self.n)
                      for i, j in zip(encrypted_terms, f_of_x)]
        eval_of_f = self.__encrypted_product__(evals_of_f)

        evals_of_f_prime = [pow(i, j, self.n)
                            for i, j in zip(encrypted_terms_with_a, f_of_x)]
        eval_of_f_prime = self.__encrypted_product__(evals_of_f_prime)

        evals_of_h = [pow(i, int(j), self.n)
                      for i, j in zip(encrypted_terms, h_of_x)]
        eval_of_h = self.__encrypted_product__(evals_of_h)

        return (eval_of_f, eval_of_f_prime, eval_of_h)


# USAGE

# f(x) = (x ** 3) - 7x - 6
# factorised form of f(x) = (x + 1)(x + 2)(x - 3)
# t(x) = (x + 1)(x + 2) = (x ** 2) + 3x + 2
# h(x) = (x - 3)

# Secret
x = generate_random_prime(1, 0xffff)
a = generate_random_prime(1, 0xffff)

# Public
d = 3
g = 5
n = 11


poly_mod = PolyComm_Mod(d, g, n)

# SETUP (By Verifier)
encrypted_terms, encrypted_terms_with_a, eval_of_t = poly_mod.setup(x, a, [
                                                                    2, 3, 1, 0])

# EVALUATION (By Prover)
coefficients_of_f = [-6, -7, 0, 1]
coefficients_of_t = [2, 3, 1, 0]

eval_of_f, eval_of_f_prime, eval_of_h = poly_mod.evaluate(
    encrypted_terms, encrypted_terms_with_a, coefficients_of_f, coefficients_of_t)

# CHECKING POLYNOMIAL FOR CORRECT POLYNOMIAL (By Verifier)
status = poly_mod.check_polynomial(a, eval_of_f, eval_of_f_prime)
assert (status)

# CHECKING POLYNOMIAL FOR KNOWLEDGE OF POLYNOMIAL (By Verifier)
status = poly_mod.check_knowledge_of_polynomial(
    eval_of_h, eval_of_t, eval_of_f)
assert (status)
