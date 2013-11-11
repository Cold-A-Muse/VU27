__author__ = 'Helsloot'

donatedAmount = input("Enter the amount you want to donate: ")
while donatedAmount < 50.00:
    donatedAmount = input("Enter the amount you want to donate: ")
print("Thank you for your contribution of %0.2f euro" % donatedAmount)