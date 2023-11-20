# Cryptographic Techniques

## Overview

A collection of cryptographic techniques implemented from scratch in python.

## Techniques

### Ancient Cryptography

- [Ceasar Cipher](/ciphers/caesar_cipher.py)
- [Simple Substitution Cipher](/ciphers/simple_substitution.py)
- [Polyalphabetic Cipher](/ciphers/polyaphabetic_cipher.py)

### 19th Century Cryptography

- [One Time Pad](/ciphers/one_time_pad.py)
- [XOR + One Time Pad](/ciphers/xor_and_one_time_pad.py)

### Modern Cryptography

- [Simple Hashing](/commitments/simple_hashing.py) (WIP)
- [Diffie Hallman Key Exchange](/key_exchange/diffie_hellman.py)
- [RSA](./rsa.py)
- [Elliptic Curve Diffie-Hellman (ECDH)](/key_exchange/ecdh.py)
- [Elliptic Curve Digital Signature Algorithm (ECDSA)](/signatures/ecdsa.py)
- [Edwards-curve Digital Signature Algorithm (EdDSA)](/signatures/eddsa.py) (WIP)
- [BLS Signature](/signatures/bls_sig.py) (WIP)
- [Schnorr Signature](/signatures/schnorr_sig.py) (WIP)
- [Pedersen Commitments using Modular Exponentiation](/commitments/pedcomm_mod.py)
- [Pedersen Commitments using Elliptic Curve Cryptography](/commitments/pedcomm_ecc.py)
- [Pedersen Commitments + Inner Product Argument](/commitments/pedcomm_ipa.py) (WIP)
- [Basic Polynomial Commitment using Modular Exponentiation](/commitments/polynomials/basic_polynomial_comm_using_mod.py)
- [Basic Polynomial Commitment using Elliptic Curve Cryptography](/commitments/polynomials/basic_polynomial_comm_using_ecc.py)
- [Basic Trusted Setup using Modular Exponentiation](/commitments/polynomials/basic_trusted_setup_mod.py)
- [Basic Trusted Setup using Elliptic Curve Cryptography](/commitments/polynomials/basic_trusted_setup_ecc.py)
- [KZG Polynomial Commitments](/commitments/kzg.py) (WIP)

#### Utils

- [Number Theory](/utils/number_theory.py)
- [Finite Field](/utils/fields.py)
- [Naive Elliptic Curve](/utils/ecc.py)
- [Bandersnatch Curve](/utils/ecc/bandersnatch/curve.py)
- [Bandersnatch Field](/utils/ecc/bandersnatch/fields.py)

## Usage

This serves as a learning material for me in my journey to becoming a proficient at cryptography. I hope it helps you learn as well.

## Disclamer

You probably know this but DO NOT USE IN PRODUCTION. Cryptography is a delicate pierce of art.
