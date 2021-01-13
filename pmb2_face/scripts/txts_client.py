#!/usr/bin/env python

from std_msgs.msg import String 
import rospy 


pub = rospy.Publisher('chatter', String,queue_size=10) 
rospy.init_node('txts_client') 
r = rospy.Rate(1)  


def listener(): 
    input = raw_input("") 
    pub.publish(input) 
    r.sleep()
    
if __name__ == '__main__': 
    rospy.loginfo("Starting Txts Client")   
    while not rospy.is_shutdown(): 
        listener()  
   

