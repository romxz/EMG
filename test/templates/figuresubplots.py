# """Examples illustrating the use of plt.subplots().
# 
# This function creates a figure and a grid of subplots with a single call, while
# providing reasonable control over how the individual plots are created.  For
# very refined tuning of subplot creation, you can still use add_subplot()
# directly on a new figure.
# """
# 
# import matplotlib.pyplot as plt
# import numpy as np
# 
# # Simple data to display in various forms
# x = np.linspace(0, 2 * np.pi, 400)
# y = np.sin(x ** 2)
# 
# plt.close('all')
# 
# # Just a figure and one subplot
# f, ax = plt.subplots()
# ax.plot(x, y)
# ax.set_title('Simple plot')
# 
# 
# # Two subplots, the axes array is 1-d
# f, axarr = plt.subplots(2, sharex=True)
# axarr[0].plot(x, y)
# axarr[0].set_title('Sharing X axis')
# axarr[1].scatter(x, y)
# 
# # Two subplots, unpack the axes array immediately
# f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize = (10,5))
# ax1.plot(x, y)
# ax1.set_title('Sharing Y axis')
# ax2.scatter(x, y)

# # Three subplots sharing both x/y axes
# f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
# ax1.plot(x, y)
# ax1.set_title('Sharing both axes')
# ax2.scatter(x, y)
# ax3.scatter(x, 2 * y ** 2 - 1, color='r')
# # Fine-tune figure; make subplots close to each other and hide x ticks for
# # all but bottom plot.
# f.subplots_adjust(hspace=0)
# plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
# 
# # row and column sharing
# f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
# ax1.plot(x, y)
# ax1.set_title('Sharing x per column, y per row')
# ax2.scatter(x, y)
# ax3.scatter(x, 2 * y ** 2 - 1, color='r')
# ax4.plot(x, 2 * y ** 2 - 1, color='r')
# 
# # Four axes, returned as a 2-d array
# f, axarr = plt.subplots(2, 2)
# axarr[0, 0].plot(x, y)
# axarr[0, 0].set_title('Axis [0,0]')
# axarr[0, 1].scatter(x, y)
# axarr[0, 1].set_title('Axis [0,1]')
# axarr[1, 0].plot(x, y ** 2)
# axarr[1, 0].set_title('Axis [1,0]')
# axarr[1, 1].scatter(x, y ** 2)
# axarr[1, 1].set_title('Axis [1,1]')
# # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
# plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
# plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
# 
# # Four polar axes
# plt.subplots(2, 2, subplot_kw=dict(projection='polar'))

"""
Demonstrate the mixing of 2d and 3d subplots
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig1 = plt.figure(figsize = (24,8))
ax1 = fig1.add_subplot(1, 2, 1, projection="3d")
ax2 = fig1.add_subplot(1, 2, 2, projection='3d')

# def f(t):
#     s1 = np.cos(2*np.pi*t)
#     e1 = np.exp(-t)
#     return np.multiply(s1, e1)
# 
# 
# ################
# # First subplot
# ################
# t1 = np.arange(0.0, 5.0, 0.1)
# t2 = np.arange(0.0, 5.0, 0.02)
# t3 = np.arange(0.0, 2.0, 0.01)
# 
# # Twice as tall as it is wide.
# fig = plt.figure(figsize=plt.figaspect(2.))
# fig.suptitle('A tale of 2 subplots')
# ax = fig.add_subplot(2, 1, 1)
# l = ax.plot(t1, f(t1), 'bo',
#             t2, f(t2), 'k--', markerfacecolor='green')
# ax.grid(True)
# ax.set_ylabel('Damped oscillation')
# 
# 
# #################
# # Second subplot
# #################
# ax = fig.add_subplot(2, 1, 2, projection='3d')
# X = np.arange(-5, 5, 0.25)
# xlen = len(X)
# Y = np.arange(-5, 5, 0.25)
# ylen = len(Y)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)
# 
# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
#                        linewidth=0, antialiased=False)
# 
# ax.set_zlim3d(-1, 1)
# 
# plt.show()
# 
# plt.show()