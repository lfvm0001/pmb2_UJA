#!/usr/bin/env python

import time
import rospy
import smach
import rosnode
import smach_ros
from std_msgs.msg import *
from pmb2_face.srv import talk_service
from pmb2_face.srv import listen_service


class init(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])
        
    def execute(self, userdata):
        if (len(rosnode.get_node_names())>1):
            return ('done')
        else:
            return('error')


class welcome(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])

        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
        self.listen_srv = rospy.ServiceProxy('listen_srv', listen_service) 
    
    def execute(self, userdata):
        resultTalk = self.talk_srv("talk", 0)
        if resultTalk.talk_resp == 0:
            resultListen = self.listen_srv("conversation")
            time.sleep(5)
            return ('done')
        else:
            return('error')

class ready(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])
        
        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
        self.listen_srv = rospy.ServiceProxy('listen_srv', listen_service) 
    
    def execute(self, userdata):
        resultTalk = self.talk_srv("talk", 99)
        if resultTalk.talk_resp == 0:
            resultListen = self.listen_srv("listen")
            time.sleep(3)
            if resultListen.listen_resp == "si":
                resultTalk = self.talk_srv("talk", 98)
                if resultTalk.talk_resp == 0:
                    return ('done')
                else:
                    time.sleep(5)
                    return('error')
            else:
                time.sleep(5)
                return('error')
        else:
            time.sleep(5)
            return('error')


class sm2(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])

    def execute(self, userdata):
        return ('done')
    
def controlSM_node():
    rospy.init_node('controlSM_node')
    rospy.loginfo("Starting controlSM Node") 
  
    sm = smach.StateMachine(outcomes = ['succeeded', 'failed'])
    sm.userdata.counter  = 0

    with sm:
   
        smach.StateMachine.add('INIT', init(),
                                transitions = {'done':'WELCOME',
                                               'error':'INIT'})

        smach.StateMachine.add('WELCOME', welcome(),
                                transitions = {'done':'READY',
                                               'error':'WELCOME'})

        smach.StateMachine.add('READY', ready(),
                                transitions = {'done':'SM2',
                                               'error':'READY'})  
                                              
        smach.StateMachine.add('SM2', sm2(),
                               transitions = {'done':'succeeded',
                                              'error':'failed'})                                          


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