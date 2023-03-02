import globals, constants, pygame

class DrawText():
    def __init__(self, text, font, text_color, x, y):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))
    def update_text(self, player):
        if (player.encounter_cd) <= 10000 and player.encounter_cd > 0:
            encounter_color = constants.RED
            encounter_label = '!!!'
        elif (player.encounter_cd) <= 20000 and player.encounter_cd > 10000:
            encounter_color = constants.YELLOW
            encounter_label = '!!'
        elif (player.encounter_cd) <= 36000 and player.encounter_cd > 20000:
            encounter_color = constants.GREEN
            encounter_label = 'SAFE'
            img = self.font.render(self.text, True, encounter_color)
            screen.blit(img, (self.x, self.y))
            
class InventoryMenu():
    def __init__(self, player, rows, columns):
        self.player = player
        self.inventory = player.inventory
        self.rows = rows
        self.x = 0
        self.y = 0
        
    def draw_panel(self):
        #panel bg
        panel_img = pygame.image.load("assets/images/buttons/panel.png")
        bottom_panel = 150
        screen.blit(panel_img, (0, constants.SCREENHEIGHT - bottom_panel))
        #show player stats
        Name = DrawText('Nero', font, constants.WHITE, 50, constants.SCREENHEIGHT - bottom_panel + 10)
        Player_HP = DrawText(f'HP: {self.player.hp}/{self.player.max_hp}', font, constants.WHITE, 210, constants.SCREENHEIGHT - bottom_panel + 25)
        Player_MP = DrawText(f'MP: {self.player.current_mana}/{self.player.max_mana}', font, constants.WHITE, 210, constants.SCREENHEIGHT - bottom_panel + 45)
        
    def draw(self, surface):
        pygame.draw.rect(surface, constants.BLACK, (self.x, self.y, constants.SCREENWIDTH, constants.SCREENHEIGHT))
        rowimg = pygame.image.load("assets/images/buttons/inventoryrow.png")
        i = 0
        while i < self.rows:
            surface.blit(rowimg, (0, i * 25))
        self.draw_panel()