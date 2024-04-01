import pytest

from field import FieldElement, random_field_element

PRIME = 17


def test_value_is_stored_mod_prime():
    e = FieldElement(20, PRIME)
    assert e.value == 3


def test_negative_value_wraps():
    e = FieldElement(-1, PRIME)
    assert e.value == 16


def test_zero():
    e = FieldElement(0, PRIME)
    assert e.value == 0


def test_addition():
    a = FieldElement(7, PRIME)
    b = FieldElement(8, PRIME)
    assert a + b == FieldElement(15, PRIME)


def test_addition_wraps():
    a = FieldElement(10, PRIME)
    b = FieldElement(10, PRIME)
    assert a + b == FieldElement(3, PRIME)


def test_subtraction():
    a = FieldElement(10, PRIME)
    b = FieldElement(3, PRIME)
    assert a - b == FieldElement(7, PRIME)


def test_subtraction_wraps():
    a = FieldElement(3, PRIME)
    b = FieldElement(10, PRIME)
    assert a - b == FieldElement(10, PRIME)


def test_multiplication():
    a = FieldElement(3, PRIME)
    b = FieldElement(4, PRIME)
    assert a * b == FieldElement(12, PRIME)


def test_multiplication_wraps():
    a = FieldElement(10, PRIME)
    b = FieldElement(10, PRIME)
    assert a * b == FieldElement(100 % PRIME, PRIME)


def test_division():
    a = FieldElement(6, PRIME)
    b = FieldElement(3, PRIME)
    result = a / b
    assert result * b == a


def test_division_by_zero_raises():
    a = FieldElement(5, PRIME)
    zero = FieldElement(0, PRIME)
    with pytest.raises(ValueError, match="division by zero"):
        a / zero


def test_power():
    a = FieldElement(3, PRIME)
    assert a**3 == FieldElement(27 % PRIME, PRIME)


def test_power_zero():
    a = FieldElement(5, PRIME)
    assert a**0 == FieldElement(1, PRIME)


def test_negation():
    a = FieldElement(5, PRIME)
    assert -a == FieldElement(12, PRIME)


def test_additive_inverse():
    a = FieldElement(5, PRIME)
    assert a + (-a) == FieldElement(0, PRIME)


def test_different_primes_raises():
    a = FieldElement(3, 17)
    b = FieldElement(3, 19)
    with pytest.raises(ValueError, match="different primes"):
        a + b
    with pytest.raises(ValueError, match="different primes"):
        a - b
    with pytest.raises(ValueError, match="different primes"):
        a * b
    with pytest.raises(ValueError, match="different primes"):
        a / b


@pytest.mark.parametrize("a_val,b_val,c_val", [(3, 7, 11), (1, 0, 16), (5, 5, 5)])
def test_associativity_addition(a_val, b_val, c_val):
    a = FieldElement(a_val, PRIME)
    b = FieldElement(b_val, PRIME)
    c = FieldElement(c_val, PRIME)
    assert (a + b) + c == a + (b + c)


@pytest.mark.parametrize("a_val,b_val", [(3, 7), (0, 5), (16, 1)])
def test_commutativity(a_val, b_val):
    a = FieldElement(a_val, PRIME)
    b = FieldElement(b_val, PRIME)
    assert a + b == b + a
    assert a * b == b * a


@pytest.mark.parametrize("a_val,b_val,c_val", [(3, 7, 11), (2, 5, 9)])
def test_distributivity(a_val, b_val, c_val):
    a = FieldElement(a_val, PRIME)
    b = FieldElement(b_val, PRIME)
    c = FieldElement(c_val, PRIME)
    assert a * (b + c) == (a * b) + (a * c)


@pytest.mark.parametrize("a_val", [1, 3, 7, 16])
def test_multiplicative_inverse(a_val):
    a = FieldElement(a_val, PRIME)
    one = FieldElement(1, PRIME)
    assert a * (one / a) == one


def test_random_field_element():
    for _ in range(50):
        e = random_field_element(PRIME)
        assert isinstance(e, FieldElement)
        assert e.prime == PRIME
        assert 0 <= e.value < PRIME
