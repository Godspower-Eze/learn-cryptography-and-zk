import unittest

from utils.fields import Field


class TestFields(unittest.TestCase):

    def test_sub(self):

        modulus = 13

        field_1 = Field(19, modulus)
        field_2 = Field(13, modulus)

        got = field_1 - field_2

        expected = Field(6, modulus)
        
        self.assertEqual(got, expected)

        field_3 = Field(2, modulus)
        field_4 = Field(13, modulus)

        got = field_3 - field_4

        expected = Field(-11, modulus)
        
        self.assertEqual(got, expected)

    def test_add(self):

        modulus = 13

        field_1 = Field(19, modulus)
        field_2 = Field(13, modulus)

        got = field_1 + field_2

        expected = Field(32, modulus)
        
        self.assertEqual(got, expected)

    def test_mul(self):

        modulus = 13

        field_1 = Field(19, modulus)
        field_2 = Field(56, modulus)

        got = field_1 * field_2

        expected = Field(1064, modulus)
        
        self.assertEqual(got, expected)

    def test_div_inv(self):

        modulus = 13

        field_1 = Field(87, modulus)
        field_2 = Field(67, modulus)

        got = field_1 / field_2

        ## (87 * inverse_of_67) mod 13
        expected = Field(0, modulus)
        expected.inv(field_2)
        expected = expected * field_1
        
        self.assertEqual(got, expected)

    def test_inv(self):
        b = Field(3, 13)

        b_inv = Field(0, 13)
        b_inv.inv(b)

        result = b_inv * b

        expected = Field(1, 13)

        self.assertEqual(expected, result)

    def test_sqrt_sqr(self):
        b = Field(3, 13)
        self.assertTrue(b.legendre() == 1)

        b_sqrt = Field(0, 13)
        b_sqrt.sqrt(b)

        result = Field(0, 13)
        result.exp(b_sqrt, 2)

        expected = b

        self.assertEqual(expected, result)

    def test_neg(self):
        b = Field(3, 13)
        self.assertTrue(b.legendre() == 1)

        b_neg = Field(0, 13)
        b_neg.neg(b)

        expected = Field(-3, 13)

        self.assertEqual(expected, b_neg)

    def test_serialise(self):
        three = Field(3, 13)

        bytes = three.to_bytes(2)
        deserialised_three = Field.from_bytes(bytes, 13)

        self.assertEqual(three, deserialised_three)

    def test_multi_inv(self):
        values = [Field(1, 13), Field(2, 13), Field(3, 13)]

        got_inverse = Field.multi_inv(values)
        expected_inverse = _naive_multi_inv(values)

        self.assertEqual(got_inverse, expected_inverse)


def _naive_multi_inv(values: list[Field]):
    
    modulus = values[0].modulus

    inv_values = []
    for val in values:
        inverse = Field.zero(modulus)
        inverse.inv(val)
        inv_values.append(inverse)
    return inv_values