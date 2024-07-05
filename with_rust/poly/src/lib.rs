use ff::{FF, FFE};
use std::marker::PhantomData;
use std::ops::{Add, AddAssign, Mul, Neg, Sub};

pub trait Polynomial<F>: Sized {
    fn is_zero(&self) -> bool;

    fn degree(&self) -> usize;

    fn new(coefficients: Vec<F>) -> Self;

    fn x() -> Self;

    fn zero() -> Self;

    fn one() -> Self;
}

pub trait UnivariatePolynomial<F>: Polynomial<F> {
    fn evaluate(&self, x: F) -> F;

    fn interpolate(y_values: &Vec<F>) -> Self;

    fn interpolate_xy(x_values: &Vec<F>, y_values: &Vec<F>) -> Self;

    fn get_lagrange_polynomial(x_value: F, x_values: &Vec<F>) -> Self;
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
        Self::new(vec![F::zero(), F::one()])
    }

    fn one() -> Self {
        Self::new(vec![F::one()])
    }

    fn zero() -> Self {
        Self::new(vec![F::zero()])
    }

    fn is_zero(&self) -> bool {
        self.coefficients.is_empty()
            || (self.coefficients.len() == 1 && self.coefficients[0] == F::zero())
    }

    fn degree(&self) -> usize {
        if self.is_zero() {
            0
        } else {
            self.coefficients.len() - 1
        }
    }
}

impl<F: FFE<S> + Neg<Output = F> + Sub<Output = F> + Add<Output = F>, S: FF> UnivariatePolynomial<F>
    for UniPoly<F, S>
{
    fn evaluate(&self, var: F) -> F {
        let mut identity = F::zero();
        for (i, x) in self.coefficients.iter().enumerate() {
            let exp = var.pow(i);
            let mul = exp * *x;
            identity += mul
        }
        identity
    }

    fn interpolate(y_values: &Vec<F>) -> Self {
        let mut x_values = vec![];
        for i in 0..y_values.len() {
            x_values.push(F::new(i.try_into().unwrap()));
        }
        Self::interpolate_xy(&x_values, y_values)
    }

    fn interpolate_xy(x_values: &Vec<F>, y_values: &Vec<F>) -> Self {
        assert_eq!(x_values.len(), y_values.len());
        let mut resulting_polynomial = Self::zero();
        for (x, y) in x_values.iter().zip(y_values.iter()) {
            let lagrange_polynomial = Self::get_lagrange_polynomial(*x, &x_values);
            let y_poly = Self::new(vec![*y]);
            let product = &y_poly * &lagrange_polynomial;
            resulting_polynomial = &resulting_polynomial + &product;
        }
        resulting_polynomial
    }

    fn get_lagrange_polynomial(x_value: F, x_values: &Vec<F>) -> Self {
        /*
         * L_i = \prod_{j=0, j \neq i}^{n} \dfrac{x - x_j}{x_i - x_j}
         *
         *  where:
         *      `i` is x_value
         *      `j` is the index in the loop below
         */
        let mut resulting_polynomial = Self::one();
        for x in x_values.iter() {
            if *x == x_value {
                continue;
            }
            let numerator = Self::new(vec![-(*x), F::one()]);
            let inverse_of_denominator = Self::new(vec![(x_value - *x).inverse()]);
            let product = &numerator * &inverse_of_denominator;
            // TODO: implement mul_assign() for &UniPoly
            resulting_polynomial = &resulting_polynomial * &product;
        }
        resulting_polynomial
    }
}

impl<F: FFE<S> + AddAssign, S: FF> Mul for &UniPoly<F, S> {
    type Output = UniPoly<F, S>;

    fn mul(self, other: Self) -> Self::Output {
        if self.is_zero() || other.is_zero() {
            UniPoly::zero()
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
            poly
        }
    }
}

impl<F: FFE<S> + Add<Output = F>, S: FF> Add for &UniPoly<F, S> {
    type Output = UniPoly<F, S>;

    fn add(self, rhs: Self) -> Self::Output {
        if self.is_zero() {
            rhs.clone()
        } else if rhs.is_zero() {
            self.clone()
        } else {
            let new_coefficients = add_list(self.coefficients.clone(), rhs.coefficients.clone());
            UniPoly::new(new_coefficients)
        }
    }
}

