import rospy
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
import ros_numpy


class PointCloudPublisher():
    def __init__(self, anonymous):
        rospy.init_node('PointCloudPublisher', anonymous=anonymous)
        self.pub = rospy.Publisher('points', PointCloud2, queue_size=10)
        self.rate = rospy.Rate(20)   # 10hz

    def publish_pointcloud(self, data):

        msg = ros_numpy.msgify(PointCloud2, data)

        msg.header.frame_id = "base_link"

        self.pub.publish(msg)

        # print("publishing")

