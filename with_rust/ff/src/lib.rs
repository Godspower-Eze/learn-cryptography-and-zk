use std::ops::{Add, Mul, Rem, Sub};

#[derive(Debug, PartialEq, Clone, Copy)]
pub struct FF {
    // modulus
    n: usize,
    // generator
    g: usize,
}

#[derive(Debug, PartialEq, Clone, Copy)]
pub struct FFE<'a> {
    ff: &'a FF,
    // element
    value: usize,
}

struct ISize {
    value: isize,
}

#[derive(Debug)]
pub enum Error {
    InvalidModulus,
    InvalidPower,
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

impl Add for FFE<'_> {
    type Output = Result<Self, Error>;

    fn add(self, rhs: Self) -> Self::Output {
        if self.ff != rhs.ff {
            return Err(Error::DifferentModulus);
        } else {
            Ok(Self {
                value: (self.value + rhs.value) % rhs.ff.n,
                ..self
            })
        }
    }
}

impl Mul for FFE<'_> {
    type Output = Result<Self, Error>;

    fn mul(self, rhs: Self) -> Self::Output {
        if self.ff != rhs.ff {
            return Err(Error::DifferentModulus);
        } else {
            Ok(Self {
                value: (self.value * rhs.value) % rhs.ff.n,
                ..self
            })
        }
    }
}

impl Sub for FFE<'_> {
    type Output = Result<Self, Error>;

    fn sub(self, rhs: Self) -> Self::Output {
        if self.ff != rhs.ff {
            return Err(Error::DifferentModulus);
        } else {
            // TODO: investigate safety of conversion
            let (sub, _) = self.value.overflowing_sub(rhs.value);
            Ok(Self {
                value: ISize {
                    value: sub as isize,
                } % rhs.ff.n,
                ..self
            })
        }
    }
}

impl FF {
    pub fn init(g: usize, n: usize) -> Result<Self, Error> {
        if n == 0 || n == 1 {
            return Err(Error::InvalidModulus);
        } else {
            Ok(Self { n, g })
        }
    }

    pub fn zero(&self) -> FFE {
        FFE { ff: self, value: 0 }
    }

    pub fn one(&self) -> FFE {
        FFE { ff: self, value: 1 }
    }

    pub fn new(&self, value: isize) -> Result<FFE, Error> {
        if self.n == 0 || self.n == 1 {
            return Err(Error::InvalidModulus);
        }
        Ok(FFE {
            ff: self,
            value: ISize { value } % self.n,
        })
    }

    pub fn generator(&self) -> FFE {
        FFE {
            ff: self,
            value: self.g,
        }
    }
}

impl FFE<'_> {
    pub fn pow(&self, mut n: usize) -> Result<Self, Error> {
        let mut current_power = Self { ..*self };
        let mut result = self.ff.one();
        while n > 0 {
            if n % 2 == 1 {
                result = (result * current_power)?;
            }
            n = n / 2;
            current_power = (current_power * current_power)?;
        }
        Ok(result)
    }

    pub fn is_order(&self, order: usize) -> bool {
        let identity = self.ff.one();
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

    pub fn ff(&self) -> FF {
        *self.ff
    }
}

#[cfg(test)]
mod tests {
    use crate::*;

    const FIELD_MODULUS: usize = 3221225473;

    const GENERATOR: usize = 5;

    const FINITE_FIELD: FF = FF {
        g: GENERATOR,
        n: FIELD_MODULUS,
    };

    #[test]
    fn init() {
        assert_eq!(
            FF::init(GENERATOR, FIELD_MODULUS).unwrap(),
            FF {
                g: GENERATOR,
                n: FIELD_MODULUS
            }
        );
    }

