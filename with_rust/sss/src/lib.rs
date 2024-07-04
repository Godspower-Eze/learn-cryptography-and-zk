use ff::{FF, FFE};
use poly::UnivariatePolynomial;

pub struct SSS<P, F> {
    polynomial: P,
    points: Vec<(F, F)>,
}

enum Error {
    InvalidPoint,
}

impl<P: UnivariatePolynomial<F>, F: PartialEq> SSS<P, F> {
    fn add_points(&mut self, point: (F, F)) -> Result<(F, F), Error> {
        if self.points.contains(&point) {}
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
}
