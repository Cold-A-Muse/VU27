__author__ = 'Helsloot'

itemOne = input("Enter price of first item: ")
itemTwo = input("Enter price of second item: ")
itemThree = input("Enter price of third item: ")
totalOldPrice = itemOne + itemTwo + itemThree
items = (itemOne, itemTwo, itemThree)

if itemOne > itemTwo and itemThree:
    maxValue = itemOne
elif itemTwo > itemOne and itemThree:
    maxValue = itemTwo
else:
    maxValue = itemThree
discount = 0.15 * maxValue
print("Total old price: %0.2f" % totalOldPrice)
print("Discount: %0.2f" % discount)
print("Total new price: %0.2f" % (totalOldPrice - discount))