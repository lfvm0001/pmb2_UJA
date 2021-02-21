#!/usr/bin/env python

import rospy
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class nav_client():
    
    def __init__(self):
        
        rospy.init_node('send_nav_goal')
    
        result = navClient = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        wait = navClient.wait_for_server(rospy.Duration(5.0))

        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return
        
        rospy.loginfo("Connected to move base server")

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # goal.target_pose.pose.position.x =  3.40
        # goal.target_pose.pose.position.y = -0.28
        # goal.target_pose.pose.position.z =  0.00 

        # goal.target_pose.pose.orientation.x = 0.00
        # goal.target_pose.pose.orientation.y = 0.00 
        # goal.target_pose.pose.orientation.z = 0.97
        # goal.target_pose.pose.orientation.w = 0.22
        
        goal.target_pose.pose.position.x =  0.79
        goal.target_pose.pose.position.y =  1.89
        goal.target_pose.pose.position.z =  0.00 

        goal.target_pose.pose.orientation.x = 0.00
        goal.target_pose.pose.orientation.y = 0.00 
        goal.target_pose.pose.orientation.z = 0.06
        goal.target_pose.pose.orientation.w = 0.99

        navClient.send_goal(goal)
        navClient.wait_for_result()
        
        print(navClient.get_state())

if __name__ == '__main__':
    try:
        nav_client()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished")
