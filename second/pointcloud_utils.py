import numpy as np
from mpl_toolkits.mplot3d.axes3d import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sensor_msgs.msg import PointCloud2
from ros_numpy import point_cloud2
import ros_numpy
from sensor_msgs.msg import PointCloud2
from second import config as cfg
import rospy
import os
import math as m

def save_data(save_directory, filename, data):

    if filename.endswith(".bin"):
        save_path = os.path.join(save_directory, filename)
    else:
        save_path = os.path.join(save_directory, filename + '.bin')

    with open(save_path, 'w') as f:
        data.tofile(f)


def load_data(load_directory, filename):
    load_path = os.path.join(load_directory, filename)

    data_points = np.fromfile(load_path, dtype=np.float32, count=-1).reshape([-1, 4])

    return data_points


def reduce_pointcloud(data):

    idx = []
    for i in range(len(data)):
        if (data[i] == np.array([0, 0, 0, 0])).all():
            idx.append(i)
    reduced_array = np.delete(data, idx, 0)
    return reduced_array


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def cart2sph(x, y, z):
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(z, hxy)
    az = np.arctan2(y, x)
    return az, el, r

def sph2cart(az, el, r):
    rcos_theta = r * np.cos(el)
    x = rcos_theta * np.cos(az)
    y = rcos_theta * np.sin(az)
    z = r * np.sin(el)
    return x, y, z

def reduce_resolution(data, input_resolution, output_resolution=cfg.resolution, channels=cfg.channels):

    # Create empty polar array
    # polar_array = np.zeros([data.shape[0], data.shape[1]])

    # reduced_array = np.array([])

    reduced_array = np.empty((0, 4), 'f')

    # # Convert cartesian data to polar data
    # for i in range(len(data)):
    #     # print(f"i: {i}")
    #     rho, phi = cart2pol(data[i, 0], data[i, 1])
    #     polar_array[i] = [rho, phi, data[i, 2], data[i, 3]]

    # Convert cartesian coordinates to spherical coordinates
    sph_array = np.zeros([data.shape[0], data.shape[1]], dtype='f')

    for i in range(len(sph_array)):
        az, el, r = cart2sph(data[i, 0], data[i, 1], data[i, 2])
        sph_array[i] = np.array([az, el, r, data[i, 3]], dtype='f')



    # Sort polar array with respect to the elevation column (1)
    sortedArr = np.array(sph_array[sph_array[:, 1].argsort()])

    # Create histogram of the polar array
    hist, bin_edges = np.histogram(sortedArr[:, 1], channels)

    # Digitize the sorted array to extract which coordinates fall in which bin
    idx = np.digitize(sortedArr[:, 1], bin_edges)

    # For each extracted channel, do:
    for j in range(1, channels+1):

        # Create empty array to store the lower resoltion
        reduced_channel_array = np.zeros([1024, 4], dtype='f')

        # Retrieve indices per channel
        channel_idx = np.where(idx == j)

        # Get array related to specific channel
        channel_array = sortedArr[channel_idx]

        # Sort spherical array with respect to the azimuth column (0), thus from -Pi to +Pi
        sorted_channel_array = np.array(channel_array[channel_array[:, 0].argsort()], dtype='f')

        # Divide the high angular resolution (azimuths) into equally spaced segments with lower resoltion
        azimuths = np.linspace(-np.pi, np.pi, 4096)

        # Digitize the sorted array to extract which coordinates fall in which bin
        sorted_channel_array_idx = np.digitize(sorted_channel_array[:, 0], azimuths)


        for k in range(len(sorted_channel_array)):
            # print(f"k is: {k}")
            index = sorted_channel_array_idx[k] - 1
            # print(f"Index is: {index}")
            reduced_index = math.floor(index / 4)
            if (reduced_channel_array[reduced_index] == np.array([0.,0.,0.,0.])).all():
                reduced_channel_array[reduced_index] = sorted_channel_array[k]
            else:
                # TODO --> Compute mean the correct way!
                mean = (sorted_channel_array[k] + reduced_channel_array[reduced_index])/2
                reduced_channel_array[reduced_index] = mean

        reduced_array = np.append(reduced_array, reduced_channel_array, axis=0)


    for i in range(len(reduced_array)):

        x, y, z = sph2cart(reduced_array[i, 0], reduced_array[i, 1], reduced_array[i, 2])

        reduced_array[i] = np.array([x, y, z, reduced_array[i, 3]], dtype='f')

    reduced_array = reduce_pointcloud(reduced_array)

    return reduced_array
