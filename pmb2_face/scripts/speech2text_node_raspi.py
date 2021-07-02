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
        rospy.Service('listen_srv', listen_service, self.get_text) 
        rospy.spin() 
    
    
    def get_text(self, req): 
        
        p = pyaudio.PyAudio()

        stream = p.open(rate=16000, format=p.get_format_from_width(2), channels=1, input=True, input_device_index=0)
        rospy.loginfo("Hearing...")

        frames = []

        for i in range(0, int(16000 / 1024 * 5)):
            dataAudio = stream.read(1024)
            frames.append(dataAudio)
                
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
            
        r = sr.Recognizer()
        with sr.AudioFile(sound) as source:
            r.adjust_for_ambient_noise(source) 
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio,language="es-ES")
                if req.listen_req == "conversation":
                    self.text_pub.publish(text)

                rospy.loginfo("Human said: "+text)
                os.remove(sound)
                return (text)
                    
            except:
                rospy.loginfo("Connection problem")
                return ("error")


if __name__ == '__main__':
    try:
        speech2text_node()
        
    except rospy.ROSInterruptException:
        pass
  