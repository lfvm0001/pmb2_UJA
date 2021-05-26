#!/usr/bin/env python

import ttk
import rospy
from Tkinter import *
from std_msgs.msg import *

class GUI():
    def __init__(self):
        self.window = Tk()
        
        rospy.init_node('messages_node')
        rospy.loginfo("Starting messages Node") 
        
        rospy.Subscriber("info_msgs", String, self.messages, queue_size=10) 
        self.create()
        
    def messages(self, data):
        msg = data.data
        self.autoMsj_text.insert(INSERT, msg)
        self.autoMsj_text.see(END)
        self.autoMsj_text.insert(INSERT, "\n")
        self.autoMsj_text.see(END)
     
    def create(self):
        self.window.title("Robot Guia")
       
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        self.window_height = 80  
        self.window_width = 157  
        
        self.y_cordinate = int((self.screen_height) - (self.window_height/2))
        self.window.geometry("{}x{}+{}+{}".format(self.screen_width, self.window_height, 0, self.y_cordinate))
        
        #Componentes 
        self.autoMsj_text = Text(self.window, height=3, width=self.window_width)
        self.autoMsj_text.grid(row=0, column=0, padx=10, pady=10)
        self.autoMsj_text.insert(INSERT, "Cargando Archivos... \n")
        self.autoMsj_text.see(END)
        
        scroll = Scrollbar(self.window, command=self.autoMsj_text.yview)
        scroll.grid(row=0, column=2, sticky='nsew')
        self.autoMsj_text['yscrollcommand'] = scroll.set
        
    def __enter__(self):
        print("Inicializando programa")
        return self 
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cerrando programa")

if __name__ == '__main__':
    with GUI() as mainProgram:
        mainProgram.window.mainloop()





  