fn add_list<T: FFE<F> + Add<Output = T>, F: FF>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let mut res: Vec<T> = vec![];
    if a.len() == b.len() {
        for (x, y) in a.iter().zip(b.iter()) {
            res.push(*x + *y);
        }
    } else if a.len() > b.len() {
        let diff = a.len() - b.len();
        let mut b = b;
        for _ in 0..diff {
            b.push(T::zero());
        }
        for (x, y) in a.iter().zip(b.iter()) {
            res.push(*x + *y);
        }
    } else {
        let diff = b.len() - a.len();
        let mut a = a;
        for _ in 0..diff {
            a.push(T::zero());
        }
        for (x, y) in a.iter().zip(b.iter()) {
            res.push(*x + *y);
        }
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;
    use ff::{SampleFF, SampleFFE};

    #[test]
    fn mul() {
        // Test:
        let x = UniPoly::<SampleFFE<SampleFF>, SampleFF>::x();
        let co_effs = vec![SampleFFE::one(), SampleFFE::one()];
        let x_plus_1 = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(co_effs);
        let actual = &x * &x_plus_1;
        let co_effs = vec![SampleFFE::zero(), SampleFFE::one(), SampleFFE::one()];
        let expected = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(co_effs);
        assert_eq!(actual, expected);

        // Tests (x^3 - 3x + 2) * (2x + 5)
        let co_effs_1 = vec![
            SampleFFE::new(2),
            SampleFFE::new(-3),
            SampleFFE::zero(),
            SampleFFE::new(1),
        ];
        let poly_1 = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(co_effs_1);
        let co_effs_2 = vec![SampleFFE::new(5), SampleFFE::new(2)];
        let poly_2 = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(co_effs_2);
        let actual = &poly_1 * &poly_2;
        let exp_co_effs = vec![
            SampleFFE::new(10),
            SampleFFE::new(-11),
            SampleFFE::new(-6),
            SampleFFE::new(5),
            SampleFFE::new(2),
        ];
        let expected = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(exp_co_effs);
        assert_eq!(actual, expected);
    }

    #[test]
    fn add() {
        // Test: (x^2 + x + 5) + (2x^2 + 4x + 2)
        let co_eff_1 = vec![SampleFFE::new(5), SampleFFE::new(1), SampleFFE::new(1)];
        let poly_1 = UniPoly::new(co_eff_1);
        let co_eff_2 = vec![SampleFFE::new(2), SampleFFE::new(4), SampleFFE::new(2)];
        let poly_2 = UniPoly::new(co_eff_2);
        let actual = &poly_1 + &poly_2;
        let exp_co_effs = vec![SampleFFE::new(7), SampleFFE::new(5), SampleFFE::new(3)];
        let expected = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(exp_co_effs);
        assert_eq!(actual, expected);

        // Test: (x^3 - 3x + 2) * (2x + 5)
        let co_eff_3 = vec![SampleFFE::new(5), SampleFFE::new(2)];
        let poly_3 = UniPoly::new(co_eff_3);
        let co_eff_4 = vec![
            SampleFFE::new(2),
            SampleFFE::new(-3),
            SampleFFE::new(0),
            SampleFFE::new(1),
        ];
        let poly_4 = UniPoly::new(co_eff_4);
        let actual = &poly_3 + &poly_4;
        let exp_co_effs = vec![
            SampleFFE::new(7),
            SampleFFE::new(-1),
            SampleFFE::zero(),
            SampleFFE::one(),
        ];
        let expected = UniPoly::<SampleFFE<SampleFF>, SampleFF>::new(exp_co_effs);
        assert_eq!(actual, expected);
    }

    #[test]
    fn interpolate() {
        // Interpolating the values: [3, 1, 2, 4]
        let co_effs = vec![
            SampleFFE::new(3),
            SampleFFE::new(1),
            SampleFFE::new(2),
            SampleFFE::new(4),
        ];
        let polynomial: UniPoly<SampleFFE<SampleFF>, SampleFF> =
            UniPoly::<SampleFFE<SampleFF>, SampleFF>::interpolate(&co_effs);
        println!("{:?}", polynomial);
    }
}
