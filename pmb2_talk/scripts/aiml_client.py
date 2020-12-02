#!/usr/bin/env python

from std_msgs.msg import String 
import rospy 

pub = rospy.Publisher('chatter', String,queue_size=10) 
rospy.init_node('aiml_client') 
r = rospy.Rate(1)  

while not rospy.is_shutdown(): 
   input = raw_input("") 
   pub.publish(input) 
   r.sleep()