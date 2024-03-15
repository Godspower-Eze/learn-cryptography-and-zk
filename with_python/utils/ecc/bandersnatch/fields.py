from utils.fields import Field


# This is the basefield(modulus) assosciated with the bandersnatch curve
BASE_FIELD = 52435875175126190479447740508185965837690552500527637822603658699938581184513

# This is the scalar field(order) assosciated with the bandersnatch curve
SCALAR_FIELD = 13108968793781547619861935127046491459309155893440570251786403306729687672801

# (p-1)/2
Q_MIN_ONE_DIV_2_BASE_FIELD = (BASE_FIELD - 1) // 2

# (p-1)/2
Q_MIN_ONE_DIV_2_SCALAR_FIELD = (SCALAR_FIELD - 1) // 2

BYTE_LEN = 32


class Fp(Field):

    """
    A generic implementation of a finite field over the modulus of the bandersnatch curve
    """

    def __init__(self, value=None, generic_field=None) -> None:
        if generic_field is not None:
            assert generic_field.modulus == BASE_FIELD
            super().__init__(generic_field.value, BASE_FIELD)
            return

        super().__init__(value, BASE_FIELD)

    def zero() -> 'Fp':
        return Fp(None, Field.zero(BASE_FIELD))

    def one() -> 'Fp':
        return Fp(None, Field.one(BASE_FIELD))

    def from_bytes(bytes) -> 'Fp':
        return Fp(None, Field.from_bytes(bytes, BASE_FIELD))

    def from_bytes_reduce(bytes) -> 'Fp':
        return Fp(None, Field.from_bytes_reduce(bytes, BASE_FIELD))

    def to_bytes(self) -> bytes:
        return super().to_bytes(BYTE_LEN)

    def lexographically_largest(self) -> bool:
        return super().lexographically_largest(Q_MIN_ONE_DIV_2_BASE_FIELD)

    def multi_inv(values) -> list['Fp']:
        result = []
        inverses = Field.multi_inv(values)
        for inv in inverses:
            result.append(Fp(None, inv))
        return result

    # Method overloads

    def __add__(self, other):
        return Fp(None, super().__add__(other))

    def __sub__(self, other):
        return Fp(None, super().__sub__(other))

    def __mul__(self, other):
        return Fp(None, super().__mul__(other))

    def __neg__(self):
        return Fp(None, super().__neg__())

    def __truediv__(self, other):
        return Fp(None, super().__truediv__(other))


class Fr(Field):

    """
    A generic implementation of a finite field over the order of the bandersnatch curve
    """

    def __init__(self, value=None, generic_field=None) -> None:
        if generic_field is not None:
            assert generic_field.modulus == SCALAR_FIELD
            super().__init__(generic_field.value, SCALAR_FIELD)
            return

        super().__init__(value, SCALAR_FIELD)

    def zero() -> 'Fr':
        return Fr(None, Field.zero(SCALAR_FIELD))

    def one() -> 'Fr':
        return Fr(None, Field.one(SCALAR_FIELD))

    def from_bytes(bytes) -> 'Fr':
        return Fr(None, Field.from_bytes(bytes, SCALAR_FIELD))

    def from_bytes_reduce(bytes) -> 'Fr':
        return Fr(None, Field.from_bytes_reduce(bytes, SCALAR_FIELD))

    def to_bytes(self) -> 'Fr':
        return super().to_bytes(BYTE_LEN)

    def lexographically_largest(self) -> bool:
        return super().lexographically_largest(Q_MIN_ONE_DIV_2_SCALAR_FIELD)

    def multi_inv(values) -> list['Fr']:
        result = []
        inverses = Field.multi_inv(values)
        for inv in inverses:
            result.append(Fr(None, inv))
        return result

    # Method Overloads

    def __add__(self, other):
        return Fr(None, super().__add__(other))

    def __sub__(self, other):
        return Fr(None, super().__sub__(other))

    def __mul__(self, other):
        return Fr(None, super().__mul__(other))

    def __neg__(self):
        return Fr(None, super().__neg__())

    def __truediv__(self, other):
        return Fr(None, super().__truediv__(other))
