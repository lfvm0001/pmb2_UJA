#!/usr/bin/env python

import time
import rospy
import pygame
import rospkg
import actionlib
from std_msgs.msg import String 
from pmb2_face.srv import talk_service


class talk_node():

    def __init__(self):
    
        rospack = rospkg.RosPack()
        self.audiosPath = rospack.get_path("pmb2_face") + "/audios/"
        
        rospy.init_node('talk_node')
        rospy.loginfo("Starting talk Node") 
        
        self.face_pub = rospy.Publisher('face_action', String, queue_size=10)
        rospy.Service('talk_srv', talk_service, self.talk_response) 
        rospy.spin() 


    def talk_response(self,req):
        
        if req.talk_req == "talk":
            if req.pose_req >= 0:
                
                pygame.init()
                pygame.mixer.init()
                
                audio = self.audiosPath + str(req.pose_req) + ".ogg"
                pygame.mixer.music.load(audio)
                self.face_pub.publish("talk")
                pygame.mixer.music.play()
                
                time.sleep(0.2)
                while pygame.mixer.music.get_busy():
                    pass
                    
                pygame.mixer.quit()
                self.face_pub.publish("idle")
                return (0)
                
            else:
                return(2)
                
        else:
            return(2)

    
if __name__ == '__main__':
    try:
        talk_node()
        
    except rospy.ROSInterruptException:
        pass
