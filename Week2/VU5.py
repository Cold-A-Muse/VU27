__author__ = 'Helsloot'


def formatMilliseconds(timeMilliseconds):
    seconds = (int(((timeMilliseconds / 1000) % 60)))
    minutes = (int((((timeMilliseconds / 1000) / 60) % 60)))
    hours = (int(((((timeMilliseconds / 1000) / 60) / 60) % 60)))
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


blackPlayer = input("Enter the time the black player thought: ")
whitePlayer = input("Enter the time the white player thought: ")
# option 1
human = max(formatMilliseconds(blackPlayer), formatMilliseconds(whitePlayer))
print("Amount of time the white player was thinking: " + formatMilliseconds(blackPlayer))
print("Amount of time the black player was thinking: " + formatMilliseconds(whitePlayer))
print("The time the human player has spend thinking: %s" % human)

#option 2
blackPlayer = input("Enter the time the black player thought: ")
whitePlayer = input("Enter the time the white player thought: ")
if blackPlayer > 1000:
    print("The time the human player has spend thinking: " + formatMilliseconds(blackPlayer))
else:
    print("The time the human player has spend thinking: " + formatMilliseconds(whitePlayer))
