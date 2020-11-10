import os
from second.pointcloud_utils import reduce_resolution, load_data, save_data

load_directory = '/home/niels/data/kitti_datasets/kitti_16_1024/kitti/testing/velodyne'

i = 1

dir_list = os.listdir(load_directory)
for filename in dir_list:
    print(f"Reducing file {i} of {len(dir_list)}")
    if filename.endswith(".bin"):

        old_filename = os.path.join(load_directory, filename)
        new_filename = os.path.join(load_directory, os.path.splitext(filename)[0])

        os.rename(old_filename, new_filename)
        print("File renamed!")

        # data = load_data(load_directory, filename)
        #
        # save_data(load_directory, filename, data)

    i = i + 1




