import pygame, csv, os, constants, json

class Spritesheet:
    def __init__(self, filename):
        #init func for creating a spritesheet (loading multiple images for game out of one file)
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('png', 'json')
        #this is a little bit of json magic so that we don't have to manually define each sprite in the game and
        #can instead load them all at once
        with open(self.meta_data) as file:
            self.data = json.load(file)
        file.close()
        
        
    def scale_img(self, image, scale):
        #helper function for scaling
        w = image.get_width()
        h = image.get_height()
        return pygame.transform.scale(image, (w * scale, h * scale))
        
    def get_sprite(self, x, y, w, h):
        #pulls one sprite out of the sheet
        sprite = pygame.Surface((w , h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite
    
    def parse_sprite(self, id):
        #defines where the sprites are to begin with
        sprite = self.data['frames'][id]['frame']
        x, y, w, h =  sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.scale_img(self.get_sprite(x, y, w, h), constants.TILE_SCALE)
        return image

        