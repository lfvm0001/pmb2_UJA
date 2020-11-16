#!/usr/bin/env python

import os
import glob
import rospy
import pygame
from pathlib import Path
from robot_test.srv import face_action, face_actionResponse

global my_group

SIZE = WIDTH, HEIGHT = 775, 545
FPS = 15
PATH = Path(os.path.dirname(os.path.realpath(__file__))).parent

 
class MySprite(pygame.sprite.Sprite):
    
    def __init__(self, action):
        super(MySprite, self).__init__()

        if action == "idle":
            self.images = [pygame.image.load(img) for img in glob.glob(str(PATH) + '/imgs/robot1*.jpeg')]
        if action == "talk":
            self.images = [pygame.image.load(img) for img in glob.glob(str(PATH) + '/imgs/robot*.jpeg')]
        
        self.index = 0
        self.rect = pygame.Rect(5, 5, 150, 198)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1

def face_response(request):
    
    global my_group
    
    if request.action_req == "talk":
        action = request.action_req
    else:
        action = "idle"
    
    robot = MySprite(action)
    my_group = pygame.sprite.Group(robot)
           
    return face_actionResponse(
        change_face = True,
        action_resp = action 
    )
    

def main ():
    rospy.init_node('face_node')                    
    my_service = rospy.Service('/face_service', face_action, face_response)
    
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
        pygame.init()
        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("My robot")
    
        robot = MySprite("idle")
        my_group = pygame.sprite.Group(robot)
    
        clock = pygame.time.Clock()
        main()
        
    except rospy.ROSInterruptException:
        pass