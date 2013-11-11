__author__ = 'Helsloot'

import math


def combinaties(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

mario = combinaties(10, 3)
luigi = combinaties(9, 4)

print("Mario can make %d pizzas." % mario)
print("Luigi is able to make %d pizzas." % luigi)

if luigi > mario:
    print("Luigi has won the bet!")
else:
    print("Mario has won the bet!")