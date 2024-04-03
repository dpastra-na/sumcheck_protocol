from tests.conftest import PRIME, fe, thaler_polynomial


def test_evaluate_at_point():
    p = thaler_polynomial()
    assert p.evaluate([fe(0), fe(0), fe(0)]) == fe(0)


def test_evaluate_at_nonzero_point():
    p = thaler_polynomial()
    # g(1, 1, 1) = 2*1 + 1*1 + 1*1 = 4
    assert p.evaluate([fe(1), fe(1), fe(1)]) == fe(4)


def test_evaluate_at_another_point():
    p = thaler_polynomial()
    # g(2, 3, 1) = 2*8 + 2*1 + 3*1 = 16 + 2 + 3 = 21
    assert p.evaluate([fe(2), fe(3), fe(1)]) == fe(21)


def test_partial_evaluate_fixes_variable():
    p = thaler_polynomial()
    reduced = p.partial_evaluate(0, fe(2))
    assert reduced.evaluate([fe(3), fe(1)]) == fe(21)


def test_partial_evaluate_consistency():
    p = thaler_polynomial()
    full = p.evaluate([fe(2), fe(3), fe(1)])
    reduced = p.partial_evaluate(0, fe(2))
    partial = reduced.evaluate([fe(3), fe(1)])
    assert full == partial


def test_sum_over_boolean_hypercube():
    p = thaler_polynomial()
    # Sum over {0,1}^3 = 12
    assert p.sum_over_boolean_hypercube() == fe(12)


def test_to_univariate_first_round():
    p = thaler_polynomial()
    # g_0(t) = 8t^3 + 2t + 1, coefficients [1, 2, 0, 8]
    coeffs = p.to_univariate(challenges=[])
    assert coeffs == [fe(1), fe(2), fe(0), fe(8)]


def test_to_univariate_sums_correctly():
    p = thaler_polynomial()
    # g_0(0) + g_0(1) = H = 12
    coeffs = p.to_univariate(challenges=[])
    g_at_0 = coeffs[0]
    g_at_1 = fe(sum(c.value for c in coeffs) % PRIME)
    assert g_at_0 + g_at_1 == fe(12)


def test_to_univariate_second_round():
    p = thaler_polynomial()
    # With challenge r0=2: g_1(t) = 34 + t
    coeffs = p.to_univariate(challenges=[fe(2)])
    assert coeffs == [fe(34), fe(1)]
