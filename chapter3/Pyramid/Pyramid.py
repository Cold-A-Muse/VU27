'''Assignment: Pyramid
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''
ROWS = 15

def palindroom(char):
    output = ""
    for i in range (ord("a"), ord(char) + 1):
        output += chr(i)
    for k in range (ord(char) - 1, ord("a") -1, -1):
        output += chr(k)
    return output

for x in range(ROWS):
    print palindroom(chr(ord('a') + x)).center(80)

