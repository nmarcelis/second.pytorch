import torch
from second.protos import pipeline_pb2
from google.protobuf import text_format
from second.utils import config_tool
from second.pytorch.train import build_network
import numpy as np


class Network():
    def __init__(self, config_path, ckpt_path):

        self.config = pipeline_pb2.TrainEvalPipelineConfig()
        with open(config_path, "r") as f:
            proto_str = f.read()
            text_format.Merge(proto_str, self.config)
        self.input_cfg = self.config.eval_input_reader
        self.model_cfg = self.config.model.second
        # config_tool.change_detection_range_v2(self.model_cfg, [-10, -10, 10, 10])

        self.ckpt_path = ckpt_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = build_network(self.model_cfg).to(self.device).eval()
        self.net.share_memory()

        self.net.load_state_dict(torch.load(self.ckpt_path))
        self.target_assigner = self.net.target_assigner
        self.voxel_generator = self.net.voxel_generator

        # ------------- Generate Anchors ------------------
        self.grid_size = self.voxel_generator.grid_size
        # print(f"Voxel grid size is: {self.grid_size}")
        self.feature_map_size = self.grid_size[:2] // config_tool.get_downsample_factor(self.model_cfg)
        self.feature_map_size = [*self.feature_map_size, 1][::-1]
        # print(f"Feature map size: {self.feature_map_size}")

        self.anchors = self.target_assigner.generate_anchors(self.feature_map_size)["anchors"]
        self.anchors = torch.tensor(self.anchors, dtype=torch.float32, device=self.device)
        self.anchors = self.anchors.view(1, -1, 7)

        print(f"Anchors: {self.anchors}")

    def inference(self, points, max_voxels):

        # points = np.transpose(points[0:4])

        # print(f"Points shape: {points.shape}")

        result = self.voxel_generator.generate(points, max_voxels=max_voxels)         #90000

        # print(f"result: {result}")


        # add batch idx to coords
        coords = np.pad(result['coordinates'], ((0, 0), (1, 0)), mode='constant', constant_values=0)
        voxels = torch.tensor(result['voxels'], dtype=torch.float32, device=self.device)
        coords = torch.tensor(coords, dtype=torch.int32, device=self.device)
        num_points = torch.tensor(result['num_points_per_voxel'], dtype=torch.int32, device=self.device)

        example = {
            "anchors": self.anchors,
            "voxels": voxels,
            "num_points": num_points,
            "coordinates": coords,
        }

        # print(f"Doing inference!!!!!!!!")

        pred = self.net(example)[0]

        # print("Prediction is: " + str(pred))

        boxes_lidar = pred["box3d_lidar"].detach().cpu().numpy()
        scores = pred["scores"].detach().cpu().numpy()

        return boxes_lidar, scores



        # vis_voxel_size = [0.1, 0.1, 0.1]
        # vis_point_range = [-20, -20, -3, 20, 20, 1]
        #
        # bev_map = simplevis.point_to_vis_bev(points, vis_voxel_size, vis_point_range, max_voxels=max_voxels)
        # bev_map = simplevis.draw_box_in_bev(bev_map, vis_point_range, boxes_lidar, [0, 255, 0], 2)
        #
        # plt.imshow(bev_map)
        # plt.show()
        # print("Finished")

