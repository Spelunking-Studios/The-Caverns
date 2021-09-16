import pygame
from stgs import *

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)

## Provide name: file and volume offset (will not exceed one or drop below zero)
fx = {
    'launch1': [asset('sounds/random5.wav'), 0],
    'hit1': [sAsset('random3.wav'), 0],
    'hit2': [sAsset('random2.wav'), 0],
    'pHit': [sAsset('sounds/Hit_02.mp3'), 0.2],
    'menu1':[sAsset('switch10.wav'), 0],
    'menu2': [sAsset('mouseclick1.wav'), 0],
    'menu3': [sAsset('misc_menu_3.wav'), 0.1],
    'yay': [sAsset('yay.wav'), 0.1],
    'swing':[sAsset('swing.wav'), 0],
}

class gameMixer:
    def __init__(self):
        global fx
        self.fx = fx
        self.fxVolume = 1
        self.musicVolume = 1
        self.musicChannel = pygame.mixer.Channel(0)
    
    def setMusicVolume(self, volume):
        if isinstance(volume, str):
            pass
        else:
            self.musicVolume = volume

        self.musicChannel.set_volume(self.musicVolume)
    
    def setFxVolume(self, volume): ## Probably won't affect sfx in mid play 
        if isinstance(volume, str):
            pass
        else:
            self.fxVolume = volume

    def playFxFile(self, sfile, *args):
        sound = pygame.mixer.Sound(sfile)
        if args:
            sound.set_volume(args[0]/100)

        sound.play()

    def playFx(self, key):
        try:
            sound = pygame.mixer.Sound(self.fx[key][0])
            if self.fx[key][1] > 0:
                sound.set_volume(min(self.fxVolume + self.fx[key][1], 1))
            else:
                sound.set_volume(max(self.fxVolume + self.fx[key][1], 0))
            sound.play()
        except KeyError:
            print("Sound not registered. Maybe you meant playFxFile(*file)")

    def playMusic(self, sfile):
        sound = pygame.mixer.Sound(sfile)
        self.musicChannel.play(sound, -1)
    
    def stop(self):
        pygame.mixer.stop()
