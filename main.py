import pygame
import csv
import constants
from character import Player
from enemy import Enemy
import battle
from tiles import *
from spritesheet import Spritesheet
from items import Item
from camera import *
import globals
from inventory import InventoryMenu

pygame.init()

screen = pygame.display.set_mode((constants.SCREENWIDTH, constants.SCREENHEIGHT))
pygame.display.set_caption("Eirilia")

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 18)
font2 = pygame.font.Font("assets/fonts/AtariClassic.ttf", 24)

#define run speed of game (frame rate)
clock = pygame.time.Clock()

#define player movement
moving_up = False
moving_left = False
moving_down = False
moving_right = False
speed = 6

#scale sprite assist function
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#draw text method
class DrawText():
    def __init__(self, text, font, text_color, x, y):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))
    def update_text(self, player):
        if (player.encounter_cd) <= 36000 and player.encounter_cd > 0:
            encounter_color = constants.RED
            encounter_label = 'DANGER: !!!'
            img = self.font.render(encounter_label, True, encounter_color)
            screen.blit(img, (self.x, self.y))
    

"""    
#Draw grid method
def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREENHEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREENWIDTH, x * constants.TILE_SIZE))
"""


    

#define character types
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

#load character sprites
animation_types = ["idle", "run", "run_up", "run_down"]
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        #reset temp list
        temp_list = []
        for i in range(4):
            img = scale_img(pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha(), constants.CHARACTER_SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)
    
#load item sprites
mana_image = scale_img(pygame.image.load("assets/images/items/potion_blue.png").convert_alpha(), constants.UI_SCALE)
health_image = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.UI_SCALE)


#load tilemap images
tile_list = []
dungeon_sheet = Spritesheet('assets/Dungeon_BW_TP.png')
for x in range(constants.TILE_COLS):
    for y in range(constants.TILE_ROWS):
        tile_image = dungeon_sheet.parse_sprite(int(x))
        tile_list.append(tile_image)

#battle class
class Battle():
    def __init__(self):
        self.battle_running = 0 #0 = not running, 1 = running
        
    def calculate_xp(self, enemy_list):
        xp_total = 0
        for enemy in enemy_list:
            xp_total += enemy.xp
        return xp_total
        
    def report_player_health(self, player):
        hp = player.hp
        return hp
        
    def report_player_mana(self, player):
        mana = player.current_mana
        return mana
    
    def kill(self):
        self.battle_running = 0
        globals.battle_over = -1
        globals.pause = False
        pass

    def stop_battle(self, player, enemy_list):
        xp = self.calculate_xp(enemy_list)
        health = self.report_player_health(player)
        mana = self.report_player_mana(player)
        self.kill()
        return xp, health, mana
    
    #draw stat panel
    def draw_panel(self, player, enemy_list):
        #panel bg
        panel_img = pygame.image.load("assets/images/buttons/panel.png")
        bottom_panel = 150
        screen.blit(panel_img, (0, constants.SCREENHEIGHT - bottom_panel))
        #show player stats
        Name = DrawText('Nero', font, constants.WHITE, 50, constants.SCREENHEIGHT - bottom_panel + 10)
        Player_HP = DrawText(f'HP: {player.hp}/{player.max_hp}', font, constants.WHITE, 210, constants.SCREENHEIGHT - bottom_panel + 25)
        Player_MP = DrawText(f'MP: {player.current_mana}/{player.max_mana}', font, constants.WHITE, 210, constants.SCREENHEIGHT - bottom_panel + 45)
        #show enemy stats
        for count, i in enumerate(enemy_list):
            DrawText(f'{i.name}', font, constants.WHITE, 420, (constants.SCREENHEIGHT - bottom_panel + 10) + count * 40)
            
    #draw background image
    def draw_bg(self):
        bg_img = pygame.image.load("assets/images/backgrounds/dungeonbg1.png").convert_alpha()
        screen.blit(bg_img, (0, 0))



#create player
player = Player(1818, 2563, mob_animations, 0, 20, 10)

#define camera
camera = Camera(player)
followcam = camera.Follow(camera, player)
camera.setmethod(followcam)

#create world instance
world = TileMap('levels\level0_data.csv', dungeon_sheet, camera, player)

