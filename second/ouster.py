from os1 import OS1
from second import config as cfg
import rospy
from second.inference import Network
from second.frame_construction import FrameConstruction
from second.multi_threading import handler, worker, spawn_workers
from os1.utils import frame_handler
import json
import torch.multiprocessing as mp
from torch.multiprocessing import set_start_method
from second.spencer_tracking_msgs.msg import DetectedPersons
from second.detected_persons_publisher import DetectedPersonsPublisher
from time import perf_counter
from sensor_msgs.msg import PointCloud2
from jsk_recognition_msgs.msg import BoundingBoxArray
from torch.multiprocessing import Queue




if __name__ == '__main__':

    # Multithreading settings
    queue = Queue()

    # # Create network object
    net = Network(cfg.config_path, cfg.ckpt_path)

    rospy.init_node('DetectedPersonsPublisher', anonymous=False)
    pub_detected_persons = rospy.Publisher('detected_persons', BoundingBoxArray, queue_size=10)
    pub_pointcloud = rospy.Publisher('points', PointCloud2, queue_size=10)
    rate = rospy.Rate(20)   # 20hz

    # Create detected persons object
    dpb = DetectedPersonsPublisher()

    # Create frame constructor
    frame_constructor = FrameConstruction(pub_pointcloud)

    if cfg.simulate == False:

        # Create ouster object
        os1 = OS1(cfg.OS1_IP, cfg.HOST_IP, mode=cfg.lidar_mode)

        # Load beam parameters
        beam_intrinsics = json.loads(os1.get_beam_intrinsics())
        beam_alt_angles = beam_intrinsics['beam_altitude_angles']
        beam_az_angles = beam_intrinsics['beam_azimuth_angles']

        # Spawn multiple workers for multi threading
        workers = spawn_workers(cfg.num_workers, worker, cfg.unprocessed_packets, beam_alt_angles, beam_az_angles, frame_constructor)

        # Start ouster
        os1.start()
        print("Starting Ouster")

        # Handle incoming packets
        spawn_workers(1, os1.run_forever, handler)


    while not rospy.is_shutdown():
        try:
            t1_start = perf_counter()



            # os1.handle_request(handler)

            # print(frame_constructor.new_data_available())
            if frame_constructor.new_data_available():

                data = frame_constructor.get_data()

                boxes_lidar, scores = net.inference(data, cfg.max_voxels)

                dpb.fill_detected_persons_message(pub_detected_persons, boxes_lidar, scores)

                frame_constructor.set_new_data_false()

                # Stop the stopwatch / counter
                t1_stop = perf_counter()

                # print(f"Elapsed time during inference in seconds: {t1_stop-t1_start}")

        except KeyboardInterrupt:
            for w in workers:
                w.terminate()

    if rospy.is_shutdown() == False:
        print("Roscore is not running...")
