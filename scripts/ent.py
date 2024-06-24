import pygame
import math
import random
from loadermap import enemystates

from scripts.utility import cut_image, get_imag_dir, get_images, Animation
from scripts.faisca import Faisca
class PhysicsEntity:
    def __init__(self,pygm, entype, pos, size):
        self.game = pygm
        self.type = entype
        self.pos = list(pos)
        self.size = size
        self.vel = [0,0]
        self.colison = {'up':False, 'down':False, 'left':False, 'right':False}
        self.state = ''
        self.anim_offset = (-6,-14)
        self.flip = False
        self.set_state('idle')
        self.ult_mov = [0,0]
        self.terminou = False
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_state(self, action):
        if action != self.state:
            self.state = action
            self.animation = self.game.coisas[self.type +'/'+ self.state].copy()
    def update(self, tilemap ,movement = (0,0)):
        
        self.colison = {'up':False, 'down':False, 'left':False, 'right':False}
        frame_movement = (movement[0] + self.vel[0],movement[1] + self.vel[1])
        
        self.pos[0] += frame_movement[0]
        ent_rect = self.rect()
        for rect in tilemap.phycics_chk_around(self.pos):
            if ent_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    ent_rect.right = rect.left  
                    self.colison['right'] = True
                    
                if frame_movement[0] < 0:
                    ent_rect.left = rect.right
                    self.colison['left'] = True
                self.pos[0] = ent_rect.x
                
                                
        
        self.pos[1] += frame_movement[1]
        
        ent_rect = self.rect()
        for rect in tilemap.phycics_chk_around(self.pos):
            
            if ent_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    ent_rect.bottom = rect.top
                    self.colison['down'] = True
                if frame_movement[1] < 0:
                    ent_rect.top = rect.bottom
                    self.colison['up'] = True
                self.pos[1] = ent_rect.y
            
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
              
        self.ult_mov = movement

        self.vel[1] = min(5,self.vel[1] + 0.1)
        
        
        
        
        if self.colison['down'] or self.colison['up']:
            self.vel[1] = 0
        
        
        self.animation.update()  
    def render(self, surf, offset = (0,0)):
       
        surf.blit(pygame.transform.flip(self.animation.img(),self.flip, False),(self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
            #surf.blit(pygame.transform.scale(sprite,(32,32)),(self.pos[0]-offset[0], self.pos[1]-offset[1]))    


class Player(PhysicsEntity):
    def __init__(self, pygm, pos, size):
        super().__init__(pygm,'player', pos, size)
        self.tp_air = 0
        self.jump = False
        self.jumps = 1
        self.wall_slide = False
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement = movement)
        
        if self.vel[1] <= 0 and self.vel[1] >= -0.1:
            self.tp_air = 0   
            self.jumps = 1
        elif self.vel[1] >= 0.7:
            self.tp_air += 1
        self.wall_slide = False
        if (self.colison['right'] or self.colison['left']) and self.tp_air > 4:
            self.wall_slide = True
            self.vel[1] = min(self.vel[1], 0.5)
            if self.colison['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_state('run')
        
        if not self.wall_slide:
            if self.jump:
                self.set_state('jump')
            elif movement[0] != 0:
                self.set_state('walk')
            else:
                
                self.set_state('idle')
        
        if self.vel[0] > 0:
            self.vel[0] = max(self.vel[0] - 0.1, 0)
        else:
            self.vel[0] = min(self.vel[0] + 0.1, 0)        
    def pulo(self):
        if self.wall_slide:
            if self.flip and self.ult_mov[0] < 0:
                self.vel[0] = 3.5
                self.vel[1] = -2.5
                self.tp_air= 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.ult_mov[0] > 0:
                self.vel[0] = -3.5
                self.vel[1] = -2.5
                self.tp_air = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:
            self.vel[1] = -3
            self.jumps -= 1
            self.tp_air= 5
            return True
        
        
class Enemy(PhysicsEntity):
    def __init__(self,pygm, pos, size):
        super().__init__(pygm,'enemy', pos, size)
        self.life = 100
        self.graph = {
            'idle':{'walk':0.5, 'run':0.2, 'jump':0.3},
            'walk':{'idle':0.5, 'run':0.8, 'jump':0.1},
            'run':{'idle':0.4, 'walk':0.7, 'jump':0.1},
            'jump':{'idle':0.1, 'walk':0.2, 'run':0.7}
        }
        self.state = 'idle'
        self.flip = False
        self.set_state('idle')
        
    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement)
        if self.life <= 0:
            self.terminou = True
        elif self.colison['right'] or self.colison['left']:
            self.state = 'idle'
            self.set_state('idle')
            self.vel[1] = 0
        elif self.colison['up']:
            if self.vel[1] > 0:
                self.state = 'idle'
                self.set_state('idle')
        elif self.colison['down']:
            self.vel[1] = 0
            self.state = 'jump'
            self.set_state('jump')
        else:
            self.vel[1] += 0.1
            if self.state == 'idle':
                if self.vel[0] > 0:
                    self.flip = False
                if self.vel[0] < 0:
                    self.flip = True
            elif self.state == 'run':
                if self.vel[0] > 0:
                    self.flip = False
                if self.vel[0] < 0:
                    self.flip = True
            elif self.state == 'walk':
                if self.vel[0] > 0:
                    self.flip = False
                if self.vel[0] < 0:
                    self.flip = True
            elif self.state == 'jump':
                if self.vel[0] > 0:
                    self.flip = False
                if self.vel[0] < 0:
                    self.flip = True
            self.set_state(self.state)
            
    def set_state(self, state):
        if state != self.state:
            self.state = state
            if state == 'idle':
                self.vel[0] = 0
                self.anim = self.game.enemy_idle
            elif state == 'walk':
                self.vel[0] = 1
                self.anim = self.game.enemy_walk
            elif state == 'run':
                self.vel[0] = 3
                self.anim = self.game.enemy_run
            elif state == 'jump':
                self.vel[0] = -2
                self.anim = self.game.enemy_jump
