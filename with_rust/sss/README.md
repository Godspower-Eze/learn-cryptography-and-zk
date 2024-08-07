# Shamir Secret Sharing

Shamir Secret Sharing is a form of multi-party computation. Multi-party computation is a form of cryptography where multiple parties combine keys/secrets privately to compute a function.

Let's see how Shamir Secret Sharing works.

## How does it work?

Alice has a secret number $y$ that she wants to keep hidden but she also wants to hide it in plain sight. She decides to hide it using the points of a polynomial.

- She creates a point: $(0, y)$
- Generates multiple other points $(x_i, y_i)$ where $(0, y)$ is labelled $(x_0, y_0)$ and the number of extra points needed depends on the degree of the polynomial. That is, a polynomial of degree 2(quadratic) needs three points so she generates two other points $(x_1, y_1)$ and $(x_2, y_2)$. A polynomial of degree $n$ requires $n + 1$ points.
- Using lagrange interpolation, these points are used to create a unique polynomial.
- New points are generated by evaluating the polynomial at new values of $x$. That is, $(x, f(x))$
- These points are then shared privately across individuals. For a degree $n$ polynomial, $n + 1$ or more points are distributed. The only point that is required not to be shared is the $(0, y)$ point but in this case we would decide not to share the points used in the generation of the polynomial.
- Alice has successfully hidden and stored the secret $y$ in a polynomial.
- To recover this secret, she gets at least $n + 1$ points and then, performs lagrange interpolation on it to get a polynomial.
- If all points are correct, then an evaluation of the polynomial at $0$ should give $y$.

As shown in the code, we use finite field elements to amplify the security of this.

## Code

```rust
let degree = 5;
let nums = 20;

let (secret, points) = SSS::<F, E>::generate(degree, num);

assert!(SSS::recover(secret, &points));
```

Full code [here](./src/lib.rs)
