#!/usr/bin/env python

import rospy
import smach
import atexit
import smach_ros
from std_msgs.msg import *
from pmb2_face.srv import talk_service
from pmb2_lab_nav.srv import move_service


class initRobot(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])

    def execute(self):
        
        
        if resultMove.move_resp == 0:
            return ('done')
        elif resultMove.move_resp == 1:
            return('error')  




def exit_handler():
    print("Cerrando aplicacion")
    
def controlSM_node():
    rospy.init_node('controlSM_node')
    rospy.loginfo("Starting controlSM Node") 
  
    sm = smach.StateMachine(outcomes = ['succeeded', 'failed'])
    sm.userdata.counter  = 0

    with sm:
   
        smach.StateMachine.add('STATE1', initRobot(),
                               transitions = {'done':'STATE2',
                                              'error':'STATE1'})

        smach.StateMachine.add('STATE2', initRaspi(),
                               transitions = {'done':'STATE3',
                                              'error':'STATE2')

        smach.StateMachine.add('STATE3', welcome(),
                               transitions = {'done':'STATE4',
                                              'error':'STATE3')  
                                              
        smach.StateMachine.add('STATE4', initPose(),
                               transitions = {'done':'STATE5',
                                              'error':'STATE4')
                                              
        smach.StateMachine.add('STATE5', askUser(),
                               transitions = {'done':'succeeded',
                                              'error':'failed')                                              



    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    
    outcome = sm.execute()
    
    rospy.spin()
    sis.stop()
    
    
if __name__ == '__main__':
    try:
        controlSM_node()
        
    except rospy.ROSInterruptException:
        pass