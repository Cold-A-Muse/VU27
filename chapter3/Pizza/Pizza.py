'''
Assignment: Pizza
Created: 14-11-2013
@author: Daan Helsloot (dht340)
'''
N_MARIO = 10
K_MARIO = 3
N_LUIGI = 9
K_LUIGI = 4


def factorial(number):
    product = 1
    for i in range(number):
        product = (product * (i + 1))
    return product


def combinations(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

mario = combinations(N_MARIO, K_MARIO)
luigi = combinations(N_LUIGI, K_LUIGI)

print("Mario can make %d pizzas." % mario)
print("Luigi is able to make %d pizzas." % luigi)

if luigi > mario:
    print("Luigi has won the bet!")
else:
    print("Mario has won the bet!")