import pygame
import os 
BASE_PATH = 'imagens pygame/'

def cut_image(x, y, width, height , spritesheet):
    sprite = pygame.Surface((width, height))
    sprite.blit(spritesheet, (0, 0), (x, y, width, height))
    sprite.set_colorkey((0, 0, 0)) # Define a cor de transparência
    return sprite
def get_image(name):
    img = pygame.image.load(BASE_PATH + name).convert()
    img.set_colorkey((0,0,0))
    return img

def get_imag_dir(path):
    images = []
    for img in os.listdir(BASE_PATH + path):
        images.append(get_image(path + '/' + img))
    return images   
def get_images(path, spritesheetsize = [128,128], spritesize = [32,32], spritsheetstart = [0,0]):
    
    images = []
    for y in range(spritsheetstart[1],spritesheetsize[1],spritesize[1]):
        for x in range(spritsheetstart[0],spritesheetsize[0],spritesize[0]):
            img_atual = cut_image(x , y, spritesize[0], spritesize[1], get_image(path))
            images.append(img_atual)    
            
    return images        

class Animation():
    def __init__(self, images, ani_dur = 5, loop = True):
        self.images = images
        self.ani_dur = ani_dur
        self.loop = loop
        self.current = 0
        self.done = False
        
    def copy(self):
        return Animation(self.images, self.ani_dur, self.loop)
    def update(self):
        if self.loop:
            self.current = (self.current + 1) % (self.ani_dur*len(self.images))
            
        else:
            self.current = min(self.current + 1, self.ani_dur*len(self.images) - 1)
            if self.current >= self.ani_dur*len(self.images) - 1:
                self.done = True
    def img(self):
        return self.images[int(self.current/self.ani_dur)]
'''# Class map == Class Node()
class map():
    def __init__(self, dados, proxFase= None, antFase = None):
        self.map_data = dados
        self.proxFase = proxFase
        self.antFase = antFase
# Class fases == Class LinkedList()
class fases():
    def __init__(self):
        # self.faseinicial = self.head
        # self.id_retroceder = self.tail
        
        self.faseinicial = None
        self.id_retroceder = None
        
    
    
    def add_map_start(self, dados): 
        new_map = map(dados)
        if self.faseinicial is None:
            self.faseinicial = new_map
            self.id_retroceder = new_map
            return
# Func = add_no_inicio
        new_map.proxFase = self.faseinicial
        self.faseinicial.antFase = new_map
        self.faseinicial = new_map
# Func = add_no_final
    def add_map_end(self, dados):
        new_map = map(dados)
        if self.id_retroceder is None:
            self.faseinicial = new_map
            self.id_retroceder = new_map
            return
        
        current_map = self.id_retroceder
        current_map = current_map.antFase 
        new_map.antFase = current_map
        current_map.proxFase = new_map
        self.id_retroceder = new_map
# Func = add_no_meio
    def add_map_mid(self, dados, data_id):
        new_map = map(dados)
        current_map = self.faseinicial
        while current_map is not None:
            if current_map.map_data == data_id:
                new_map.proxFase = current_map.proxFase
                current_map.proxFase = new_map
                new_map.antFase = current_map
                new_map.proxFase.antFase = new_map
                return
            current_map = current_map.proxFase
            
# Func = get_index
    def get_map(self,data_id):
        count = 0 
        current_map = self.faseinicial
        while current_map.proxFase is not None:
            if current_map.map_data == data_id:
                return count
            
                current_map = current_map.proxFase
            count += 1
        return None

    
# Func = len(ListaEncadeada)
    def qtn_fases(self):
        count = 1
        current_map = self.faseinicial
        while current_map is not self.id_retroceder:
            current_map = current_map.proxFase
            count += 1
        return count
# Func = delete_no_meio
    def delete_map_mid(self, data_id):
        current_map = self.faseinicial
        antFaseious_map = None
        while current_map is not None:
            if current_map.map_data == data_id:
                if antFaseious_map is not None:
                    antFaseious_map.proxFase = current_map.proxFase
                else:
                    self.faseinicial = current_map.proxFase
                return
            antFaseious_map = current_map
            current_map = current_map.proxFase
# Func = delete_no_final
    def delete_map_end(self):
        current_map = self.faseinicial
        antFaseious_map = None
        while current_map.proxFase is not None:
            antFaseious_map = current_map
            current_map = current_map.proxFase
        antFaseious_map.proxFase = None
# Func = delete_no_inicio
    def delete_map_start(self):
        self.faseinicial.proxFase.antFase = None
        self.faseinicial = self.faseinicial.proxFase
        self.faseinicial.antFase = None
# Func = get_data
    def load_map(self, map_id):
        current_map = self.faseinicial
        while current_map is not None:
            if str(current_map.map_data) == map_id:
                return str(current_map.map_data)
            current_map = current_map.proxFase
        return None        
    '''
        