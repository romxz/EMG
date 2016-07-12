a = [[ 81.79825411,  51.43512363,  85.77357055],
 [ 87.41168797,  84.78433072,  16.3074],
 [ 12.25613638,  43.49164483,  56.0307],
 [ 82.25960461,  23.74852474,  49.83725]]
 
a = np.transpose(np.array(np.round(a)))
 
print(a)

def threeDtotwoD(array): #array = 2D matrix (3 rows, N columns (number of samples))
    new_list = [[],[]]
    for i in range(len(array[0])):
        a = float(array[0][i])
        b = float(array[1][i])
        c = float(array[2][i])  
        f = (np.sqrt(3.0)/2)*(a-b)
        g = (1/2)*(2*c-a-b)
        r = np.sqrt(a**2 + b**2 + c**2)
        s = np.sqrt(f**2 + g**2 + 1)
        j = (r/s)*f
        k = (r/s)*g
        new_list[0].append(j)
        new_list[1].append(k)
    return new_list
    
b = threeDtotwoD(a)
print("hi")
print(np.array(b))