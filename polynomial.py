from dataclasses import dataclass

from field import FieldElement


@dataclass
class Term:
    coefficient: FieldElement
    variables: dict[int, int]  # {variable_index: exponent}


class MultilinearPolynomial:
    def __init__(self, terms: list[Term], num_variables: int, prime: int) -> None:
        self.terms = terms
        self.num_variables = num_variables
        self.prime = prime

    def evaluate(self, assignment: list[FieldElement]) -> FieldElement:
        result = FieldElement(0, self.prime)
        for term in self.terms:
            term_value = term.coefficient
            for var_index, exponent in term.variables.items():
                term_value = term_value * (assignment[var_index] ** exponent)
            result = result + term_value
        return result

    def partial_evaluate(
        self, variable_index: int, value: FieldElement
    ) -> "MultilinearPolynomial":
        new_terms: list[Term] = []
        for term in self.terms:
            new_coeff = term.coefficient
            new_vars: dict[int, int] = {}
            for var_idx, exp in term.variables.items():
                if var_idx == variable_index:
                    new_coeff = new_coeff * (value**exp)
                elif var_idx > variable_index:
                    new_vars[var_idx - 1] = exp
                else:
                    new_vars[var_idx] = exp
            new_terms.append(Term(new_coeff, new_vars))
        return MultilinearPolynomial(new_terms, self.num_variables - 1, self.prime)

    def sum_over_boolean_hypercube(self) -> FieldElement:
        result = FieldElement(0, self.prime)
        for point in range(2**self.num_variables):
            bits = format(point, "b").zfill(self.num_variables)
            assignment = [FieldElement(int(b), self.prime) for b in bits]
            result = result + self.evaluate(assignment)
        return result

    def max_degree(self) -> int:
        deg = 0
        for term in self.terms:
            for exp in term.variables.values():
                if exp > deg:
                    deg = exp
        return deg

    def to_univariate(
        self, round_index: int, challenges: list[FieldElement]
    ) -> list[FieldElement]:
        reduced = self
        for challenge in challenges:
            reduced = reduced.partial_evaluate(0, challenge)

        num_free = reduced.num_variables - 1
        degree = reduced.max_degree()
        eval_points = degree + 1

        values = [FieldElement(0, self.prime) for _ in range(eval_points)]
        for t in range(eval_points):
            t_val = FieldElement(t, self.prime)
            fixed_t = reduced.partial_evaluate(0, t_val)
            if num_free > 0:
                values[t] = fixed_t.sum_over_boolean_hypercube()
            else:
                values[t] = fixed_t.evaluate([])
        return _interpolate(values, self.prime)


def _interpolate(values: list[FieldElement], prime: int) -> list[FieldElement]:
    n = len(values)
    coeffs = [FieldElement(0, prime)] * n

    for i in range(n):
        basis_coeffs = [FieldElement(0, prime)] * n
        basis_coeffs[0] = values[i]
        for j in range(n):
            if j == i:
                continue
            xi = FieldElement(i, prime)
            xj = FieldElement(j, prime)
            denom = xi - xj
            inv_denom = FieldElement(1, prime) / denom
            new_basis = [FieldElement(0, prime)] * n
            for k in range(n - 1, -1, -1):
                neg_xj = FieldElement(0, prime) - xj
                new_basis[k] = new_basis[k] + basis_coeffs[k] * neg_xj * inv_denom
                if k + 1 < n:
                    new_basis[k + 1] = new_basis[k + 1] + basis_coeffs[k] * inv_denom
            basis_coeffs = new_basis
        for k in range(n):
            coeffs[k] = coeffs[k] + basis_coeffs[k]
    return coeffs
