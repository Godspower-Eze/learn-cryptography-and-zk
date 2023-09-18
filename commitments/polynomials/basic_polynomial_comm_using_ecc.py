import collections

from numpy.polynomial.polynomial import polydiv

from utils.ecc import ECC
from utils.number_theory import generate_random_prime

class PolyComm_ECC(ECC):

    d = None # degree
    g = None # generator
    n = None # modulus
    a = None 

    def __init__(self, curve, d: int, a: int) -> None:
        super().__init__(curve)
        self.d = d
        self.a = a
        self.g = curve.g
        self.n = curve.n
    
    def __encrypted_summation__(self, values: list[tuple[int, int]]):
        assert len(values)  == self.d + 1, "wrong degree"

        sum = self.point_at_infinity
        for i in values:
            sum = self.point_addition(sum, i)
        return sum

    def __unencrypted_summation__(self, values: list[int]):
        assert len(values)  == self.d + 1, "wrong degree"

        sum = 0
        for i in values:
            sum = (sum + i)
        return sum

    """
    VERIFIER    
    """

    def setup(self, s: int, t_of_x: list[int]) -> (list[int], list[int], int):

        assert len(t_of_x)  == self.d + 1, "wrong degree"

        encrypted_terms = [] ## [((r ** 0) * G), ((r ** 1) * G), ..., ((r ** d) * G)]
        
        for i in range(0, self.d + 1):
            value = self.scalar_multiplication(s ** i, self.g)
            encrypted_terms.append(value)

        encrypted_terms_with_a = [] ## [(((r ** 0) * a) * G), (((r ** 1) * a) * G), ..., (((r ** 0) * d) * G)]
        for i in range(0, self.d + 1):
            value = self.scalar_multiplication((s ** i) * self.a, self.g)
            encrypted_terms_with_a.append(value)

        t_at_s = []
        for i in range(0, self.d + 1):
            value = t_of_x[i] * (s ** i)
            t_at_s.append(value)

        eval_of_t_at_s = self.__unencrypted_summation__(t_at_s)
        
        return encrypted_terms, encrypted_terms_with_a, eval_of_t_at_s
    
    def check_polynomial(self, eval_of_f: int, eval_of_f_prime: int) -> bool:
        return self.scalar_multiplication(self.a, eval_of_f) == eval_of_f_prime
    
    def check_knowledge_of_polynomial(self, eval_of_h: int, eval_of_t: int, eval_of_f: int) -> bool:
        return self.scalar_multiplication(eval_of_t, eval_of_h) == eval_of_f


    """
    PROVER    
    """
    
    def evaluate(self, encrypted_terms: list[int], encrypted_terms_with_a: list[int], f_of_x: list[int], t_of_x: list[int]) -> (int, int, int):

        assert len(encrypted_terms)  == self.d + 1, "wrong degree"
        assert len(encrypted_terms_with_a)  == self.d + 1, "wrong degree"
        assert len(f_of_x)  == self.d + 1, "wrong degree"
        assert len(t_of_x)  == self.d + 1, "wrong degree"

        quotient, _ = polydiv(f_of_x, t_of_x) ## f(x) / t(x) using polynomial division
        quotient = [float(i) for i in quotient] ## Convert from numpy.float to float
        len_of_quotient = len(quotient)

        ## Padding the quotient array to be of length `d`

        if len_of_quotient != self.d:
            diff = self.d - len_of_quotient
            padding = [0.0 for i in range(0, diff + 1)]
            quotient = quotient + padding
        h_of_x = quotient
        
        evals_of_f = [self.scalar_multiplication(i, j) for i, j in zip(f_of_x, encrypted_terms)]
        eval_of_f = self.__encrypted_summation__(evals_of_f)

        evals_of_f_prime = [self.scalar_multiplication(i, j) for i, j in zip(f_of_x, encrypted_terms_with_a)]
        eval_of_f_prime = self.__encrypted_summation__(evals_of_f_prime)

        evals_of_h = [self.scalar_multiplication(int(i), j) for i, j in zip(h_of_x, encrypted_terms)]
        eval_of_h = self.__encrypted_summation__(evals_of_h)

        return (eval_of_f, eval_of_f_prime, eval_of_h)
    

## USAGE

# f(x) = (x ** 3) - 7x - 6
# factorised form of f(x) = (x + 1)(x + 2)(x - 3)
# t(x) = (x + 1)(x + 2) = (x ** 2) + 3x + 2
# h(x) = (x - 3)


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

## Secret
a = 8
d = 3

poly_ecc = PolyComm_ECC(curve, d, a)

s = generate_random_prime(1, 0xffff)
# s = 4

## SETUP (By Verifier)
encrypted_terms, encrypted_terms_with_a, eval_of_t = poly_ecc.setup(s, [2, 3, 1, 0])

## EVALUATION (By Prover)
coefficients_of_f = [-6, -7, 0, 1]
coefficients_of_t = [2, 3, 1, 0]

eval_of_f, eval_of_f_prime, eval_of_h = poly_ecc.evaluate(encrypted_terms, encrypted_terms_with_a, coefficients_of_f, coefficients_of_t)

## CHECKING POLYNOMIAL FOR CORRECT POLYNOMIAL (By Verifier)
status = poly_ecc.check_polynomial(eval_of_f, eval_of_f_prime)
assert(status)

# CHECKING POLYNOMIAL FOR KNOWLEDGE OF POLYNOMIAL (By Verifier)
status = poly_ecc.check_knowledge_of_polynomial(eval_of_h, eval_of_t, eval_of_f)
assert(status)