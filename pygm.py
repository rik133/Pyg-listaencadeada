
import pygame
from pygame.locals import *
import sys 
import random
import os
import math
from scripts.utility import get_image, get_images, get_imag_dir, Animation
from scripts.ent import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.faisca import Faisca

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
            'player/idle' : Animation(get_images('player/idle-sheet1.png', spritesheetsize = [32*12, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 3),
            'player/run' : Animation(get_images('player/run-sheet.png', spritesheetsize = [32*4, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 5),
            'player/jump' : Animation(get_images('player/jump-sheet.png', spritesheetsize = [32*6, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 6),
            'player/roll' : Animation(get_images('player/roll-sheet.png', spritesheetsize = [32*12, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 5),
            'player/walk' : Animation(get_images('player/walk-sheet.png', spritesheetsize = [32*4, 32], spritesize = [32, 32], spritsheetstart= [0, 0]), ani_dur = 5),
            'particle/leaf': Animation(get_imag_dir('particles/leaf'), ani_dur=40, loop=False),
            'portal': get_images('mundo/portal.png', spritesheetsize = [32, 32], spritesize = [32, 32], spritsheetstart= [0, 0]),
            'gun': get_image('gun.png'),
            'projectile': get_image('projectile.png'),
        }
        
        
        self.clouds = Clouds(self.coisas['clouds'], count=16)
        
        
        self.player = Player(self,(50, 50), (16,16))
        self.tilemap = Tilemap(self,tile_size=16)
        


        
        
        
        
        self.level = 0
        
        self.load_level(self.level)
        
        
    def load_level(self, level):
        self.tilemap.load('pygame-listaencadeada/dados/mapas/' + str(level) + '.json')
        
        self.leaf_spawners = []
        self.saidas = []
        
        for tree in self.tilemap.extract([("tree", 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 32, 20))
        for saida in self.tilemap.extract([('portal', 0)], keep=True):
            self.saidas.append(pygame.Rect(saida['pos'][0], saida['pos'][1], 16, 16))
        
        
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.cameramove = [0,0]
        self.dead = 0
        self.transition = -30
        self.player.terminou = False
        
        
    def run(self):
        
        while True:
            self.camera.blit(pygame.transform.scale(self.coisas['bg1'], self.camera.get_size()), (0, 0))
            
            if self.player.terminou == True:
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('pygame-listaencadeada/dados/mapas')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
                
            
            
            
            
            self.cameramove[0] += (self.player.rect().centerx - self.camera.get_width()/2 - self.cameramove[0] )/10
            self.cameramove[1] += (self.player.rect().centery - self.camera.get_height()/2 - self.cameramove[1] )/10
            render_camove = [int(self.cameramove[0]), int(self.cameramove[1])]
            
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.5], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.camera, offset=render_camove)
            self.tilemap.render(self.camera, offset=render_camove)
            if not self.dead:
                self.player.update(self.tilemap, (self.mov[1] - self.mov[0], 0))
                self.player.render(self.camera, offset=render_camove)
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_camove[0], projectile[0][1] - img.get_height() / 2 - render_camove[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(faisca(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(faisca(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
   






            for faisca in self.sparks.copy():
                kill = faisca.update()
                faisca.render(self.camera, offset=render_camove)
                if kill:
                    self.sparks.remove(faisca)
            
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
            
            
game().run()

