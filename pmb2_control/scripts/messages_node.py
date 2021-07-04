#!/usr/bin/env python

import os
import ttk
import rospy
import actionlib
from Tkinter import *
from std_msgs.msg import *
from geometry_msgs.msg import *
from pmb2_face.srv import talk_service
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class GUI():
    def __init__(self):
        self.window = Tk()
        
        rospy.init_node('messages_node')
        rospy.loginfo("Starting messages Node") 
        
        rospy.Subscriber("info_msgs", String, self.messages, queue_size=10) 
        self.navInit = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.talk_srv = rospy.ServiceProxy('talk_srv', talk_service)
        self.create()
   
    def messages(self, data):
        msg = data.data
        self.autoMsj_text.insert(INSERT, msg)
        self.autoMsj_text.see(END)
        self.autoMsj_text.insert(INSERT, "\n")
        self.autoMsj_text.see(END)
    
    def endProgram(self):
        try:
            resultTalk = self.talk_srv("talk", 100)
        except:
            pass
        
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
                
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.position.z = 0
        goal.target_pose.pose.orientation.x = 0
        goal.target_pose.pose.orientation.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 0.99
                
        self.navInit.send_goal(goal)
        self.navInit.wait_for_result()
                
        if self.navInit.get_state() == 3:
            os.system("rosnode kill aiml_node")
            os.system("rosnode kill amcl")
            os.system("rosnode kill check_node")
            os.system("rosnode kill face_node")
            os.system("rosnode kill map_server")
            os.system("rosnode kill controlSM_node")
            os.system("rosnode kill movePoint_node")
            os.system("rosnode kill move_base")
            os.system("rosnode kill speech2text_node")
            os.system("rosnode kill talk_node")
            os.system("rosnode kill text2speech_node ")
            exit()
    
    def create(self):
        self.window.title("Robot Guia")
       
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        self.window_height = 80  
        self.window_width = 157  
        
        self.y_cordinate = int((self.screen_height) - (self.window_height/2))
        self.window.geometry("{}x{}+{}+{}".format(self.screen_width, self.window_height, 0, self.y_cordinate))
        
        #Componentes 
        self.autoMsj_text = Text(self.window, height=3, width=self.window_width-15)
        self.autoMsj_text.grid(row=0, column=0, padx=10, pady=10)
        self.autoMsj_text.insert(INSERT, "ROBOT GUIA \n")
        self.autoMsj_text.see(END)
        
        scroll = Scrollbar(self.window, command=self.autoMsj_text.yview)
        scroll.grid(row=0, column=1, sticky='nsew')
        self.autoMsj_text['yscrollcommand'] = scroll.set
        
        self.exit_buttom = Button(self.window, text ="Salir", command = self.endProgram, width=10)
        self.exit_buttom.grid(row=0, column=2, padx=5, pady=5)
    
    def __enter__(self):
        print("Inicializando programa")
        return self 
  
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cerrando programa")

if __name__ == '__main__':
    with GUI() as mainProgram:
        mainProgram.window.mainloop()





  

