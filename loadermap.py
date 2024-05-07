import os
import json
from scripts.utility import map, fases
BASE_PATH = 'pygame-listaencadeada/dados/mapas/'
class loader():
    def __init__(self):
        self.fases = fases()
        self.levelset = []
        for mapas in os.listdir('pygame-listaencadeada/dados/mapas'):
                self.fases.add_map_start(mapas)
                self.levelset.append(mapas)


    def load(self, int):
        f = open(self.levelset[int], 'r')
        map_data = json.load(f)
        f.close()
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    def del_map(self, target, pos):
        if pos == 'start':
            self.fases.delete_map_start()
        elif pos == 'end':
            self.fases.delete_map_end()  
        else:
            self.fases.delete_map_mid(target)
    def add_map(self, dados, data_id, pos):
        if pos == 'start':
            self.fases.add_map_start(dados)
        elif pos == 'end':
            self.fases.add_map_end(dados)
        else:
            self.fases.add_map_mid(dados, data_id)
    def qtn_fases(self):
        return self.fases.qtn_fases()
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
    
    
        