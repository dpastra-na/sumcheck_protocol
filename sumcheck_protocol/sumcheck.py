from collections.abc import Callable

from .field import FieldElement, random_field_element
from .polynomial import MultilinearPolynomial


def evaluate_univariate(
    coeffs: list[FieldElement], point: FieldElement
) -> FieldElement:
    result = FieldElement(0, point.prime)
    for degree, coeff in enumerate(coeffs):
        result = result + coeff * (point**degree)
    return result


class Prover:
    def __init__(self, polynomial: MultilinearPolynomial) -> None:
        self.polynomial = polynomial

    def compute_round_polynomial(
        self, challenges: list[FieldElement]
    ) -> list[FieldElement]:
        return self.polynomial.to_univariate(challenges)


class Verifier:
    def __init__(
        self, num_variables: int, prime: int, claimed_sum: FieldElement
    ) -> None:
        self.num_variables = num_variables
        self.prime = prime
        self.claimed_sum = claimed_sum

    def verify_round(
        self, round_poly: list[FieldElement], expected: FieldElement
    ) -> bool:
        g_at_0 = evaluate_univariate(round_poly, FieldElement(0, self.prime))
        g_at_1 = evaluate_univariate(round_poly, FieldElement(1, self.prime))
        return g_at_0 + g_at_1 == expected

    def generate_challenge(self) -> FieldElement:
        return random_field_element(self.prime)

    def verify_final(self, oracle_value: FieldElement, expected: FieldElement) -> bool:
        return oracle_value == expected


RoundCallback = Callable[
    [int, list[FieldElement], FieldElement, bool, FieldElement], None
]


def run_protocol(
    polynomial: MultilinearPolynomial,
    on_round: RoundCallback | None = None,
) -> bool:
    prover = Prover(polynomial)
    claimed_sum = polynomial.sum_over_boolean_hypercube()
    verifier = Verifier(
        num_variables=polynomial.num_variables,
        prime=polynomial.prime,
        claimed_sum=claimed_sum,
    )

    challenges: list[FieldElement] = []
    expected = claimed_sum

    for round_index in range(polynomial.num_variables):
        round_poly = prover.compute_round_polynomial(challenges)
        passed = verifier.verify_round(round_poly, expected)
        challenge = verifier.generate_challenge()

        if on_round:
            on_round(round_index, round_poly, expected, passed, challenge)

        if not passed:
            return False

        challenges.append(challenge)
        expected = evaluate_univariate(round_poly, challenge)

    oracle_value = polynomial.evaluate(challenges)
    return verifier.verify_final(oracle_value, expected)
