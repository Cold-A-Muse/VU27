__author__ = 'Helsloot'


def printCollatzSequencey(n):
    if n < 0:
        print("Number has to be positive, Terminating program!")
        return
    elif n == 1:
        print("Collatz sequence has reached 1 and is finished, Terminating program!")
        return
    elif n % 2 == 0:
        print n
        return printCollatzSequencey(n/2)
    else:
        print n
        return printCollatzSequencey(3 * n + 1)

n = int(raw_input("Select a random number: "))
printCollatzSequencey(n)