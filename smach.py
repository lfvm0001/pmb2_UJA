#!/usr/bin/env python

import rospy
import smach
import smach_ros
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


waypoints = [[0.79,1.89,0.00,0.00,0.00,0.06,0.99],[-4.02,2.03,0.00,0.00,0.00,-0.08,0.99],[-4.00,-4.03,0.00,0.00,0.00,-0.06,0.99]]
  
class test(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])
        
    def execute(self, userdata):
        print("Estado final")                
        return outcome1


def main():
    rospy.init_node('navigate_smach')

    sm = smach.StateMachine(outcomes=['succeeded1', 'failed'])
    
    sm.userdata.sm_counter = 0

    with sm:
        def nav_goal_cb(pose):
        
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "map"
            goal.target.pose.header.stamp = rospy.Time.now()
            
            goal.target_pose.pose.position.x = pose[0]
            goal.target_pose.pose.position.y = pose[1]
            goal.target_pose.pose.position.z = pose[2]
            
            goal.target_pose.pose.orientation.x = pose[3]
            goal.target_pose.pose.orientation.y = pose[4]
            goal.target_pose.pose.orientation.z = pose[5]
            goal.target_pose.pose.orientation.w = pose[6]
            
            return goal
            
             
        smach.StateMachine.add('NAV_GOAL0', smach_ros.SimpleActionState('move_base', MoveBaseAction, goal=nav_goal_cb(waypoints[0])),
                               transitions={'succeeded':'NAV_GOAL1',
                                            'aborted':'failed'})

        smach.StateMachine.add('NAV_GOAL1', smach_ros.SimpleActionState('move_base', MoveBaseAction, goal=nav_goal_cb(waypoints[1])),
                               transitions={'succeeded':'NAV_GOAL2',
                                            'aborted':'failed'})
    
        smach.StateMachine.add('NAV_GOAL2', smach_ros.SimpleActionState('move_base', MoveBaseAction, goal=nav_goal_cb(waypoints[2])),
                               transitions={'succeeded':'TEST',
                                            'aborted':'failed'})   
        
        smach.StateMachine.add('TEST', test(),
                               transitions={'outcome1':'succeeded1')   

    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    
    outcome = sm.execute()
    
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    while not rospy.is_shutdown():
        try:
            main()
        except rospy.ROSInterruptException:
            pass

