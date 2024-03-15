import copy


class Field:

    """
    A generic implementation of a finite field
    """

    value: int = None
    modulus: int = None

    def __init__(self, value, modulus) -> None:
        self.value = value % modulus
        self.modulus = modulus

    def zero(modulus) -> 'Field':
        return Field(0, modulus)

    def one(modulus) -> 'Field':
        return Field(1, modulus)

    def is_constant(self, constant: int) -> bool:
        # Here we assume that the number has been reduced.
        # Which should be the case, if values are initialized using the
        # constructors
        return self.value == constant

    def is_zero(self) -> bool:
        return self.is_constant(0)

    def is_one(self) -> bool:
        return self.is_constant(1)

    def to_bytes(self, byte_length: int) -> bytes:
        return self.value.to_bytes(byte_length, byteorder='little')

    def from_bytes(bytes_little_endian: int, modulus: int) -> 'Field':
        """
        Return None if the bytes are not in canonical form.

        Canonical here means that the integer representation of the bytes must be
        between [0, modulus-1]
        """

        value = int.from_bytes(bytes_little_endian, byteorder='little')

        if value >= modulus:
            return None

        return Field(value, modulus)

    def from_bytes_reduce(bytes_little_endian: int, modulus: int) -> 'Field':
        value = int.from_bytes(
            bytes_little_endian, byteorder='little')
        return Field(value, modulus)

    def lexographically_largest(x: 'Field', q_min_one_div_2: int) -> bool:
        return x.value > q_min_one_div_2

    def string(self) -> str:
        return str(self.value)

    def add(self, a: 'Field', b: 'Field') -> 'Field':
        self._check_all_integers_same_modulus(a, b)
        self.value = (a.value + b.value) % self.modulus
        return self

    def sub(self, a: 'Field', b: 'Field') -> 'Field':
        self._check_all_integers_same_modulus(a, b)
        self.value = (a.value - b.value) % self.modulus
        return self

    def neg(self, a: 'Field') -> 'Field':
        self._check_all_integers_same_modulus(a, a)
        self.value = -a.value % self.modulus
        return self

    def mul(self, a: 'Field', b: 'Field') -> 'Field':
        self._check_all_integers_same_modulus(a, b)
        self.value = (a.value * b.value) % self.modulus
        return self

    def equal(self, b: 'Field') -> 'Field':
        self._check_all_integers_same_modulus(b, b)
        return self.value == b.value

    def dup(self) -> 'Field':
        return copy.deepcopy(self)

    def inv(self, a: 'Field') -> 'Field':
        if a.is_zero():
            return None
        self.value = pow(a.value, -1, self.modulus)
        return self

    def multi_inv(values: list['Field']) -> list['Field']:

        modulus = values[0].modulus

        zero = Field.zero(modulus)
        one = Field.one(modulus)
        inv = Field.zero(modulus)

        partials = [one]
        for i in range(len(values)):
            partials.append(partials[-1] * values[i] or one)

        inv.inv(partials[-1])

        outputs = [zero] * len(values)
        for i in range(len(values), 0, -1):
            outputs[i - 1] = partials[i - 1] * inv if values[i - 1] else zero
            inv = inv * values[i - 1] or one

        return outputs

    def sqrt(self, a: 'Field') -> 'Field':
        self._check_all_integers_same_modulus(a, a)
        self.value = modular_sqrt(a.value, self.modulus)
        if self.value is None:
            return None
        return self

    def exp(self, a: 'Field', exponent: int) -> 'Field':
        self._check_all_integers_same_modulus(a, a)
        self.value = pow(a.value, exponent, self.modulus)
        return self

    def legendre(self) -> int:
        return legendre_symbol(self.value, self.modulus)

    def div(self, a: 'Field', b: 'Field') -> 'Field':
        b_inv = b.dup()
        b_inv.inv(b_inv)
        if b_inv is None:
            return None

        self.mul(a, b_inv)
        return self

    # Method overloads
    def __add__(self, other):
        result = Field(0, self.modulus)
        result.add(self, other)
        return result

    def __sub__(self, other):
        result = Field(0, self.modulus)
        result.sub(self, other)
        return result

    def __mul__(self, other):
        result = Field(0, self.modulus)
        result.mul(self, other)
        return result

    def __neg__(self):
        result = Field(0, self.modulus)
        result.neg(self)
        return result

    def __truediv__(self, other):
        result = Field(0, self.modulus)
        result.div(self, other)
        return result

    def __eq__(self, obj):
        assert (isinstance(obj, Field))
        return self.equal(obj)

    # Utils
    def _check_all_integers_same_modulus(self, a: 'Field', b: 'Field'):
        assert (self.modulus == a.modulus)
        assert (self.modulus == b.modulus)


def modular_sqrt(a: int, p: int):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return None
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a: int, p: int):
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)

        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls
