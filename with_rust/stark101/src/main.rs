use ff::FF;

const FIELD_MODULUS: usize = 3221225473;

const GENERATOR: usize = 5;

fn main() {
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
    let mut G = Vec::new();

    for i in 0..1024 {
        G.push(g.pow(i))
    }
    println!("{:?}", G);
}
