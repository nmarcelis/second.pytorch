import pickle

# file = '/mnt/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/recordings/extracted_bags/bag11/kitti_infos_val.pkl'

# file = '/mnt/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/data/kitti_datasets/kitti_64_4096/kitti/kitti_infos_train.pkl'

# file = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_64_4096/eval_results/step_50000/result.pkl'

file = '/mnt/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/recordings/extracted_bags/bag8/kitti_dbinfos_train.pkl'

if __name__ == '__main__':

    # open a file, where you stored the pickled data
    file = open(file, 'rb')

    # dump information to that file
    data = pickle.load(file)

    # close the file
    file.close()
