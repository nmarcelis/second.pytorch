import torch.multiprocessing as mp
import numpy as np
import second.config as cfg
import os
import ros_numpy
from sensor_msgs.msg import PointCloud2
from jsk_recognition_msgs.msg import BoundingBox


# frame_length =cfg.frame_length
frame_length =10

frame_id = 4444
save_directory = '/home/niels/data/temp/ouster/Recordings/test'

array_x = mp.Array('f', np.array(range(10), dtype='f'))
array_y = mp.Array('f', np.array(range(10), dtype='f'))
array_z = mp.Array('f', np.array(range(10), dtype='f'))
array_r = mp.Array('I', np.array(range(10), dtype='I'))


# array_x = mp.Array('f', np.ones([frame_length], 'f'))
# array_y = mp.Array('f', np.ones([frame_length], 'f'))
# array_z = mp.Array('f', np.ones([frame_length], 'f'))
# array_r = mp.Array('I', np.ones([frame_length], 'I'))


# Reduce data
mask = np.frombuffer(array_r.get_obj(), dtype='I') == 0

array_x = np.frombuffer(array_x.get_obj(), dtype='f')[~mask]
array_y = np.frombuffer(array_y.get_obj(), dtype='f')[~mask]
array_z = np.frombuffer(array_z.get_obj(), dtype='f')[~mask]
array_r = np.frombuffer(array_r.get_obj(), dtype='I')[~mask]

reduced_data = np.array([array_x, array_y, array_z, array_r], dtype='f').transpose()

# Save data
filename = str(frame_id)

save_path = os.path.join(save_directory, filename)

with open(save_path, 'w') as f:
    reduced_data.tofile(f)

load_path1 = save_path

data_points = np.fromfile(load_path1, dtype=np.float32, count=-1).reshape([-1, 4])



print(np.shape(data_points))

frame = np.zeros([len(reduced_data[:,0])], dtype=[
                ('x', np.float32),
                ('y', np.float32),
                ('z', np.float32),
                ('reflectivity', np.uint16)])
frame['x'] = reduced_data[:,0]
frame['y'] = reduced_data[:,1]
frame['z'] = reduced_data[:,2]
frame['reflectivity'] = reduced_data[:,3]

msg = ros_numpy.msgify(PointCloud2, frame)

print("Finished")
