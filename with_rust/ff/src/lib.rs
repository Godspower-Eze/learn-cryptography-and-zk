use std::{
    ops::{Add, AddAssign, Div, DivAssign, Mul, MulAssign, Rem, Sub, SubAssign},
    usize,
};

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

pub trait FF {
    type FieldType;

    const GENERATOR: Self::FieldType;

    const MODULUS: Self::FieldType;
}

pub trait FFE<F: FF>:
    Sized
    + PartialEq
    + Copy
    + Add
    + Sub
    + Mul<Output = Self>
    + Div
    + SubAssign
    + AddAssign
    + MulAssign
    + DivAssign
{
    fn from_field(element: isize) -> Self;

    fn new(element: isize) -> Self {
        Self::from_field(element)
    }

    fn zero() -> Self {
        Self::from_field(0)
    }

    fn one() -> Self {
        Self::from_field(1)
    }

    fn inverse(&self) -> Self;

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

fn multiplicative_inverse(a: usize, b: usize) -> Result<usize, String> {
    /*
     * Computes the multiplicative inverse of a mod b
     * using the "Extended Euclidean Algorithm"
     */

    let modulus = b;

    let (mut m, mut n);
    if a > b {
        m = a;
        n = b;
    } else {
        m = b;
        n = a;
    }
    let mut q = m / n; // quotient
    let mut r = m % n; // remainder
    let (mut t_0, mut t_1) = (0, 1);
    let mut t = t_0 - (t_1 * q);

    while n != 0 {
        (m, n) = (n, r);
        (t_0, t_1) = (t_1, t);
        q = m / n;
        r = m % n;
        t = t_0 - t_1 * q
    }

    match n {
        1 => Ok(t_1 % modulus),
        _ => Err(String::from("Nultiplicative inverse does not exist")),
    }
}

#[cfg(test)]
mod tests {
    use crate::*;
    use std::ops::{Add, AddAssign, Div, Sub};

    #[derive(Debug, Clone, Copy, PartialEq)]
    struct TestFF {}

    impl FF for TestFF {
        type FieldType = usize;
        const GENERATOR: usize = 5;
        const MODULUS: usize = 3221225473;
    }

    #[derive(Debug, Clone, Copy, PartialEq)]
    struct TestFFE<F: FF> {
        element: F::FieldType,
    }

    impl<F: FF<FieldType = usize> + Copy + PartialEq> FFE<F> for TestFFE<F> {
        fn from_field(value: isize) -> Self {
            let field_element = ISize { value } % F::MODULUS;
            TestFFE {
                element: field_element,
            }
        }

        fn inverse(&self) -> Self {
            let inv = multiplicative_inverse(self.element, F::MODULUS).unwrap();
            Self { element: inv }
        }
    }

    impl<F: FF<FieldType = usize>> Add for TestFFE<F> {
        type Output = Self;

        fn add(self, rhs: Self) -> Self::Output {
            Self {
                element: (self.element + rhs.element) % F::MODULUS,
            }
        }
    }

    impl<F: FF<FieldType = usize> + Copy> AddAssign for TestFFE<F> {
        fn add_assign(&mut self, rhs: Self) {
            let addition = *self + rhs;
            *self = addition;
        }
    }

    impl<F: FF<FieldType = usize>> Mul for TestFFE<F> {
        type Output = Self;

        fn mul(self, rhs: Self) -> Self::Output {
            Self {
                element: (self.element * rhs.element) % F::MODULUS,
            }
        }
    }

    impl<F: FF<FieldType = usize> + Copy> MulAssign for TestFFE<F> {
        fn mul_assign(&mut self, rhs: Self) {
            let mul = *self * rhs;
            *self = mul;
        }
    }

    impl<F: FF<FieldType = usize>> Sub for TestFFE<F> {
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

    impl<F: FF<FieldType = usize> + Copy> SubAssign for TestFFE<F> {
        fn sub_assign(&mut self, rhs: Self) {
            let sub = *self - rhs;
            *self = sub;
        }
    }

    impl<F: FF<FieldType = usize> + Copy + PartialEq> Div for TestFFE<F> {
        type Output = Self;

        fn div(self, rhs: Self) -> Self::Output {
            let inv = rhs.inverse();
            self * inv
        }
    }

    impl<F: FF<FieldType = usize> + Copy + PartialEq> DivAssign for TestFFE<F> {
        fn div_assign(&mut self, rhs: Self) {
            let div = *self / rhs;
            *self = div;
        }
    }

    #[test]
    fn assignment() {
        let ffe_1 = TestFFE::<TestFF>::new(-56);
        let ffe_2 = TestFFE::<TestFF>::new(9704);
        let ffe_3 = TestFFE::<TestFF>::new(3221225477);
        assert_eq!(
            ffe_1,
            TestFFE {
                element: 3221225417
            }
        );
        assert_eq!(ffe_2, TestFFE { element: 9704 });
        assert_eq!(ffe_3, TestFFE { element: 4 });
    }

    #[test]
    fn add() {
        let ffe_1 = TestFFE::<TestFF>::new(56);
        let ffe_2 = TestFFE::<TestFF>::new(8902);
        let new_ff = ffe_1 + ffe_2;
        assert_eq!(new_ff, TestFFE { element: 8958 });
    }

    #[test]
    fn add_assign() {
        let mut ffe_1 = TestFFE::<TestFF>::new(56);
        let ffe_2 = TestFFE::<TestFF>::new(8902);
        ffe_1 += ffe_2;
        assert_eq!(ffe_1, TestFFE { element: 8958 });
    }

    #[test]
    fn mul() {
        let ffe_1 = TestFFE::<TestFF>::new(1912323);
        let ffe_2 = TestFFE::<TestFF>::new(111091);
        let new_ff = ffe_1 * ffe_2;
        assert_eq!(
            new_ff,
            TestFFE {
                element: 3062218648
            }
        );
    }

    #[test]
    fn mul_assign() {
        let mut ffe_1 = TestFFE::<TestFF>::new(1912323);
        let ffe_2 = TestFFE::<TestFF>::new(111091);
        ffe_1 *= ffe_2;
        assert_eq!(
            ffe_1,
            TestFFE {
                element: 3062218648
            }
        );
    }

    #[test]
    fn sub() {
        let ffe_1 = TestFFE::<TestFF>::new(892);
        let ffe_2 = TestFFE::<TestFF>::new(7);
        let new_ff = ffe_1 - ffe_2;
        assert_eq!(new_ff, TestFFE { element: 885 });

        let ffe_3 = TestFFE::<TestFF>::new(2);
        let ffe_4 = TestFFE::<TestFF>::new(11);
        let new_ff = ffe_3 - ffe_4;
        assert_eq!(
            new_ff,
            TestFFE {
                element: 3221225464
            }
        );
    }

    #[test]
    fn sub_assign() {
        let mut ffe_1 = TestFFE::<TestFF>::new(2);
        let ffe_2 = TestFFE::<TestFF>::new(11);
        ffe_1 -= ffe_2;
        assert_eq!(
            ffe_1,
            TestFFE {
                element: 3221225464
            }
        );
    }

    #[test]
    fn div() {
        let ffe_1 = TestFFE::<TestFF>::new(892);
        let ffe_2 = TestFFE::<TestFF>::new(7);
        let new_ff = ffe_1 / ffe_2;
        println!("{:?}", new_ff);
        assert_eq!(new_ff, TestFFE { element: 885 });

        // let ffe_3 = TestFFE::<TestFF>::new(2);
        // let ffe_4 = TestFFE::<TestFF>::new(11);
        // let new_ff = ffe_3 / ffe_4;
        // assert_eq!(
        //     new_ff,
        //     TestFFE {
        //         element: 3221225464
        //     }
        // );
    }
}
