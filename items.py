import globals
import constants
import pygame
import camera



class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0: mana pickup, 1: health pickup
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, player):
        #reposition item with screen scroll
        #check for collision with player
        if self.rect.colliderect(player.rect):
            #mana pickup
            if self.item_type == 0:
                player.mana += 5
                if player.mana > player.max_mana:
                    player.mana = player.max_mana
            #health pickup
            elif self.item_type == 1:
                player.health += 5
                if player.health > player.max_health:
                    player.health = player.max_health
            self.kill()
        #handle animation
        animation_cd = 130
        #update image
        self.image = self.animation_list[self.frame_index]
        #check timer for update
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
    def get_keys(self, tiles):
        #checks for keys in level
        pass
        #return keys
    
    def get_potions(self, tiles):
        #checks for potions in level, and what kind
        pass
        #return health pots, mana pots
        
            
    def draw(self, camera, surface):
        surface.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
        
        