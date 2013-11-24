__author__ = 'Helsloot'


class BMIHelper(object):

    def __init__(self, length, weight, gender, last_name):
        self.length = length
        self.weight = weight
        self.gender = gender
        self.last_name = last_name

    def __str__(self):
        return "%s %s's BMI is %.1f and is %s " % (self.getGender(), self.getLastName(),
                                                   self.calculateBMI(), self.isHealthy())

    def __repr__(self):
        return str(self)

    def getGender(self):
        return 'Mr.' if self.gender == 'M' else 'Mrs.'

    def getLastName(self):
        return self.last_name

    def getLength(self):
        return float(self.length)

    def getWeight(self):
        return int(self.weight)

    def calculateBMI(self):
        return self.getWeight()/(self.getLength() ** 2)

    def isHealthy(self):
        return "unhealthy" if self.calculateBMI() < 18.5 or self.calculateBMI() > 25 else "healthy"