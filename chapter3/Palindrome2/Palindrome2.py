'''Assignment: Palindrome2
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''

   
def palindroom(char):
    output = ""
    for i in range (ord("a"), ord(char) + 1):
        output += chr(i)
    for k in range (ord(char) - 1, ord("a") -1, -1):
        output += chr(k)
    return output

char = raw_input("Please select a random character: ")
print palindroom(char)



