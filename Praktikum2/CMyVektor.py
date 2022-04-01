from copy import deepcopy
import math
from operator import truediv
from pyexpat.errors import XML_ERROR_XML_DECL
from re import X, sub
import re
from tokenize import Double, Number


class CMyVektor:
    __vec =[]
    def getVec(self):
        return self.__vec

    def __init__(self, vec):
        self.__vec = vec

    def __str__(self):
        return str(self.__vec);

    def __len__(self):
        return len(self.__vec)

    def length(self):
        sum = 0
        for i in self.__vec:
            sum += i * i
        return math.sqrt(sum);

    def __getitem__(self,key):
        return self.__vec[key]

    def __setitem__(self, key, value):
        self.__vec[key] = value

    def __add__(self, other):
        vec1 = []
        if len(self.__vec)==len(other.__vec):
            for i in range(len(self.__vec)):
                vec1.append(self.__vec[i] + other.__vec[i])
        else:
            raise RuntimeError("Invalid dimensions")

        return CMyVektor(vec1);

    def __sub__(self, other):
        vec1 = []
        if len(self.__vec)==len(other.__vec):
            for i in range(len(self.__vec)):
                vec1.append(self.__vec[i] - other.__vec[i])
        else:
            raise RuntimeError("Invalid dimensions")

        return CMyVektor(vec1);

    def __mul__(self, other):
        return CMyVektor([x*other for x in self.__vec])

    def gradient(self, function, h):
        subtrahend = function(self)
        minuend = CMyVektor(self.__vec)
        grad= CMyVektor([0 for _ in range (len(self.__vec))]);

        for i in range(len(self.__vec)):
            minuend.__vec[i]+= h
            grad.__vec[i] = (function(minuend)-subtrahend) / h
            minuend.__vec[i]-= h
           
        return grad;

    def gradientenVerfahren(self, x, function, lambd, steps):
        break_condition = False
        print("Maximization: \n")
        x_neu = CMyVektor(x.__vec)
        grad = CMyVektor(x.__vec)
        f_x_neu = function(x)
        f = function(x)
        length = x.length()
        abbruch = 1e-5
        for i in range(steps):
            f= function(x)
            grad = x.gradient(function, 1e-8)
            x_neu = x + (grad * lambd)
            f_x_neu = function(x_neu)
            length = grad.length()

            if length < abbruch: 
                break_condition =True
                break
            print("Step: ", i)
            print("x = ", x)
            print("lambda = ", lambd)
            print("f(x) =  ",f)
            print("grad f(x) ", grad)
            print("||grad f(x)|| = ", length)
            print("f(x_neu) ", f_x_neu, "\n")

            if f_x_neu  > f :
                xtest = CMyVektor(x)
                f_grad_x_test = f_x_neu
                test_lambda = lambd
                x_test = x + (grad*test_lambda)
                f_grad_x_test =  function(x_test)
                print("Test mit doppelter Schrittweite (lambda = ", test_lambda, "):\n")
                print("x_test = ", x_test, "\n")
                print("f(x_test) = ", f_grad_x_test, "\n\n")

                if f_grad_x_test > f_x_neu:
                    x = x_test
                    lambd = test_lambda
                    print("Verdoppelte Schrittweite!\n\n")
                else:
                    x = x_neu
                    print("behalte alte Schrittweite!\n\n")
            elif f_x_neu <=f:
                test_lambda = lambd
                while not (f_x_neu> f):
                    test_lambda *=0.5
                    print("halbiere Schrittweite (lambda = ", test_lambda, ") : \n")
                    x_neu = x + (grad * test_lambda)
                    f_x_neu = function(x_neu)
                    print("x_neu = ", x_neu)
                    print("f(x_neu) = ", f_x_neu,"\n\n")
                
                lambd = test_lambda
                x= x_neu
                print("\n")

        f = function(x)
        grad = x.gradient(function, 1e-8)
        if break_condition: 
            print("Ende wegen ||grad f(x)||<1e-5 bei")
        else:
            print("Ende wegen Schrittweite.")
        print("x = ", x)
        print("lambda ", lambd)
        print("f(x)", f)
        print("grad f(x)", grad)
        print("||grad f(x)||", grad.length(), "\n")
        return x





def func(x:CMyVektor):
    return math.pow(x[0],2) *math.sin(x[1] * x[2])

def funcF(x:CMyVektor):
    return math.sin(x[0]*x[1]) + math.sin(x[0]) + math.cos(x[1])
def funcG(x:CMyVektor):
    return (-(2.0*(x[0]*x[0])-2.0*x[0]*x[1]+(x[1]*x[1])+ (x[2]*x[2])-(2.0*x[0])-(4.0*x[2])));
    