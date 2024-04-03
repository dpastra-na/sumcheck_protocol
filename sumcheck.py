from field import FieldElement, random_field_element
from polynomial import MultilinearPolynomial


class Prover:
    def __init__(self, polynomial: MultilinearPolynomial) -> None:
        self.polynomial = polynomial

    def compute_round_polynomial(
        self, round_index: int, challenges: list[FieldElement]
    ) -> list[FieldElement]:
        return self.polynomial.to_univariate(round_index, challenges)


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
        g_at_0 = self._evaluate_univariate(round_poly, FieldElement(0, self.prime))
        g_at_1 = self._evaluate_univariate(round_poly, FieldElement(1, self.prime))
        return g_at_0 + g_at_1 == expected

    def generate_challenge(self) -> FieldElement:
        return random_field_element(self.prime)

    def verify_final(self, oracle_value: FieldElement, expected: FieldElement) -> bool:
        return oracle_value == expected

    def _evaluate_univariate(
        self, coeffs: list[FieldElement], point: FieldElement
    ) -> FieldElement:
        result = FieldElement(0, self.prime)
        for degree, coeff in enumerate(coeffs):
            result = result + coeff * (point**degree)
        return result


def run_protocol(polynomial: MultilinearPolynomial) -> bool:
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
        round_poly = prover.compute_round_polynomial(round_index, challenges)
        if not verifier.verify_round(round_poly, expected):
            return False
        challenge = verifier.generate_challenge()
        challenges.append(challenge)
        expected = verifier._evaluate_univariate(round_poly, challenge)

    oracle_value = polynomial.evaluate(challenges)
    return verifier.verify_final(oracle_value, expected)
