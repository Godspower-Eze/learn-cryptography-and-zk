use std::{
    marker::PhantomData,
    ops::{Add, Neg, Sub},
};

use rand::Rng;

use ff::{FF, FFE};
use poly::{Polynomial, UniPoly, UnivariatePolynomial};

#[derive(Debug, Clone)]
pub struct SSS<E, F> {
    _field_element: PhantomData<E>,
    _field: PhantomData<F>,
}

impl<F: FF<FieldType = usize>, E: FFE<F> + Neg<Output = E> + Sub<Output = E> + Add<Output = E>>
    SSS<E, F>
{
    fn generate_polynomial(degree: usize) -> (E, UniPoly<E, F>, Vec<E>) {
        let mut rng = rand::thread_rng();
        let modulus = F::MODULUS;
        let zero = E::zero();
        let secret = E::new(rng.gen_range(0..modulus).try_into().unwrap());
        let mut x_values = vec![zero];
        let mut y_values = vec![secret];
        while x_values.len() != (degree + 1) {
            let x = E::new(rng.gen_range(0..modulus).try_into().unwrap());
            let y = E::new(rng.gen_range(0..modulus).try_into().unwrap());
            if !x_values.contains(&x) {
                x_values.push(x);
                y_values.push(y);
            } else {
                continue;
            }
        }
        let poly = UniPoly::interpolate_xy(&x_values, &y_values);
        return (secret, poly, x_values);
    }

    pub fn generate(degree: usize, num_of_points: usize) -> (E, Vec<(E, E)>) {
        let (mut secret, mut poly, mut x_values) = Self::generate_polynomial(degree);
        while poly.degree() != degree {
            (secret, poly, x_values) = Self::generate_polynomial(degree);
        }
        let mut rng = rand::thread_rng();
        let modulus = F::MODULUS;

        let mut new_x_values = vec![];
        let mut y_values = vec![];

        while new_x_values.len() != num_of_points {
            let x = E::new(rng.gen_range(0..modulus).try_into().unwrap());
            if !x_values.contains(&x) {
                new_x_values.push(x);
                let y = poly.evaluate(x);
                y_values.push(y);
            } else {
                continue;
            }
        }

        let mut points = vec![];
        for (x, y) in new_x_values.iter().zip(y_values.iter()) {
            points.push((*x, *y));
        }
        return (secret, points);
    }

    pub fn recover(secret: E, points: &Vec<(E, E)>) -> bool {
        let mut x_values = vec![];
        let mut y_values = vec![];
        for (x, y) in points.iter() {
            x_values.push(*x);
            y_values.push(*y)
        }
        let poly = UniPoly::interpolate_xy(&x_values, &y_values);
        return secret == poly.evaluate(E::zero());
    }
}

#[cfg(test)]
mod tests {

    use ff::{SampleFF, SampleFFE};

    use super::*;

    #[test]
    fn sss() {
        let degree = 5;
        let num_of_points = 20;
        let (secret, points) =
            SSS::<SampleFFE<SampleFF>, SampleFF>::generate(degree, num_of_points);
        // True Cases
        assert!(SSS::recover(secret, &points));
        assert!(SSS::recover(secret, &points[..15].to_vec()));
        assert!(SSS::recover(secret, &points[..10].to_vec()));
        assert!(SSS::recover(secret, &points[..6].to_vec()));
        assert!(SSS::recover(secret, &points[5..].to_vec()));
        assert!(SSS::recover(secret, &points[11..].to_vec()));
        assert!(SSS::recover(secret, &points[14..].to_vec()));
        // False Cases
        assert!(!SSS::recover(secret, &points[15..].to_vec()));
        assert!(!SSS::recover(secret, &points[16..].to_vec()));
        assert!(!SSS::recover(secret, &points[..5].to_vec()));
        assert!(!SSS::recover(secret, &points[..4].to_vec()));

        let mut points = vec![];
        let mut rng = rand::thread_rng();
        for _ in 0..20 {
            let x = SampleFFE::new(rng.gen_range(0..SampleFF::MODULUS).try_into().unwrap());
            let y = SampleFFE::new(rng.gen_range(0..SampleFF::MODULUS).try_into().unwrap());
            points.push((x, y));
        }
        assert!(!SSS::recover(secret, &points));
        assert!(!SSS::recover(secret, &points[..15].to_vec()));
        assert!(!SSS::recover(secret, &points[..10].to_vec()));
        assert!(!SSS::recover(secret, &points[..6].to_vec()));
    }
}
