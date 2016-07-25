import numpy as np

print("A.\n")

x = np.array([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[5,4,3,2,1]])
y = np.array([[1,2,3,4,5],[2,3,4,5,6]])
print(x)

print (np.cov(x))
print (np.cov(y))