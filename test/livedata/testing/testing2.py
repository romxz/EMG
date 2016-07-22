import matplotlib.pyplot as plt
import numpy as np
import random
import time

#example variables
constants = [[25,25,75,75],[25,75,25,75]]
colours = ["r", "g", "b", "m"]
fig = plt.figure()
plt.axis([0,100,0,100])

#plotting the constants
for i in range(4):
    plt.scatter(constants[0][i], constants[1][i], c = colours[i], s = 50)

j = 0
while j<1000:
    
    plt.clf()
    for i in range(4):
        plt.scatter(constants[0][i], constants[1][i], c = colours[i], s = 50)
    
    value = [random.randint(0,100) , random.randint(0,100)]
    plt.scatter(value[0], value[1])
    
    j+=1