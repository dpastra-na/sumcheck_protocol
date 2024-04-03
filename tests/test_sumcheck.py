from field import FieldElement
from polynomial import MultilinearPolynomial, Term
from sumcheck import Prover, Verifier, run_protocol

PRIME = 97


def _fe(v: int) -> FieldElement:
    return FieldElement(v, PRIME)


def _thaler_polynomial() -> MultilinearPolynomial:
    """g(x0, x1, x2) = 2*x0^3 + x0*x2 + x1*x2 over F_97."""
    terms = [
        Term(_fe(2), {0: 3}),
        Term(_fe(1), {0: 1, 2: 1}),
        Term(_fe(1), {1: 1, 2: 1}),
    ]
    return MultilinearPolynomial(terms, num_variables=3, prime=PRIME)


def test_prover_first_round_polynomial():
    p = _thaler_polynomial()
    prover = Prover(p)
    # Round 0, no challenges yet
    # g_0(t) = 8t^3 + 2t + 1, coefficients [1, 2, 0, 8]
    coeffs = prover.compute_round_polynomial(round_index=0, challenges=[])
    assert coeffs == [_fe(1), _fe(2), _fe(0), _fe(8)]


def test_verifier_accepts_honest_round():
    # H = 12, g_0 = [1, 2, 0, 8] -> g_0(0)=1, g_0(1)=11, 1+11=12
    verifier = Verifier(num_variables=3, prime=PRIME, claimed_sum=_fe(12))
    coeffs = [_fe(1), _fe(2), _fe(0), _fe(8)]
    assert verifier.verify_round(coeffs, expected=_fe(12)) is True


def test_verifier_rejects_dishonest_round():
    verifier = Verifier(num_variables=3, prime=PRIME, claimed_sum=_fe(12))
    # Tampered coefficients: g(0)+g(1) != 12
    coeffs = [_fe(5), _fe(2), _fe(0), _fe(8)]
    assert verifier.verify_round(coeffs, expected=_fe(12)) is False


def test_protocol_passes_with_honest_prover():
    p = _thaler_polynomial()
    assert run_protocol(p) is True


def test_protocol_fails_with_wrong_claimed_sum():
    p = _thaler_polynomial()
    # Honest sum is 12, claim 99 instead
    wrong_sum = _fe(99)
    prover = Prover(p)
    verifier = Verifier(num_variables=3, prime=PRIME, claimed_sum=wrong_sum)

    round_poly = prover.compute_round_polynomial(round_index=0, challenges=[])
    # g_0(0) + g_0(1) = 12, but verifier expects 99
    assert verifier.verify_round(round_poly, expected=wrong_sum) is False
