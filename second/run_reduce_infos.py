import pickle

# file = '/home/niels/data/kitti/kitti_infos_val.pkl'
# file = '/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/data/kitti_datasets/kitti_original/kitti/kitti_infos_train.pkl'
# file = '/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/data/result_annos.pkl'
file = '/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/data/high_recall_result_annos.pkl'
# file = '/media/niels/8e0c28e0-5ce1-418a-a2f9-5d6269277d27/data/result_filenames.pkl'

if __name__ == '__main__':

    # open a file, where you stored the pickled data
    file = open(file, 'rb')

    # dump information to that file
    data = pickle.load(file)

    # close the file
    file.close()
