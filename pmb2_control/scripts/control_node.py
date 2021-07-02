#!/usr/bin/env python

import time
import rospy
import smach
import rospkg
import smach_ros
from std_msgs.msg import *
from pmb2_face.srv import talk_service
from pmb2_face.srv import listen_service
from pmb2_lab_nav.srv import move_service


class state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'],
                                 input_keys = ['cont_in','names_in'],
                                output_keys = ['point_out','final_out','cont_out','names_out'])

        self.tts_pub = rospy.Publisher('tts', String, queue_size=10) 
        self.listen_srv = rospy.ServiceProxy('listen_srv', listen_service)        
    
    def execute(self, userdata):
        if len(userdata.names_in) == 1:
            userdata.point_out = int(list(userdata.names_in)[0])
            userdata.final_out = 1

        else:
            if userdata.cont_in == 0:
                response="Primer punto"
                self.tts_pub.publish(response) 


                userdata.point_out = int(list(userdata.names_in)[0])
                userdata.cont_out = 1
                
                del userdata.names_in[list(userdata.names_in)[0]]
            
            else:
                self.tts_pub.publish(" ")
                response="Deseas ir a "+ userdata.names_in[list(userdata.names_in)[0]] + " o a " +userdata.names_in[list(userdata.names_in)[1]]
                self.tts_pub.publish(response) 
                time.sleep(3)
                
                resultListen = self.listen_srv("listen")
                
                if resultListen.listen_resp == userdata.names_in[list(userdata.names_in)[1]]:
                    userdata.point_out = int(list(userdata.names_in)[1])
                    del userdata.names_in[list(userdata.names_in)[1]]
                else:
                    userdata.point_out = int(list(userdata.names_in)[0])
                    del userdata.names_in[list(userdata.names_in)[0]]                
                    
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
                resultTalk = self.talk_srv("talk", 100)
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
    
    rospack = rospkg.RosPack()
    configPath = rospack.get_path("pmb2_control") + "/config/pointsConfig.txt"

    sm = smach.StateMachine(outcomes = ['succeeded', 'failed'])
    sm.userdata.point  = 0
    sm.userdata.final = 0
    sm.userdata.cont = 0
    
    sm.userdata.names = {}
    with open(configPath) as f:
        for line in f:
            (key, val,name) = line.split()
            sm.userdata.names[int(key)] = name

    with sm:
   
        smach.StateMachine.add('STATE', state(),
                               transitions = {'done':'NAV',
                                              'error':'STATE'},
                                 remapping = {'cont_in':'cont',
                                              'names_in':'names',
                                              'point_out':'point',
                                              'final_out':'final',
                                              'cont_out':'cont',
                                              'names_out':'names'})

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

