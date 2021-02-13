#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import *
from pmb2_face.srv import talk_service
from pmb2_lab_nav.srv import move_service


class nav(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error','invalid'],
                                 input_keys = ['cont_in'])

        self.move_srv = rospy.ServiceProxy('move_srv', move_service)

    def execute(self, userdata):
        resultMove = self.move_srv("move",userdata.cont_in)
        
        if resultMove.move_resp == 0:
            return ('done')
        elif resultMove.move_resp == 1:
            return('error')  
        else:
            return('invalid')


class talk(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error','final'],
                                 input_keys = ['cont_in'],
                                output_keys = ['cont_out'])
        
        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
        self.face_pub = rospy.Publisher('face_action', String, queue_size=10)

    def execute(self, userdata):
        self.face_pub.publish("talk")
        resultTalk = self.talk_srv("talk", userdata.cont_in)
        self.face_pub.publish("idle")
        
        if resultTalk.talk_resp == 0:
            userdata.cont_out = userdata.cont_in + 1
            
            if userdata.cont_in == 5:
                return('final')
            else:
                return ('done')
                
        else:
            userdata.cont_out = userdata.cont_in
            return ('error')


def control_node():
    rospy.init_node('control_node')
    rospy.loginfo("Starting control Node") 
  
    sm = smach.StateMachine(outcomes = ['succeeded', 'failed'])
    sm.userdata.counter  = 0

    with sm:
   
        smach.StateMachine.add('NAV_GOAL', nav(),
                               transitions = {'done':'TALK',
                                              'error':'NAV_GOAL',
                                              'invalid':'failed'},
                                 remapping = {'cont_in':'counter'})

        smach.StateMachine.add('TALK', talk(),
                               transitions = {'done':'NAV_GOAL',
                                              'error':'failed',
                                              'final':'succeeded'},
                                 remapping = {'cont_in':'counter',
                                              'cont_out':'counter'})                                            

    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    
    outcome = sm.execute()
    
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    try:
        control_node()
    except rospy.ROSInterruptException:
        pass

