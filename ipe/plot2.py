
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from mpl_toolkits.mplot3d import Axes3D

x = np.random.random(10)
y = np.random.random(10)
z = np.random.random(10)

spline = ip.Rbf(x,y,z,function='thin-plate')

xi = np.linspace(x.min(), x.max(), 50)
yi = np.linspace(y.min(), y.max(), 50)
xi, yi = np.meshgrid(xi, yi)

zi = spline(xi,yi)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(xi,yi,zi)
plt.show()