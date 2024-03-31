from field import FieldElement
from polynomial import MultilinearPolynomial, Term


PRIME = 97


def _fe(v: int) -> FieldElement:
    return FieldElement(v, PRIME)


def _thaler_polynomial() -> MultilinearPolynomial:
    """g(x0, x1, x2) = 2*x0^3 + x0*x2 + x1*x2 over F_97."""
    terms = [
        Term(_fe(2), {0: 3}),       # 2*x0^3
        Term(_fe(1), {0: 1, 2: 1}), # x0*x2
        Term(_fe(1), {1: 1, 2: 1}), # x1*x2
    ]
    return MultilinearPolynomial(terms, num_variables=3, prime=PRIME)


def test_evaluate_at_point():
    p = _thaler_polynomial()
    # g(0, 0, 0) = 0
    assert p.evaluate([_fe(0), _fe(0), _fe(0)]) == _fe(0)


def test_evaluate_at_nonzero_point():
    p = _thaler_polynomial()
    # g(1, 1, 1) = 2*1 + 1*1 + 1*1 = 4
    assert p.evaluate([_fe(1), _fe(1), _fe(1)]) == _fe(4)


def test_evaluate_at_another_point():
    p = _thaler_polynomial()
    # g(2, 3, 1) = 2*8 + 2*1 + 3*1 = 16 + 2 + 3 = 21
    assert p.evaluate([_fe(2), _fe(3), _fe(1)]) == _fe(21)


def test_partial_evaluate_fixes_variable():
    p = _thaler_polynomial()
    # Fix x0=2: g(2, x1, x2) = 2*8 + 2*x2 + x1*x2 = 16 + 2*x2 + x1*x2
    reduced = p.partial_evaluate(0, _fe(2))
    # Evaluate reduced at x1=3, x2=1: 16 + 2 + 3 = 21
    assert reduced.evaluate([_fe(3), _fe(1)]) == _fe(21)


def test_partial_evaluate_consistency():
    p = _thaler_polynomial()
    # p(2, 3, 1) should equal partial_evaluate(x0=2) then evaluate(x1=3, x2=1)
    full = p.evaluate([_fe(2), _fe(3), _fe(1)])
    reduced = p.partial_evaluate(0, _fe(2))
    partial = reduced.evaluate([_fe(3), _fe(1)])
    assert full == partial


def test_sum_over_boolean_hypercube():
    p = _thaler_polynomial()
    # Sum g over all (x0,x1,x2) in {0,1}^3:
    # g(0,0,0)=0, g(0,0,1)=0, g(0,1,0)=0, g(0,1,1)=1,
    # g(1,0,0)=2, g(1,0,1)=3, g(1,1,0)=2, g(1,1,1)=4
    # Total = 0+0+0+1+2+3+2+4 = 12
    assert p.sum_over_boolean_hypercube() == _fe(12)


def test_to_univariate_first_round():
    p = _thaler_polynomial()
    # Round 0: no fixed variables, free var is x0, sum over x1,x2 in {0,1}^2
    # g_0(t) = sum_{x1,x2} g(t, x1, x2)
    # g_0(t) = g(t,0,0) + g(t,0,1) + g(t,1,0) + g(t,1,1)
    #        = 2t^3 + (2t^3 + t) + (2t^3) + (2t^3 + t + 1)
    #        = 8t^3 + 2t + 1
    # Coefficients: [1, 2, 0, 8] (index = degree)
    coeffs = p.to_univariate(round_index=0, challenges=[])
    assert coeffs == [_fe(1), _fe(2), _fe(0), _fe(8)]


def test_to_univariate_sums_correctly():
    p = _thaler_polynomial()
    # The univariate g_0(t) must satisfy: g_0(0) + g_0(1) = H
    # H = 12, g_0(0) = 1, g_0(1) = 8+2+1 = 11, 1+11 = 12
    coeffs = p.to_univariate(round_index=0, challenges=[])
    g_at_0 = coeffs[0]  # only constant term survives
    g_at_1 = _fe(sum(c.value for c in coeffs) % PRIME)
    assert g_at_0 + g_at_1 == _fe(12)


def test_to_univariate_second_round():
    p = _thaler_polynomial()
    # Round 1 with challenge r0=2:
    # g(2, x1, x2) = 16 + 2*x2 + x1*x2
    # g_1(t) = sum_{x2 in {0,1}} g(2, t, x2) = (16) + (16 + 2 + t) = 34 + t
    # Coefficients: [34, 1]
    coeffs = p.to_univariate(round_index=1, challenges=[_fe(2)])
    assert coeffs == [_fe(34), _fe(1)]
