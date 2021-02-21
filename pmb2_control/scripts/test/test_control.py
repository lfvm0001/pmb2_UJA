#!/usr/bin/env python

import time
import rospy
from std_msgs.msg import *
from pmb2_lab_nav.srv import move_service
from pmb2_face.srv import talk_service


class control_node():
    
    def __init__(self):
        
        rospy.init_node('control_node')
        rospy.wait_for_service('move_srv')
        
        self.pub = rospy.Publisher('face_action', String, queue_size=10)
        
        try:
            self.move_srv = rospy.ServiceProxy('move_srv', move_service)
            self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
            self.loop()
        
        except rospy.ServiceException:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        
    def loop(self):
    
        for i in range(0,6):
            resultMove = self.move_srv("move",i)
            print(resultMove.move_resp)
            
            if resultMove.move_resp == 0:
                self.pub.publish("talk")
                resultTalk = self.talk_srv("talk",i)
                
                if resultTalk.talk_resp == 0:
                    self.pub.publish("idle")
            
            else:
                print("fallo")
        
        print("FINAL DONE")
   
   
if __name__ == '__main__':
    
    try:
        control_node()
        
    except rospy.ROSInterruptException:
        pass
