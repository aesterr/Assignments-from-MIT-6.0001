import math

class Fraction(object):
    def __init__(self, num, denom):
        assert type(num) == int and type(denom) == int and denom != 0, "Value error: Integers not used or denominator is 0."
        self.num = num
        self.denom = denom
    
    def __str__(self):
        return(str(self.num) + "/" + str(self.denom))
    
    def __add__(self, other):
        new_num = self.num*other.denom + other.num*self.denom
        new_denom = self.denom*other.denom
        new_numm = int(new_num/math.gcd(new_num, new_denom))
        new_denomm = int(new_denom/math.gcd(new_num, new_denom))
        return(Fraction(new_numm, new_denomm))
    
    def __sub__(self, other):
        new_num = self.num*other.denom - other.num*self.denom
        new_denom = self.denom*other.denom
        new_numm = int(new_num/math.gcd(new_num, new_denom))
        new_denomm = int(new_denom/math.gcd(new_num, new_denom))
        return(Fraction(new_numm, new_denomm))
    
    def multiply(self, other):
        new_num = self.num*other.num
        new_denom = self.denom*other.denom
        new_numm = int(new_num/math.gcd(new_num, new_denom))
        new_denomm = int(new_denom/math.gcd(new_num, new_denom))
        return(Fraction(new_numm, new_denomm))
    
    def divide(self, other):
        new_num = self.num*other.denom
        new_denom = self.denom*other.num
        new_numm = int(new_num/math.gcd(new_num, new_denom))
        new_denomm = int(new_denom/math.gcd(new_num, new_denom))
        return(Fraction(new_numm, new_denomm))

x = Fraction(3, 4)
y = Fraction(1, 2)
print(x - y)
print(x.multiply(y))
print(x.divide(y))