# Learn Cryptography - cryptography from scratch

## Overview

A collection of cryptographic techniques implemented from scratch in Python.

## Techniques

### Ancient Cryptography

- [Ceasar Cipher](/py/ciphers/caesar_cipher.py)
- [Simple Substitution Cipher](/py/ciphers/simple_substitution.py)
- [Polyalphabetic Cipher](/py/ciphers/polyaphabetic_cipher.py)

### 19th Century Cryptography

- [One Time Pad](/py/ciphers/one_time_pad.py)
- [XOR + One Time Pad](/py/ciphers/xor_and_one_time_pad.py)

### Modern Cryptography

- [Hash-based Message Authentication Code (HMAC)](/py/mac/hmac.py)
- [Diffie Hallman Key Exchange](/py/key_exchange/diffie_hellman.py)
- [RSA](/py/rsa.py)
- [Secure Hashing Algorithm 1 (SHA-1)](/py/commitments/hashing/sha1.py)
- [Secure Hashing Algorithm 2 224 (SHA2-224)](/py/commitments/hashing/sha2/sha224.py)
- [Secure Hashing Algorithm 2 256 (SHA2-256)](/py/commitments/hashing/sha2/sha256.py)
- [Secure Hashing Algorithm 2 384 (SHA2-384)](/py/commitments/hashing/sha2/sha384.py)
- [Secure Hashing Algorithm 2 512 (SHA2-512)](/py/commitments/hashing/sha2/sha512.py)
- [Elliptic Curve Diffie-Hellman (ECDH)](/py/key_exchange/ecdh.py)
- [Elliptic Curve Digital Signature Algorithm (ECDSA)](/py/signatures/ecdsa.py)
<!-- - [Edwards-curve Digital Signature Algorithm (EdDSA)](/py/signatures/eddsa.py) (WIP) -->
<!-- - [BLS Signature](/py/signatures/bls_sig.py) (WIP) -->
<!-- - [Schnorr Signature](/py/signatures/schnorr_sig.py) (WIP) -->
- [Pedersen Commitments using Modular Exponentiation](/py/commitments/pedcomm_mod.py)
- [Pedersen Commitments using Elliptic Curve Cryptography](/py/commitments/pedcomm_ecc.py)
<!-- - [Pedersen Commitments + Inner Product Argument](/py/commitments/pedcomm_ipa.py) (WIP) -->
- [Basic Polynomial Commitment using Modular Exponentiation](/py/commitments/polynomials/basic_polynomial_comm_using_mod.py)
- [Basic Polynomial Commitment using Elliptic Curve Cryptography](/py/commitments/polynomials/basic_polynomial_comm_using_ecc.py)
- [Basic Trusted Setup using Modular Exponentiation](/py/commitments/polynomials/basic_trusted_setup_mod.py)
- [Basic Trusted Setup using Elliptic Curve Cryptography](/py/commitments/polynomials/basic_trusted_setup_ecc.py)
<!-- - [KZG Polynomial Commitments](/py/commitments/kzg.py) (WIP) -->

#### Utils

- [Number Theory](/py/utils/number_theory.py)
- [Finite Field](/py/utils/fields.py)
- [Naive Elliptic Curve](/py/utils/ecc.py)
- [Bandersnatch Curve](/py/utils/ecc/bandersnatch/curve.py)
- [Bandersnatch Field](/py/utils/ecc/bandersnatch/fields.py)

## Usage

This serves as a learning material for me in my journey to becoming proficient at cryptography. I hope it helps you learn as well.

## Disclamer

You probably know this but DO NOT USE IN PRODUCTION.
