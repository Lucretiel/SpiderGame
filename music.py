import pygame
import config

all_sounds = dict()

def music_begin():
    pygame.mixer.init()
    all_sounds["main"] = pygame.mixer.Sound("Assets/Music/ForestFunk.ogg")
    all_sounds["escape"] = pygame.mixer.Sound("Assets/Music/Escape.ogg")
    all_sounds["frog"] = pygame.mixer.Sound("Assets/Music/croak.wav")
    all_sounds["wasp"] = pygame.mixer.Sound("Assets/Music/mosquito_2.wav")
    all_sounds["hand"] = pygame.mixer.Sound("Assets/Music/ow.wav")
    all_sounds["smack"] = pygame.mixer.Sound("Assets/Music/smack.wav")
    all_sounds["venom"] = pygame.mixer.Sound("Assets/Music/spit2.wav")
    all_sounds["whip"] = pygame.mixer.Sound("Assets/Music/whip.wav")
    all_sounds["bird"] = pygame.mixer.Sound("Assets/Music/whistle.wav")
    
    
def play_music():
    pygame.mixer.Channel(1).play(all_sounds["main"])
    pygame.mixer.Channel(1).queue(all_sounds["escape"])
    
def stop_music():
    pygame.mixer.Channel(1).stop()
    
def play_wasp():
    all_sounds["wasp"].set_volume(0.3)
    pygame.mixer.Channel(2).play(all_sounds["wasp"])
    
def play_frog():
    all_sounds["frog"].set_volume(0.7)
    pygame.mixer.Channel(3).play(all_sounds["frog"])
    
def play_hand():
    pygame.mixer.Channel(4).play(all_sounds["hand"])
    
def play_smack():
    pygame.mixer.Channel(5).play(all_sounds["smack"])
    
def play_venom():
    all_sounds["venom"].set_volume(1.0)
    pygame.mixer.Channel(6).play(all_sounds["venom"])
    
def play_whip():
    all_sounds["whip"].set_volume(0.3)
    pygame.mixer.Channel(7).play(all_sounds["whip"])
    
def play_bird():
    pygame.mixer.Channel(0).play(all_sounds["bird"])