    #[test]
    fn new() {
        assert_eq!(
            FINITE_FIELD.new(90).unwrap(),
            FFE {
                value: 90,
                ff: &FINITE_FIELD
            },
        );
        assert_eq!(
            FINITE_FIELD.new(3).unwrap(),
            FFE {
                value: 3,
                ff: &FINITE_FIELD
            }
        );
        assert_eq!(
            FINITE_FIELD.new(3221225482).unwrap(),
            FFE {
                value: 9,
                ff: &FINITE_FIELD
            }
        );
        // negative value
        assert_eq!(
            FINITE_FIELD.new(-6).unwrap(),
            FFE {
                value: 3221225467,
                ff: &FINITE_FIELD
            }
        );
        assert_eq!(
            FINITE_FIELD.new(-20).unwrap(),
            FFE {
                value: 3221225453,
                ff: &FINITE_FIELD
            }
        );
        assert_eq!(
            FINITE_FIELD.new(-89).unwrap(),
            FFE {
                value: 3221225384,
                ff: &FINITE_FIELD
            }
        );
    }

    #[test]
    fn zero() {
        assert_eq!(
            FINITE_FIELD.zero(),
            FFE {
                value: 0,
                ff: &FINITE_FIELD
            }
        );
    }

    #[test]
    fn one() {
        assert_eq!(
            FINITE_FIELD.one(),
            FFE {
                value: 1,
                ff: &FINITE_FIELD
            }
        );
    }

    #[test]
    fn add() {
        let ffe_1 = FINITE_FIELD.new(322122547).unwrap();
        let ffe_2 = FINITE_FIELD.new(8902).unwrap();
        let new_ff = ffe_1 + ffe_2;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 322131449,
                ff: &FINITE_FIELD
            }
        );

        let ffe_3 = FINITE_FIELD.new(-67).unwrap();
        let ffe_4 = FINITE_FIELD.new(60).unwrap();
        let new_ff = ffe_3 + ffe_4;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 3221225466,
                ff: &FINITE_FIELD
            }
        );

        let ffe_5 = FINITE_FIELD.new(67).unwrap();
        let ff = FF::init(1, 5).unwrap();
        let ffe_6 = ff.new(60).unwrap();
        let new_ff = ffe_5 + ffe_6;
        assert!(new_ff.is_err());
    }

    #[test]
    fn mul() {
        let ffe_1 = FINITE_FIELD.new(1912323).unwrap();
        let ffe_2 = FINITE_FIELD.new(111091).unwrap();
        let new_ff = ffe_1 * ffe_2;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 3062218648,
                ff: &FINITE_FIELD
            }
        );

        let ffe_3 = FINITE_FIELD.new(67).unwrap();
        let ffe_4 = FINITE_FIELD.new(4).unwrap();
        let new_ff = ffe_3 * ffe_4;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 268,
                ff: &FINITE_FIELD
            }
        );

        let ffe_5 = FINITE_FIELD.new(67).unwrap();
        let ff = FF::init(1, 5).unwrap();
        let ffe_6 = ff.new(60).unwrap();
        let new_ff = ffe_5 * ffe_6;
        assert!(new_ff.is_err());
    }

    #[test]
    fn sub() {
        let ffe_1 = FINITE_FIELD.new(892).unwrap();
        let ffe_2 = FINITE_FIELD.new(7).unwrap();
        let new_ff = ffe_1 - ffe_2;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 885,
                ff: &FINITE_FIELD
            }
        );

        let ffe_3 = FINITE_FIELD.new(2).unwrap();
        let ffe_4 = FINITE_FIELD.new(11).unwrap();
        let new_ff = ffe_3 - ffe_4;
        assert_eq!(
            new_ff.unwrap(),
            FFE {
                value: 3221225464,
                ff: &FINITE_FIELD
            }
        );

        let ffe_5 = FINITE_FIELD.new(67).unwrap();
        let ff = FF::init(1, 5).unwrap();
        let ffe_6 = ff.new(60).unwrap();
        let new_ff = ffe_5 - ffe_6;
        assert!(new_ff.is_err());
    }
}
