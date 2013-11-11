'''Assignment: Pyramid
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def palindrome(char, amount):
    index = ALPHABET.index(char)
    previous = ""
    for x in range(index - amount, index):
        previous += ALPHABET[x]
    return previous + ALPHABET[index] + previous[::-1]


def pyramid(rows):
    output = ""
    for x in range(rows):
        output += ' '*(rows - 1 * x) + palindrome(chr(ord('a') + x), x) + "\n"
    return output

print pyramid(25)