#!/usr/bin/env python

import time
import boto3
import rospy 
import pygame
import rospkg
from std_msgs.msg import String 

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class text2speech_node():

    def __init__(self):
        rospy.init_node('text2speech_node')
        rospy.loginfo("Starting text2speech Node") 
        
        rospack = rospkg.RosPack()
        self.audioPath = rospack.get_path("pmb2_face") + "/audios/speech.ogg"
        
        self.polly = boto3.client('polly')
       
        self.face_pub = rospy.Publisher('face_action', String, queue_size=10)
        rospy.Subscriber("tts", String, self.get_audio, queue_size=10) 
        
        rospy.spin() 
    
    
    def get_audio(self,data): 
        text = data.data 
       
        response = self.polly.synthesize_speech(Text=text, VoiceId='Lucia', OutputFormat='ogg_vorbis')
        body = response['AudioStream'].read()
        file_name = self.audioPath
    
        with open(file_name, 'wb') as file:
            file.write(body)
            file.close()
            
        pygame.init()
        pygame.mixer.init() 
        pygame.mixer.music.load(file_name)
        
        self.face_pub.publish("talk")
        pygame.mixer.music.play()
                
        time.sleep(0.2)
        while pygame.mixer.music.get_busy():
            pass
        
        pygame.mixer.quit()
        self.face_pub.publish("idle")


if __name__ == '__main__':
    try:
        text2speech_node()
        
    except rospy.ROSInterruptException:
        pass
  



