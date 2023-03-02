import pygame
#battle conditions/battle runtime variables
current_fighter = 1
action_cd = 0
action_wait = 70
total_fighters = 0
attack = False
heal = False
fireball = False
firewall = False
target = None
#detect mouse click
clicked = False
#game runtime variables
run = True
game_over = 0 #-1 = player loss, 0 = game not over
battle_over = -1 #0 = battle not over, 1 = battle win, 2 = battle loss, -1 = no battle
level = 0
screen_scroll = [0, 0]
start_intro = False
#game sprite lists
item_group = pygame.sprite.Group()
#lock player input
pause = False