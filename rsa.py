

class RSA:

    """
    Steps
        1. Generate two large primes `p` and `q` using a good random number generator
        2. Compute `n` where `n = p * q`
        3. Compute `e` such that `1 <= e <= ɸ(n)` so that `gcd(e, ɸ(n)) = 1`. 
           ɸ(n) is the phi of n (the number of integers from 1 to n that doesn't share a common factor with n),
           gcd is the greatest common divisor
        4. Compute `d` such that 1 < d < ɸ(n) so that d is congruent to ((1 mod ɸ(n)))/e. d can be gotten by solving the linear congruence equation.
        4. Share n and e publicly. e is the encryption key and n is the modulus
        5. Encryption is achieved by computing C = M ** e mod n where M is the message and C is encrypted message
        6. Decryption is achieved by computing N such that 1 <= N < n such that N  is congruent to (C ** d mod n). N is the original message
    """

    def gcd_by_ea(self, a: int, b: int) -> int:

        """
        Computes the GCD of a and b using the Euclidean Algorithm
        """

        higher, lower = max(a, b), min(a, b)
        mod = higher % lower
        if mod == 0:
            return lower
        else:
            return self.gcd(lower, mod)
        
    def gcd_by_eea(self, a: int, b: int) -> list[list[int]]:

        """
        Computes the gcd and reverses the process to express
        the gcd as a linear combination in the form ax + by = gcd(a, b).

        The Extended Euclidean Algorithm is used here.

        The value of x_1 and y_1 in the last row are the values of x and y respectively.
        """

        # Initial Values
        a, b = [max(a, b), min(a, b)]
        q = a // b # quotient
        r = a % b # remainder
        x_0, x_1 = 1, 0 
        x = x_0 - (x_1 * q)
        y_0, y_1 = 0, 1
        y = y_0 - (y_1 * q)

        table = [["q", "a", "b", "r", "x_0", "x_1", "x", "y_0", "y_1", "y"], [q, a, b, r, x_0, x_1, x, y_0, y_1, y]]

        while r != 0:
            a, b = b, r
            q = a // b
            r = a % b 
            x_0, x_1 = x_1, x 
            x = x_0 - (x_1 * q)
            y_0, y_1 = y_1, y
            y = y_0 - (y_1 * q)
            row = [q, a, b, r, x_0, x_1, x, y_0, y_1, y]
            table.append(row)

        return table
    
    def is_prime(self, num: int):
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
    
    def phi_of_n(self, p: int, q: int):

        """
        This function expects that p and q are primes.

        The phi of any prime number p is p - 1. To find the phi of n where n is a 
        product of two primes p, q can be computed as (phi of n = phi of p * phi of q). Therefore
        n is equal to (p - 1) * (q - 1)
        """

        p_is_prime = self.is_prime(p)
        q_is_prime = self.is_prime(q)

        if not p_is_prime:
            raise Exception(f"{p} is not prime")
        
        if not q_is_prime:
            raise Exception(f"{q} is not prime")
        
        phi_of_n = (p-1)(q-1)
        return phi_of_n

