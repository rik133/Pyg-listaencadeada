import pygame

BASE_PATH = 'imagens pygame/'

def cut_image(x, y, width, height , spritesheet):
    sprite = pygame.Surface((width, height))
    sprite.blit(spritesheet, (0, 0), (x, y, width, height))
    sprite.set_colorkey((0, 0, 0))  # Define a cor de transparência
    return sprite
def get_image(name):
    img = pygame.image.load(BASE_PATH + name).convert()
    img.set_colorkey((0,0,0))
    return img