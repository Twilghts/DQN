from sympy import *

x = var('x')

init_printing()

print(integrate(atan(x ** 2)))
print(diff(atan(x)))
# plot_implicit(atan(x**2))
print(integrate(1 / (x ** 3 + x ** 2 + x)))
print('1*' * 20)
print(integrate(1 / (x ** 4 + x ** 3 + x ** 2 + x)))
print('2*' * 20)
print(integrate(1 / (x ** 5 + x ** 4 + x ** 3 + x ** 2 + x)))
print('3*' * 20)
print(integrate(1 / (x ** 3 + x ** 2 + x + x ** 4 + x ** 5 + x ** 6)))
print('4*' * 20)
print(integrate(1 / (
            x ** 3 + x ** 2 + x + x ** 4 + x ** 5 +
            x ** 6 + x ** 7 + x ** 8 + x ** 9 + x ** 10
            + x ** 11 + x ** 12 + x ** 13 + x ** 14 + x ** 15 + x ** 16)))
