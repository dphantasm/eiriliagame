import pygame
import constants
import math
import random
from character import Player
from camera import *

class Enemy(Player):
    def __init__(self, x, y, mob_animations, char_type, health, mana):
        Player.__init__(self, x, y, mob_animations, char_type, health, mana)
        self.alive = True
        self.stunned = False
        self.can_see_player = True
    
    def update(self, enemy_list):
        #check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
            
            
    def ai(self, player, tiles, camera):
        ai_dx = 0
        ai_dy = 0
        stun_cooldown = 100
        #Line of sight check
        line_of_sight = ((self.rect.x - camera.offset.x, self.rect.y - camera.offset.y), (player.rect.centerx- camera.offset.x, player.rect.centery - camera.offset.y))
        #check if line of sight collides with walls (BROKEN)
        for tile in tiles:
            if tile.id <= 48 or tile.id in {55, 56, 57, 58, 59, 60, 61, 62, 70, 71, 72, 73, 74, 
                                            75, 76, 77, 78, 79, 80, 81, 85, 86, 87, 88, 89,
                                            90, 91, 92, 93, 94}:
                if tile.rect.clipline(line_of_sight):
                    clipped_line = tile.rect.clipline(line_of_sight)
                    if clipped_line:
                        self.can_see_player == False
    
        #check if enemy is close enough to player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx)** 2) + ((self.rect.centery - player.rect.centery)** 2))
        if self.can_see_player == True and dist < constants.AGGRORANGE and dist > constants.ENEMYDISTANCE:
                    if self.rect.centerx > player.rect.centerx:
                        #on the right of the player
                        ai_dx = -constants.ENEMYSPEED
                    if self.rect.centerx < player.rect.centerx:
                        #on the left of the player
                        ai_dx = constants.ENEMYSPEED
                    if self.rect.centery > player.rect.centery:
                        #on the down of the player
                        ai_dy = -constants.ENEMYSPEED 
                    if self.rect.centery < player.rect.centery:  
                        #on the up of the player
                        ai_dy = constants.ENEMYSPEED
                
        #call move method for enemy
        if globals.pause == False and not self.stunned:
            self.move(ai_dx, ai_dy, tiles)

class Imp(Enemy):
    def __init__(self, x, y, mob_animations, char_type, health, mana):
        self.char_type = 1
        self.health = 5
        self.xp_value = 50
        