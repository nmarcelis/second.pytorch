from second.load_pointcloud import load_data
import os
from second.pointcloud_utils import save_data
import csv

# # ------------------------- Modify Labels ---------------------------
#
# load_label_directory = '/home/niels/data/temp/kitti/training/label_2'
# save_label_directory = '/home/niels/data/kitti/training/label_2'
#
# print(f"Started with modifying training labels...")
#
# for filename in os.listdir(load_label_directory):
#     if filename.endswith(".txt"):
#         complete_load_filename = os.path.join(load_label_directory, filename)
#         complete_save_filename = os.path.join(save_label_directory, filename)
#         with open(complete_load_filename, 'r') as f:
#
#             r = csv.reader(f, delimiter=' ')
#             lines = list(r)
#
#             # In camera coordinates frame, Y is equal to Z in Lidar coordinate frame
#             y_coordinate = 12       # Column of y coordinate
#
#             for i in range(len(lines)):
#                 lines[i][y_coordinate] = str(round(float(lines[i][y_coordinate]) - 1.23, 2))      # Minus because in camera frame, Y coordinate is pointing down
#
#             writer = csv.writer(open(complete_save_filename, 'w'), delimiter=' ')
#             writer.writerows(lines)
#
# print(f"Finished with modifying training labels!")





# ------------------------- Modify Training Pointcloud ---------------------------

# load_training_directory = '/home/niels/data/temp/kitti/training/velodyne/'
# save_training_directory = '/home/niels/data/kitti_lowered/training/velodyne/'

# load_training_directory = '/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/Churchilllaan_high_res/original'
# save_training_directory = '/home/niels/data/temp/ouster/Recordings/Churchilllaan_13_09/Churchilllaan_high_res/normalized'


#
# # Normalize reflectivity
# print(f"Started with modifying training pointcloud...")
#
# for filename in os.listdir(load_training_directory):
#     # if filename.endswith(".bin"):
#     complete_load_filename = os.path.join(load_training_directory, filename)
#
#     data = load_data(complete_load_filename)
#
#     data[:, 3] = data[:, 3] / 65535
#
#
#     save_data(save_training_directory, filename, data)
#
# print(f"Finished with modifying training pointcloud!")
#




load_training_directory = '/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/recordings/extracted_bags/bag5/training/velodyne'
save_training_directory = '/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/recordings/extracted_bags/bag5/training/velodyne'


print(f"Started with modifying training pointcloud...")

for filename in os.listdir(load_training_directory):
    if filename.endswith(".bin"):
        complete_load_filename = os.path.join(load_training_directory, filename)

        data = load_data(complete_load_filename)

        data[:, 2] = data[:, 2]  +0.3                       # Plus because in Lidar coordinate, Z is pointing up



        save_data(save_training_directory, filename, data)

print(f"Finished with modifying training pointcloud!")







# # ------------------------- Modify Testing Pointcloud ---------------------------
#
# load_testing_directory = '/home/niels/data/temp/kitti/testing/velodyne/'
# save_testing_directory = '/home/niels/data/kitti_lowered/testing/velodyne/'
#
# print(f"Started with modifying testing pointcloud...")
#
# for filename in os.listdir(load_testing_directory):
#     if filename.endswith(".bin"):
#         complete_load_filename = os.path.join(load_testing_directory, filename)
#
#         data = load_data(complete_load_filename)
#
#         data[:, 2] = data[:, 2] + 1.23
#
#         save_data(save_testing_directory, filename, data)
#
# print(f"Finished with modifying testing pointcloud!")
