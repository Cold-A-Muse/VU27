__author__ = 'Helsloot'

#Option 1:
print("Integers of characters:")
for s in "abcdefghijklmnopqrstuvwxyz":
    print(ord(s)),
print("\n")

print("Characters of integers:")
for i in range(97, 123):
    print(chr(i)),
#Option 2:
for i in range(ord('a'), ord('z')+1):
    print chr(i),