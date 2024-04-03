from sumcheck_protocol.sumcheck import Prover, Verifier, run_protocol
from tests.conftest import PRIME, fe, thaler_polynomial


def test_prover_first_round_polynomial():
    p = thaler_polynomial()
    prover = Prover(p)
    coeffs = prover.compute_round_polynomial(challenges=[])
    assert coeffs == [fe(1), fe(2), fe(0), fe(8)]


def test_verifier_accepts_honest_round():
    verifier = Verifier(num_variables=3, prime=PRIME, claimed_sum=fe(12))
    coeffs = [fe(1), fe(2), fe(0), fe(8)]
    assert verifier.verify_round(coeffs, expected=fe(12)) is True


def test_verifier_rejects_dishonest_round():
    verifier = Verifier(num_variables=3, prime=PRIME, claimed_sum=fe(12))
    coeffs = [fe(5), fe(2), fe(0), fe(8)]
    assert verifier.verify_round(coeffs, expected=fe(12)) is False


def test_protocol_passes_with_honest_prover():
    p = thaler_polynomial()
    assert run_protocol(p) is True


def test_protocol_fails_with_wrong_claimed_sum():
    p = thaler_polynomial()
    prover = Prover(p)
    verifier = Verifier(num_variables=3, prime=PRIME, claimed_sum=fe(99))
    round_poly = prover.compute_round_polynomial(challenges=[])
    assert verifier.verify_round(round_poly, expected=fe(99)) is False
