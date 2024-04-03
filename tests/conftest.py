from sumcheck_protocol.field import FieldElement
from sumcheck_protocol.polynomial import MultilinearPolynomial, Term

PRIME = 97


def fe(v: int) -> FieldElement:
    return FieldElement(v, PRIME)


def thaler_polynomial() -> MultilinearPolynomial:
    """g(x0, x1, x2) = 2*x0^3 + x0*x2 + x1*x2 over F_97."""
    terms = [
        Term(fe(2), {0: 3}),
        Term(fe(1), {0: 1, 2: 1}),
        Term(fe(1), {1: 1, 2: 1}),
    ]
    return MultilinearPolynomial(terms, num_variables=3, prime=PRIME)
