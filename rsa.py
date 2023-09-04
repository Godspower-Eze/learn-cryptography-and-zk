from random import randint
from utils.number_theory import gcd_by_ea, gcd_by_eea

class RSA:

    """
    Steps
        1. Generate two large primes `p` and `q` using a good random number generator
        2. Compute `n` where `n = p * q`
        3. Compute `e` such that `1 <= e <= ɸ(n)` so that `gcd(e, ɸ(n)) = 1`. 
           ɸ(n) is the phi of n (the number of integers from 1 to n that doesn't share a common factor with n),
           gcd is the greatest common divisor
        4. Compute `d` such that 1 < d < ɸ(n) so that d is congruent to ((1 mod ɸ(n)))/e. d can be gotten by solving the linear congruence equation. 
           In other words, `d` is the multiplicative inverse of e mod ɸ(n) (ed congruent to 1 mod ɸ(n)).
        4. Share n and e publicly. e is the encryption key and n is the modulus
        5. Encryption is achieved by computing C = M ** e mod n where M is the message and C is encrypted message
        6. Decryption is achieved by computing N such that 1 <= N < n such that N = (C ** d mod n). N is the original message
    """

    ## Secret large primes
    p: int 
    q: int

    ## Public value
    n: int

    def __init__(self, p: int, q: int) -> None:
        p_is_prime = self.is_prime(p)
        q_is_prime = self.is_prime(q)

        if not p_is_prime:
            raise Exception(f"{p} is not prime")
        
        if not q_is_prime:
            raise Exception(f"{q} is not prime")

        self.p = p
        self.q = q
        self.n = p * q
    
    def is_prime(self, num: int) -> bool:
        if num == 1:
            return False
        else:
            known_primes = [2, 3, 5, 7]
            if num in known_primes:
                return True
            else:
                for i in known_primes:
                    """
                    According to the fundamental theorem of arithmetic, every positive
                    number asides 1 can be expressed as a product of unique primes. Therefore,
                    a prime number other than the `known_primes` shouldn't return 0 mod one of the
                    known prime.
                    """
                    remainder = num % i
                    if remainder == 0:
                        return False
        return True
    
    def phi_of_n(self) -> int:

        """
        The phi of any prime number p is p - 1. To find the phi of n where n is a 
        product of two primes p, q can be computed as (ɸ(n) = ɸ(p) * ɸ(q)). Therefore
        ɸ(n) is equal to (p - 1) * (q - 1)
        """

        phi_of_n = (self.p - 1) * (self.q - 1)
        return phi_of_n
    
    def generate_public_key(self) -> int:
        
        """
        The goal of this function to find `e` such that gcd(e, ɸ(n)) congruent to 1.

        `e` is the encryption key/public key

        We use brute force checking to achieve this. Do you think there are better ways to achieve this? 
        Please let me know!
        """

        phi_of_n = self.phi_of_n()
        random_number = randint(2, phi_of_n)
        gcd = gcd_by_ea(random_number, phi_of_n) 
        
        while gcd != 1:
            random_number = randint(2, phi_of_n)
            gcd = gcd_by_ea(random_number, phi_of_n)

        e = random_number
        return e
    
    def generate_private_key(self, e: int):

        """
        The goal of this function to find the multiplicative inverse `d` of (e congruent to 1 mod ɸ(n)).

        We will use the Extended Euclidean Algorithm.

        The multiplicative inverse is the value of y_1 mod ɸ(n) in the last row of the table returned by `gcd_by_eea`
        """

        phi_of_n = self.phi_of_n()
        gcd = gcd_by_ea(e, phi_of_n)

        if gcd != 1:
            raise Exception("e is invalid")
        
        table = gcd_by_eea(e, phi_of_n)
        mi = table[-1][8] % phi_of_n
        d = mi
        return d
    
    ## TODO: Optimise to use fast exponentiation algorithms in order to compute using large values of e
    def encrypt(self, m: int, e: int, n: int):

        """
        To encrypt, we compute c = m ** e mod n where m is the message, c is encrypted message and n is the modulus
        """
        c = (m ** e) % n
        return c
    
    ## TODO: Optimise to use fast exponentiation algorithms in order to compute using large values of d
    def decrypt(self, c: int, d: int, n: int):
        
        """
        To decrypt, we compute N  = (c ** d mod n). N is the original message
        """
        N = (c ** d) % n
        return N
    


## Usage (Small values are used for faster evaluation)

## Alice generates two large primes p and q(use https://bigprimes.org/ to generate large primes)

p = 97
q = 41
rsa = RSA(p, q)

n = rsa.n

## Alice generates her public and private key

public_key = rsa.generate_public_key()
private_key = rsa.generate_private_key(public_key)

"""
Alice shares her public key and n public. Keeping p, q, ɸ(n) and her private key secret
"""

## Bob picks up n and Alice's public and uses it for encryption

"""
message should of the range 1 <= m < n

Here, we assume that there's a mechanism that coverts text to numbers and this message means something in words.
"""
message = 203 
encrypted_message = rsa.encrypt(message, public_key, n)

"""
Bob shares the encrypted message publicly
"""

## Alice picks up the encrypted message and decrypts it using her private key

decrypted_message = rsa.decrypt(encrypted_message, private_key, n)

## The original message should be equal to the decrypted message

assert (message == decrypted_message)