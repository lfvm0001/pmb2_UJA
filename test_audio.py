#!/usr/bin/env python

import os
import rospy
import pygame
import rospkg
import actionlib
from pmb2_face.srv import talk_service


class talk_node():

    def __init__(self):
    
        rospack = rospkg.RosPack()
        self.audiosPath = os.path.join(rospack.get_path("pmb2_face"), "audio")
        
        rospy.init_node('robot_talk')
        
        pygame.init()
        pygame.mixer.init()
        
        rospy.Service('talk_srv', talk_service, self.talk_response) 
        rospy.spin() 


    def talk_response(self,req):
        
        if req.talk_req == "talk":
            if req.pose_req <= 5 and req.pose_req >= 0:
            
                audio = os.path.join(self.audiosPath, req.pose_req, ".mp3")
                pygame.mixer.music.load(audio)
                pygame.mixer.music.play()
    
                while pygame.mixer.music.get_busy():
                    pass  
                return ("Done")
                
            else:
                return("Not valid")
                
        else:
            return("Not valid")

    
if __name__ == '__main__':
    try:
        talk_node()
        
    except rospy.ROSInterruptException:
        pass
