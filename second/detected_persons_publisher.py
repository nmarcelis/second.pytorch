import rospy
from second.spencer_tracking_msgs.msg import DetectedPersons, DetectedPerson
from jsk_recognition_msgs.msg import BoundingBox, BoundingBoxArray
from second import config as cfg
from pyquaternion import Quaternion

class DetectedPersonsPublisher():
    # def __init__(self):
        # rospy.init_node('DetectedPersonsPublisher', anonymous=False)
        # self.pub = rospy.Publisher('detected_persons', DetectedPersons, queue_size=10)
        # self.pub_pc = rospy.Publisher()
        # self.rate = rospy.Rate(20)   # 10hz

    def fill_detected_persons_message(self, pub, boxes_lidar, scores):
        detected_persons = BoundingBoxArray()

        print(f"Length data is: {len(boxes_lidar)}")
        if len(boxes_lidar) > 0:

            for i in range(len(boxes_lidar)):
                detected_person = BoundingBox()
                # print(f"Location x: {boxes_lidar[i][0]}, y: {boxes_lidar[i][1]}, z: {boxes_lidar[i][2]}, w: {boxes_lidar[i][3]}, l: {boxes_lidar[i][4]}, h: {boxes_lidar[i][5]}")
                detected_person.pose.position.x = boxes_lidar[i][0]
                detected_person.pose.position.y = boxes_lidar[i][1]
                detected_person.pose.position.z = boxes_lidar[i][2]


                # Add the bounding box dimensions
                detected_person.dimensions.x = boxes_lidar[i][3]
                detected_person.dimensions.y = boxes_lidar[i][4]
                detected_person.dimensions.z = boxes_lidar[i][5]

                # Add the bounding box orientation in Quaternion form
                my_quaternion = Quaternion(axis=[0, 0, 1], angle=boxes_lidar[i][6])
                detected_person.pose.orientation.x = my_quaternion[1]
                detected_person.pose.orientation.y = my_quaternion[2]
                detected_person.pose.orientation.z = my_quaternion[3]
                detected_person.pose.orientation.w = my_quaternion[0]

                # Add the detection confidence
                detected_person.value = scores[i]

                # Add the frame ID to the message
                detected_person.header.frame_id = cfg.frame_id_detection

                # Append detected person in array
                detected_persons.boxes.append(detected_person)

        # print(detected_persons)
        self.publish_detected_persons(pub, detected_persons)

    def publish_detected_persons(self, pub, data):

        data.header.frame_id = cfg.frame_id_detection

        pub.publish(data)

        # print("publishing")

