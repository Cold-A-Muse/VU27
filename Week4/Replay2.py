__author__ = 'Daan Helsloot'

from ipy_lib.ipy_lib import OthelloReplayUserInterface


def getGoodColor(array):
    return ui.WHITE if array[0] == "wit" else ui.BLACK


def getXCoord(array):
    xCord = array[3]
    if xCord == 'a':
        return 0
    elif xCord == 'b':
        return 1
    elif xCord == 'c':
        return 2
    elif xCord == 'd':
        return 3
    elif xCord == 'e':
        return 4
    elif xCord == 'f':
        return 5
    elif xCord == 'g':
        return 6
    elif xCord == 'h':
        return 7
    else:
        return -1

ui = OthelloReplayUserInterface()
# Replay1Invoer moet in dezelfde directory zitten
with open('Replay2Invoer.txt') as f:
    content = f.readlines()
    splitted = [i.split() for i in content]
    print splitted

#for a in splitted:
#    try:
#        ui.wait(int(a[1]))
#        ui.place(getXCoord(a), int(a[4]) - 1, getGoodColor(a))
#       ui.show()
#        ui.print_("%s: dacht %s miliseconde(n) na over zijn beurt. Steen geplaatst op %s%s"
#                  % (a[0], a[1], a[3], a[4]) + "\n")

#    except IndexError:
#        ui.wait(int(a[1]))
#        ui.show()
#        ui.print_("%s: dacht %s miliseconde(n) na over zijn beurt. Slaat deze beurt over"
#                  % (a[0], a[1]) + "\n")








