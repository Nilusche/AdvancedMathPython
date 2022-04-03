from copy import deepcopy
from Rand import *

class Lotto:
    __numbersheet=[]
    
    __k=6,
    __n=49
    def  check(self, list1, list2):
        l2 = deepcopy(list2)
        l1 = deepcopy(list1)

        return sorted(l2) == sorted(l1)

    def __init__(self, k, n):
        self.__n = n
        self.__k = k

    @staticmethod
    def simulate(n, k,ts):
        i = 0        
        nums = []
        r = Rand(ts)
        while i<k:
            randomnum = r.value(1,n)
            if randomnum not in nums:
                nums.append(randomnum)
                i+=1
        
        return nums

    def tip(self, sheet):
       self.__numbersheet.clear() 
       if len(sheet) == self.__k:
           self.__numbersheet = sheet
       else:
           raise RuntimeError("Unequal Dimensions")

    def lottery(self, ts, sheet):
        self.__numbersheet = sheet 
        draw = self.simulate(self.__n, self.__k, ts)
        if self.check(draw, self.__numbersheet): 
            return len(self.__numbersheet)
        else:
            count = 0
            for i in self.__numbersheet:
                if i in draw:
                    count+=1
            return count 