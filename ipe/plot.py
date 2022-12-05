import matplotlib.pyplot as plt
import numpy as np

X = []
Y = []
Z = []
with open('plot', 'r') as f:
    for line in f.readlines():
        x, y, z = line.split(',')
        X.append(float(x))
        Y.append(float(y))
        Z.append(float(z))
 
# Creating figure
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
# Creating plot
ax.scatter3D(X, Y, Z, color = "green")
#plt.title("simple 3D scatter plot")
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap="autumn")
# show plot
plt.show()