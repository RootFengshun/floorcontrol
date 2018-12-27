from sympy import *

x, y = symbols('x y')
x = symbols('x')
y = symbols('y')
w, n = symbols('w n')
f = (((w + 3) ** 2 - 2 * n * (w + 3) + 2 * n * (n - 1)) * (w + 2 * n + 1)) / ((w + 1) * (w + 3) ** 2)
solve([], x)
n = Symbol('n')
w = Symbol('w')
f = (((w + 3) ** 2 - 2 * n * (w + 3) + 2 * n * (n - 1)) * (w + 2 * n + 1)) / ((w + 1) * (w + 3) ** 2)
print diff(f, w)
print solve([(-2 * n + 2 * w + 6) * (2 * n + w + 1) / ((w + 1) * (w + 3) ** 2) + (
            2 * n * (n - 1) - 2 * n * (w + 3) + (w + 3) ** 2) / ((w + 1) * (w + 3) ** 2)
             - 2 * (2 * n + w + 1) * (2 * n * (n - 1) - 2 * n * (w + 3) + (w + 3) ** 2) / ((w + 1) * (w + 3) ** 3)
             - (2 * n + w + 1) * (2 * n * (n - 1) - 2 * n * (w + 3) + (w + 3) ** 2) / ((w + 1) ** 2 * (w + 3) ** 2)], w)
