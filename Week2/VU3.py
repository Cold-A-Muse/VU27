__author__ = 'Helsloot'

whitePieces = float(raw_input("Enter the amount of white pieces: "))
blackPieces = float(raw_input("Enter the amount of black pieces: "))
percentageWhite = float(whitePieces/(blackPieces + whitePieces)*100)
percentageBlack = float(blackPieces/(blackPieces + whitePieces)*100)

print("Amount of white pieces is %d and the amount of black pieces is %d" % (whitePieces, blackPieces))
print("Percentage white pieces: %0.2f" % percentageWhite)
print("Percentage black pieces: %0.2f" % percentageBlack)