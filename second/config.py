#!/usr/bin/env python
import numpy as np
from torch.multiprocessing import Queue
import os


# config_path = "/home/niels/workspaces/second-ws/src/second.pytorch/second/models/model_people/pipeline.config"
# model_dir = "/home/niels/workspaces/second-ws/src/second.pytorch/second/models/model_people"
# ckpt_path = "/home/niels/workspaces/second-ws/src/second.pytorch/second/models/model_people/voxelnet-9285.tckpt"

# config_path = "/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/model/model_people_lowered_v1/pipeline.config"
# model_dir = "/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/model/model_people_lowered_v1"
# ckpt_path = "/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/model/model_people_lowered_v1/voxelnet-30950.tckpt"

config_path = "/home/niels/workspaces/second-ws/src/second.pytorch/second/models/model_people_lowered/pipeline.config"
model_dir = "/home/niels/workspaces/second-ws/src/second.pytorch/second/models/model_people_lowered"
ckpt_path = "/home/niels/workspaces/second-ws/src/second.pytorch/second/models/model_people_lowered/voxelnet-49520.tckpt"


max_voxels = 40000

batch_size = 1

DEBUG = True

simulate = False

save_directory = None

# -----------------------------------------------------------
# ----------------------- Simulation ------------------------
# -----------------------------------------------------------
if simulate == True:

    # Save settings
    save = False

    # Publish settings
    publish = True

    # simulation_path = "/home/niels/data/temp/ouster/Recordings/Slaapkamer_Elst_2"
    # simulation_path = '/home/niels/data/temp/ous/ter/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_lowered'
    # simulation_path = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_low_res_lowered'
    # simulation_path = '/home/niels/data/temp/ouster/kitti/training/velodyne'
    # simulation_path = '/home/niels/data/kitti/training/velodyne'
    # simulation_path = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points/data'
    # simulation_path = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_low_res_lowered'

    # simulation_path = '/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/Churchilllaan_low_res/original'
    simulation_path = '/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/Churchilllaan_high_res/original/'

    # simulation_path = '/home/niels/data/debug'

    simulation_list = os.listdir(simulation_path)

    simulation_list.sort()


# -----------------------------------------------------------
# ------------------------ Real Time ------------------------
# -----------------------------------------------------------

if simulate == False:

    # Save settings
    save = False
    # save_directory = "/home/niels/data/temp/ouster/Recordings/Churchillaan_low_res"


    # Publish settings
    publish = True

    # Multithreading settings
    unprocessed_packets = Queue()
    num_workers = 3

    # Ouster settings
    OS1_IP = '192.168.1.86'
    HOST_IP = '192.168.1.1'


# -----------------------------------------------------------
# ------------------------ Publishing ------------------------
# -----------------------------------------------------------

frame_id_detection = 'map'


# -----------------------------------------------------------
# -------------------------- LiDAR --------------------------
# -----------------------------------------------------------

# The number of azimuth blocks per received packet
azimuth_blocks_per_packet = 16

# The number of channels per packet
channels = 64

# The resolution of the LiDAR
resolution = 1024

# The frame rate (fps) of the LiDAR
frame_rate = 10

# Set the mode of the LiDAR, (resolution and frame rate, for example in format: '1024x10'
lidar_mode = str(resolution) + "x" + str(frame_rate)

# Number of features per point, e.g. [x, y, z, r]
frame_num_features = 4

# Frame length is the number of azimuths (horizontal resolution) * number of channels (vertical resolution)
frame_length = resolution * channels

# Create empty frame array to store future coordinates
frame = np.empty([frame_length, 64, frame_num_features])





