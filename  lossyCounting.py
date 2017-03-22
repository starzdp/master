#!/usr/bin/python
import random
import sys

class LossyCountingQueries(object):	
    def __init__(self, epsilon):
       # print epsilon
	self.N = 0
        self.count = {}
        self.epsilon = epsilon
        self.b_current = 1
    
    def getCount(self, item):
        return self.count[item][0]
    
    def trim(self):
        for item in self.count.keys():
            if self.count[item][0] + self.count[item][1] <= self.b_current:
                del self.count[item]
        
    def addCount(self, item):
        self.N += 1
        if item in self.count:
            self.count[item][0]= self.count[item][0] + 1 
        else:
            self.count[item]= [1,self.b_current - 1]
        #print self.count
        if self.N % int(1 / self.epsilon) == 0:
            self.trim()
	    self.b_current += 1
    	#print self.count
    def iterateOverThresholdCount(self, threshold_count):
        assert threshold_count > self.epsilon * self.N, "too small threshold"
        #print threshold_count
        for item in self.count:
            if self.count[item][0] >= threshold_count:
                yield (item, self.count[item][0])
    
    def iterateOverThresholdRate(self, threshold_rate):
        #print self.N
	return self.iterateOverThresholdCount((threshold_rate) * self.N)
    

if __name__ == '__main__':
    counter = LossyCountingQueries(0.001)
    for line in sys.stdin:
        counter.addCount(line.strip())
    
    for item, count in sorted(counter.iterateOverThresholdRate(0.01 - 0.001), key=lambda x:x[1]):
        print ("{0}".format(item))
