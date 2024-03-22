use std::ops::{Add, Mul, Rem, Sub};

#[derive(Debug, PartialEq, Eq)]
pub struct FFE {
    // modulus
    n: usize,
    // element
    value: usize,
    // generator
    g: usize,
}

struct ISize {
    value: isize,
}

#[derive(Debug)]
pub enum Error {
    InvalidModulus,
    DifferentModulus,
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

impl Add for FFE {
    type Output = Result<Self, Error>;

    fn add(self, rhs: Self) -> Self::Output {
        if self.n != rhs.n {
            return Err(Error::DifferentModulus);
        } else {
            Ok(Self {
                value: (self.value + rhs.value) % self.n,
                n: self.n,
                g: self.g,
            })
        }
    }
}

impl Mul for FFE {
    type Output = Result<Self, Error>;

    fn mul(self, rhs: Self) -> Self::Output {
        if self.n != rhs.n {
            return Err(Error::DifferentModulus);
        } else {
            Ok(Self {
                value: (self.value * rhs.value) % self.n,
                n: self.n,
                g: self.g,
            })
        }
    }
}

impl Sub for FFE {
    type Output = Result<Self, Error>;

    fn sub(self, rhs: Self) -> Self::Output {
        if self.n != rhs.n {
            return Err(Error::DifferentModulus);
        } else {
            // TODO: investigate safety of conversion
            let (sub, _) = self.value.overflowing_sub(rhs.value);
            Ok(Self {
                value: ISize {
                    value: sub as isize,
                } % self.n,
                n: self.n,
                g: self.g,
            })
        }
    }
}

impl FFE {
    pub fn new(value: isize, g: usize, n: usize) -> Result<Self, Error> {
        if n == 0 || n == 1 {
            return Err(Error::InvalidModulus);
        }
        Ok(Self {
            value: ISize { value } % n,
            n,
            g,
        })
    }

    pub fn zero(&self) -> Self {
        FFE {
            n: self.n,
            g: self.g,
            value: 0,
        }
    }

    pub fn one(&self) -> Self {
        FFE {
            n: self.n,
            g: self.g,
            value: 1,
        }
    }

    pub fn get_element(&self) -> usize {
        self.n
    }
}

#[cfg(test)]
mod tests {
    use crate::FFE;

    #[test]
    fn new() {
        assert_eq!(
            FFE::new(4, 1, 5).unwrap(),
            FFE {
                value: 4,
                n: 5,
                g: 1
            }
        );
        assert_eq!(
            FFE::new(8, 1, 5).unwrap(),
            FFE {
                value: 3,
                n: 5,
                g: 1
            }
        );
        assert_eq!(
            FFE::new(77, 1, 5).unwrap(),
            FFE {
                value: 2,
                n: 5,
                g: 1
            }
        );
        // negative value
        assert_eq!(
            FFE::new(-6, 1, 5).unwrap(),
            FFE {
                value: 4,
                n: 5,
                g: 1
            }
        );
        assert_eq!(
            FFE::new(-20, 1, 5).unwrap(),
            FFE {
                value: 0,
                n: 5,
                g: 1
            }
        );
        assert_eq!(
            FFE::new(-89, 1, 5).unwrap(),
            FFE {
                value: 1,
                n: 5,
                g: 1
            }
        );
    }

    #[test]
    fn zero() {
        let ff_1 = FFE::new(10, 1, 5).unwrap();
        assert_eq!(
            ff_1.zero(),
            FFE {
                value: 0,
                n: 5,
                g: 1
            }
        );
    }

    #[test]
    fn one() {
        let ff_1 = FFE::new(10, 1, 5).unwrap();
        assert_eq!(
            ff_1.one(),
            FFE {
                value: 1,
                n: 5,
                g: 1
            }
        );
    }

    #[test]
    fn add() {
        let ff_1 = FFE::new(19, 1, 5).unwrap();
        let ff_2 = FFE::new(10, 1, 5).unwrap();
        let new_ff = ff_1 + ff_2;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 4,
                n: 5,
                g: 1
            }
        );

        let ff_3 = FFE::new(67, 1, 7).unwrap();
        let ff_4 = FFE::new(60, 1, 7).unwrap();
        let new_ff = ff_3 + ff_4;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 1,
                n: 7,
                g: 1
            }
        );

        let ff_5 = FFE::new(67, 1, 7).unwrap();
        let ff_6 = FFE::new(60, 1, 13).unwrap();
        let new_ff = ff_5 + ff_6;
        assert!(new_ff.is_err());
    }

    #[test]
    fn mul() {
        let ff_1 = FFE::new(19, 1, 5).unwrap();
        let ff_2 = FFE::new(11, 1, 5).unwrap();
        let new_ff = ff_1 * ff_2;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 4,
                n: 5,
                g: 1
            }
        );

        let ff_3 = FFE::new(67, 1, 7).unwrap();
        let ff_4 = FFE::new(4, 1, 7).unwrap();
        let new_ff = ff_3 * ff_4;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 2,
                n: 7,
                g: 1
            }
        );

        let ff_5 = FFE::new(67, 1, 7).unwrap();
        let ff_6 = FFE::new(60, 1, 13).unwrap();
        let new_ff = ff_5 * ff_6;
        assert!(new_ff.is_err());
    }

    #[test]
    fn sub() {
        let ff_1 = FFE::new(19, 1, 5).unwrap();
        let ff_2 = FFE::new(7, 1, 5).unwrap();
        let new_ff = ff_1 - ff_2;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 2,
                n: 5,
                g: 1
            }
        );

        let ff_3 = FFE::new(2, 1, 7).unwrap();
        let ff_4 = FFE::new(11, 1, 7).unwrap();
        let new_ff = ff_3 - ff_4;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 5,
                n: 7,
                g: 1
            }
        );

        let ff_5 = FFE::new(67, 1, 7).unwrap();
        let ff_6 = FFE::new(60, 1, 13).unwrap();
        let new_ff = ff_5 - ff_6;
        assert!(new_ff.is_err());
    }
}
