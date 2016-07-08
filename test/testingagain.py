import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time
k = 0
i = 0
all_data = []
x_val = []
y_val = []
all_data_trans = []

fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))



def init():
    line.set_xdata(all_data_trans[0][0:-1])
    line.set_ydata(all_data_trans[1][0:-1])
    return line,

def animate(i):
    scat = plt.scatter(val_a, val_b, c = "y", s=10)
    return scat

def animate2(i):
    scat = plt.scatter(x_val[i], y_val[i], c = "y", s = 10)
    return scat
def animate3(i):
    scat = plt.scatter(x_val[i+30], y_val[i+30], c = "b", s = 10)
    return scat





while k<1000:
    val_a = np.random.randint(0,100)
    val_b = np.random.randint(0,100)
    value = [val_a,val_b]
    all_data.append(value)
    x_val.append(val_a)
    y_val.append(val_b)
    all_data_trans = [x_val,y_val]
    #scat = plt.scatter(val_a, val_b, c = "y", s=10)
    #line, = plt.plot(all_data_trans[0],all_data_trans[1], "x", color="red")
    #print (all_data_trans)
    #print(value)
    #anim = animation.FuncAnimation(fig, animate,
    #                           frames=100000, interval=100, blit=False)
    

    #plt.show()
    k += 1
print("hi")  
time1 = time.time()
anim = animation.FuncAnimation(fig, animate2,init = 
                            frames=100, interval=0.00001, blit=False)
anim = animation.FuncAnimation(fig, animate3,
                            frames=100, interval=0.00001, blit=False)
time2 = time.time()
print ("FPS = ")


#ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes), interval=(0.1),
#                                  fargs=(color_data, scat), blit = True)
#plt.show()
