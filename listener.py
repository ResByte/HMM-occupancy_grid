#! /usr/bin/env python
import rospy
from sensor_msgs import PointCloud2

def callback(data):
        rospy.loginfo(rospy.get_caller_id()+ "I heard %s",data.data)

def listener():
        rospy.init_node('pcl_listener',anonymous = True)
        rospy.Subscriber('/camera/depth_registered/points',PointCloud2,callback)

if __name__=='__main__':
        listener()
