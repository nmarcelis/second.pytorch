from os1.utils import xyzr_points
from second.pointcloud_utils import save_data, reduce_pointcloud, load_data
from second import config as cfg
from second.pointcloud_publisher import PointCloudPublisher
import numpy as np
import torch.multiprocessing as mp
from time import perf_counter
from torch.multiprocessing import Queue
# importing os module
import os
from itertools import cycle
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
import ros_numpy


class FrameConstruction:
    def __init__(self, pub_pc):
        self.publish = cfg.publish
        self.save = cfg.save
        self.frame_id = None
        self.resolution = cfg.resolution
        self.channels = cfg.channels
        self.frame_length = cfg.frame_length
        self.azimuth_blocks = cfg.azimuth_blocks_per_packet
        self.reduced_data = None
        self.queue = Queue()

        self.array_x = mp.Array('f', np.zeros([self.frame_length], dtype=np.float32))
        self.array_y = mp.Array('f', np.zeros([self.frame_length], dtype=np.float32))
        self.array_z = mp.Array('f', np.zeros([self.frame_length], dtype=np.float32))
        self.array_r = mp.Array('f', np.zeros([self.frame_length], dtype=np.float32))

        self.new_data = mp.Value('b', False)

        self.wait = mp.Value('b', False)

        self.processed_packets = mp.Value('i', 0)

        self.frame_timer = 0

        if cfg.simulate:
            self.pool = cycle(cfg.simulation_list)
        self.pub_pc = pub_pc

    def save_frame(self, data, save_dir=cfg.save_directory):
        if self.save == True:

            # Create file name based on the current frame id
            filename = str(self.frame_id)

            # Save file
            save_data(cfg.save_directory, filename, data)

    def construct_frame(self, packet):
        # Extract relevant data from packet
        data = xyzr_points(packet)          # [frame_id, measurement_id, data]

        # Loop through the azimuth blocks of each packet
        for x in range(self.azimuth_blocks):

            # Extract frame id of measurement
            self.frame_id = data[0][x]

            # Get the process ID of
            # the current process
            pid = os.getpid()


            # Print the process ID of
            # the current process

            # Extract measurement id of data points
            # Measurement_id possible range = [0 : RESOLUTION]
            measurement_id = data[1][x]
            # print(f"Measurement_id: {measurement_id}, Process_id: {pid}")
            self.processed_packets.value = self.processed_packets.value + 1

            # Compute begin and end of block
            begin = int((self.frame_length / self.resolution) * measurement_id)
            end = begin + self.channels

            # If end of frame is not yet reached, store measurement data in frame
            if measurement_id < self.resolution:
                self.array_x[begin:end] = data[2][x][0]
                self.array_y[begin:end] = data[2][x][1]
                self.array_z[begin:end] = data[2][x][2]
                self.array_r[begin:end] = data[2][x][3]

                # print(f"array is: {self.array_r[begin:end]}")

            else:
                print("Strange measurement id found: " + str(measurement_id))

            # Reached the end of the frame
            if measurement_id == self.resolution-1:

                # Reduce Data
                reduced_data = self.reduce_data()

                # Save Frame
                self.save_frame(reduced_data)

                # Publish Frame
                self.publish_frame(reduced_data)

                self.new_data.value = True

                # print(f"Processed packets: {self.processed_packets.value}")

                self.processed_packets.value = 0

    def publish_frame(self, data):
        if self.publish:
            # if data != None:
            frame = np.zeros([len(data[0])], dtype=[
                ('x', np.float32),
                ('y', np.float32),
                ('z', np.float32),
                ('reflectivity', np.uint16)])

            frame['x'] = data[0]
            frame['y'] = data[1]
            frame['z'] = data[2]
            frame['reflectivity'] = data[3]

            msg = ros_numpy.msgify(PointCloud2, frame)

            msg.header.frame_id = cfg.frame_id_detection

            self.pub_pc.publish(msg)
            # pcp = PointCloudPublisher(anonymous=True)

            # pcp.publish_pointcloud(frame)

    def publish_simulated_frame(self, data):
        if self.publish:
            # if data != None:
            frame = np.zeros([len(data[:, 0])], dtype=[
                ('x', np.float32),
                ('y', np.float32),
                ('z', np.float32),
                ('reflectivity', np.uint16)])

            frame['x'] = data[:,0]
            frame['y'] = data[:,1]
            frame['z'] = data[:,2]
            frame['reflectivity'] = data[:,3]

            # Convert frame to pointcloud message for Rviz
            msg = ros_numpy.msgify(PointCloud2, frame)

            # Add header to message
            msg.header.frame_id = cfg.frame_id_detection

            # Publish message
            self.pub_pc.publish(msg)

    def reduce_data(self):                  # 1.5 ms
        # TODO --> Should be adjusted to only remove data if all four elements are zero!!!!

        mask = np.frombuffer(self.array_r.get_obj(), dtype='I') == 0

        array_x = np.frombuffer(self.array_x.get_obj(), dtype='f')[~mask]
        array_y = np.frombuffer(self.array_y.get_obj(), dtype='f')[~mask]
        array_z = np.frombuffer(self.array_z.get_obj(), dtype='f')[~mask]
        array_r = np.frombuffer(self.array_r.get_obj(), dtype='I')[~mask]

        self.reduced_data = np.array([array_x, array_y, array_z, array_r], dtype='f').transpose()
        return self.reduced_data

    def get_reduced_data(self):
        return self.reduced_data

    def new_data_available(self):
        if cfg.simulate:

            if perf_counter() - self.frame_timer > 0.1:
                self.new_data.value = True
                self.frame_timer = perf_counter()
        return self.new_data.value

    def set_new_data_false(self):
        self.new_data.value = False

    def get_wait(self):
        return self.wait.value

    def get_data(self):
        if cfg.simulate:
            filename = next(self.pool)
            if filename.endswith(".bin"):
                data = load_data(cfg.simulation_path, filename)
                self.publish_simulated_frame(data)
                return data
        else:
            return self.reduce_data()

    def debug(self):
        print(f"Array_x: {self.array_x[0:10]}")
        print(f"Array_y: {self.array_y[0:10]}")
        print(f"Array_z: {self.array_z[0:10]}")
        print(f"Array_r: {self.array_r[0:10]}")

