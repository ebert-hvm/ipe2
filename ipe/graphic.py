from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Graphic:
    def __init__(self, file, dist) -> None:
        self.data = pd.read_csv(file, sep=',')
        self.dist = dist
        self.set_axis()
        self.to_graphic()

    def set_axis(self):
        x, y = np.arange(0,self.data.shape[1],self.dist), np.arange(0,self.data.shape[0],self.dist)
        self.z = self.data.to_numpy()
        self.X, self.Y = np.meshgrid(x,y)

    def to_graphic(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection='3d')
        ax.plot_surface(self.X,self.Y,self.z, alpha=1, rstride=1, cstride=1, cmap=cm.coolwarm)
        plt.show()


