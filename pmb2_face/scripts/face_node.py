#!/usr/bin/env python

import os
import glob
import rospy
import pygame
from pathlib import Path
from std_msgs.msg import *


global my_group

FPS = 20
SIZE = WIDTH, HEIGHT = 795, 415
PATH = Path(os.path.dirname(os.path.realpath(__file__))).parent

 
class MySprite(pygame.sprite.Sprite):
    
    def __init__(self, action):
        
        super(MySprite, self).__init__()

        if action == "idle":
            self.images = [pygame.image.load(img) for img in glob.glob(str(PATH) + '/imgs/robot1*.png')]  
        elif action == "talk":
            self.images = [pygame.image.load(img) for img in glob.glob(str(PATH) + '/imgs/robot*2.png')]
        elif action == "smile":
            self.images = [pygame.image.load(img) for img in glob.glob(str(PATH) + '/imgs/robot3.png')]
        
        self.index = 0
        self.rect = self.images[0].get_rect()
        self.rect.center = (398,208)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1


def face_response(data):
    
    global my_group
    
    if (data.data == "talk") or (data.data == "smile"):
        action = data.data  
    else:
        action = "idle"
    
    robot = MySprite(action)
    my_group = pygame.sprite.Group(robot)
    

def face_node ():
    
    rospy.init_node('face_node')   
    rospy.loginfo("Starting face Node")  
    
    rospy.Subscriber("face_action", String, face_response)
    
    loop = 1
    while loop and not rospy.is_shutdown():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
        my_group.update()
        screen.fill((0,0,0))
        my_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
        
    rospy.spin() 


if __name__ == '__main__':
    
    try:
        pygame.display.init()
        
        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("My robot")
    
        robot = MySprite("idle")
        my_group = pygame.sprite.Group(robot)
    
        clock = pygame.time.Clock()
        face_node()
        
    except rospy.ROSInterruptException:
        pass