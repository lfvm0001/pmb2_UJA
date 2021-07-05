#!/usr/bin/env python

import os
import wave
import rospy 
import pyaudio
import speech_recognition as sr
from std_msgs.msg import String 
from pmb2_face.srv import listen_service


class speech2text_node():

    def __init__(self):
        
        rospy.init_node('speech2text_node')
        rospy.loginfo("Starting speech2text Node") 
        
        self.text_pub = rospy.Publisher('stt', String,queue_size=10) 
        self.info_pub = rospy.Publisher('info_msgs', String, queue_size=10)
        rospy.Service('listen_srv', listen_service, self.get_text) 
        rospy.spin() 
    
    
    def get_text(self, req): 
        
        r = sr.Recognizer()
        listen = False

        with  sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            rospy.loginfo('Hearing...')

            while (not listen):
                try:
                    self.info_pub.publish("Escuchando") 
                    audio = r.listen(source,timeout=5, phrase_time_limit=5)
                    listen = True
                except:
                    pass

            try:
                text = r.recognize_google(audio, language="es-ES")
                if req.listen_req == "conversation":
                    self.text_pub.publish(text)
                
                rospy.loginfo("Human said: "+text)
                self.info_pub.publish("Has dicho: "+text) 
                return (text)
            except:
                rospy.loginfo("Connection problem")
                return ("error")


if __name__ == '__main__':
    try:
        speech2text_node()
        
    except rospy.ROSInterruptException:
        pass
  