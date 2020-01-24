import numpy as np
from ann import network

class Brain:
    def __init__(self,layers=4,structure=[10,10,10,10]):
        self.factor=20
        self.brain=[]
        jumpx,jumpy=0,0
        for _ in range(layers):
            self.brain.append(network(structure,jumpx,jumpy))
            jumpy+=self.factor
            if jumpy>=320:
                jumpy=0
                jumpx+=self.factor
