import sympy as sp
import numpy as np


def get_sum(p: sp.Poly, n_var: int, variables: list[str], r: dict = {}) -> sp.Poly:
    sub_p = 0
    for point in range(2**n_var):
        point = format(point, "b").zfill(n_var)
        assignments = {}
        for bit, var in zip(point, variables):
            assignments[var] = bit
        # print(assignments)

        sub_p += p.subs(assignments)
    if r:
        sub_p = sub_p.subs(r)
    return sub_p


def get_random(r: dict, variable: str, N: int) -> None:
    # v = [2, 3, 6]
    # r[variable] = v[i]
    r[variable] = np.random.randint(N)


def check(s_n1: sp.Poly, s_n: sp.Poly, n_var: int, variables: list[str], r: dict = {}):
    return get_sum(s_n1, n_var, variables) == s_n.subs(r)


def sumcheck(p: sp.Poly, N: int = 10) -> None:
    r = {}
    s_n = get_sum(p, len(variables), variables)
    for iterration in range(len(variables) + 1):

        try:
            var = variables.pop(0)
            s_n1 = get_sum(p, len(variables), variables, r)
            print('iteration:', iterration, s_n, s_n1, r)
            assert check(s_n1, s_n, 1, [var], r), 'SUMCHECK FAILED!'
            get_random(r, var, N)
            s_n = s_n1
        except IndexError:
            s_n = s_n1
            s_n1 = p.subs(r)
            print('iteration:', iterration, s_n, s_n1)
            assert check(s_n1, s_n, 0, [], r), 'SUMCHECK FAILED!'
    print('SUMCHECK PASSED!')


def get_radom_poly(max_degree: int, max_coefficient: int):
    variables = [sp.Symbol(f'x{i}') for i in range(1, 11)]

    random_poly = 0
    for var in variables:
        for degree in range(max_degree + 1):
            random_coefficient = np.random.randint(
                -max_coefficient, max_coefficient)
            random_poly += random_coefficient * (var ** degree)
    print(random_poly)
    return sp.Poly(random_poly, variables), variables


if __name__ == '__main__':

    """
    This is the polynomial use as example in the book 'J., Thaler, Proofs, Arguments, and Zero-Knowledge., 2023 page 36'. Note that to get the same results you need to modify the get_random function to return the same values as the book.
    """
    # variables = ['x1', 'x2', 'x3']
    # poly_expresion = '2*x1**3 + x1*x3 + x2*x3'
    # x1, x2, x3, = sp.symbols(' '.join(variables))
    # p = sp.Poly(eval(poly_expresion), x1, x2, x3)

    p, variables = get_radom_poly(max_degree=7, max_coefficient=10)
    sumcheck(p, N=10)
