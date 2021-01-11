#!/usr/bin/env python

from std_msgs.msg import String 
import rospy 
import aiml
import os


rospy.init_node('chat_server')
mybot = aiml.Kernel()
response_publisher = rospy.Publisher('response',String,queue_size=10)


def load_aiml(xml_file): 
    data_path = rospy.get_param("aiml_path") 
    os.chdir(data_path) 

    if os.path.isfile("standard.brn"): 
        mybot.bootstrap(brainFile = "standard.brn") 

    else: 
        mybot.bootstrap(learnFiles = xml_file, commands = "load aiml") 
        mybot.saveBrain("standard.brn") 

def callback(data): 
    input = data.data 
    response = mybot.respond(input) 
    rospy.loginfo("I heard:: %s",data.data) 
    rospy.loginfo("I spoke:: %s",response) 
    response_publisher.publish(response) 

def listener(): 
    rospy.Subscriber("chatter", String, callback) 
    rospy.spin() 

if __name__ == '__main__': 
    rospy.loginfo("Starting Chat Server") 
    load_aiml('startup.xml') 
    listener() 