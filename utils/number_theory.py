import sympy

def gcd_by_ea(a: int, b: int) -> int:

        """
        Computes the GCD of a and b using the Euclidean Algorithm
        """

        higher, lower = max(a, b), min(a, b)
        mod = higher % lower
        while mod != 0:
            higher, lower = lower, mod
            mod = higher % lower
        return lower

def gcd_by_eea(a: int, b: int) -> list[list[int]]:

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


def generate_random_prime(min: int, max: int):
      return sympy.randprime(min, max)