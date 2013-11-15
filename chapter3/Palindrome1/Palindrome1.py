'''Assignment: Palindrome1
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''

def palindroom():
    output = ""
    for i in range(ord('a'),ord('z')):
        output += chr(i)
    for s in range(ord('z'), ord('a') -1, -1):
        output += chr(s)
    return output        

print palindroom()
