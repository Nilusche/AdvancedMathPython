from copy import deepcopy
from pickle import TRUE
from MyVektor import *

class DGLSolver:
    __DGL = ()
    __DGLSystem = True
    def __init__(self, systemtype, DGL):
        self.__DGLSystem = True if systemtype else False
        self.__DGL = DGL
    
    def __derivatives(self, y:MyVektor, x):
        sys = deepcopy(y)
        if self.__DGLSystem: 
            sys = self.__DGL(y,x)
        else: 
            n  = len(y)
            sys = MyVektor([0 for x in range(n)])
            sys[n-1] =self.__DGL(y,x)

            for i in range(n-1):
                sys[i] = y[i+1]

        return sys 
    
    def euler(self, x_start, x_end, steps, y_start:MyVektor):
        eul = deepcopy(y_start)
        deri = self.__derivatives(eul, x_start)

        diff = x_end - x_start
        x = x_start
        h = diff/steps

        print("h = ", h , "\n")
        for i in range(steps):
            x = x_start + (diff*i)/steps
            deri = self.__derivatives(eul, x)
            print("Schritt ", i, ":")
            print("\t x = ", x)
            print("\t y =  ", eul)
            print("\t y'= ", deri)
            eul += self.__derivatives(eul, x) * h
            k  =i
            if k+1 == steps:
                x = (diff * k+1)/steps + x_start
                print("End")
                print("\t x = ", x)
                print("\t y = ", eul)
            
        return eul

    def heun(self, x_start, x_end, steps, y_start):
        heun = deepcopy(y_start)
        deri = self.__derivatives(heun,x_start)
        yt = deepcopy(y_start)
        yt_deriv = deepcopy(y_start)
        y_middle = deepcopy(y_start)

        x = x_start
        diff = x_end - x_start
        h = diff/steps

        print("h = ", h)
        for i in range(steps):
            x = (diff * i) / steps + x_start
            deri = self.__derivatives(heun,x)
            yt = heun + self.__derivatives(heun,x)*h
            yt_deriv = self.__derivatives(yt, x+h)
            y_middle = (deri + yt_deriv) * 0.5
            print("Schritt ", i, ":")
            print("\t x = ", x)
            print("\t y =  ", heun)
            print("\t y_orig'= ", deri)
            print("\t y_Test",yt)
            print("\t y'_Test", yt_deriv)
            print("\t y'_Middle", y_middle)

            heun+=y_middle * h
            x+=h

            k=i
            if k+1 == steps:
                x = (diff* k+1)/steps + x_start
                print("End")
                print("\t x = ", x)
                print("\t y = ", heun)
         



def DGLSystem1(y:MyVektor, x):
    return MyVektor([(2.0 * y[1]) - (x * y[0]),(y[0] * y[1]) - (2.0 * x * x * x)])
  

def DGLSystem2(y:MyVektor, x):
    return  MyVektor([y[0] + x])

def DGLthirdOrder(y:MyVektor, x):
    return (2.0 * x * y[1] * y[2]) + (2.0 * y[0] * y[0] * y[1])

'''dgl = DGLSolver(True,DGLSystem2)
y = MyVektor([-1])
dgl.euler(1, 2.0,100,y)'''

'''
dgl = DGLSolver(True, DGLSystem1)
y = MyVektor([0,1])
dgl.euler(0.0, 2.0, 100,y)
dgl.heun(0.0, 2.0, 100,y)'''

dgl = DGLSolver(False, DGLthirdOrder)
y = MyVektor([1,-1,2])
dgl.euler(1,2,10,y)
dgl.heun(1,2,10,y)
