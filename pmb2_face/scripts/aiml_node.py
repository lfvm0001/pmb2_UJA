#!/usr/bin/env python

import os
import aiml
import rospy 
import rospkg
from std_msgs.msg import String 


class aiml_node():
    
    def __init__(self):
    
        rospy.init_node('aiml_node')
        rospy.loginfo("Starting aiml Node")
        
        rospack = rospkg.RosPack()
        self.aimlPath = rospack.get_path("pmb2_face") + "/aiml"
        
        self.mybot = aiml.Kernel()
        self.load_aiml()
        
        self.resp_pub = rospy.Publisher('tts', String, queue_size=10)
        rospy.Subscriber("stt", String, self.get_resp, queue_size=10)
        
        rospy.spin()
 

    def load_aiml(self):

        os.chdir(self.aimlPath) 

        if os.path.isfile("standard.brn"): 
            self.mybot.bootstrap(brainFile = "standard.brn") 

        else: 
            self.mybot.bootstrap(learnFiles = "startup.xml", commands = "load aiml") 
            self.mybot.saveBrain("standard.brn") 

 
    def get_resp(self, data): 
    
        input = data.data 
        response = self.mybot.respond(input) 
        rospy.loginfo("I heard:: %s",data.data) 
        rospy.loginfo("I spoke:: %s",response) 
        self.resp_pub.publish(response) 


if __name__ == '__main__': 
    try:
        aiml_node()
        
    except rospy.ROSInterruptException:
        pass


