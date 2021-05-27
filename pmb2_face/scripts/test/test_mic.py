#!/usr/bin/env python

import os
import wave
import rospy 
import pyaudio
import speech_recognition as sr
from std_msgs.msg import String 


class speech2text_node():

    def __init__(self):
        rospy.init_node('speech2text_node')
        rospy.loginfo("Starting speech2text Node") 
        
        rospy.Subscriber("conv_req", String, self.get_text, queue_size=10) 

        rospy.spin() 
    
    
    def get_text(self, data): 
        
        if data.data == "Talk":
            p = pyaudio.PyAudio()

            stream = p.open(rate=16000, format=p.get_format_from_width(2), channels=2, input=True, input_device_index=0)
            rospy.loginfo("Hearing...")

            frames = []

            for i in range(0, int(16000 / 1024 * 5)):
                data = stream.read(1024)
                frames.append(data)
                
            rospy.loginfo("Done hearing...")
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            sound = "audio.wav"
            
            wf = wave.open(sound, 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(p.get_sample_size(p.get_format_from_width(2)))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()
            

if __name__ == '__main__':
    try:
        speech2text_node()
        
    except rospy.ROSInterruptException:
        pass
  