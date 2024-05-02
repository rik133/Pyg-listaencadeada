
import pygame
from pygame.locals import *
import sys 
import random
import os
from scripts.utility import get_image
from scripts.ent import PhysicsEntity

class game():
    def __init__(self):
        pygame.init()
        self.flags = pygame.RESIZABLE 
        self.screen = pygame.display.set_mode((640,480), self.flags)
        self.camera = pygame.Surface((320, 240))
        pygame.display.set_caption('gojo')
        
        
        
        self.coisas = {'player': get_image('player\idel-sheet.png')}
        self.fps = pygame.time.Clock()
        self.mov = [False, False]
        self.player = PhysicsEntity(self, 'player', (50, 50), (50, 50), 0.9)
    def run(self):
        while True:
            self.camera.fill((5, 144, 252))  
            self.player.update((self.mov[1] - self.mov[0], 0))
            self.player.render(self.camera) 
            
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.mov[0] = True
                        print('esquerda')
                    if event.key == K_RIGHT:
                        self.mov[1] = True
                        print('direita')
                    '''if event.key == K_UP:
                        self.mov[2] = True
                        print('cima')
                    if event.key == K_DOWN:
                        self.mov[3] = True
                        print('baixo')'''
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.mov[0] = False
                    if event.key == K_RIGHT:
                        self.mov[1] = False
                    ''' if event.key == K_UP:
                        self.mov[2] = False
                    if event.key == K_DOWN:
                        self.mov[3] = False'''
            self.screen.blit(pygame.transform.scale(self.camera, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.fps.tick(30)
            
'''class tela():
    def __init__(self):
        self.width = 640
        self.height = 480
        
        self.image = pygame.draw.rect(self.screen, (5, 144, 252), (0, 0, 640, 480))

        
   
    def update(self):
        self.screen.fill((5, 144, 252))
        
class player():
    
    def __init__(self):
        self.img_pos = [320, 240]
        self.x = self.img_pos[0]
        self.y = self.img_pos[1]
        self.speed = 0.9
        self.xlr8 = 5
        self.life = 3
        self.image = pygame.image.load('imagens pygame\player\idel.png')
        
        self.img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
        
        
    def move(self, event):
        
        
        
        
        
        keys = pygame.key.get_pressed()
        if self.xlr8 > 10:
            self.xlr8 -= 2
        if keys[K_LEFT] and self.x > 5:
            self.x -= self.speed*self.xlr8
            
            self.xlr8 += 1
            print('esquerda')
        if keys[K_RIGHT] and self.x < 612:
            self.x += self.speed*self.xlr8
            
            self.xlr8 += 1
            print('direita')
        if keys[K_UP] and self.y > 5:
            self.y -= self.speed*self.xlr8
            
            self.xlr8 += 1
            print('cima')
        if keys[K_DOWN] and self.y < 453:
            self.y += self.speed*self.xlr8
            
            self.xlr8 += 1
            print('baixo')
        
    def update(self):
        self.img_pos[0] += (self.mov[1] - self.mov[0]) * 10
        self.img_pos[1] += (self.mov[3] - self.mov[2]) * 10
        
    
        
'''
            
game().run()