#create inventory
inventory_menu = InventoryMenu(player, 18, 1)
#create enemies

#create empty enemy list
enemy_list = []

#create battle 
#create player fighter and player UI
player_battle = battle.Fighter(200, 220, "Knight", player.health, player.max_health, player.attack_dmg, player.mana, player.max_mana)

#create enemy fighters and enemy UI
bandit1 = battle.Fighter(450, 220, "Bandit", 10, 10, 4, 5, 5, 100)
bandit2 = battle.Fighter(550, 220, "Bandit", 10, 10, 4, 5, 5, 100)
bandit1_health_bar = battle.StatBar(420, battle.screenheight-battle.bottom_panel + 30, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = battle.StatBar(420, battle.screenheight-battle.bottom_panel + 70, bandit2.hp, bandit2.max_hp)

goblin1 = battle.Fighter(450, 220, "Bandit", 5, 5, 3, 5, 5, 75)
goblin2 = battle.Fighter(550, 220, "Bandit", 5, 5, 3, 5, 5, 75)
red_goblin1 = battle.Fighter(650, 220, "Bandit", 10, 12, 7, 5, 5, 200)
goblin1_health_bar = battle.StatBar(420, battle.screenheight-battle.bottom_panel + 30, goblin1.hp, goblin1.max_hp)
goblin2_health_bar = battle.StatBar(420, battle.screenheight-battle.bottom_panel + 70, goblin2.hp, goblin2.max_hp)
redgoblin1_health_bar = battle.StatBar(420, battle.screenheight-battle.bottom_panel + 110, red_goblin1.hp, red_goblin1.max_hp)

expert = battle.Fighter(450, 220, "Bandit", 20, 20, 3, 5, 5, 500)
expert_health_bar = battle.StatBar(420, battle.screenheight-battle.bottom_panel + 30, expert.hp, expert.max_hp)

#create empty battle lists
battle_list1 = []
battle_list2 = []
battle_list3 = []

#create empty health lists
health_battle_list1 = []
health_battle_list2 = []
health_battle_list3 = []

#populate fighters
battle_list1.append(bandit1)
battle_list1.append(bandit2)

battle_list2.append(goblin1)
battle_list2.append(goblin2)
battle_list2.append(red_goblin1)

battle_list3.append(expert)

health_battle_list1.append(bandit1_health_bar)
health_battle_list1.append(bandit2_health_bar)

health_battle_list2.append(goblin1_health_bar)
health_battle_list2.append(goblin2_health_bar)
health_battle_list2.append(redgoblin1_health_bar)

health_battle_list3.append(expert_health_bar)

#add items to sprite group
#potion = Item(220, 400, 1, [health_image])
#globals.item_group.add(potion)

mana_pot = Item(300, 400, 0, [mana_image])
globals.item_group.add(mana_pot)

encounter_color = constants.WHITE
encounter_label = 'SAFE'
DangerMeter = DrawText(f'DANGER: {encounter_label}', font, encounter_color, 320, 45)

#screen fade handler
class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            #fade up
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, constants.SCREENWIDTH, constants.SCREENHEIGHT))
        if self.fade_counter <= constants.SCREENHEIGHT:
            fade_complete = True
            
        return fade_complete
        
#create screen fade
intro_fade = ScreenFade(1, constants.BLACK, 4)
gameover_fade = ScreenFade(1, constants.RED, 3)

