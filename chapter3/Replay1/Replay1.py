'''Assignment: Replay1
   Created on 11-11-2013
   @author: Daan Helsloot (dht340) '''

from ipy_lib import OthelloReplayUserInterface, file_input

MILISECONDS = 100
THREE = 3
FOUR = 4

ui = OthelloReplayUserInterface()


def getGoodColor(array):
    kleur = array[0]
    return ui.WHITE if kleur == "wit" else ui.BLACK


def getXCoordinate(array):
    x_coordinate_without_adjustments = array[3]
    return ord(x_coordinate_without_adjustments) - ord('a')


def getWaitingTime(beurt):
    return int(beurt[1])


def zetSteen(beurt):
    kleur = beurt[0]
    miliseconden = getWaitingTime(beurt)
    letter_x_as = beurt[3] 
    juiste_steen = getGoodColor(beurt)
    x_coord = getXCoordinate(beurt)
    y_coord = int(beurt[4]) - 1
    
    ui.place(x_coord, y_coord, juiste_steen)
    ui.show()
    ui.print_("%s: dacht %d miliseconde(n) na over zijn beurt. Steen geplaatst op %s%d"
              % (kleur, miliseconden, letter_x_as, y_coord) + "\n")


def wachtBeurt(beurt):
    kleur = beurt[0]
    miliseconden = getWaitingTime(beurt)
    ui.print_("%s: dacht %d miliseconde(n) na over zijn beurt. Slaat deze beurt over"
                % (kleur, miliseconden) + "\n")


def getAction(beurt):
    return beurt[2]    
    

def play():
    for beurt in beurten:
        ui.wait(getWaitingTime(beurt))
        if getAction(beurt) == 'zet':
            zetSteen(beurt)
        elif getAction(beurt) == 'pas':
            wachtBeurt(beurt)       

ui.place(THREE, THREE, ui.WHITE)
ui.place(FOUR, FOUR, ui.WHITE)
ui.place(THREE, FOUR, ui.BLACK)
ui.place(FOUR, THREE, ui.BLACK)
ui.show()
ui.wait(MILISECONDS)

f = file_input()
content = f.splitlines()
beurten = [i.split() for i in content] 
play()