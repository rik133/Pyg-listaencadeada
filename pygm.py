
import pygame
from pygame.locals import *
import sys 
import random
import os
import math
from scripts.utility import get_image, get_images, get_imag_dir, Animation
from scripts.ent import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle


class game():
    def __init__(self):
        pygame.init()
        self.flags = pygame.RESIZABLE 
        self.screen = pygame.display.set_mode((1280,720), self.flags)
        self.camera = pygame.Surface((640, 360))
        pygame.display.set_caption('gojo')
        self.fps = pygame.time.Clock()
        self.mov = [False, False, False, False]
        
        self.coisas = {
            'tileset': get_images('mundo/tileset.png', spritesheetsize = [16*3, 160], spritesize = [16, 16], spritsheetstart= [0, 16*3]),
            'tree': get_images('mundo/tileset.png', spritesheetsize = [48, 48], spritesize = [48, 48], spritsheetstart= [0, 0]),
            'bg1': get_image('mundo/background.png'),
            'clouds': get_imag_dir('mundo/clouds'),
            'player/idle' : Animation(get_images('player/FinnSpriteidle.png', spritesheetsize = [32*9, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 10),
            'player/run' : Animation(get_images('player/FinnSpriterun.png', spritesheetsize = [32*6, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 5),
            'player/jump' : Animation(get_images('player/FinnSpritejump.png', spritesheetsize = [32, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 6),
            'player/roll' : Animation(get_images('player/FinnSprite.png', spritesheetsize = [32*2, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 5),
            'player/walk' : Animation(get_images('player/FinnSpriterun.png', spritesheetsize = [32*6, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 5),
            'particle/leaf': Animation(get_imag_dir('particles/leaf'), ani_dur=20, loop=False),
            'portal': get_images('mundo/portal.png', spritesheetsize = [32, 32], spritesize = [32, 32], spritsheetstart= [0, 0]),
        }
        
        
        self.clouds = Clouds(self.coisas['clouds'], count=16)
        
        
        self.player = Player(self,(50, 50), (20,14))
        self.tilemap = Tilemap(self,tile_size=16)
       


        
        
        self.leaf_spawners = []
        self.saidas = []
        for tree in self.tilemap.extract([('tree', 1)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        for saida in self.tilemap.extract([('portal', 10)], keep=True):
            self.saidas.append(pygame.Rect(saida['pos'][0], saida['pos'][1], 16, 16))
        self.particles = []
        
        self.level = 0
        
        self.load_level(self.level)
        self.cameramove = [0,0]
        
    def load_level(self, level):
        
        self.tilemap.load('dados/mapas/' + str(level) + '.json')
        self.transition = -30
        self.player.terminou = False
        
        
    def run(self):
        while True:
            self.camera.blit(pygame.transform.scale(self.coisas['bg1'], self.camera.get_size()), (0, 0))
            
            if self.player.terminou == True:
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('dados\mapas')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
                
            
            
            
            
            self.cameramove[0] += (self.player.rect().centerx - self.camera.get_width()/2 - self.cameramove[0] )/10
            self.cameramove[1] += (self.player.rect().centery - self.camera.get_height()/2 - self.cameramove[1] )/10
            render_camove = [int(self.cameramove[0]), int(self.cameramove[1])]
            
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.camera, offset=render_camove)
            self.tilemap.render(self.camera, offset=render_camove)
            
            
            self.player.update(self.tilemap, (self.mov[1] - self.mov[0], 0))
            self.player.render(self.camera, offset=render_camove)
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.camera, offset=render_camove)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        self.mov[0] = True
                        print('esquerda')
                    if event.key == K_d:
                        self.mov[1] = True
                        print('direita')
                    if event.key == K_w:
                        self.player.pulo()
                    
                         
                        
                    if event.key == K_DOWN:
                       
                        self.player.terminou = True
                        
                if event.type == KEYUP:
                    
                    if event.key == K_a:
                        self.mov[0] = False
                    if event.key == K_d:
                        self.mov[1] = False
            if self.transition:
                transition_surf = pygame.Surface(self.camera.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.camera.get_width() // 2, self.camera.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.camera.blit(transition_surf, (0, 0))
             
            self.screen.blit(pygame.transform.scale(self.camera, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.fps.tick(60)
            
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

