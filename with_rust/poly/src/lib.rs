use ff::{FF, FFE};
use std::{
    marker::PhantomData,
    ops::{AddAssign, Mul},
};

// Univariant Polynomial
#[derive(Debug, PartialEq, Clone)]
pub struct UniPoly<F, S> {
    // Co-effecients represented from lower degree to higher
    // For example: 2x^2 + x + 1 is represented as [1, 1, 2]
    coefficients: Vec<F>,
    _field: PhantomData<S>,
}

impl<F: FFE<S>, S: FF> UniPoly<F, S> {
    pub fn new(coefficients: Vec<F>) -> UniPoly<F, S> {
        UniPoly {
            coefficients,
            _field: PhantomData,
        }
    }

    pub fn x() -> UniPoly<F, S> {
        let zero = F::zero();
        let one = F::one();
        UniPoly {
            coefficients: vec![zero, one],
            _field: PhantomData,
        }
    }

    pub fn is_zero(&self) -> bool {
        self.coefficients.is_empty()
    }

    pub fn degree(&self) -> usize {
        if self.coefficients.is_empty() {
            0
        } else {
            self.coefficients.len() - 1
        }
    }

    // pub fn pow(&self) -> UniPoly<FFE<'_>> {

    // }
}

pub enum Error {
    FieldMismatch,
}

impl<F: FFE<S> + AddAssign, S: FF> Mul for UniPoly<F, S> {
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

    struct TestField {}

    impl FF for TestField {
        type FieldType = usize;

        const GENERATOR: usize = 5;

        const MODULUS: usize = 3221225473;

        fn zero() -> Self::FieldType {
            0
        }

        fn one() -> Self::FieldType {
            1
        }
    }

    #[test]
    fn multiplication() {
        let poly_1: UniPoly<i32, _> = UniPoly::new(vec![2, 0, 1]);
    }
}
