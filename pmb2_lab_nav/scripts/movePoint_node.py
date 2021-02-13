#!/usr/bin/env python

import rospy
import actionlib
from pmb2_lab_nav.srv import move_service
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class movePoint_node():

    def __init__(self):
        
        self.goals = [[0.79,1.89,0.00,0.00,0.00,0.06,0.99],[-4.02,2.03,0.00,0.00,0.00,-0.08,0.99],[-4.00,-4.03,0.00,0.00,0.00,-0.06,0.99],
                      [0.22,-4.68,0.00,0.00,0.00,-0.07,0.99],[-1.20,-1.32,0.00,0.00,0.00,-0.07,0.99],[-1.57,2.16,0.00,0.00,0.00,-0.75,0.65]]
        
        rospy.init_node('movePoint_node')
        rospy.loginfo("Starting movePoint Node") 
        
        self.navClient = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        wait = self.navClient.wait_for_server(rospy.Duration(5.0))

        if not wait:
            rospy.loginfo("move_base server not available!")
            rospy.signal_shutdown("move_base server not available!")
            return
        
        rospy.loginfo("Connected to move_base server")
           
        rospy.Service('move_srv', move_service, self.move_response) 
        rospy.spin() 

    def move_response(self,req):
        
        if req.move_req == "move":
            
            if req.pose_req <= 5 and req.pose_req >= 0:
                target = self.goals[req.pose_req]
                
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                
                goal.target_pose.pose.position.x = target[0]
                goal.target_pose.pose.position.y = target[1]
                goal.target_pose.pose.position.z = target[2]
                
                goal.target_pose.pose.orientation.x = target[3]
                goal.target_pose.pose.orientation.y = target[4]
                goal.target_pose.pose.orientation.z = target[5]
                goal.target_pose.pose.orientation.w = target[6]
                
                self.navClient.send_goal(goal)
                self.navClient.wait_for_result()
                
                if self.navClient.get_state() == 3:
                    return (0)
                else:
                    return(1)
                
            else:
                return(2)
        
        else:
            return(2)

    
if __name__ == '__main__': 
    try:
        movePoint_node()
        
    except rospy.ROSInterruptException:
        pass
