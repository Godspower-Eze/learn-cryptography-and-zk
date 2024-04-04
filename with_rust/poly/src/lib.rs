// use std::ops::Mul;

// use ff::{FF, FFE};

// // Univariant Polynomial
// #[derive(Debug, PartialEq, Clone)]
// pub struct UniPoly<F> {
//     // Co-effecients represented from lower degree to higher
//     // For example: 2x^2 + x + 1 is represented as [1, 1, 2]
//     coefficients: Vec<F>,
//     field: FF,
// }

// impl UniPoly<FFE<'_>> {
//     pub fn new(field: FF, coefficients: Vec<FFE<'_>>) -> UniPoly<FFE<'_>> {
//         UniPoly {
//             field,
//             coefficients,
//         }
//     }

//     pub fn x(field: &FF) -> UniPoly<FFE<'_>> {
//         let zero = field.zero();
//         let one = field.one();
//         UniPoly {
//             field: field.clone(),
//             coefficients: vec![zero, one],
//         }
//     }

//     pub fn is_zero(&self) -> bool {
//         self.coefficients.is_empty()
//     }

//     pub fn degree(&self) -> usize {
//         if self.coefficients.is_empty() {
//             0
//         } else {
//             self.coefficients.len() - 1
//         }
//     }

//     // pub fn pow(&self) -> UniPoly<FFE<'_>> {

//     // }
// }

// pub enum Error {
//     FieldMismatch,
// }

// impl<'a> Mul for UniPoly<FFE<'a>> {
//     type Output = Result<UniPoly<FFE<'a>>, Error>;

//     fn mul(self, other: Self) -> Self::Output {
//         if self.field != other.field {
//             Err(Error::FieldMismatch)
//         } else {
//             if self.is_zero() || other.is_zero() {
//                 Ok(UniPoly::new(self.field, vec![]))
//             } else {
//                 let deg_a = self.coefficients.len() - 1;
//                 let deg_b = other.coefficients.len() - 1;
//                 let product_max_degree = deg_a + deg_b + 1;
//                 let field = self.field.clone();
//                 let zero = field.zero();
//                 let mut product_coefficients = vec![zero; product_max_degree];
//                 for i in 0..=self.degree() {
//                     for j in 0..=other.degree() {
//                         let index = i + j;
//                         let product = (self.coefficients[i] * other.coefficients[j]).unwrap();
//                         product_coefficients[index] += product;
//                     }
//                 }
//                 let poly = UniPoly::new(field, product_coefficients);
//                 Ok(poly)
//             }
//         }
//     }
// }

// // #[cfg(test)]
// // mod tests {
// //     use super::*;

// //     #[test]
// //     fn it_works() {
// //         let result = add(2, 2);
// //         assert_eq!(result, 4);
// //     }
// // }
