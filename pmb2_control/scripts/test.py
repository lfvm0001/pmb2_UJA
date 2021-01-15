#!/usr/bin/env python

import rospy
from pmb2_lab_nav.srv import move_service


class control_node():
    
    def __init__(self):
        
        rospy.init_node('control_node')
        rospy.wait_for_service('move_srv')
        
        try:
            self.move_srv = rospy.ServiceProxy('move_srv', move_service)
            self.loop()
        
        except rospy.ServiceException:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        
    def loop(self):
    
        for i in range(0,6):
            result = self.move_srv("move",i)
            print(result.move_resp)
        
        print("FINAL DONE")
        
        
if __name__ == '__main__':
    try:
        control_node()
        
    except rospy.ROSInterruptException:
        pass
