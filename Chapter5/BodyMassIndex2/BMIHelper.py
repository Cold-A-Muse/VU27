__author__ = 'Helsloot'


class BMIHelper(object):

    total_persons = 0
    total_bmi = 0.0

    def __init__(self, length, weight, gender, last_name, syndrome):
        BMIHelper.total_persons += 1
        self.length = length
        self.weight = weight
        self.gender = gender
        self.last_name = last_name
        self.syndrome = syndrome

    def __str__(self):
        return "The average BMI of the test subjects is %.1f " % self.getAverageBMI()

    def __repr__(self):
        return str(self)

    def hasSyndrome(self):
        return True if self.syndrome == 'Yes' else False

    def getGender(self):
        return 'Mr.' if self.gender == 'M' else 'Mrs.'

    def getLastName(self):
        return self.last_name

    def getLength(self):
        return float(self.length)

    def getWeight(self):
        return int(self.weight)

    def calculateBMI(self):
        bmi = self.getWeight()/(self.getLength() ** 2)
        BMIHelper.total_bmi += bmi
        return bmi

    def getAverageBMI(self):
        return BMIHelper.total_bmi/BMIHelper.total_persons

    def isHealthy(self):
        return "unhealthy" if self.calculateBMI() < 18.5 or self.calculateBMI() > 25 else "healthy"