'''Assignment: Replay2
   Created on 18-11-2013
   @author: Daan Helsloot (dht340) '''

__author__ = 'Daan Helsloot'

from ipy_lib import BarChartUserInterface, file_input

#barChart = BarChartUserInterface(10)
#for i in range(10):
#    barChart.raise_bar(1)
#barChart.show()

f = file_input()
content = f.splitlines()
for i in content:
    i.split('-')
    i.split()
    print i