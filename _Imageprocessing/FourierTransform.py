from datetime import MAXYEAR
from decimal import Decimal
from Complex import *

def readComplex(file):
    vec = [Complex(0,0) for _ in range(1000)]
    with open(file) as f:
        f.readline()
        for line in f:
            array = line.split()
            vec[int(array[0])]=(Complex(float(array[1]), float(array[2])))

    return vec

def writeComplex(file, data, epsilon=-1.0):
    with open(file, 'w') as f:
        f.write("1000\n")
        for i in range(len(data)):
            if data[i].abs()>epsilon:
                f.write(str(i)+"\t"+str(data[i].getReal())+"\t"+str(data[i].getImg())+"\n")


def transformed(data, direction):
    transformed = []

    N = len(data)
    factor = 1/math.sqrt(N)
    for n in range(N):
        c = Complex(0,0)
        for k in range(N):
            if direction==True:
                c+=data[k][1] * Complex(-(2.0 * math.pi * k * n)/N)
            else:
                c+=data[k][1] * Complex((2.0 * math.pi * k * n)/N)
        
        c*=factor
        transformed.append((data[n][0],c))
        
        
    return transformed

def deviation(data1, data2):
    sub = []
    for i in range(len(data1)):
        sub.append((data2[i]-data1[i]).abs())
    return max(sub)

'''
data = readComplex("Data_original.txt")
fourier_transformed = transformed(data, True)

writeComplex("transformed_default.txt",fourier_transformed)
writeComplex("transformed_1.txt",fourier_transformed,1.0)
writeComplex("transformed_01.txt",fourier_transformed,0.1)
writeComplex("transformed_001.txt",fourier_transformed, 0.01)
writeComplex("transformed_0001.txt",fourier_transformed, 0.001)

#default
datanew = readComplex("transformed_default.txt")
fourier_transformed = transformed(datanew, False)
writeComplex("transformedback_default.txt", fourier_transformed)

#1.0
datanew = readComplex("transformed_1.txt")
fourier_transformed = transformed(datanew, False)
writeComplex("transformedback_1.txt", fourier_transformed)


#0.1
datanew = readComplex("transformed_01.txt")
fourier_transformed = transformed(datanew, False)
writeComplex("transformedback_01.txt", fourier_transformed)

#0.01
datanew = readComplex("transformed_001.txt")
fourier_transformed = transformed(datanew, False)
writeComplex("transformedback_001.txt", fourier_transformed)

#0.001
datanew = readComplex("transformed_0001.txt")
fourier_transformed = transformed(datanew, False)
writeComplex("transformedback_0001.txt", fourier_transformed)

epsilondefault = readComplex("transformedback_default.txt")
epsilon_0001 = readComplex("transformedback_0001.txt")
epsilon_001 = readComplex("transformedback_001.txt")
epsilon_01 = readComplex("transformedback_01.txt")
epsilon_1 = readComplex("transformedback_1.txt")

print("Maximum deviation with default epsilon: ", deviation(data, epsilondefault))
print("Maximum deviation with epsilon = 0.001: ", deviation(data, epsilon_0001))
print("Maximum deviation with epsilon = 0.01: ", deviation(data, epsilon_001))
print("Maximum deviation with epsilon = 0.1: ", deviation(data, epsilon_01))
print("Maximum deviation with epsilon = 1: ", deviation(data, epsilon_1))

'''