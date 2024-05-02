import pygame

from scripts.utility import cut_image

class PhysicsEntity:
    def __init__(self,pygm, entype, pos, size, speed):
        self.game = pygm
        self.type = entype
        self.pos = list(pos)
        self.size = size
        self.vel = [0,0]
       
       
    def update(self, movement = (0,0)):
        frame_movement = (movement[0] + self.vel[0],movement[1] + self.vel[1])
        self.pos[0] += frame_movement[0]*5
        self.pos[1] += frame_movement[1]*5
        ''' if self.type == 'player':
            self.pos[0] += (movment[1] - movment[0]) * self.speed
            self.pos[1] += (movment[3] - movment[2]) * self.speed
            self.pos[1] += self.gravity
            if movment[4]:
                self.pos[1] -= self.jump
        if self.type == 'enemy':
            self.pos[0] += self.speed
            if self.pos[0] > 640:
                self.pos[0] = 0
            if self.pos[0] < 0:
                self.pos[0] = 640
            self.pos[1] += self.gravity
        if self.type == 'platform':
            pass'''
    def render(self, surf):
        if self.type == 'player':
            spritesheet = self.game.coisas['player']
            sprite = cut_image(0, 0, 32, 32, spritesheet)
            surf.blit(sprite, self.pos)    
