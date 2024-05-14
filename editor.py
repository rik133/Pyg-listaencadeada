import pygame
from pygame.locals import *
import sys 
import random
import os
from scripts.utility import get_image, get_images, get_imag_dir
from scripts.tilemap import Tilemap
RENDER_SCALE = 2.0
class editor():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.camera = pygame.Surface((320, 240))
        pygame.display.set_caption('toredi_gojo')
        self.fps = pygame.time.Clock()
        self.mov = [False, False, False, False]
        
        self.coisas = {
            'tileset': get_images('mundo/tileset.png', spritesheetsize = [48, 142], spritesize = [16, 16], spritsheetstart= [0, 16*3]),
            'tileset1': get_images('mundo/sheet1.png', spritesheetsize = [112, 64], spritesize = [16, 16], spritsheetstart= [0, 0]),
            'tileset2': get_images('mundo/tileset1.png', spritesheetsize = [16*3, 160], spritesize = [16, 16], spritsheetstart= [0, 16*3]),
            'tree': get_images('mundo/tileset.png', spritesheetsize = [48, 48], spritesize = [48, 48], spritsheetstart= [0, 0]),
            'portal': get_images('mundo/portal.png', spritesheetsize = [32, 32], spritesize = [32, 32], spritsheetstart= [0, 0])
            
        }
        
        self.tilemap = Tilemap(self,tile_size=16)
        
        
        
        
        self.level = 0
        self.load_level(self.level)
        
        self.cameramove = [0,0]
        
        self.tile_list = list(self.coisas)
        self.tile_grupos = 0
        self.tile_index = 0

        self.click = False
        self.click_rght = False
        self.shift = False
        self.ongrid = True
    def load_level(self, map_id):
        self.tilemap.load('dados/mapas/' + str(map_id) + '.json')
        self.transition = -30
        
    def run(self):
        while True:
            self.camera.fill((0,0,0))
            
            self.cameramove[0] += (self.mov[1] - self.mov[0]) * 2
            self.cameramove[1] += (self.mov[3] - self.mov[2]) * 2
            render_move = (int(self.cameramove[0]), int(self.cameramove[1]))
            
            self.tilemap.render(self.camera, offset=render_move)
            
            
            tile_atual = self.coisas[self.tile_list[self.tile_grupos]] [self.tile_index].copy()
            tile_atual.set_alpha(160)
            
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            
            tile_pos = (int((mpos[0] + self.cameramove[0]) // self.tilemap.tile_size), int((mpos[1] + self.cameramove[1]) // self.tilemap.tile_size))
            
            if self.ongrid:
                self.camera.blit(tile_atual, (tile_pos[0] * self.tilemap.tile_size - self.cameramove[0], tile_pos[1] * self.tilemap.tile_size - self.cameramove[1]))
            else:
                self.camera.blit(tile_atual, mpos)
                
            
            if self.click and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0])+';'+ str(tile_pos[1])] = {'type':self.tile_list[self.tile_grupos], 'vari': self.tile_index, 'pos':tile_pos}
            if self.click_rght:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.coisas[tile['type']][tile['vari']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.cameramove[0], tile['pos'][1] - self.cameramove[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
                    
                    
            
            self.camera.blit(tile_atual, (5,5))
            
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True      
                        if not self.ongrid:                                     
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_grupos], 'vari': self.tile_index, 'pos':(mpos[0] + self.cameramove[0], mpos[1] + self.cameramove[1])})
                    if event.button == 3:
                        self.click_rght = True
                        '''for tile in self.tilemap.offgrid_tiles:
                            if tile['pos'] == (event.pos[0]//32, event.pos[1]//32):
                                self.tilemap.offgrid_tiles.remove(tile)'''
                        
                    if self.shift:
                        
                        if event.button == 4:
                            self.tile_index = (self.tile_index - 1) % len(self.coisas[self.tile_list[self.tile_grupos]])
                        if event.button == 5:
                            self.tile_index = (self.tile_index + 1) % len(self.coisas[self.tile_list[self.tile_grupos]])
                        print(self.tile_index)
                    else:   
                        if event.button == 4:
                            self.tile_grupos = (self.tile_grupos - 1) % len(self.tile_list)
                            self.tile_index = 0
                        if event.button == 5:
                            self.tile_grupos = (self.tile_grupos + 1) % len(self.tile_list)
                            self.tile_index = 0
                
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.click_rght = False
                
                        
                        
                        
                        
                        
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.mov[0] = True
                        if event.key == pygame.K_d:
                            self.mov[1] = True
                        if event.key == pygame.K_w:
                            self.mov[2] = True
                        if event.key == pygame.K_s:
                            self.mov[3] = True
                        if event.key == pygame.K_g:
                            self.ongrid = not self.ongrid
                        if event.key == pygame.K_t:
                            self.tilemap.autotile()
                        if event.key == pygame.K_o:
                            self.tilemap.save('0.json')
                        if event.key == pygame.K_LSHIFT:
                            self.shift = True
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.mov[0] = False
                        if event.key == pygame.K_d:
                            self.mov[1] = False
                        if event.key == pygame.K_w:
                            self.mov[2] = False
                        if event.key == pygame.K_s:
                            self.mov[3] = False
                        if event.key == pygame.K_LSHIFT:
                            self.shift = False
            self.screen.blit(pygame.transform.scale(self.camera, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.fps.tick(60)
        
editor().run()