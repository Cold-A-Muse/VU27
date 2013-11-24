'''Assignment: BodyMassIndex
   Created on 24-11-2013
   @author: Daan Helsloot (dht340) '''

import sys

from BMIHelper import BMIHelper

with open('bmi.txt') as f:
    content = f.readlines()
    persons = [x.split() for x in content]
    print persons

for person in persons:
    last_name = person[1]
    gender = person[2]
    length = person[3]
    weight = person[4]
    bmi_helper = BMIHelper(length, weight, gender, last_name)
    print bmi_helper
