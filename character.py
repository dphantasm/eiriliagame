import pygame
import constants, globals
import math
import random
import camera
import items

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

mana_image = scale_img(pygame.image.load("assets/images/items/potion_blue.png"), constants.UI_SCALE)
health_image = scale_img(pygame.image.load("assets/images/items/potion_red.png"), constants.UI_SCALE)

#player class to hold player data
class Player():
    def __init__(self, x, y, mob_animations, char_type, health, mana):
        #basic player definition
        self.char_type = char_type
        self.flip = False
        #setup animation
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        #action 0 = idle, 1 = moving, 2 = moving up, 3 = moving down
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.moving_up = False
        self.moving_down = False
        #character attributes
        self.level = 1
        self.experience = 0
        self.max_health = 20 + (5 * self.level)
        self.health = health
        self.max_mana = 10 + (5 * self.level)
        self.mana = mana
        self.attack_dmg = 5
        self.keys = 0
        self.alive = True
        self.inventory = []
        #control collision bounding
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE - 3, constants.TILE_SIZE - 3)
        self.rect.center = (x + 3, y + 3)  
        self.image = self.animation_list[self.action][self.frame_index]
        self.touchingEnemy = False
        self.last_encounter = pygame.time.get_ticks()
        self.encounter_cd = 31000
        
    def get_hits(self, tiles, camera):
        #checks for tile collision
        hits = []
        for count, tile in enumerate(tiles):
            if tile.id <= 48 or tile.id in {55, 56, 57, 58, 59, 60, 61, 62, 72, 73, 74, 
                                            75, 76, 77, 78, 79, 80, 81, 85, 86, 87, 88, 89,
                                            90, 91, 92, 93, 94}:
                if self.rect.colliderect(tile):
                    hits.append(tile)
            #makes locked doors passable if player has keys
            elif tile.id in {49, 50, 51, 52, 64, 65, 66, 67}:
                touched = 0
                if self.rect.colliderect(tile):
                    if self.keys >= 1 and touched == 0:
                        self.keys -= 1
                        touched = 1
                        #changes door into open floor after passing
                        tile.changesprite(69)
                    else:
                        hits.append(tile)
            #health/mana pickups
            elif tile.id in {70, 71}:
                potion = -1
                if tile.id == 70 and potion != 1:
                    potion = 1 #hp potion
                    #changes potion placeholder into open floor with potion on top
                    tile.changesprite(69)
                    potion_item = items.Item(tile.rect.x - camera.offset.x, tile.rect.y - camera.offset.y, 1, [health_image])
                    globals.item_group.add(potion_item)
                if tile.id == 71 and potion != 0:
                    potion = 0 #mana potion
                    #changes potion placeholder into open floor with potion on top
                    tile.changesprite(69)
                    potion = items.Item(tile.rect.x - camera.offset.x, tile.rect.y - camera.offset.y, 0, [mana_image])
                    globals.item_group.add(potion_item)
                    
                    
            elif tile.id in {63}:
                key_touched = 0
                if self.rect.colliderect(tile) and key_touched == 0:
                    self.keys += 1
                    key_touched = 1
                    tile.changesprite(69)
                
        return hits
        
    def checkCollisionsx(self, tiles, camera):
        collisions = self.get_hits(tiles, camera)
        for tile in collisions:
            if self.running == True and self.flip == True:
                #collided moving right
                positionx = tile.rect.left - self.rect.w
                self.rect.x = positionx
            elif self.running == True and self.flip == False:
                #collided moving left
                positionx = tile.rect.right
                self.rect.x = positionx
                
    def checkCollisionsy(self, tiles, camera):
        collisions = self.get_hits(tiles, camera)
        for tile in collisions:
            if self.moving_down == True:
                #collided moving down
                positiony = tile.rect.top
                self.rect.bottom = positiony
            if self.moving_up == True:
                #collided moving up
                positiony = tile.rect.bottom
                self.rect.top = positiony
        
    def move(self, dx, dy, tiles, camera):
        self.running = False
        self.moving_up = False
        self.moving_down = False
        if dx < 0:
                #moving left
                self.running = True
                self.flip = False
        if dx > 0:
                #moving right
                self.running = True
                self.flip = True
        if dy < 0:
                #moving up
                self.moving_up = True
        if dy > 0:
                #moving down
                self.moving_down = True
            #diagonal speed control
        if dx != 0 and dy != 0:
                dx = dx * (math.sqrt(2)/2)
                dy = dy * (math.sqrt(2)/2)
            #actual movement
        self.rect.x += dx
        self.checkCollisionsx(tiles, camera)
        self.rect.y += dy
        self.checkCollisionsy(tiles, camera)
        #fight cooldown
        self.touchingEnemy = False
        if pygame.time.get_ticks() - self.last_encounter > self.encounter_cd:
            self.touchingEnemy = True
            self.last_encounter = pygame.time.get_ticks()
            self.encounter_cd = 10000
        
        
        #DEFUNCT: check if screen needs to be moved
        #apply logic ONLY IF PLAYER
        '''
        if self.char_type == 0:
            #update scroll based on player posi
            #move camera left & right
            if self.rect.right > (constants.SCREENWIDTH - constants.SCROLL_THRES):
                screen_scroll[0] = (constants.SCREENWIDTH - constants.SCROLL_THRES) - self.rect.right
                self.rect.right = constants.SCREENWIDTH - constants.SCROLL_THRES
            if self.rect.left < constants.SCROLL_THRES:
                screen_scroll[0] = constants.SCROLL_THRES - self.rect.left
                self.rect.left = constants.SCROLL_THRES
            #move camera up & down
            if self.rect.bottom > (constants.SCREENHEIGHT - constants.VERT_SCROLL_THRES):
                screen_scroll[1] = (constants.SCREENHEIGHT - constants.VERT_SCROLL_THRES) - self.rect.bottom
                self.rect.bottom = constants.SCREENHEIGHT - constants.VERT_SCROLL_THRES
            if self.rect.top < constants.VERT_SCROLL_THRES:
                screen_scroll[1] = constants.VERT_SCROLL_THRES - self.rect.top
                self.rect.top = constants.VERT_SCROLL_THRES
        return screen_scroll
        '''         
    
    #control animation 
    def update(self, enemy_list):
        #check for current action
        if self.running == True:
            self.update_action(1) #1 = run
        elif self.moving_up == True:
            self.update_action(2) #2 = move up
        elif self.moving_down == True:
            self.update_action(3) #3 = move down
        else:
            self.update_action(0) #0 = idle
        animation_cd = 70
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check for last update
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        #check for collision with enemy
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive and self.touchingEnemy == False:
                self.touchingEnemy = True
            break
        if self.health < 1:
            self.health = 0
            self.alive = False
                
        
            
    def update_action(self, new_action):
        #check if new action is different
        if new_action != self.action:
            self.action = new_action
            #reset animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def draw(self, camera, surface):
        #self.rect.x -= camera.offset.x
        #self.rect.y -= camera.offset.y
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
        #pygame.draw.rect(surface, constants.GREEN, self.rect, 1)
        
        
    