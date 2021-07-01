#!/usr/bin/env python

import rospy
import rospkg
import actionlib
from pmb2_lab_nav.srv import move_service
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class movePoint_node():

    def __init__(self):
        
        rospy.init_node('movePoint_node')
        rospy.loginfo("Starting movePoint Node") 
        
        rospack = rospkg.RosPack()
        self.configPath = rospack.get_path("pmb2_control") + "/config/pointsConfig.txt"
        
        self.goals = {}
        
        with open(self.configPath) as f:
            for line in f:
                (key, val,name) = line.split()
                self.goals[int(key)] = val
                

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
            
            if req.pose_req <= len(self.goals) and req.pose_req >= 1:
            
                target = self.goals[req.pose_req].split(",")
                
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                
                goal.target_pose.pose.position.x = float(target[0])
                goal.target_pose.pose.position.y = float(target[1])
                goal.target_pose.pose.position.z = float(target[2])
                
                goal.target_pose.pose.orientation.x = float(target[3])
                goal.target_pose.pose.orientation.y = float(target[4])
                goal.target_pose.pose.orientation.z = float(target[5])
                goal.target_pose.pose.orientation.w = float(target[6])
                
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
