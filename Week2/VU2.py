__author__ = 'Helsloot'


wage = input("Enter the hourly wages: ")
hours = input("How many hours of work: ")
totalCost = int(wage * hours + 16)
print("Plumber has worked for " + str(hours) + " hours with hourly wage of " + str(wage))
print("Total cost is: %d" % totalCost)