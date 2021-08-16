import pygame
import colors
from stgs import *
from menu import *

pygame.font.init()
class text:
    def __init__(self, fNum, text, color, aalias, pos, multiline=False, size=(900, 600), bgColor=(0, 0, 0, 0)):
        if multiline:
            ## This code is thanks to https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame 
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill(bgColor)
            font = fonts[fNum]
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
            space = font.size(' ')[0]  # The width of a space.
            max_width, max_height = size
            x, y = 0, 0
            for line in words:
                for word in line:
                    if word  != '':
                        word_surface = font.render(word, aalias, color)
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = 0  # Reset the x.
                            y += word_height  # Start on new row.
                        self.image.blit(word_surface, (x, y))
                        x += word_width + space
                x = 0 # Reset the x.
                y += word_height  # Start on new row.
            
        else: 
            self.image = fonts[fNum].render(text, aalias, color)
        self.pos = pygame.Vector2(pos)
        
        self.rect = (self.pos.x, self.pos.y, size[0], size[1])
        self.image = self.image.convert_alpha()
    
    def __str__(self):
        return self.rend

def transparentRect(size, alpha, color=(0, 0, 0)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((color[0], color[1], color[2], alpha))
    return surf 

class pauseOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA).convert_alpha()
        self.loadComponents()
        self.render()

    def loadComponents(self):
        for comp in self.components:
            comp.kill()
            
        self.audioSlider1 = settingSlider(self.game, (100, 350), addGroups = [self.components])
        self.audioSlider2 = settingSlider(self.game, (100, 500), addGroups = [self.components])
        self.audioSlider1.image.set_colorkey((0,0,0))
        self.audioSlider2.image.set_colorkey((0,0,0))
        self.fpsButton = button(self.game, (800, 250), text = 'Toggle FPS', onClick = lambda:self.game.toggleFps() ,groups = [self.components], center = True, colors=(colors.yellow, colors.white))
        self.aaliasButton = button(self.game, (800, 330), text = 'Toggle Anti - Aliasing', onClick = lambda:self.game.toggleAalias() ,groups = [self.components], center = True, colors=(colors.yellow, colors.white))
        button(self.game, (350, 550), groups = [self.components], text = "Return to menu", onClick=self.game.endgame, center = True, colors = (colors.yellow, colors.white))
    
        self.text = [
            text('5', 'Paused', colors.orangeRed, self.game.antialiasing, (self.rect.width/2.4, 10)),
            text('1', 'Audio Control', colors.orangeRed, self.game.antialiasing, (75, 250)),
            text('6', 'Music Volume', colors.orangeRed, self.game.antialiasing, (75, 325)),
            text('6', 'Fx Volume', colors.orangeRed, self.game.antialiasing, (75, 475))
        ]

        self.audioSlider1.setRatio(self.game.mixer.musicVolume)
        self.audioSlider2.setRatio(self.game.mixer.fxVolume)
        
    def applyComponents(self):
        self.game.mixer.setMusicVolume(self.audioSlider1.get_ratio())
        self.game.mixer.setFxVolume(self.audioSlider2.get_ratio())

    def activate(self):
        self.active = True
        self.audioSlider1.setRatio(self.game.mixer.musicVolume)
        self.audioSlider2.setRatio(self.game.mixer.fxVolume)

    def deactivate(self):
        self.active = False

    def update(self):
        if self.active:
            self.render()
            self.components.update()
            self.applyComponents()
    
    def render(self):
        self.image.fill((0,0,0,190)) #self.transparent)
        for comp in self.components:
            self.image.blit(comp.image, comp.rect)
        for text in self.text:
            self.image.blit(text.image, text.pos)

class mapOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA).convert()
        self.loadComponents()
        self.render()

    def loadComponents(self):
        for comp in self.components:
            comp.kill()
            
        self.mapImage = pygame.image.load(asset('gameMap.png'))
        self.mapImage = pygame.transform.scale(self.mapImage, (int(winWidth), int(winHeight))).convert()

    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False

    def update(self):
        now = pygame.time.get_ticks()
        if self.active:
            self.render()
            self.components.update()
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.deactivate()
                self.game.unPause()
                self.game.lastPause = now
        else:
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.activate()
                self.game.pause = True
                self.game.lastPause = now
    
    def render(self):
        self.image.fill((0,0,0,190)) #self.transparent)
        self.image.blit(self.mapImage, (0, 0))
        # for comp in self.components:
        #     self.image.blit(comp.image, comp.rect)
        # for text in self.text:
        #     self.image.blit(text.image, text.pos)      
