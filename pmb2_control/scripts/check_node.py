#!/usr/bin/env python

import os
import rospy
import rosnode


class check_node():
    
    def __init__(self):
        rospy.init_node('check_node')
        rospy.loginfo("Starting check Node")
        
        self.check_nodes()
        
    def check_nodes(self):    
        done = False
        
        while(not done):
            nodes=rosnode.get_node_names()
            if (("/aiml_node" in nodes) and ("/amcl" in nodes) and ("/face_node" in nodes) and ("/map_server" in nodes) and 
            ("/move_base" in nodes) and ("/speech2text_node" in nodes) and ("/talk_node" in nodes) and ("/text2speech_node" in nodes)):
                
                os.system('roslaunch pmb2_control load_nodes.launch')
                done=True
                
            else:
                pass  
    
   
if __name__ == '__main__': 
    try:
        check_node()
        
    except rospy.ROSInterruptException:
        pass
