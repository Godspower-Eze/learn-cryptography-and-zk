use ff::{FF, FFE};

trait Polynomial {
    fn evaluate(&self) -> isize;
    fn interpolate(&self) -> Self;
}

// Univariant Polynomial
struct UniPoly<FE> {
    // Co-effecients represented from lower degree to higher
    // For example: 2x^2 + x + 1 is represented as [1, 1, 2]
    coefficients: Vec<FE>,
    field: FF,
}

impl UniPoly<FFE<'_>> {
    pub fn new(field: FF, coefficients: Vec<FFE<'_>>) -> UniPoly<FFE<'_>> {
        UniPoly {
            field,
            coefficients,
        }
    }

    pub fn x(field: &FF) -> UniPoly<FFE<'_>> {
        let zero = field.zero();
        let one = field.one();
        UniPoly {
            field: field.clone(),
            coefficients: vec![zero, one],
        }
    }
}

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn it_works() {
//         let result = add(2, 2);
//         assert_eq!(result, 4);
//     }
// }
