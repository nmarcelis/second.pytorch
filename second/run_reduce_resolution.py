from second.pointcloud_utils import reduce_resolution, load_data, save_data
import os

input_resolution = 4096
output_resolution = 1024

# load_data_directory = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_lowered/'
# save_data_directory = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_lowered_low_resolution'

# load_data_directory = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points/data'
# load_data_directory = '/home/niels/data/temp/kitti/training/velodyne'

load_training_data_directory = '/home/niels/data/kitti/training/velodyne'
load_testing_data_directory = '/home/niels/data/kitti/testing/velodyne'

save_training_data_directory = '/home/niels/data/temp/ouster/kitti/train'
save_testing_data_directory = '/home/niels/data/temp/ouster/kitti/testing/velodyne'


# save_data_directory = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_low_res'

i = 1

dir_list = os.listdir(load_training_data_directory)
for filename in dir_list:
    print(f"Reducing file {i} of {len(dir_list)}")
    if filename.endswith(".bin"):

        data = load_data(load_training_data_directory, filename)

        reduced = reduce_resolution(data, input_resolution, output_resolution)

        save_data(save_training_data_directory, filename, reduced)

    i = i + 1


i = 1

dir_list = os.listdir(load_testing_data_directory)
for filename in dir_list:
    print(f"Reducing file {i} of {len(dir_list)}")
    if filename.endswith(".bin"):

        data = load_data(load_testing_data_directory, filename)

        reduced = reduce_resolution(data, input_resolution, output_resolution)

        save_data(save_testing_data_directory, filename, reduced)

    i = i + 1


print(f"Finished reducing the resolution of all data!")


