use ff::{SampleFF, SampleFFE, FF, FFE};
use std::marker::PhantomData;
use std::ops::{Add, AddAssign, Mul};

pub trait Polynomial<F>: Sized {
    fn is_zero(&self) -> bool;

    fn degree(&self) -> usize;

    fn new(coefficients: Vec<F>) -> Self;

    fn x() -> Self;

    fn interpolate(y: Vec<F>) -> Self;
}

// Univariate Polynomial
#[derive(Debug, PartialEq, Clone)]
pub struct UniPoly<F, S> {
    // Co-efficients represented from lower degree to higher
    // For example: 2x^2 + x + 1 is represented as [1, 1, 2]
    coefficients: Vec<F>,
    _field: PhantomData<S>,
}

impl<F: FFE<S>, S: FF> Polynomial<F> for UniPoly<F, S> {
    fn new(coefficients: Vec<F>) -> Self {
        UniPoly {
            coefficients,
            _field: PhantomData,
        }
    }

    fn x() -> Self {
        let zero = F::zero();
        let one = F::one();
        UniPoly {
            coefficients: vec![zero, one],
            _field: PhantomData,
        }
    }

    fn is_zero(&self) -> bool {
        self.coefficients.is_empty()
    }

    fn degree(&self) -> usize {
        if self.coefficients.is_empty() {
            0
        } else {
            self.coefficients.len() - 1
        }
    }

    fn interpolate(y: Vec<F>) -> Self {
        todo!()
    }
}

#[derive(Debug)]
pub enum Error {
    FieldMismatch,
}

impl<F: FFE<S> + AddAssign, S: FF> Mul for &UniPoly<F, S> {
    type Output = Result<UniPoly<F, S>, Error>;

    fn mul(self, other: Self) -> Self::Output {
        if self.is_zero() || other.is_zero() {
            Ok(UniPoly::new(vec![]))
        } else {
            let deg_a = self.coefficients.len() - 1;
            let deg_b = other.coefficients.len() - 1;
            let max_coefficients = deg_a + deg_b + 1;
            let zero = F::zero();
            let mut product_coefficients = vec![zero; max_coefficients];
            for i in 0..=self.degree() {
                for j in 0..=other.degree() {
                    let index = i + j;
                    let product = self.coefficients[i] * other.coefficients[j];
                    product_coefficients[index] += product;
                }
            }
            let poly = UniPoly::new(product_coefficients);
            Ok(poly)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[derive(Debug, Clone, Copy, PartialEq)]
    struct TestFF {}

    impl FF for TestFF {
        type FieldType = usize;
        const MODULUS: usize = 3221225473;
    }

    #[test]
    fn mul() {
        // Tests x * (x + 1)
        let x = UniPoly::<SampleFFE<SampleFF>, SampleFF>::x();
        let co_effs = vec![SampleFFE::one(), SampleFFE::one()];
        let x_plus_1 = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(co_effs);
        let actual = &x * &x_plus_1;
        let co_effs = vec![SampleFFE::zero(), SampleFFE::one(), SampleFFE::one()];
        let expected = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(co_effs);
        assert_eq!(actual.unwrap(), expected);

        // Tests (x^3 - 3x + 2) * (2x + 5)
    }
}
