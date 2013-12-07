'''
Created on 6 dec. 2013
Author: Daan Helsloot

'''
from ipy_lib import SnakeUserInterface
ui = SnakeUserInterface(40, 30, 0.5)


def processEvent(event):
    ui.print_(event.name + " " + event.data + "\n")
    if event.name == "click":
        processClick(event)
    elif event.name == "other":
        processSpacebar(event)


def processClick(event):
    click_coordinates = event.data.split()
    x = int(click_coordinates[0])
    y = int(click_coordinates[1])
    ui.place(x, y, ui.WALL)
    ui.show()


def processSpacebar(event):
    ui.clear()
    ui.show()

while True:
    event = ui.get_event()
    processEvent(event)