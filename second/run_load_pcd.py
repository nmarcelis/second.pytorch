import open3d as o3d
import numpy as np

if __name__ == '__main__':

    pcd = o3d.io.read_point_cloud('/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/data/InLiDa/Sequence1/1469447787647564.pcd')

    data = np.asarray(pcd.points)
    print(pcd)

    print('end')


