import pygame
from pygame.locals import *
import sys 
import random
import os
from scripts.utility import get_image, get_images, get_imag_dir
from scripts.tilemap import Tilemap
from scripts.textsys import Text, DialogNode, DialogTree
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
            'tileset1': get_images('mundo/sheettiles.png', spritesheetsize = [112, 64], spritesize = [16, 16], spritsheetstart= [0, 0]),
            'tileset2': get_images('mundo/tileset2.png', spritesheetsize = [16*3, 160], spritesize = [16, 16], spritsheetstart= [0, 16*3]),
            'tree': get_images('mundo/tileset.png', spritesheetsize = [48, 48], spritesize = [48, 48], spritsheetstart= [0, 0]),
            'portal': get_images('mundo/portal.png', spritesheetsize = [32, 32], spritesize = [32, 32], spritsheetstart= [0, 0]),
            'npc': get_images('player/player2/idel-sheet.png', spritesheetsize = [32*5, 32], spritesize = [32, 32], spritsheetstart= [0, 0]),
            'dialogbox': get_images('mundo/dialogbox.png', spritesheetsize = [96, 32], spritesize = [96, 32], spritsheetstart= [0, 0]),
        }
        self.str = ''
        i = 0
        self.fontsize = 10
        self.fontlist = [os.path.join('', f) for f in os.listdir('pygame-listaencadeada/fonts') if f.endswith('.ttf')]
        self.fontindex = 0
        self.tilemap = Tilemap(self,tile_size=16)
        
        self.text = Text(self.str, (10,10), self.fontsize, game = self)
        self.dialogbox = self.text
        self.dialog_tree = DialogTree(DialogNode(0,self.str))
        self.dialogatual = (self.dialogbox.img, (10,10))
        self.rect = self.text.rect.copy()
        self.level = 0
        self.load_level(self.level)
        self.dialogindex = 0
        self.cameramove = [0,0]
        
        self.tile_list = list(self.coisas)
        self.tile_grupos = 0
        self.tile_index = 0
        
        self.click = False
        self.click_rght = False
        self.shift = False
        self.ongrid = True
        self.edittext = False
    def load_level(self, map_id):
        self.tilemap.load('pygame-listaencadeada/dados/mapas/' + str(map_id) + '.json')
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
            if not self.edittext:    
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
            else:
                
                imag = pygame.transform.scale(self.coisas['dialogbox'][0].copy(), (310, 64))
                imag.set_alpha(200)
                self.dialog_tree.current_node.text = self.str
                self.dialogbox.text = self.str
                self.dialogbox.fontsize = self.fontsize
                self.dialogbox.set_font()
                self.dialogbox.render()
                imag.blit(self.dialogbox.img, (10,10))
                self.dialogatual = (imag, (10,240 - 64))
                self.camera.blit(self.dialogatual[0], self.dialogatual[1])
                
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.edittext:
                         self.click = True      
                         if not self.ongrid:                                     
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_grupos], 'vari': self.tile_index, 'pos':(mpos[0] + self.cameramove[0], mpos[1] + self.cameramove[1])})
                    if event.button == 3 and not self.edittext:
                        self.click_rght = True
                    if self.shift:
                        if event.button in [4, 5] and not self.edittext:
                            self.tile_index = (self.tile_index - 1) % len(self.coisas[self.tile_list[self.tile_grupos]]) if event.button == 4 else (self.tile_index + 1) % len(self.coisas[self.tile_list[self.tile_grupos]])
                            print(self.tile_index)
                    else:   
                        if event.button in [4, 5] and not self.edittext:
                            self.tile_grupos = (self.tile_grupos - 1) % len(self.tile_list) if event.button == 4 else (self.tile_grupos + 1) % len(self.tile_list)
                            self.tile_index = 0
                        
                    if event.button == 1 and self.edittext:
                        self.click = True
                        self.text.pos = mpos
                        self.text.render()
                    if event.button == 3 and self.edittext:
                        self.click_rght = True
                    if self.shift and self.edittext:
                        if event.button == 4:
                            self.fontsize += 1
                            self.text.set_font()
                            self.text.render()
                        if event.button == 5:
                            self.fontsize -= 1
                            self.text.set_font()
                            self.text.render()
                    elif self.edittext:
                        if event.button == 4:
                            self.fontindex = ((self.fontindex-1) % len(self.fontlist)) 
                            self.dialogbox.fontname = self.fontlist[self.fontindex]
                            self.dialogbox.set_font()
                            self.text.fontname = self.fontlist[self.fontindex]
                            self.text.set_font()
                            self.text.render()
                        if event.button == 5:
                            self.fontindex = ((self.fontindex+1) % len(self.fontlist))
                            self.dialogbox.fontname = self.fontlist[self.fontindex]
                            print(self.dialogbox.fontname)
                            self.dialogbox.set_font()
                            self.text.fontname = self.fontlist[self.fontindex]
                            self.text.set_font()
                            self.text.render()
                    
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.click_rght = False
                
                        
                        
                        

                    
                if event.type == pygame.KEYDOWN:
                    if self.edittext:
                            
                            response = self.str
                            if event.key == K_RIGHT:
                                node = DialogNode(len(self.dialog_tree.node_dict), self.str)
                                self.dialog_tree.add_node(node)
                                self.dialog_tree.node_dict[node.id] = node
                            elif event.key == K_UP:
                                self.dialogindex += 1
                                try:   
                                    self.dialog_tree.current_node.text = self.dialog_tree.node_dict[self.dialogindex].text
                                    
                
                                except KeyError:
                                    print(f'IndexError, tente numero abaixo de : {len(self.dialog_tree.node_dict)}')
                                    self.dialogindex = 0
                                print(self.dialog_tree.current_node.text)
                                print(self.dialogindex)
                            
                            elif event.key == K_DOWN:
                                self.dialogindex -= 1
                                try:
                                    self.dialog_tree.current_node.text = self.dialog_tree.node_dict[self.dialogindex].text
                                except KeyError:
                                    print(f'IndexError, tente numero abaixo de : {len(self.dialog_tree.node_dict)}')
                                    self.dialogindex = 0
                                print(self.dialog_tree.current_node.text)
                                print(self.dialogindex)
                                
                            elif event.key == K_LEFT:
                                self.edittext = False
                                break
                            elif event.key == K_SLASH:
                                if self.dialog_tree.current_node.checkfilho(self.dialog_tree):
                                    print("Não é possível adicionar um nó com mesmo pai + de 1 vez.")
                                else:
                                    self.dialog_tree.current_node.add_response(response, self.dialog_tree.node_dict[self.dialogindex])
                                
                            elif event.key == K_BACKSPACE:
                                if len(self.str)>0:
                        
                                    self.str = self.str[:-1]
                            elif event.key == K_LSHIFT:
                                self.shift = True
                                
                            else:
                                self.str += event.unicode
                                self.text.text = self.str
                                self.text.render()
                            img = self.text.img.copy()
                            self.rect.size= img.get_size()
                        
                    else:
                        if event.key == pygame.K_a:
                            self.mov[0] = True
                        if event.key == pygame.K_d:
                            self.mov[1] = True
                        if event.key == pygame.K_w:
                            self.mov[2] = True
                        if event.key == pygame.K_s:
                            self.mov[3] = True
                        if event.key == pygame.K_n:
                            self.edittext = True
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
