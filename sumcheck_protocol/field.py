import random
from dataclasses import dataclass
from math import isqrt


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    return all(not (n % i == 0 or n % (i + 2) == 0) for i in range(5, isqrt(n) + 1, 6))


@dataclass
class FieldElement:
    value: int
    prime: int

    def __post_init__(self) -> None:
        if not _is_prime(self.prime):
            raise ValueError(f"{self.prime} is not a prime number")
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
