use std::path::Display;

#[derive(Debug)]
struct FF {
    // modulus
    n: usize,
    // element
    value: isize
}

impl FF {

    fn new(value: isize, n: usize) -> Self {
        FF{value: value % n, n: n}
    }
    
    fn zero(&self) -> Self {
        FF{n: self.n, value: 0}
    }

    fn one(&self) -> Self {
        FF{n: self.n, value: 1}
    }
}

// impl FF {
    
// }

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        // let result = add(2, 2);
        // assert_eq!(result, 4);
    }
}