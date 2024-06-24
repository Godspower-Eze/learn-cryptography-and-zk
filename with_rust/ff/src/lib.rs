use std::{
    ops::{Add, AddAssign, Mul, Rem, Sub},
    usize,
};

pub trait FF: Sized {
    type FieldType: From<usize> + Default + Add + Mul + Rem + Sub + AddAssign;

    const GENERATOR: usize;

    const MODULUS: usize;

    fn zero() -> Self::FieldType;

    fn one() -> Self::FieldType;
}

pub trait FFE<F: FF>: Sized + Copy + Mul<Output = Self> + PartialEq + From<usize> {
    const ELEMENT: usize;

    fn from_field(field: F::FieldType) -> Self;

    fn element() -> Self {
        (Self::ELEMENT % F::MODULUS).into()
    }

    fn generator() -> Self {
        Self::from_field(F::GENERATOR.into())
    }

    fn modulus() -> Self {
        Self::from_field(F::MODULUS.into())
    }

    fn zero() -> Self {
        Self::from_field(F::zero())
    }

    fn one() -> Self {
        Self::from_field(F::one())
    }

    fn pow(&self, mut n: usize) -> Result<Self, Error> {
        let mut current_power = self.to_owned();
        let mut result = Self::one();
        while n > 0 {
            if n % 2 == 1 {
                result = result * current_power;
            }
            n = n / 2;
            current_power = current_power * current_power;
        }
        Ok(result)
    }

    fn is_order(&self, order: usize) -> bool {
        let identity = Self::one();
        let exp = self.pow(order).unwrap();
        let res = if identity == exp {
            let mut res = true;
            for i in 1..order {
                let exp_inner = self.pow(i).unwrap();
                if exp_inner == identity {
                    res = false;
                    break;
                }
            }
            res
        } else {
            false
        };
        return res;
    }
}

#[derive(Debug)]
pub enum Error {
    InvalidModulus,
    InvalidPower,
    DifferentModulus,
}

struct ISize {
    value: isize,
}

impl Rem<usize> for ISize {
    type Output = usize;

    fn rem(self, rhs: usize) -> Self::Output {
        if self.value.is_negative() {
            // -a mod b = (b - (a mod b) mod b
            (rhs - (self.value.abs() as usize % rhs)) % rhs
        } else {
            let val = self.value as usize;
            val % rhs
        }
    }
}

// #[derive(Debug, Clone, Copy, PartialEq)]
// pub struct ST101Field {}

// impl FF for ST101Field {
//     type FieldType = usize;

//     const GENERATOR: usize = 5;

//     const MODULUS: usize = 3221225473;

//     fn zero() -> Self::FieldType {
//         0
//     }

//     fn one() -> Self::FieldType {
//         1
//     }
// }

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ST101FieldElement<F: FF> {
    element: F::FieldType,
}

impl<F: FF<FieldType = usize> + Copy + PartialEq> FFE<F> for ST101FieldElement<F> {
    fn from_field(element: F::FieldType) -> Self {
        ST101FieldElement { element }
    }
}

impl<F: FF<FieldType = usize>> Add for ST101FieldElement<F> {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            element: (self.element + rhs.element) % F::MODULUS,
        }
    }
}

impl<F: FF<FieldType = usize> + Copy> AddAssign for ST101FieldElement<F> {
    fn add_assign(&mut self, rhs: Self) {
        let addition = *self + rhs;
        *self = addition;
    }
}

impl<F: FF<FieldType = usize>> Mul for ST101FieldElement<F> {
    type Output = Self;

    fn mul(self, rhs: Self) -> Self::Output {
        Self {
            element: (self.element * rhs.element) % F::MODULUS,
        }
    }
}

impl<F: FF<FieldType = usize>> Sub for ST101FieldElement<F> {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        // TODO: investigate safety of conversion
        let (sub, _) = self.element.overflowing_sub(rhs.element);
        Self {
            element: ISize {
                value: sub as isize,
            } % F::MODULUS,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::*;

    // #[test]
    // fn add() {
    //     let ffe_1 = FINITE_FIELD.new(322122547).unwrap();
    //     let ffe_2 = FINITE_FIELD.new(8902).unwrap();
    //     let new_ff = ffe_1 + ffe_2;
    //     assert_eq!(
    //         new_ff.unwrap(),
    //         FFE {
    //             value: 322131449,
    //             ff: &FINITE_FIELD
    //         }
    //     );

    //     let ffe_3 = FINITE_FIELD.new(-67).unwrap();
    //     let ffe_4 = FINITE_FIELD.new(60).unwrap();
    //     let new_ff = ffe_3 + ffe_4;
    //     assert_eq!(
    //         new_ff.unwrap(),
    //         FFE {
    //             value: 3221225466,
    //             ff: &FINITE_FIELD
    //         }
    //     );

    //     let ffe_5 = FINITE_FIELD.new(67).unwrap();
    //     let ff = FF::init(1, 5).unwrap();
    //     let ffe_6 = ff.new(60).unwrap();
    //     let new_ff = ffe_5 + ffe_6;
    //     assert!(new_ff.is_err());
    // }

    //     #[test]
    //     fn mul() {
    //         let ffe_1 = FINITE_FIELD.new(1912323).unwrap();
    //         let ffe_2 = FINITE_FIELD.new(111091).unwrap();
    //         let new_ff = ffe_1 * ffe_2;
    //         assert_eq!(
    //             new_ff.unwrap(),
    //             FFE {
    //                 value: 3062218648,
    //                 ff: &FINITE_FIELD
    //             }
    //         );

    //         let ffe_3 = FINITE_FIELD.new(67).unwrap();
    //         let ffe_4 = FINITE_FIELD.new(4).unwrap();
    //         let new_ff = ffe_3 * ffe_4;
    //         assert_eq!(
    //             new_ff.unwrap(),
    //             FFE {
    //                 value: 268,
    //                 ff: &FINITE_FIELD
    //             }
    //         );

    //         let ffe_5 = FINITE_FIELD.new(67).unwrap();
    //         let ff = FF::init(1, 5).unwrap();
    //         let ffe_6 = ff.new(60).unwrap();
    //         let new_ff = ffe_5 * ffe_6;
    //         assert!(new_ff.is_err());
    //     }

    //     #[test]
    //     fn sub() {
    //         let ffe_1 = FINITE_FIELD.new(892).unwrap();
    //         let ffe_2 = FINITE_FIELD.new(7).unwrap();
    //         let new_ff = ffe_1 - ffe_2;
    //         assert_eq!(
    //             new_ff.unwrap(),
    //             FFE {
    //                 value: 885,
    //                 ff: &FINITE_FIELD
    //             }
    //         );

    //         let ffe_3 = FINITE_FIELD.new(2).unwrap();
    //         let ffe_4 = FINITE_FIELD.new(11).unwrap();
    //         let new_ff = ffe_3 - ffe_4;
    //         assert_eq!(
    //             new_ff.unwrap(),
    //             FFE {
    //                 value: 3221225464,
    //                 ff: &FINITE_FIELD
    //             }
    //         );

    //         let ffe_5 = FINITE_FIELD.new(67).unwrap();
    //         let ff = FF::init(1, 5).unwrap();
    //         let ffe_6 = ff.new(60).unwrap();
    //         let new_ff = ffe_5 - ffe_6;
    //         assert!(new_ff.is_err());
    //     }
}
