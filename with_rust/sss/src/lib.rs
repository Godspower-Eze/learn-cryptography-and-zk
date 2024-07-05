use std::{
    collections::HashSet,
    marker::PhantomData,
    ops::{Add, Neg, Sub},
};

use rand::Rng;

use ff::{FF, FFE};
use poly::{UniPoly, UnivariatePolynomial};

#[derive(Debug, Clone)]
pub struct SSS<P, F, S> {
    secret_y: F,
    polynomial: P,
    points: Vec<(F, F)>,
    _field: PhantomData<S>,
}

pub enum STRATEGY {
    FIRST,
    LAST,
    RANDOM,
}

pub enum Error {
    InvalidPoint,
}

impl<
        P: UnivariatePolynomial<F>,
        F: FFE<S> + Add<Output = F> + Sub<Output = F> + Neg<Output = F>,
        S: FF,
    > SSS<P, F, S>
{
    pub fn add_points(&mut self, point: (F, F)) -> Result<(F, F), Error> {
        if !self.points.contains(&point) {
            let (x_var, _) = point;
            for (x, _) in self.points.iter() {
                if *x == x_var {
                    return Err(Error::InvalidPoint);
                }
            }
            self.points.push(point);
            return Ok(point);
        } else {
            return Err(Error::InvalidPoint);
        }
    }

    fn evaluate(points: &Vec<(F, F)>) -> F {
        let mut x_values = vec![];
        let mut y_values = vec![];
        for (x, y) in points.iter() {
            x_values.push(*x);
            y_values.push(*y);
        }
        let poly = UniPoly::<F, S>::interpolate_xy(&x_values, &y_values);
        let eval = poly.evaluate(F::zero());
        return eval;
    }

    pub fn compute(self, point_strategy: STRATEGY) -> bool {
        if self.polynomial.degree() + 1 < self.points.len() {
            return false;
        } else {
            let number_of_points = self.polynomial.degree() + 1;
            match point_strategy {
                STRATEGY::FIRST => {
                    let points = self.points[..number_of_points].to_vec();
                    let f_of_zero = Self::evaluate(&points);
                    return self.secret_y == f_of_zero;
                }
                STRATEGY::LAST => {
                    let length = self.points.len();
                    let diff = length - number_of_points;
                    let points = self.points[diff..].to_vec();
                    let f_of_zero = Self::evaluate(&points);
                    return self.secret_y == f_of_zero;
                }
                STRATEGY::RANDOM => {
                    let mut rng = rand::thread_rng();
                    let mut random_indexes: HashSet<usize> = HashSet::new();
                    while random_indexes.len() < number_of_points {
                        let index = rng.gen_range(0..number_of_points);
                        random_indexes.insert(index);
                    }
                    let mut points: Vec<(F, F)> = vec![];
                    for i in random_indexes.into_iter() {
                        points.push(self.points[i]);
                    }
                    let f_of_zero = Self::evaluate(&points);
                    return self.secret_y == f_of_zero;
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use ff::{SampleFF, SampleFFE, FFE};
    use poly::{Polynomial, UniPoly};

    use super::*;

    #[test]
    fn add_points() {
        let coefficients: Vec<SampleFFE<SampleFF>> = vec![
            SampleFFE::new(-6),
            SampleFFE::new(11),
            SampleFFE::new(-6),
            SampleFFE::new(1),
        ];
        let points: Vec<(SampleFFE<SampleFF>, SampleFFE<SampleFF>)> = vec![];
        let polynomial = UniPoly::new(coefficients);
        let mut sss = SSS {
            secret_y: SampleFFE::new(2),
            polynomial,
            points,
            _field: PhantomData,
        };
        assert_eq!(sss.points.len(), 0);

        let point1 = (SampleFFE::new(23), SampleFFE::new(45));
        let point2 = (SampleFFE::new(34), SampleFFE::new(78));

        assert!(sss.add_points(point1).is_ok());
        assert!(sss.add_points(point2).is_ok());

        assert_eq!(sss.points.len(), 2);

        assert!(sss.add_points(point1).is_err());

        let point3 = (SampleFFE::new(23), SampleFFE::new(91));

        assert!(sss.add_points(point3).is_err());
        assert_eq!(sss.points.len(), 2);
    }

    #[test]
    fn compute() {
        let coefficients: Vec<SampleFFE<SampleFF>> = vec![
            SampleFFE::new(-6),
            SampleFFE::new(11),
            SampleFFE::new(-6),
            SampleFFE::new(1),
        ];
        let points: Vec<(SampleFFE<SampleFF>, SampleFFE<SampleFF>)> = vec![];
        let polynomial = UniPoly::new(coefficients);
        let mut sss = SSS {
            secret_y: SampleFFE::new(-6),
            polynomial,
            points,
            _field: PhantomData,
        };
        let point1 = (SampleFFE::new(5), SampleFFE::new(24));
        let point2 = (SampleFFE::new(7), SampleFFE::new(120));
        let point3 = (SampleFFE::new(9), SampleFFE::new(336));
        let point4 = (SampleFFE::new(11), SampleFFE::new(720));

        let _ = sss.add_points(point1);
        let _ = sss.add_points(point2);
        let _ = sss.add_points(point3);
        let _ = sss.add_points(point4);

        assert!(sss.clone().compute(STRATEGY::FIRST));
        assert!(sss.clone().compute(STRATEGY::LAST));
        assert!(sss.compute(STRATEGY::RANDOM));
    }
}
