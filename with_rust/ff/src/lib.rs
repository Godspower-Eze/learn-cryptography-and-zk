use std::ops::{Rem, Add, Sub, Mul, Div};

#[derive(Debug, PartialEq, Eq)]
pub struct FF {
    // modulus
    n: usize,
    // element
    value: usize
}

struct ISize {
    value: isize,
}

#[derive(Debug)]
pub enum Error {
    InvalidModulus,
    DifferentModulus
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

impl Add for FF {

    type Output = Result<Self, Error>;

    fn add(self, rhs: Self) -> Self::Output {
        if self.n != rhs.n {
            return Err(Error::DifferentModulus);
        } else {
            Ok(Self {value: (self.value + rhs.value) % self.n, n: self.n})
        }
    }
    
}

impl Mul for FF {

    type Output = Result<Self, Error>;

    fn mul(self, rhs: Self) -> Self::Output {
        if self.n != rhs.n {
            return Err(Error::DifferentModulus);
        } else {
            Ok(Self {value: (self.value * rhs.value) % self.n, n: self.n})
        }
    }
}

impl Sub for FF {

    type Output = Result<Self, Error>;

    fn sub(self, rhs: Self) -> Self::Output {
        if self.n != rhs.n {
            return Err(Error::DifferentModulus);
        } else {
            // TODO: investigate safety of conversion
            let (sub, _) = self.value.overflowing_sub(rhs.value);
            Ok(Self {value: ISize {value: sub as isize} % self.n, n: self.n})
        }
    }

}

// impl Div for FF {
    
// }

impl FF {

    pub fn new(value: isize, n: usize) -> Result<Self, Error> {
        if n == 0 || n == 1 {
            return Err(Error::InvalidModulus);
        }
        Ok(Self{value: ISize {value} % n, n: n})
    }

    pub fn zero(n: usize) -> Self {
        FF{n, value: 0}
    }

    pub fn one(n: usize) -> Self {
        FF{n, value: 1}
    }
}

#[cfg(test)]
mod tests {
    use crate::FF;

    #[test]
    fn new() {
        assert_eq!(FF::new(4, 5).unwrap(), FF{value: 4, n: 5});
        assert_eq!(FF::new(8, 5).unwrap(), FF{value: 3, n: 5});
        assert_eq!(FF::new(77, 5).unwrap(), FF{value: 2, n: 5});
        // negative value
        assert_eq!(FF::new(-6, 5).unwrap(), FF{value: 4, n: 5});
        assert_eq!(FF::new(-20, 5).unwrap(), FF{value: 0, n: 5});
        assert_eq!(FF::new(-89, 5).unwrap(), FF{value: 1, n: 5});
    }

    #[test]
    fn zero() {
        assert_eq!(FF::zero(5), FF{value: 0, n: 5});
    }
    
    #[test]
    fn one() {
        assert_eq!(FF::one(5), FF{value: 1, n: 5});
    }

    #[test]
    fn add() {
        let ff_1 = FF::new(19, 5).unwrap();
        let ff_2 = FF::new(10, 5).unwrap();
        let new_ff = ff_1 + ff_2;
        assert_eq!(new_ff.unwrap(), FF{value: 4, n: 5});

        let ff_3 = FF::new(67, 7).unwrap();
        let ff_4 = FF::new(60, 7).unwrap();
        let new_ff = ff_3 + ff_4;
        assert_eq!(new_ff.unwrap(), FF{value: 1, n: 7});

        let ff_5 = FF::new(67, 7).unwrap();
        let ff_6 = FF::new(60, 13).unwrap();
        let new_ff = ff_5 + ff_6;
        assert!(new_ff.is_err());
    }

    #[test]
    fn mul() {
        let ff_1 = FF::new(19, 5).unwrap();
        let ff_2 = FF::new(11, 5).unwrap();
        let new_ff = ff_1 * ff_2;
        assert_eq!(new_ff.unwrap(), FF{value: 4, n: 5});

        let ff_3 = FF::new(67, 7).unwrap();
        let ff_4 = FF::new(4, 7).unwrap();
        let new_ff = ff_3 * ff_4;
        assert_eq!(new_ff.unwrap(), FF{value: 2, n: 7});

        let ff_5 = FF::new(67, 7).unwrap();
        let ff_6 = FF::new(60, 13).unwrap();
        let new_ff = ff_5 * ff_6;
        assert!(new_ff.is_err());
    }

    #[test]
    fn sub() {
        let ff_1 = FF::new(19, 5).unwrap();
        let ff_2 = FF::new(7, 5).unwrap();
        let new_ff = ff_1 - ff_2;
        assert_eq!(new_ff.unwrap(), FF{value: 2, n: 5});

        let ff_3 = FF::new(2, 7).unwrap();
        let ff_4 = FF::new(11, 7).unwrap();
        let new_ff = ff_3 - ff_4;
        assert_eq!(new_ff.unwrap(), FF{value: 5, n: 7});

        let ff_5 = FF::new(67, 7).unwrap();
        let ff_6 = FF::new(60, 13).unwrap();
        let new_ff = ff_5 - ff_6;
        assert!(new_ff.is_err());
    }
}