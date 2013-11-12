__author__ = 'Helsloot'


def factorial(number):
    product = 1
    for i in range(number):
        product = (product * (i + 1))
    return product


def combinations(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

mario = combinations(10, 3)
luigi = combinations(9, 4)

print("Mario can make %d pizzas." % mario)
print("Luigi is able to make %d pizzas." % luigi)

if luigi > mario:
    print("Luigi has won the bet!")
else:
    print("Mario has won the bet!")