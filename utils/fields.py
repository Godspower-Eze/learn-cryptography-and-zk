
class Field:

    value = None
    modulus = None

    def __init__(self, value, modulus) -> None:
        self.value = value % modulus
        self.modulus = modulus

    def zero(self) -> 'Field':
        return Field(0, self.modulus)
    
    def one(self) -> 'Field':
        return Field(1, self.modulus)
    
    def is_constant(self, constant: int) -> bool:
        # Here we assume that the number has been reduced.
        # Which should be the case, if values are initialised using the constructors
        return self.value == constant

    def is_zero(self) -> bool:
        return self.is_constant(0)

    def is_one(self) -> bool:
        return self.is_constant(1)
    
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

    def _check_all_integers_same_modulus(self, a: 'Field', b: 'Field'):
        assert(self.modulus == a.modulus)
        assert(self.modulus == b.modulus)

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

    def __eq__(self, obj):
        assert(isinstance(obj, Field))
        return self.equal(obj)