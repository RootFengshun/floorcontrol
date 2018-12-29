from sympy import *

# x, y = symbols('x y')
# x = symbols('x')
# y = symbols('y')
# w, n = symbols('w n')
# f = (((w + 3) ** 2 - 2 * n * (w + 3) + 2 * n * (n - 1)) * (w + 2 * n + 1)) / ((w + 1) * (w + 3) ** 2)
# solve([], x)
# n = Symbol('n')
# w = Symbol('w')
# f = (((w + 3) ** 2 - 2 * n * (w + 3) + 2 * n * (n - 1)) * (w + 2 * n + 1)) / ((w + 1) * (w + 3) ** 2)
# print diff(f, w)
# print solve([(-2 * n + 2 * w + 6) * (2 * n + w + 1) / ((w + 1) * (w + 3) ** 2) + (
#             2 * n * (n - 1) - 2 * n * (w + 3) + (w + 3) ** 2) / ((w + 1) * (w + 3) ** 2)
#              - 2 * (2 * n + w + 1) * (2 * n * (n - 1) - 2 * n * (w + 3) + (w + 3) ** 2) / ((w + 1) * (w + 3) ** 3)
#              - (2 * n + w + 1) * (2 * n * (n - 1) - 2 * n * (w + 3) + (w + 3) ** 2) / ((w + 1) ** 2 * (w + 3) ** 2)], w)

lmd = Symbol('lmd')
cw = Symbol('cw')
n = Symbol('n')
f = 1-((2*n*exp(-lmd)/((cw-1)*(-exp(-lmd))+2))+n*(n-1)*4*exp(-2*lmd)/(2*(((cw-1)*exp(-lmd)+2)**2))*(cw*exp(-lmd)+2*n-1+(3-2*n)*(1-exp(-lmd)))/(cw*exp(-lmd)+2-3*exp(-lmd)))
#print diff(f,cw)
# -2*n*(n - 1)*exp(-3*lmd)/(((cw - 1)*exp(-lmd) + 2)**2*(cw*exp(-lmd) + 2 - 3*exp(-lmd))) + 2*n*(n - 1)*(cw*exp(-lmd) + 2*n + (1 - exp(-lmd))*(-2*n + 3) - 1)*exp(-3*lmd)/(((cw - 1)*exp(-lmd) + 2)**2*(cw*exp(-lmd) + 2 - 3*exp(-lmd))**2) + 4*n*(n - 1)*(cw*exp(-lmd) + 2*n + (1 - exp(-lmd))*(-2*n + 3) - 1)*exp(-3*lmd)/(((cw - 1)*exp(-lmd) + 2)**3*(cw*exp(-lmd) + 2 - 3*exp(-lmd))) - 2*n*exp(-2*lmd)/(-(cw - 1)*exp(-lmd) + 2)**2
print solve([-2*n*(n - 1)*exp(-3*lmd)/(((cw - 1)*exp(-lmd) + 2)**2*(cw*exp(-lmd) + 2 - 3*exp(-lmd))) + 2*n*(n - 1)*(cw*exp(-lmd) + 2*n + (1 - exp(-lmd))*(-2*n + 3) - 1)*exp(-3*lmd)/(((cw - 1)*exp(-lmd) + 2)**2*(cw*exp(-lmd) + 2 - 3*exp(-lmd))**2) + 4*n*(n - 1)*(cw*exp(-lmd) + 2*n + (1 - exp(-lmd))*(-2*n + 3) - 1)*exp(-3*lmd)/(((cw - 1)*exp(-lmd) + 2)**3*(cw*exp(-lmd) + 2 - 3*exp(-lmd))) - 2*n*exp(-2*lmd)/(-(cw - 1)*exp(-lmd) + 2)**2],lmd)