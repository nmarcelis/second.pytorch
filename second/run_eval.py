from second.pytorch import train as tr

model_dir_16_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_16_4096'
config_path_16_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_16_4096.config'

model_dir_64_4096 = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/model_people_64_4096'


config_path_jackal = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/Mocap_Data/model_jackal_V1/pipeline.config'
model_dir_jackal = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/models/Mocap_Data/model_jackal_V1'

config_path_jackal_kitti = '/home/niels/workspaces/detection-networks-ws/second-ws/src/second.pytorch/second/configs/people.fhd_lowered_64_4096_jackal.config'



if __name__ == '__main__':

    tr.evaluate(config_path=config_path_jackal, model_dir=model_dir_jackal, measure_time=False, batch_size=1)
