#!/usr/bin/env python

import wave
import rospy 
import rospkg
import pyaudio
import speech_recognition as sr
from std_msgs.msg import String 

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class speech2text_node():

    def __init__(self):
        rospy.init_node('speech2text_node')
        rospy.loginfo("Starting speech2text Node") 
        
        rospack = rospkg.RosPack()
        self.audioPath = rospack.get_path("pmb2_face") + "/audios/micRecord.wav"
        
        self.text_pub = rospy.Publisher('stt', String,queue_size=10) 
        rospy.Subscriber("conv_req", String, self.get_text, queue_size=10) 

        rospy.spin() 
    
    
    def get_text(self, data): 
        
        if data.data == "Talk":
            sound = "audio.wav"
            
            r = sr.Recognizer()
            with sr.AudioFile(sound) as source:
                r.adjust_for_ambient_noise(source) 
                print("Converting")
                audio = r.listen(source)
                try:
                    test = r.recognize_google(audio,language="es-ES")
                    print(test)
                except:
                    pass



if __name__ == '__main__':
    try:
        speech2text_node()
        
    except rospy.ROSInterruptException:
        pass
  