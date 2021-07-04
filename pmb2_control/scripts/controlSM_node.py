#!/usr/bin/env python

import os
import time
import rospy
import smach
import rospkg
import rosnode
import smach_ros
import actionlib
from std_msgs.msg import *
from geometry_msgs.msg import *
from pmb2_face.srv import talk_service
from pmb2_face.srv import listen_service
from pmb2_lab_nav.srv import move_service
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class state(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'],
                                 input_keys = ['cont_in','names_in'],
                                output_keys = ['point_out','final_out','cont_out','names_out'])

        self.tts_pub = rospy.Publisher('tts', String, queue_size=10) 
        self.listen_srv = rospy.ServiceProxy('listen_srv', listen_service) 
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10)        
    
    def execute(self, userdata):
        if len(userdata.names_in) == 1:
            userdata.point_out = int(list(userdata.names_in)[0])
            userdata.final_out = 1

        else:
            if userdata.cont_in == 0:
                response="Vamos al primer punto"
                self.info_pub.publish(response) 
                self.tts_pub.publish(response) 

                userdata.point_out = int(list(userdata.names_in)[0])
                userdata.cont_out = 1
                
                del userdata.names_in[list(userdata.names_in)[0]]
            
            else:
                response="Deseas ir a ver "+ userdata.names_in[list(userdata.names_in)[0]] + " o " +userdata.names_in[list(userdata.names_in)[1]]
                self.info_pub.publish(response) 
                self.tts_pub.publish(response) 
                time.sleep(3)
                
                resultListen = self.listen_srv("listen")
                
                if resultListen.listen_resp.lower() == userdata.names_in[list(userdata.names_in)[1]].lower():
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
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10) 

    def execute(self, userdata):
        self.info_pub.publish("Iniciando trayectoria hacia el punto indicado...")
        resultMove = self.move_srv("move",userdata.point_in)
 
        
        if resultMove.move_resp == 0:
            self.info_pub.publish("Robot en posicion") 
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
        self.face_pub = rospy.Publisher('face_action', String, queue_size=10)
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10) 
        self.navInit = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def execute(self, userdata):
        resultTalk = self.talk_srv("talk", userdata.point_in)
        
        if resultTalk.talk_resp == 0:
            if userdata.final_in == 1:
                self.info_pub.publish("Gracias por tu atencion") 
                resultTalk = self.talk_srv("talk", 100)
                
                if resultTalk.talk_resp == 0:
                    self.face_pub.publish("smile")
                    time.sleep(2)
                    self.face_pub.publish("idle")
                
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                
                goal.target_pose.pose.position.x = 0
                goal.target_pose.pose.position.y = 0
                goal.target_pose.pose.position.z = 0
                goal.target_pose.pose.orientation.x = 0
                goal.target_pose.pose.orientation.y = 0
                goal.target_pose.pose.orientation.z = 0
                goal.target_pose.pose.orientation.w = 0.99
                
                self.navInit.send_goal(goal)
                self.navInit.wait_for_result()
                
                if self.navInit.get_state() == 3:
                    return('final')
                else:
                    return('error')
            else:
                return ('done')
        else:
            return ('error')

    
class init(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])
        
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10)
        self.pose_pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
        self.navInit = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        
    def execute(self, userdata):
        self.info_pub.publish("Inicializando...") 
        
        start_pose = PoseWithCovarianceStamped()
        start_pose.header.frame_id = "map"
        start_pose.header.stamp = rospy.Time.now()
        start_pose.pose.pose.position.x = 0.0
        start_pose.pose.pose.position.y = 0.0
        start_pose.pose.pose.position.z = 0.0

        start_pose.pose.pose.orientation.x = 0.0
        start_pose.pose.pose.orientation.y = 0.0
        start_pose.pose.pose.orientation.z = 0.0
        start_pose.pose.pose.orientation.w = 0.99
        
        try:
            self.pose_pub.publish(start_pose)
            self.rotate()
            return ('done')
            
        except:
            return ('error')   

    def rotate(self):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
                
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.position.z = 0
        goal.target_pose.pose.orientation.x = 0
        goal.target_pose.pose.orientation.y = 0
        goal.target_pose.pose.orientation.z = -0.99
        goal.target_pose.pose.orientation.w = 0.12
                
        self.navInit.send_goal(goal)
        self.navInit.wait_for_result()
                
        if self.navInit.get_state() == 3:
            goal.target_pose.pose.orientation.z = -0.79
            goal.target_pose.pose.orientation.w = 0.61  

            self.navInit.send_goal(goal)
            self.navInit.wait_for_result()                
        
            if self.navInit.get_state() == 3:
                goal.target_pose.pose.orientation.z = 0.0
                goal.target_pose.pose.orientation.w = 0.99  

                self.navInit.send_goal(goal)
                self.navInit.wait_for_result()    
   

class welcome(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['done','error'])

        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
        self.listen_srv = rospy.ServiceProxy('listen_srv', listen_service) 
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10)
    
    def execute(self, userdata):
        self.info_pub.publish("Bienvenido") 
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
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10)
    
    def execute(self, userdata):
        self.info_pub.publish("Estas listo para iniciar...") 
        resultTalk = self.talk_srv("talk", 99)
        if resultTalk.talk_resp == 0:
            resultListen = self.listen_srv("listen")
            time.sleep(2)
            if "si" in resultListen.listen_resp.lower():
                resultTalk = self.talk_srv("talk", 98)
                if resultTalk.talk_resp == 0:
                    return ('done')
                else:
                    return('error')
            else:
                time.sleep(3)
                return('error')
        else:
            time.sleep(3)
            return('error')

  
def controlSM_node():
    rospy.init_node('controlSM_node')
    rospy.loginfo("Starting controlSM Node") 
  
    sm_top = smach.StateMachine(outcomes = ['final_succeeded', 'final_failed'])
    sm_top.userdata.counter  = 0

    with sm_top:
   
        smach.StateMachine.add('INIT', init(),
                                transitions = {'done':'WELCOME',
                                               'error':'INIT'})

        smach.StateMachine.add('WELCOME', welcome(),
                                transitions = {'done':'READY',
                                               'error':'WELCOME'})

        smach.StateMachine.add('READY', ready(),
                                transitions = {'done':'SUB',
                                               'error':'READY'})  
                                               
    
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
    
        smach.StateMachine.add('SUB', sm,
                                 transitions={'succeeded':'final_succeeded',
                                              'failed':'final_failed'})                                              
   
    outcome = sm_top.execute()
    os.system("rosnode kill aiml_node")
    os.system("rosnode kill amcl")
    os.system("rosnode kill check_node")
    os.system("rosnode kill face_node")
    os.system("rosnode kill map_server")
    os.system("rosnode kill messages_node")
    os.system("rosnode kill movePoint_node")
    os.system("rosnode kill move_base")
    os.system("rosnode kill speech2text_node")
    os.system("rosnode kill talk_node")
    os.system("rosnode kill text2speech_node ")
    time.sleep(2)
    exit()
    
if __name__ == '__main__':
    try:
        controlSM_node()
        
    except rospy.ROSInterruptException:
        pass