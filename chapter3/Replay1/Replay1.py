'''Assignment: Replay1
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''
#test
from ipy_lib import OthelloReplayUserInterface


def getGoodColor(array):
    kleur = array[0]
    return ui.WHITE if kleur == "wit" else ui.BLACK


def getXCoordinate(array):
    x_coordinate_without_adjustments = array[3]
    return ord(x_coordinate_without_adjustments) - ord('a')

ui = OthelloReplayUserInterface()
# Replay1Invoer.txt moet in dezelfde directory zitten
with open('Replay1Invoer.txt') as f:
    content = f.readlines()
    splitted = [i.split() for i in content]

for a in splitted:
    steen = a
    kleur = steen[0]
    miliseconden = int(steen[1])

    try:
        juiste_steen = getGoodColor(steen)
        letter_x_as = steen[3]
        x_coord = getXCoordinate(steen)
        y_coord = int(steen[4]) - 1

        ui.wait(miliseconden)
        ui.place(x_coord, y_coord, juiste_steen)
        ui.show()
        ui.print_("%s: dacht %d miliseconde(n) na over zijn beurt. Steen geplaatst op %s%d"
                  % (kleur, miliseconden, letter_x_as, y_coord) + "\n")

    except IndexError:
        ui.wait(miliseconden)
        ui.show()
        ui.print_("%s: dacht %d miliseconde(n) na over zijn beurt. Slaat deze beurt over"
                  % (kleur, miliseconden) + "\n")








