import pygame, csv, os, globals, constants, items

#defining tiles for tilemaps
class Tile(pygame.sprite.Sprite):
    def __init__(self, id, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.spritesheet = spritesheet
        self.image = spritesheet.parse_sprite(self.id)
        self.x = x
        self.y = y
        #manually load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def changesprite(self, id):
        self.id = id
        self.image = self.spritesheet.parse_sprite(id)
        
    def draw(self, surface, camera):
        surface.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y)) 
        
class Door(Tile):
    def __init__(self, id, x, y, spritesheet, player):
        Tile.__init__(self, id, x, y, spritesheet)
        
        
    
    
class TileMap():
    def __init__(self, filename, spritesheet, camera, player):
        self.tile_size = constants.TILE_SIZE
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename, player)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey(constants.BLACK)
        self.load_map(camera)
        
    
    def draw_map(self, surface, camera):
        for tile in self.tiles:
            tile.draw(surface, camera)
    
    def load_map(self, camera):
        for tile in self.tiles:
            tile.draw(self.map_surface, camera)
        
    #function to read level data from csv file
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    
    #function loads in the actual tiles and their images
    def load_tiles(self, filename, player):
        tiles = []
        
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for count, tile in enumerate(row):
                #define each tile type and image
                if tile in {49, 50, 51, 52, 64, 65, 66, 67}: #adds doors
                    tiles.append(Door(int(tile), x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile in {70, 71}: #replaces potion placeholders with blank floor
                    tiles.append(Tile(int(tile), x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile in {63}: #places keys
                    tiles.append(Tile(int(tile), x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif int(tile) >= 0:
                    tiles.append(Tile(int(tile), x * self.tile_size, y * self.tile_size, self.spritesheet))
                #move to next tile in row
                x += 1
            #move to next row
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
    
