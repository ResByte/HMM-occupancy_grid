#! /usr/bin/env python
import rospy
from roslib import message
from sensor_msgs.msg import PointCloud2,PointField
import sensor_msgs.point_cloud2 as pc2

def callback(data):
	#print (data.data)
	print "-------------------------------------------"
	height = int(data.height/2)
	width = int(data.width)
	#print (data.header)
	data_out= pc2.read_points(data)
	#cloud = pc2.create_cloud_xyz32(data.header,data.data)
	int_data = next(data_out)	
	#print size(data_out)
	g=[]
	for i in data_out:
		k=i
		if i[0] is None or i[1] is None or i[2] is None:
			pass				
			#print "skipped"
		elif i[3]>0.00:		
		#elif i[0] < 5.00 or i[1]<5.00 or i[2]<5.00 or i[3]<5.00:
			#pass
			#print "skip
			g.append(i)	
	#print len(g),len(g[0])
	print g
	#	print i
	print "--------------------------------------------"
	        
	#rospy.loginfo(rospy.get_caller_id()+ "I heard %s",data.data)

def listener():
        rospy.init_node('pcl_listener',anonymous = True)
        rospy.Subscriber('/camera/depth_registered/points',PointCloud2,callback)
	rospy.spin()

if __name__=='__main__':
        listener()
