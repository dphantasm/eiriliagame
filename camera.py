import globals, constants, pygame
from abc import ABC, abstractmethod
#pygame function to make vector math easier
vec = pygame.math.Vector2

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0,0)
        self.offset_float = vec(0,0)
        #const is just half the screen height and width, negative, to ensure the camera is centered
        self.CONST = vec(-400, -300)
        
    #picks camera function out of existing ones
    def setmethod(self, method):
        self.method = method
    
    #basic camera scrolling function
    def scroll(self):
        self.method.scroll()
        
    class CamScroll(ABC):
        def __init__(self, camera, player):
            self.camera = camera
            self.player = player

        #this just throws an error if the scroll function doesnt exist
        @abstractmethod
        def scroll(self):
            pass
        
    class Follow(CamScroll):
        def __init__(self, camera, player):
            camera.CamScroll.__init__(self, camera, player)
            
        def scroll(self):
            #this makes the camera follow the player so they are always centered
            self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
            self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
            #casting floats to ints for pixel perfect scrolling
            self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
    class Border(CamScroll):
        def __init__(self, camera, player):
            camera.CamScroll.__init__(self, camera, player)
            
        def scroll(self):
            #this makes the camera follow the player so they are always centered
            self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
            self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
            #casting floats to ints for pixel perfect scrolling
            self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
            #limit horizontal scroll to border
            self.camera.offset.x = max(constants.LEFT_BORDER, self.camera.offset.x)
            self.camera.offset.x = min(constants.BOT_BORDER, self.camera.offset.x - constants.SCREENWIDTH)
            #limit vertical scroll to border
            self.camera.offset.y = max(constants.TOP_BORDER, self.camera.offset.y)
            self.camera.offset.y = min(constants.BOT_BORDER, self.camera.offset.y - constants.SCREENHEIGHT)