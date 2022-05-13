
from copy import deepcopy
import math


class Complex:
    __a=0
    __b=0
    def __init__(self,a,b=None):
        if b is not None:
            self.__a=a 
            self.__b=b
        else:
            self.__a = math.cos(a)
            self.__b = math.sin(a)

    def __str__(self):
        pos = "+" if self.__b > 0 else "-"
        return str(self.__a) + " , " + str(self.__b)+ "i"

    def getReal(self):
        return self.__a

    def getImg(self):
        return self.__b
    
    def conjugated(self):
        conj = deepcopy(self)
        conj.__b = -conj.__b
        return conj

    def __add__(self, other):
        return Complex(self.__a+other.__a, self.__b+other.__b)
    
    def __sub__(self, other):
        return Complex(self.__a-other.__a, self.__b-other.__b)
    
    def __mul__(self, other):
        if type(other) is Complex:
            real = self.__a*other.__a - self.__b * other.__b
            im = self.__a*other.__b + self.__b * other.__a
            return Complex(real, im)
        else:
            return Complex(self.__a*other, self.__b*other)

    def __truediv__(self, other):
        if type(other) is Complex:
            numerator = self * other.conjugated()
            denominator = other * other.conjugated()
            return Complex(numerator.__a/denominator.__a,numerator.__b/denominator.__a)
        else:
            return Complex(self.__a/other, self.__b/other)
    def abs(self):
        return math.sqrt((self.__a * self.__a)+ (self.__b * self.__b))

