from second.load_pointcloud import load_data
import numpy as np

# velodyne_path = '/home/niels/data/kitti/testing/velodyne/000000.bin'
# velodyne_initial_path = '/home/niels/data/kitti/testing/velodyne_initial/000000.bin'

# velodyne_path = '/home/niels/data/kitti/training/velodyne/000000.bin'
# velodyne_initial_path = '/home/niels/data/kitti/training/velodyne_initial/000000.bin'

# velodyne_path = '/home/niels/data/kitti/training/velodyne_reduced/000006.bin'
velodyne_path = '/home/niels/data/temp/kitti/training/velodyne/000000.bin'

velodyne_path = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points/data/0000000030.bin'

# velodyne_path = '/home/niels/data/temp/ouster/Recordings/2011_09_28/2011_09_28_drive_0053_sync/velodyne_points_lowered/0000000000.bin'


velodyne_data = load_data(velodyne_path)





# polar_array.sort(axis=0)










# velodyne_initial_data = load_data(velodyne_initial_path)
data_z = np.array(velodyne_data[:,2])

data_z_2 = np.sort(data_z)
print("Finished")
