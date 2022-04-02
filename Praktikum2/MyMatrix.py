from copy import deepcopy
import math
from operator import truediv
from pyexpat.errors import XML_ERROR_XML_DECL
from re import X, sub
import re
from tokenize import Double, Number


class MyVektor:
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

        return MyVektor(vec1);

    def __sub__(self, other):
        vec1 = []
        if len(self.__vec)==len(other.__vec):
            for i in range(len(self.__vec)):
                vec1.append(self.__vec[i] - other.__vec[i])
        else:
            raise RuntimeError("Invalid dimensions")

        return MyVektor(vec1);

    def __mul__(self, other):
        return MyVektor([x*other for x in self.__vec])

    def gradient(self, function, h):
        subtrahend = function(self)
        minuend = MyVektor(self.__vec)
        grad= MyVektor([0 for _ in range (len(self.__vec))]);

        for i in range(len(self.__vec)):
            minuend.__vec[i]+= h
            grad.__vec[i] = (function(minuend)-subtrahend) / h
            minuend.__vec[i]-= h
           
        return grad;

    def gradientenVerfahren(self, x, function, lambd, steps):
        break_condition = False
        print("Maximization: \n")
        x_neu = MyVektor(x.__vec)
        grad = MyVektor(x.__vec)
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
                xtest = MyVektor(x)
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

    def newton(self,function, steps):
        x_copy = deepcopy(self)
        fx = function(x_copy)
        dx = deepcopy(x_copy)
        jacob = MyMatrix([MyVektor([0]* len(x_copy)), MyVektor([0]* len(x_copy))] )
        print(jacob)
        inv_jacob = deepcopy(jacob)
        abs_fx = 1e-5
        i = 0
        while i<steps and fx.length()>abs_fx:
            jacob = jacob.jacobi(x_copy, function)
            inv_jacob = jacob.invers()
            dx = (inv_jacob * fx) * -1.0
            print("Schritt: ", i)
            print("x = ", x_copy)
            print("f(x) =\n", fx)
            print("(f\'(x))^(-1) =\n", inv_jacob)
            print("dx = ", dx)
            print("||f(x)|| = ", fx.length(),"\n")
            x_copy +=dx
            fx = function(x_copy)
            i+=1
        
        if i>=steps:
            print("\nOut of Steps")
        else:
            print("\n Out of Length")
        
        print("x = ",x_copy)
        print("f(x) = ", fx)
        print("||f(x)|| = ", fx.length())

        return x_copy


class MyMatrix:
    __mat = []

    def __init__(self, __mat):
        self.__mat = __mat
    
    def add_dimension(self, __vec : MyVektor):
        self.__mat.append(__vec)
        
    def __len__(self):
        return len(self.__mat)
    def __add__(self, other:MyVektor):
        res = self.__mat
        if len(self.__mat) == len(other.__mat) and len(self.__mat[0]) == len(other.__mat[0]):
            for i in range(len(self.__mat)):
                for j in range(len(self.__mat[0])):
                    res[i][j]  += other.__mat[i][j]
        else:
            raise RuntimeError("Unequal Dimensions")            
        return MyMatrix(res)
    
    def __sub__(self, other:MyVektor):
        res = self.__mat
        if len(self.__mat) == len(other.__mat) and len(self.__mat[0]) == len(other.__mat[0]):
            for i in range(len(self.__mat)):
                for j in range(len(self.__mat[0])):
                    res[i][j]  -= other.__mat[i][j]
        else:
            raise RuntimeError("Unequal Dimensions")            
        return MyMatrix(res)
        

    def __mul__(self, other):
        res = [0]* len(self.__mat)
        if type(other) is MyVektor:
            if len(self.__mat) == len(other):
                for  i in range(len(self.__mat[0])):
                    for j in range(len(other)):
                        res[i] += self.__mat[j][i] * other[j] 
                
                return MyVektor(res)
            else:  
                raise RuntimeError("Dimensions of Instances are not compatible")
        else:
            return MyMatrix([x*other for x in self.__mat])

    def __str__(self):
        res = ""
        for i in range(len(self.__mat[0])):
            res+= "| "
            for j in range(len(self.__mat)):
                res += str(self.__mat[j][i])
                res += " "
            res+="|\n"
        
        return res

        
    def __getitem__(self, key):
        return self.__mat[key]
    
    def __setitem__(self, key, value):
        self.__mat[key] = value


    def jacobi(self, v:MyVektor, function):     
        h = 1e-4
        f = function(v)
        
        temp = []
        for i in range(len(v)):
            temp.append(MyVektor([0]*len(f)))
        jaco = MyMatrix(temp)

        copy = deepcopy(v)
        for i in range(len(f)):
            sub = f[i]
            for j in range(len(v)):
                copy[j] +=h
                jaco[j][i] = (function(copy)[i]-sub) /h
                copy[j] = v[j]

        return jaco

    def invers(self):
        if len(self.__mat[0]) == len(self.__mat):
            a = self.__mat[0][0]
            b = self.__mat[1][0]
            c = self.__mat[0][1]
            d = self.__mat[1][1]
            factor = 1.0 / ((a*d) - b*c)
            mat =  MyMatrix([MyVektor([0,0]), MyVektor([0,0])])
            print(mat[0][0])
            mat[0][0] = d
            mat[1][0] = -b
            mat[0][1] = -c
            mat[1][1] = a
            return MyMatrix(mat * factor)
        else:
            raise RuntimeError("Matrix not 2x2")
    


def func3(x: MyVektor):
    res = MyVektor([0,0])
    res[0] =  4 * x[0] * x[0] * x[1]
    res[1] = 4 * x[2] * x[2] + 4
    return res

def func2(x:MyVektor):
    res = MyVektor([0,0])
    res[0] = (x[0] * x[0] * x[0] * x[1] * x[1] * x[1]) - (2.0 * x[1]);
    res[1] = x[0] - 2.0;
    return res

c = MyMatrix([MyVektor([0,0]), MyVektor([0,0]),MyVektor([0,0])]) 
a = MyVektor([1,1])
a.newton(func2, 50)

