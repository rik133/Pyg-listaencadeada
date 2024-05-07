import json
import pygame

TILES_VIZINHOS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
TILES_C_FISICA = {'tileset'}
AUTOTILE_TYPES = {'tileset'}
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 3,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 4,
    tuple(sorted([(-1, 0), (0, 1)])): 5, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 8,
    tuple(sorted([(-1, 0), (0, -1)])): 11,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 10,
    tuple(sorted([(1, 0), (0, -1)])): 9,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 6,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 7,

}
class Tilemap:
    def __init__(self,game, tile_size = 32):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['vari']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['vari']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches
    def get_tilesaround(self, pos):
        tiles = []
        tile_loc = (int(pos[0]//self.tile_size), int(pos[1]//self.tile_size))
        for offset in TILES_VIZINHOS:
            chkloc = str(tile_loc[0] + offset[0]) +';'+ str(tile_loc[1] + offset[1])
            if chkloc in self.tilemap:
                tiles.append(self.tilemap[chkloc])
        return tiles
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    def phycics_chk_around(self, pos):
        rects = []
        for tile in self.get_tilesaround(pos):
            if tile['type'] in TILES_C_FISICA:
                rects.append(pygame.Rect(tile['pos'][0]*self.tile_size, tile['pos'][1]*self.tile_size, self.tile_size, self.tile_size))
            
        return rects
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['vari'] = AUTOTILE_MAP[neighbors]
    def render(self, surf, offset):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.coisas[tile['type']][tile['vari']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        for x in range(offset[0]//self.tile_size, (offset[0] + surf.get_width())//self.tile_size + 1):
            for y in range(offset[1]//self.tile_size, (offset[1] + surf.get_height())//self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(pygame.transform.scale(self.game.coisas[tile['type']][tile['vari']],(16,16)), (tile['pos'][0]*self.tile_size - offset[0], (tile['pos'][1]*self.tile_size) - offset[1]))
            
        
            
            
            