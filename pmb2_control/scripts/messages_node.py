#!/usr/bin/env python

import rospy
import atexit
from tkinter import *
from tkinter import ttk

class GUI():
    def __init__(self):
        self.window = Tk() 
        
    def messages(self, data):
        msg = data.data
        self.autoMsj_text.insert(INSERT, msg)
        self.autoMsj_text.see(END)
     
    def create(self):
        self.window.title("Robot Guía")
        self.window_height = 80
        self.window_width  = 720
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (self.window_width/2))
        y_cordinate = int((screen_height/2) - (self.window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_cordinate, y_cordinate))
        
        #Componentes 
        self.autoMsj_text = Text(self.window, height=3, width=85)
        self.autoMsj_text.grid(row=0, column=0, padx=10, pady=10)
        self.autoMsj_text.insert(INSERT, "Cargando Archivos... \n")
        self.autoMsj_text.see(END)
        
        scroll = Scrollbar(self.window, command=self.autoMsj_text.yview)
        scroll.grid(row=0, column=2, sticky='nsew')
        self.autoMsj_text['yscrollcommand'] = scroll.set
 
class messages_node():

    def __init__(self):
        rospy.init_node('messages_node')
        rospy.loginfo("Starting messages Node") 
        
        msg_app = GUI()
        msg_app.create()
        
        rospy.Subscriber("info_msgs", String, msg_app.messages, queue_size=10) 

        self.window.mainloop()
    

if __name__ == '__main__':
    try:
        messages_node()
        
    except rospy.ROSInterruptException:
        pass
    
    

