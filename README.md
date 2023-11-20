# cryptographic techniques

## overview

a collection of cryptographic techniques implemented from scratch in python.

## techniques

### ancient cryptography

- [ceasar cipher](/ciphers/caesar_cipher.py)
- [simple substitution cipher](/ciphers/simple_substitution.py)
- [polyalphabetic cipher](/ciphers/polyaphabetic_cipher.py)

### 19th century cryptography

- [one time pad](/ciphers/one_time_pad.py)
- [XOR + one time pad](/ciphers/xor_and_one_time_pad.py)

### modern cryptography

- [simple hashing](/commitments/simple_hashing.py) (WIP)
- [diffie hellman key exchange](/key_exchange/diffie_hellman.py)
- [RSA](./rsa.py)
- [elliptic curve diffie-hellman (ECDH)](/key_exchange/ecdh.py)
- [elliptic curve digital signature algorithm (ECDSA)](/signatures/ecdsa.py)
- [edwards-curve digital signature algorithm (EdDSA)](/signatures/eddsa.py) (WIP)
- [BLS signature](/signatures/bls_sig.py) (WIP)
- [schnorr signature](/signatures/schnorr_sig.py) (WIP)
- [pedersen commitments using modular exponentiation](/commitments/pedcomm_mod.py)
- [pedersen commitments using elliptic curve cryptography](/commitments/pedcomm_ecc.py)
- [pedersen commitments + inner product argument](/commitments/pedcomm_ipa.py) (WIP)
- [basic polynomial commitment using modular exponentiation](/commitments/polynomials/basic_polynomial_comm_using_mod.py)
- [basic polynomial commitment using elliptic curve cryptography](/commitments/polynomials/basic_polynomial_comm_using_ecc.py)
- [basic trusted setup using modular exponentiation](/commitments/polynomials/basic_trusted_setup_mod.py)
- [basic trusted setup using elliptic curve cryptography](/commitments/polynomials/basic_trusted_setup_ecc.py)
- [KZG polynomial commitments](/commitments/kzg.py) (WIP)

#### utils

- [number theory](/utils/number_theory.py)
- [finite field](/utils/fields.py)
- [naive elliptic curve](/utils/ecc.py)
- [bandersnatch curve](/utils/ecc/bandersnatch/curve.py)
- [bandersnatch field](/utils/ecc/bandersnatch/fields.py)

## usage

this serves as a learning material for me in my journey to becoming a proficient at cryptography. I hope it helps you learn as well.

## disclaimer

**this is a learning material and not to be used as in production**.
