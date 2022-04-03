import math
from Lotto import *

def Monte_carlo(r, k, n , N, typ):
    sim=Lotto(k,n)
    sheet = Lotto.simulate(n,k, random.randint(k,n))

    total = 0
    occurence = 0
    ran = random.randint(k,n)

    for i in range (1, N+1):
        ran+=1
        if not typ:
            sheet = Lotto.simulate(n,k,ran)
            occurence = sim.lottery(0, sheet)
        else:
            occurence = sim.lottery(ran, sheet)
        
        if occurence == r:
            total+=1
    return total / N * 100.0


print(Monte_carlo(4,7,36, int(math.pow(10,5)), False))