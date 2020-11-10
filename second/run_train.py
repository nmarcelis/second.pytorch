from second.pytorch import train as tr

# config_path = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/pedestrian.fhd.config'
# config_path_v2 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_full/pipeline.config'
#
#
# model_dir_16_1024 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_16_1024'
# config_path_16_1024 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_16_1024.config'
#
#
# model_dir_16_1024_lite = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_16_1024_lite'
# config_path_16_1024_lite = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/pedestrian.lite_16_1024.config'
#
#
# model_dir_64_1024 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_64_1024'
# config_path_64_1024 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_64_1024.config'
#
#
# model_dir_16_2048 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_16_2048'
# config_path_16_2048 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_16_2048.config'
#
#
# model_dir_64_2048 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_64_2048'
# config_path_64_2048 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_64_2048.config'
#
#
# model_dir_64_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_64_4096'
# config_path_64_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_64_4096.config'
#
#
# model_dir_16_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_16_4096'
# config_path_16_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_16_4096.config'


# model_dir_test = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_test'
# config_path_16_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_16_4096.config'

# config_path_jackal = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/pedestrian_jackal.fhd.config'
# model_dir_jackal = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/Mocap_Data/model_jackal_V1'

config_path_jackal = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/mocap/pedestrian_jackal_V2.fhd.config'
model_dir_jackal = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/Mocap_Data/model_jackal_V2'




if __name__ == '__main__':

    tr.train(config_path=config_path_jackal, model_dir=model_dir_jackal, resume=True)


