from utilities import Subscriber, Subscribable, UpdateSignal
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter
import time
import threading
from multiprocessing import Process
import uncertainties
from uncertainties import unumpy

class PointCloudVisualizer(Subscriber):
    def __init__(self, point_cloud_file_name):
        print('Initializing')
        self.point_cloud_file_name = point_cloud_file_name
        self.data = np.load(self.point_cloud_file_name, allow_pickle = True)
        print('Loaded data')
        self.fig = plt.figure()

    def begin(self):
        print('Begin')
        self.ax = self.fig.add_subplot(111, projection='3d')
    
        x = unumpy.nominal_values(self.data[:, 0])
        print('Read x')
        y = unumpy.nominal_values(self.data[:, 1])
        print('Read y')
        z = unumpy.nominal_values(self.data[:, 2])
        print('Read z')

        dx = unumpy.std_devs(self.data[:, 0])
        print('Read dx')
        dy = unumpy.std_devs(self.data[:, 1])
        print('Read dy')
        dz = unumpy.std_devs(self.data[:, 2])
        print('Read dy')

        dtotal = np.sqrt(np.square(dx) + np.square(dy) + np.square(dz))
        print('Calculated dtotal')

        self.scat = self.ax.scatter(x, y, z, c=dtotal) 

        self.minx = min(x)
        self.miny = min(y)
        self.minz = min(z)
        self.maxx = max(x)
        self.maxy = max(y)
        self.maxz = max(z)

        self.ax.set_xlim(self.minx, self.maxx)
        self.ax.set_ylim(self.miny, self.maxy)
        self.ax.set_zlim(self.minz, self.maxz)

        # static axes
        # ax.set_xlim(0, 10)
        # ax.set_ylim(0, 10)
        # ax.set_zlim(0, 10) 
        
        # plt.colorbar(self.scat, label='Uncertainty (cm)', boundaries=np.linspace(0,5,100)) 
        plt.colorbar(self.scat, label='Uncertainty (cm)')
        plt.show()
        self.fig.suptitle("Point Cloud Final")     
    

if __name__ == '__main__':
    point_cloud_visualizer = PointCloudVisualizer('sample_point_data.npy')
    point_cloud_visualizer.begin()
    print('Done')
