'''
Assignment: Pirate
Created on 30 nov. 2013
Author: Lizzy Sinnema
'''

from ipy_lib import file_input
data = file_input()

from CoordinateRow import CoordinateRow
from Coordinate import Coordinate


def verwerk_data(data):
    regels = data.split("=")
    for regel in regels:
        verwerk_regel(regel)

def verwerk_regel(regel):
    cr = CoordinateRow()
    coordinaten = regel.split()
    for coordinaat in coordinaten:
        verwerkt_coordinaat = verwerk_coordinaat(coordinaat)
        cr.add(verwerkt_coordinaat)
    cr2 = CoordinateRow()
    cr12 = cr.weave(cr2)
    print cr12


def verwerk_coordinaat(coordinaat):
    coordinaat = coordinaat.split(",")
    x = coordinaat[0]
    y = coordinaat[1]
    nieuw_coordinaat = Coordinate(x)
    adjusted_x = nieuw_coordinaat.pas_x_aan()
    return str(adjusted_x) + ',' + str(y)
        
verwerk_data(data)
    
# deelprobleem weven: maak een class en weef