#main game loop
while globals.run:
    
    #framerate control
    clock.tick(constants.TICKRATE)
    
    if player.alive:
        #cull previous frame
        screen.fill(constants.BACKGROUND)
        #globals.pause = False
        
        
        #calculate player movement
        dx = 0
        dy = 0
        if moving_right == True:
            dx = speed
        if moving_left == True:
            dx = -speed
        if moving_up == True:
            dy = -speed
        if moving_down == True:
            dy = speed
        
        
        #game objects update
        player.update(enemy_list)
        #player movement
        if globals.pause == False:
            player.move(dx, dy, world.tiles, camera)
        #for enemy in enemy_list:
            #enemy.update(enemy_list) 
            #enemy movement 
            #enemy.ai(player, world.tiles, camera)
        
        
    #camera movement and world draw
    camera.scroll()
    world.draw_map(screen, camera)
        
            
    #draw player
    player.draw(camera, screen)
            
    #draw items
    globals.item_group.update(player)
    for item in globals.item_group:
        item.draw(camera, screen)
            
    #fade in
    globals.start_intro = True
    #show intro
    if globals.start_intro == True:
        if intro_fade.fade():
            globals.start_intro = False

            
    
        
   
        
    #draw UI
    ui_panel = pygame.rect.Rect(0, 0, constants.SCREENWIDTH, 100)
    pygame.draw.rect(screen, constants.BLACK, ui_panel)
    MPUI = DrawText(f'HP: {player.health} / {player.max_health}', font2, constants.RED, 25, 25)
    MPUI = DrawText(f'MP: {player.mana} / {player.max_mana}', font2, constants.BLUE, 25, 45)
    LVLUI = DrawText(f'LVL: {player.level}', font, constants.WHITE, 600, 25)
    XPUI = DrawText(f'XP: {player.experience}', font, constants.WHITE, 600, 45)
    KeysUI = DrawText(f'KEYS: {player.keys}', font, constants.WHITE, 320, 25)
    DangerMeter.update_text(player)
            
            
    #battle setup
    battlecount = 0
    
    if player.touchingEnemy == True:
        globals.pause = True
        player.last_touched = pygame.time.get_ticks()
        current_battle = Battle()
        #updates battle with current hp and mana
        if globals.battle_over == -1:
            player_battle.sethealth(player.health)
            player_battle.setmana(player.mana)
        player_health_bar = battle.StatBar(50, battle.screenheight-battle.bottom_panel + 30, player.health, player_battle.max_hp)
        player_mana_bar = battle.StatBar(50, battle.screenheight-battle.bottom_panel + 50, player.mana, player_battle.max_mana)
        #launch battle
        #current_battle.update_fighters()
        #enter battle
        player.touchingEnemy = False
        if current_battle:
            current_battle.battle_running = 1
            battlecount += 1
            if battlecount == 1:
                battle_list = battle_list1
                health_battle_list = health_battle_list1
            if battlecount == 2:
                battle_list = battle_list2
                health_battle_list = health_battle_list2
            if battlecount == 3:
                battle_list = battle_list3
                health_battle_list = health_battle_list3
            while current_battle.battle_running == 1:
                    #draw background
                    screen.fill(constants.BATTLE_BACKGROUND)
                    current_battle.draw_bg()
                    current_battle.draw_panel(player_battle, battle_list)
                    #draw hp of players and enemies
                    player_health_bar.draw(player_battle.hp, constants.RED)
                    player_mana_bar.draw(player_battle.current_mana, constants.BLUE)
                    for count, i in enumerate(health_battle_list):
                        i.draw(battle_list[count].hp, constants.RED)
                    
                    #draw fighters
                    player_battle.update()
                    player_battle.draw()
                    for enemy in battle_list:
                        enemy.update()
                        enemy.draw()
                    
                    #draw damage/heal text
                    battle.damage_text_group.update()
                    battle.damage_text_group.draw(screen)
                    
                    #control actions
                    #reset action variables
                    globals.heal = False
                    globals.fireball = False
                    globals.firewall = False
                    globals.attack = False
                    globals.target = None
                    #ensure mouse is visible
                    pygame.mouse.set_visible(True)
                    pos = pygame.mouse.get_pos()
                    #allow clicking enemies to attack them
                    for count, enemy in enumerate(battle_list):
                        if enemy.alive == True:
                            if enemy.rect.collidepoint(pos):
                                #hide cursor
                                pygame.mouse.set_visible(False)
                                #show sword cursor
                                screen.blit(battle.cursor_img, pos)
                                if globals.clicked == True:
                                    globals.attack = True
                                    globals.target = battle_list[count]
                    #allow clicking heal button
                    if battle.heal_button.draw():
                        globals.heal = True
                    #allow clicking magic buttons
                    if battle.fireball_button.draw():
                        if player_battle.current_mana >= 7:
                            globals.fireball = True
                    if battle.firewall_button.draw():
                        if player_battle.current_mana >= 12:
                            globals.firewall = True
                        
                    
                    
                    #player action
                    battle.set_fighters(battle_list)
                    if globals.game_over == 0:
                        if player_battle.alive == True:
                            globals.battle_over = 0
                            if globals.current_fighter == 1:
                                globals.action_cd += 1
                                if globals.action_cd >= globals.action_wait:
                                    #look for player action
                                    #attack
                                    if globals.attack == True and globals.target != None:
                                        player_battle.attack(globals.target)
                                        globals.current_fighter += 1
                                        globals.action_cd = 0
                                    #heal spell
                                    if globals.heal == True:
                                        if player_battle.current_mana >= 5:
                                            damage_text = battle.DamageText(player_battle.rect.centerx, player_battle.rect.y, str(player_battle.heal_power), constants.GREEN)
                                            battle.damage_text_group.add(damage_text)
                                            player_battle.current_mana -= 5
                                            if player_battle.hp + player_battle.heal_power > player_battle.max_hp:
                                                player_battle.hp = player_battle.max_hp
                                            else:
                                                player_battle.hp = player_battle.hp + player_battle.heal_power
                                            globals.current_fighter += 1
                                            globals.action_cd = 0
                                    #single target fire spell  
                                    if globals.fireball == True:
                                        if player_battle.current_mana >= 7:
                                            player_battle.current_mana -= 7
                                            for enemy in battle_list:
                                                #attacks the first enemy in the lineup
                                                if enemy.alive == True:
                                                    player_battle.fireball(enemy)
                                                    break
                                        globals.current_fighter += 1
                                        globals.action_cd = 0
                                    #AoE fire spell     
                                    if globals.firewall == True:
                                        if player_battle.current_mana >= 12:
                                            player_battle.current_mana -= 12
                                        globals.current_fighter += 1
                                        globals.action_cd = 0   
                        else:
                            globals.battle_over = 2 #battle loss
                            globals.game_over = -1 #game loss
                        
                        #enemy action
                        for count, enemy in enumerate(battle_list):
                            if globals.current_fighter == 2 + count:
                                if enemy.alive == True:
                                    #check for enemy type and execute related AI: this one is for bandit aka basic AI
                                    if enemy.name == 'Bandit':
                                        globals.action_cd += 1
                                        if globals.action_cd >= globals.action_wait:
                                            #attack
                                            enemy.attack(player_battle)
                                            globals.current_fighter += 1
                                            globals.action_cd = 0
                                else:
                                    globals.current_fighter += 1
                                    
                        #if all fighters have had turn, reset
                        if globals.current_fighter > globals.total_fighters:
                            globals.current_fighter = 1
                            
                    #check if all enemies are dead
                    alive_enemies = 0
                    for enemy in battle_list:
                        if enemy.alive == True:
                            alive_enemies += 1
                    if alive_enemies == 0:
                        globals.battle_over = 1
                        
                    #check if battle is over
                    if globals.battle_over != 0:
                        #win
                        if globals.battle_over == 1:
                            screen.blit(battle.victory_img, (250, 70))
                            break
                        #loss
                        if globals.battle_over == 2:
                            screen.blit(battle.defeat_img, (290, 70))
                            break
                        
                    for event in pygame.event.get():
                        globals.clicked = False
                        if event.type == pygame.QUIT:
                            current_battle.battle_running = 0
                            globals.run = False
                        if event.type == pygame.QUIT:
                            current_battle.battle_running = 0
                            globals.run = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            globals.clicked = True
                    
                    #display updater
                    pygame.display.update()
    #win battle
    if globals.battle_over == 1:
            player.experience, player.health, player.mana = current_battle.stop_battle(player_battle, battle_list)
            #reset battle
            player.touchingEnemy = False
            current_battle = ()
    #lose battle
    if globals.battle_over == 2:
            player.touchingEnemy = False
            current_battle.stop_battle(player_battle, battle_list)
            #reset battle
            current_battle = ()
            #game over function
            player.alive = False
            gameover_fade.fade()
            pass
            
        
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                globals.run = False
        #accept keyboard input
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_1:
                    #inventory_menu.draw(screen)
                    globals.pause = True
                if event.key == pygame.K_2:
                    globals.pause = False
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_s:
                    moving_down = False
                if event.key == pygame.K_d:
                    moving_right = False
            

            
    #display updater
    pygame.display.update()
    
pygame.quit()