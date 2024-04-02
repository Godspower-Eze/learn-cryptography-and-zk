use ff::FF;

const FIELD_MODULUS: usize = 3221225473;

const GENERATOR: usize = 5;

fn main() {
    // PART 1: Trace and Low-Degree Extension

    let ff = FF::init(GENERATOR, FIELD_MODULUS).unwrap();

    let first = ff.new(1).unwrap();
    let second = ff.new(3141592).unwrap();

    let mut elements = vec![first, second];

    for _ in 2..1023 {
        let a = elements[elements.len() - 2];
        let b = elements[elements.len() - 1];
        let val = (a.pow(2).unwrap() + b.pow(2).unwrap()).unwrap();
        elements.push(val);
    }

    let g = ff.generator().pow(3 * 2_usize.pow(20)).unwrap();
    let mut generated_elements = Vec::new();

    for i in 0..1024 {
        generated_elements.push(g.pow(i).unwrap())
    }

    assert!(g.is_order(1024), "the generator is of wrong order");
    let mut b = ff.one();
    for i in 0..1023 {
        assert!(
            b == generated_elements[i],
            "The i-th place in G is not equal to the i-th power of g."
        );
        b = (b * g).unwrap();
        assert!(b != ff.one(), "g is of order {}", i + 1)
    }
    if (b * g).unwrap() == ff.one() {
        print!("Success")
    } else {
        print!("g is order > 1024")
    }
}
