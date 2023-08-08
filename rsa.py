

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

    def gcd(self, a: int, b: int) -> int:

        """
        Computes the GCD of a and b using the Euclidean Algorithm
        """

        higher, lower = max(a, b), min(a, b)
        mod = higher % lower
        if mod == 0:
            return lower
        else:
            return self.gcd(lower, mod)
        
    def reverse_gcd(self, a: int, b: int) -> list[list[int]]:

        """
        Computes the gcd and reverses the process to express
        the gcd as a linear combination in the form ax + by = gcd(a, b).

        The Extended Euclidean Algorithm is used here.
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



        
    
        


rsa = RSA()
gcd = rsa.gcd(30, 77)
r_gcd = rsa.reverse_gcd(30, 77)
print(r_gcd)

