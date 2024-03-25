use ff::FF;

const FIELD_MODULUS: usize = 3221225473;

const GENERATOR: usize = 5;

fn main() {
    let ff = FF::init(GENERATOR, FIELD_MODULUS).unwrap();
    let ff_1 = ff.new(3221225472).unwrap();
    let ff_2 = ff.new(10).unwrap();
    let res = ff_1 + ff_2;

    // let a = vec![FFE::new(1, GENERATOR, FIELD_MODULUS)];
    println!("{:?}", res.unwrap());
}
