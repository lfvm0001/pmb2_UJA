#!/usr/bin/env python


import rospy, os, sys 
from std_msgs.msg import String 
from sound_play.msg import SoundRequest 
from sound_play.libsoundplay import SoundClient 


rospy.init_node('sound_player', anonymous = True) 
soundhandle = SoundClient() 
voice = 'voice_el_diphone' 
rospy.sleep(0.5) 
soundhandle.stopAll() 


def get_response(data): 
    response = data.data 
    soundhandle.say(response,voice) 
    print("done")

def listener(): 
    rospy.Subscriber("response",String, get_response,queue_size=10) 
    rospy.spin() 
  
if __name__ == '__main__': 
    rospy.loginfo("Starting Sound Player") 
    listener()
  



