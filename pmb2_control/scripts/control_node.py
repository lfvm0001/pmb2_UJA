#!/usr/bin/env python

import rospy
import smach
import rospkg
import smach_ros
from std_msgs.msg import *
from pmb2_face.srv import talk_service
from pmb2_lab_nav.srv import move_service


class state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done'],
                                 input_keys = ['cont_in'],
                                output_keys = ['cont_out', 'point_out','final_out'])
        
        rospack = rospkg.RosPack()
        self.configPath = rospack.get_path("pmb2_control") + "/config/pointsConfig.txt"

        self.names = {}
        with open(self.configPath) as f:
            for line in f:
                (key, val,name) = line.split()
                self.names[int(key)] = name
                
    
    def execute(self, userdata):
        if userdata.cont_in == (len(self.names)-1):
            userdata.point_out = userdata.cont_in + 1
            userdata.final_out = 1

        else:
            userdata.cont_out = userdata.cont_in + 1
            userdata.point_out = userdata.cont_in
            userdata.final_out = 0
            
        return ('done')


class nav(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error','invalid'],
                                 input_keys = ['point_in'])

        self.move_srv = rospy.ServiceProxy('move_srv', move_service)

    def execute(self, userdata):
        resultMove = self.move_srv("move",userdata.point_in)
        
        if resultMove.move_resp == 0:
            return ('done')
        elif resultMove.move_resp == 1:
            return('error')  
        else:
            return('invalid')


class talk(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','final','error'],
                                 input_keys = ['point_in','final_in'])
        
        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
                
    def execute(self, userdata):
        resultTalk = self.talk_srv("talk", userdata.point_in)
        
        if resultTalk.talk_resp == 0:
            if userdata.final_in == 1:
                resultTalk = self.talk_srv("talk", 0)
                return('final')
            else:
                return ('done')
                
        else:
            return ('error')
        
        
class final(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])
        
        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
        
    def execute(self):
        resultTalk = self.talk_srv("talk", 0)
        
        if resultTalk.talk_resp == 0:
            return ('done')  
        else:
            return ('error')


def control_node():
    rospy.init_node('control_node')
    rospy.loginfo("Starting control Node") 
  
    sm = smach.StateMachine(outcomes = ['succeeded', 'failed'])
    sm.userdata.counter = 0
    sm.userdata.point  = 0
    sm.userdata.final = 0

    with sm:
   
        smach.StateMachine.add('STATE', state(),
                               transitions = {'done':'NAV'},
                                 remapping = {'cont_in':'counter',
                                              'cont_out':'counter',
                                              'point_out':'point',
                                              'final_out':'final'})

        smach.StateMachine.add('NAV', nav(),
                               transitions = {'done':'TALK',
                                              'error':'NAV',
                                              'invalid':'failed'},
                                 remapping = {'point_in':'point'})

        smach.StateMachine.add('TALK', talk(),
                               transitions = {'done':'STATE',
                                              'final':'succeeded',
                                              'error':'failed'},
                                 remapping = {'point_in':'point',
                                              'final_in':'final'})
   

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

