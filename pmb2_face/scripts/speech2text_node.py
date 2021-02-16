#!/usr/bin/env python

import time
import os
import rospy 
import pyaudio
import speech_recognition as sr
from std_msgs.msg import String 

fd = os.open('/dev/null',os.O_WRONLY)
os.dup2(fd,2)

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn


class speech2text_node():

    def __init__(self):
        rospy.init_node('speech2text_node')
        rospy.loginfo("Starting speech2text Node") 
        
        self.text_pub = rospy.Publisher('stt', String,queue_size=10) 
        rospy.Subscriber("conv_req", String, self.get_text, queue_size=10) 

        rospy.spin() 
    
    
    def get_text(self): 
        r = sr.Recognizer() 
 
        with  sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            rospy.loginfo('Hearing...')
            
            audio = r.listen(source,timeout=5, phrase_time_limit=5)
 
            try:
                text = r.recognize_google(audio, language="es-ES")
                self.text_pub.publish(text)
            except:
                self.text_pub.publish("error")


if __name__ == '__main__':
    try:
        speech2text_node()
        
    except rospy.ROSInterruptException:
        pass
  