import logging
import random

from field import FieldElement, random_field_element
from polynomial import MultilinearPolynomial, Term
from sumcheck import Prover, Verifier

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

PRIME = 97


def _fe(v: int) -> FieldElement:
    return FieldElement(v, PRIME)


def thaler_example() -> MultilinearPolynomial:
    """g(x0, x1, x2) = 2*x0^3 + x0*x2 + x1*x2 over F_97.

    Example from Thaler, "Proofs, Arguments, and Zero-Knowledge", 2023, p.36.
    """
    terms = [
        Term(_fe(2), {0: 3}),
        Term(_fe(1), {0: 1, 2: 1}),
        Term(_fe(1), {1: 1, 2: 1}),
    ]
    return MultilinearPolynomial(terms, num_variables=3, prime=PRIME)


def random_polynomial(
    num_variables: int, max_degree: int, num_terms: int, prime: int
) -> MultilinearPolynomial:
    terms: list[Term] = []
    for _ in range(num_terms):
        coeff = random_field_element(prime)
        variables: dict[int, int] = {}
        for var_idx in range(num_variables):
            exp = random.randint(0, max_degree)
            if exp > 0:
                variables[var_idx] = exp
        terms.append(Term(coeff, variables))
    return MultilinearPolynomial(terms, num_variables=num_variables, prime=prime)


def run_verbose_protocol(polynomial: MultilinearPolynomial) -> bool:
    prover = Prover(polynomial)
    claimed_sum = polynomial.sum_over_boolean_hypercube()
    verifier = Verifier(
        num_variables=polynomial.num_variables,
        prime=polynomial.prime,
        claimed_sum=claimed_sum,
    )

    log.info("Sumcheck Protocol")
    log.info("=================")
    log.info("Claimed sum H = %s", claimed_sum.value)
    log.info("Number of variables: %d", polynomial.num_variables)
    log.info("Field: F_%d", polynomial.prime)
    log.info("")

    challenges: list[FieldElement] = []
    expected = claimed_sum

    for round_index in range(polynomial.num_variables):
        round_poly = prover.compute_round_polynomial(round_index, challenges)
        coeffs_str = [str(c.value) for c in round_poly]
        log.info("Round %d:", round_index + 1)
        log.info("  Prover sends g_%d with coefficients %s", round_index, coeffs_str)

        if not verifier.verify_round(round_poly, expected):
            log.info(
                "  Verifier REJECTS: g_%d(0) + g_%d(1) != %s",
                round_index,
                round_index,
                expected.value,
            )
            return False

        log.info(
            "  Verifier checks: g_%d(0) + g_%d(1) == %s  OK",
            round_index,
            round_index,
            expected.value,
        )

        challenge = verifier.generate_challenge()
        challenges.append(challenge)
        log.info("  Verifier sends challenge r_%d = %s", round_index, challenge.value)

        expected = FieldElement(0, polynomial.prime)
        for degree, coeff in enumerate(round_poly):
            expected = expected + coeff * (challenge**degree)
        log.info("")

    oracle_value = polynomial.evaluate(challenges)
    final_ok = verifier.verify_final(oracle_value, expected)
    log.info(
        "Final check: p(%s) = %s, expected %s  %s",
        [c.value for c in challenges],
        oracle_value.value,
        expected.value,
        "OK" if final_ok else "FAIL",
    )
    log.info("")

    if final_ok:
        log.info("SUMCHECK PASSED")
    else:
        log.info("SUMCHECK FAILED")

    return final_ok


if __name__ == "__main__":
    log.info("--- Thaler's example polynomial ---")
    log.info("g(x0, x1, x2) = 2*x0^3 + x0*x2 + x1*x2 over F_97")
    log.info("")
    p = thaler_example()
    run_verbose_protocol(p)
