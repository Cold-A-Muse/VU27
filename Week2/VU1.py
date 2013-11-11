__author__ = 'Daan Helsloot'


priceArticle = input("Please tell the price of your item including VAT: ")
percentage = priceArticle/100*21
print("The price of your item without VAT: %s " % str(priceArticle - percentage))