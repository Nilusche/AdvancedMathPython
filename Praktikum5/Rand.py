from mimetypes import init
import random
class Rand:
    random.seed()
    def initialize(self, s):
        random.seed(s)

    def __init__(self,s):
        self.initialize(s)
    
    def value(self, a, b):
        return random.randint(a,b)
    
    def test(self, a, b , N):
        v = {k:0 for k in range(b+1)}
        for i in range(N):
            randomnumber = self.value(a,b)
            v[randomnumber]+=1
        
        v = {key:val for key,val in v.items() if val!=0}
        return v
    
    def test_wrong(self, a, b , N):
        v = {k:0 for k in range(b+1)}
        for i in range(N):
            random.seed()
            randomnumber = self.value(a,b)
            v[randomnumber]+=1
        
        v = {key:val for key,val in v.items() if val!=0}
        return v


'''
test = Rand(0)
v1 = test.test(3,7,10000)
v2 = test.test_wrong(3,7,10000)

print(v1)
print(v2)
'''