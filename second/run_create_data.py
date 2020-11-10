from second.create_data import custom_data_prep
from ROS.config.config import root_path_bag9, root_path_bag10

if __name__ == '__main__':
    # kitti_data_prep(root_path=root_path)

    custom_data_prep(train_root_path=root_path_bag9, val_root_path=root_path_bag10)

