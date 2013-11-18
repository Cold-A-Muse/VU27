'''Assignment: Replay3
   Created on 18-11-2013
   @author: Daan Helsloot (dht340) '''

from ipy_lib import OthelloReplayUserInterface, file_input

MILISECONDS = 100
THREE = 3
FOUR = 4

ui = OthelloReplayUserInterface()


def getGoodColor(array):
    kleur = array[0]
    return ui.WHITE if kleur == "wit" else ui.BLACK


def getXCoordinates(array):
    x_coords = array[3::2]
    output = ""
    for coord in x_coords:
        output += str(ord(coord) - ord('a')) + " "
    splitted = output.split()
    return splitted


def getYCoordinates(array):
    y_coords = array[4::2]
    output = ""
    for coord in y_coords:
        output += str(int(coord) - 1) + " "
    splitted = output.split()
    return splitted


def getWaitingTime(beurt):
    return int(beurt[1])


def zetSteen(beurt):
    kleur = beurt[0]
    if kleur.startswith('='):
        kleur = kleur[1::]

    juiste_steen = getGoodColor(beurt)
    x_coords = getXCoordinates(beurt)
    y_coords = getYCoordinates(beurt)
    for i in range(0, min(len(x_coords), len(y_coords))):
        x = int(x_coords[i])
        y = int(y_coords[i])
        conquered = len(x_coords) - 1
        ui.place(x, y, juiste_steen)
        ui.show()
    ui.print_("%s: conquered %d piece(s) " % (kleur, conquered) + "\n")


def wachtBeurt(beurt):
    kleur = beurt[0]
    ui.print_("%s: passed" % kleur + "\n")


def getAction(beurt):
    return beurt[2]


def play():
    for beurt in beurten:
        kleur = beurt[0]
        if kleur.startswith('='):
            newGame()
            ui.wait(getWaitingTime(beurt))
            zetSteen(beurt)
        else:
            ui.wait(getWaitingTime(beurt))
            if getAction(beurt) == 'zet':
                zetSteen(beurt)
            elif getAction(beurt) == 'pas':
                wachtBeurt(beurt)


def newGame():
    ui.clear()
    ui.clear_text()
    ui.print_("Old game has ended. New game will start in ~5 seconds")
    ui.wait(5000)
    ui.clear_text()
    ui.place(THREE, THREE, ui.WHITE)
    ui.place(FOUR, FOUR, ui.WHITE)
    ui.place(THREE, FOUR, ui.BLACK)
    ui.place(FOUR, THREE, ui.BLACK)
    ui.show()


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