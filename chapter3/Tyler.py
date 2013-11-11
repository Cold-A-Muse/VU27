# coding=utf-8
__author__ = 'Tyler Sedlar'
__copyright__ = "Copyright © 2013, Sedlar. All rights reserved."
__date__ = 11 / 9 / 13
 
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "t@sedlar.me"
 


 
def palindrome(char, amount):
    letters = "abcdefghijklmnopqrstuvwxyz"
    idx = letters.index(char)
    previous = ""
    for x in range(idx - amount, idx):
        previous += letters[x]
    return previous + letters[idx] + previous[::-1]
 
def pyramid(rows):
    output = ""
    for x in range(rows):
        output += ' '*int(rows - 1 * x) + palindrome(chr(ord('a') + x), x) + "\n"
    return output

print pyramid(15)