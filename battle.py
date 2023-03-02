import pygame
import constants
from character import Player
from enemy import Enemy
import math
import random
import weapon
import globals
import button

pygame.init()

#define run speed of game (frame rate)
clock = pygame.time.Clock()

#game_window
bottom_panel = 150
screenwidth = constants.SCREENWIDTH
screenheight = constants.SCREENHEIGHT

screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Encounter')

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 18)
font2 = pygame.font.Font("assets/fonts/AtariClassic.ttf", 24)



#damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
        
    def update(self):
        #move text upwards
        self.rect.y -= 1
        #delete text after timer
        self.counter += 2
        if self.counter > 20:
            self.rect.y += 1
        if self.counter > 60:
            self.kill()
            
class ActionSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    def update(self):
        #delete sprite after timer
        self.counter += 2
        if self.counter > 60:
            self.kill()
        

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#sprite groups
damage_text_group = pygame.sprite.Group()

#load ui images
cursor_img = pygame.image.load("assets/battle/img/Icons/sword.png").convert_alpha()
#buttons
potion_img = scale_img(pygame.image.load("assets/battle/img/Icons/potion.png").convert_alpha(), constants.UI_SCALE)
fireball_img = scale_img(pygame.image.load("assets/battle/img/Icons/fireball.png").convert_alpha(), constants.UI_SCALE)
firewall_img = scale_img(pygame.image.load("assets/battle/img/Icons/fire_wall.png").convert_alpha(), constants.UI_SCALE)
#victory and defeat
victory_img = scale_img(pygame.image.load("assets/battle/img/Icons/victory.png").convert_alpha(), 1)
defeat_img = scale_img(pygame.image.load("assets/battle/img/Icons/defeat.png").convert_alpha(), 1)
restart_img = scale_img(pygame.image.load("assets/battle/img/Icons/restart.png").convert_alpha(), constants.UI_SCALE)


#create text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


        
#create battle UI buttons
heal_button = button.Button(screen, 50, screenheight - bottom_panel + 70, potion_img, 32, 32)
fireball_button = button.Button(screen, 90, screenheight - bottom_panel + 70, fireball_img, 32, 32)
firewall_button = button.Button(screen, 130, screenheight - bottom_panel + 70, firewall_img, 32, 32)
restart_button = button.Button(screen, 320, 160, restart_img, 120, 33)
        
#set number of combatants
def set_fighters(enemy_list):
    globals.total_fighters = len(enemy_list) + 1
    


#fighter classes
class Fighter():
    def __init__(self, x, y, name, hp, max_hp, attack_damage, current_mana, max_mana, xp_value = 1):
        #basic creation of actor for battle screen
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.xp = xp_value
        self.attack_damage = attack_damage
        self.heal_power = 10
        self.current_mana = current_mana
        self.max_mana = max_mana
        self.alive = True
        
        
        #animation control
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        #action 0 = idle, 1 = attack, 2 = hurt, 3 = death
        self.action = 0
        self.animation_list = []
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"assets/battle/img/{self.name}/Idle/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"assets/battle/img/{self.name}/Attack/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f"assets/battle/img/{self.name}/Hurt/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f"assets/battle/img/{self.name}/Death/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def draw(self):
        screen.blit(self.image, self.rect)
        
    def update(self):
        animation_cd = 70
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check for last update
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if current animation has finished and loop
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    
    def idle(self):
        #play idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
            
    def attack(self, target):
        #deal damage to target
        rand = random.randint(-1, 3)
        damage = self.attack_damage + rand
        target.sethealth(target.hp - damage)
        #play target's hurt animation
        target.hurt()
        #check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.death()
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), constants.RED)
        damage_text_group.add(damage_text)
        #play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def fireball(self, target):
        #deal damage to target
        rand = random.randint(-2, 5)
        damage = 10 + rand
        target.sethealth(target.hp - damage)
        #play target's hurt animation
        target.hurt()
        #check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.death()
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), constants.RED)
        damage_text_group.add(damage_text)
        #play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def hurt(self):
        #play hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def death(self):
        #play death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def refresh(self):
        #reset fighter back to fresh
        self.alive = True
        self.hp = self.max_hp
        self.current_mana = self.max_mana
        #reset animations
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
    
    def setmana(self, mana):
        self.current_mana = mana
    
    def sethealth(self, health):
        self.hp = health
        
class StatBar():
    def __init__(self, x, y, stat, maxstat):
        self.x = x
        self.y = y
        self.stat = stat
        self.maxstat = maxstat
    
    def draw(self, stat, color):
        #update with new health
        self.stat = stat
        #calculate health ratio
        ratio = self.stat / self.maxstat
        pygame.draw.rect(screen, constants.WHITE, (self.x, self.y, 150, 12))
        pygame.draw.rect(screen, color, (self.x, self.y + 2, 150 * ratio, 8))
        


    
    
        
    