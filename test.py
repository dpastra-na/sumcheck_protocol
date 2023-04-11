import unittest
import sympy as sp
from main import get_sum, check


class TestSumCheckFunctions(unittest.TestCase):
    variables = ['x1', 'x2', 'x3']
    x1, x2, x3, = sp.symbols(' '.join(variables))
    p = sp.Poly(2*x1**3 + x1*x3 + x2*x3, x1, x2, x3)

    def test_get_sum(self):
        r = {self.x1: 2}
        expected_sum = sp.Poly(34+self.x2, self.x2)
        result = get_sum(self.p, 1, [self.x3], r)
        self.assertEqual(result, expected_sum)

    def test_check(self):
        r = {self.x1: 2, self.x2: 3}
        s_n1 = get_sum(self.p, 0, [], r)
        s_n = sp.Poly(34+self.x2, self.x2)
        result = check(s_n1, s_n, 1, [self.x3], r)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
