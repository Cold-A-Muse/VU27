'''Assignment: Palindrome2
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def palindrome(char, amount=2):
    index = ALPHABET.index(char)
    previous = ""
    for x in range(index - amount, index):
        previous += ALPHABET[x]
    return previous + ALPHABET[index] + previous[::-1]

char = str(raw_input("Please select a random character: "))
print palindrome(char)



