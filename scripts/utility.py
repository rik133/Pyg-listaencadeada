import pygame
import os 
BASE_PATH = 'pygame-listaencadeada/imagens pygame/'

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

        
