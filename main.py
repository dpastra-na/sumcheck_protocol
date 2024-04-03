import logging
import random

from sumcheck_protocol.field import FieldElement, random_field_element
from sumcheck_protocol.polynomial import MultilinearPolynomial, Term
from sumcheck_protocol.sumcheck import run_protocol

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


def log_round(
    round_index: int,
    round_poly: list[FieldElement],
    expected: FieldElement,
    passed: bool,
    challenge: FieldElement,
) -> None:
    coeffs_str = [str(c.value) for c in round_poly]
    log.info("Round %d:", round_index + 1)
    log.info("  Prover sends g_%d with coefficients %s", round_index, coeffs_str)
    if passed:
        log.info(
            "  Verifier checks: g_%d(0) + g_%d(1) == %s  OK",
            round_index,
            round_index,
            expected.value,
        )
        log.info("  Verifier sends challenge r_%d = %s", round_index, challenge.value)
    else:
        log.info(
            "  Verifier REJECTS: g_%d(0) + g_%d(1) != %s",
            round_index,
            round_index,
            expected.value,
        )
    log.info("")


if __name__ == "__main__":
    log.info("--- Thaler's example polynomial ---")
    log.info("g(x0, x1, x2) = 2*x0^3 + x0*x2 + x1*x2 over F_97")
    log.info("")

    p = thaler_example()
    log.info("Sumcheck Protocol")
    log.info("=================")
    log.info("Claimed sum H = %s", p.sum_over_boolean_hypercube().value)
    log.info("Number of variables: %d", p.num_variables)
    log.info("Field: F_%d", p.prime)
    log.info("")

    result = run_protocol(p, on_round=log_round)
    log.info("SUMCHECK PASSED" if result else "SUMCHECK FAILED")
