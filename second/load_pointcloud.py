import numpy as np
from mpl_toolkits.mplot3d.axes3d import *

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from second.pointcloud_utils import reduce_pointcloud


def load_data(load_path, visualize=False):

    # data_points = np.fromfile(load_path, dtype=np.float32, count=-1).reshape([-1, 4])
    data_points = np.fromfile(load_path, dtype=np.float32, count=-1).reshape([-1, 4])

    # data_points = np.fromfile(load_filename).reshape(1024*64, 4)

    # data_points = reduce_pointcloud(data_points)

    # print(np.shape(data_points))

    if visualize == True:
        # Plot Figures
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        #
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.scatter(data_points[:, 0], data_points[:, 1], data_points[:, 2], s=1)
        plt.show()

    return data_points

