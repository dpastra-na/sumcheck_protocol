import random
from dataclasses import dataclass


@dataclass
class FieldElement:
    value: int
    prime: int

    def __post_init__(self) -> None:
        self.value = self.value % self.prime

    def _check_same_field(self, other: "FieldElement") -> None:
        if self.prime != other.prime:
            raise ValueError("Cannot operate on elements from different primes")

    def __add__(self, other: "FieldElement") -> "FieldElement":
        self._check_same_field(other)
        return FieldElement((self.value + other.value) % self.prime, self.prime)

    def __sub__(self, other: "FieldElement") -> "FieldElement":
        self._check_same_field(other)
        return FieldElement((self.value - other.value) % self.prime, self.prime)

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        self._check_same_field(other)
        return FieldElement((self.value * other.value) % self.prime, self.prime)

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        self._check_same_field(other)
        if other.value == 0:
            raise ValueError("division by zero")
        inverse = pow(other.value, self.prime - 2, self.prime)
        return FieldElement((self.value * inverse) % self.prime, self.prime)

    def __pow__(self, exponent: int) -> "FieldElement":
        return FieldElement(pow(self.value, exponent, self.prime), self.prime)

    def __neg__(self) -> "FieldElement":
        return FieldElement((-self.value) % self.prime, self.prime)


def random_field_element(prime: int) -> FieldElement:
    return FieldElement(random.randint(0, prime - 1), prime)
