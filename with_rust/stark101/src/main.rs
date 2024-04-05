use ff::{ST101Field, ST101FieldElement, FFE};
use poly::UniPoly;

fn main() {
    // PART 1: Trace and Low-Degree Extension

    let first = ST101FieldElement::<ST101Field>::from_field(3221225472);
    let second = ST101FieldElement::<ST101Field>::from_field(10);

    let mut elements = vec![first, second];

    let addition = first + second;

    for _ in 2..1023 {
        let a = elements[elements.len() - 2];
        let b = elements[elements.len() - 1];
        let val = a.pow(2).unwrap() + b.pow(2).unwrap();
        elements.push(val);
    }

    let g = ST101FieldElement::<ST101Field>::generator()
        .pow(3 * 2_usize.pow(20))
        .unwrap();
    let mut generated_elements = Vec::new();

    for i in 0..1024 {
        generated_elements.push(g.pow(i).unwrap())
    }

    let one = ST101FieldElement::<ST101Field>::one();

    assert!(g.is_order(1024), "the generator is of wrong order");
    let mut b = one;
    for i in 0..1023 {
        assert!(
            b == generated_elements[i],
            "The i-th place in G is not equal to the i-th power of g."
        );
        b = b * g;
        assert!(b != one, "g is of order {}", i + 1)
    }
    if b * g == one {
        print!("Success")
    } else {
        print!("g is order > 1024")
    }

    let x = UniPoly::<ST101FieldElement<ST101Field>, ST101Field>::x();
    println!("{:?}", x);

    // let p = 2 * x.pow(2) + 1;
    println!("{:?}", addition);
}
