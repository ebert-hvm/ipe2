from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Graphic:
    def __init__(self, tables, configure_data) -> None:
        self.tables = tables
        self.configure_data = configure_data
        #self.set_axis()
        #self.to_graphic()

    def set_axis(self):
        #x = np.arange(0,self.configure_data['columns'],self.configure_data['probes distance'])
        #y = np.arange(0,self.configure_data['rows'],self.configure_data['probes distance'])
        with open('ipe/plot', 'w') as f:
            for i in range(self.configure_data['rows']):
                for j in range(self.configure_data['columns']):
                    f.write(f"{j*self.configure_data['probes distance']},{i*self.configure_data['probes distance']},{self.tables[0][i][j]}\n")

    def read(self):
        self.x = []
        self.y = []
        self.z = []
        with open('plot', 'r') as f:
            for line in f.readlines():
                x, y, z = line.split(',')
                self.x.append(x)
                self.y.append(y)
                self.z.append(z)
    def to_graphic(self):
        self.read()
        #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection='3d')
        ax.scatter(self.x, self.y, self.z)
        #ax.plot_surface(self.X,self.Y,self.Z, rstride=1, cstride=1, cmap="autumn")
        #ax.set_zlim(-1.01, 1.01)
        #ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        #ax.zaxis.set_major_formatter('{x:.02f}')

        # Add a color bar which maps values to colors.
        #fig.colorbar(surf, shrink=0.5, aspect=5)

        #plt.savefig('fig.png')
        plt.show()
    def with_axes_3d(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(self.X, self.Y, self.Z, c=1, lw=0, s=20)
        plt.show()
m={
    'rows' : 2,
    'columns' : 2,
    'probes distance' : 2,
}
#g= Graphic([[[0.5,0.7],[0.8,0.1]]], m)
#g.to_graphic()
