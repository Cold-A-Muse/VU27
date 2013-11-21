'''Assignment: Replay2
   Created on 18-11-2013
   @author: Daan Helsloot (dht340) '''

__author__ = 'Daan Helsloot'

from ipy_lib import BarChartUserInterface, file_input
barChart = BarChartUserInterface(10)


def readFile():
    file = file_input()
    content = file.splitlines()
    for i in content:
        splitTab(i)


def splitTab(line):
    line = line.split('\t')
    if len(line) > 1:
        numbers = line[1::]
        for l in numbers:
            splitNumber(l)


def splitNumber(line):
    line = line.split()
    percentage = line[1::]
    for l in percentage:
        createDemBarz(l)


def createDemBarz(perc):
    perc = int(perc)
    if perc < 10:
        barChart.raise_bar(0)
    elif 10 <= perc < 20:
        barChart.raise_bar(1)
    elif 20 <= perc < 30:
        barChart.raise_bar(2)
    elif 30 <= perc < 40:
        barChart.raise_bar(3)
    elif 40 <= perc < 50:
        barChart.raise_bar(4)
    elif 50 <= perc < 60:
        barChart.raise_bar(5)
    elif 60 <= perc < 70:
        barChart.raise_bar(6)
    elif 70 <= perc < 80:
        barChart.raise_bar(7)
    elif 80 <= perc < 90:
        barChart.raise_bar(8)
    elif 90 <= perc < 100:
        barChart.raise_bar(9)
barChart.show()

readFile()

# for i in content:
#     i.split('\t')
#     print(i)



# print split[:58:]
# print split[58:111:]
# print split[111:172:]
# print split[172:234:]
# print split[234:290]

