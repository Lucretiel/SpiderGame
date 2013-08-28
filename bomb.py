import pygame
import config
from screen import frame_seconds
import flingable
import random
from vec2d import Vec2d

all_bombs = list()
random.seed()

def clear():
    global all_bombs
    all_bombs = []
    
def update_bombs():
    global all_bombs
    for bomb in all_bombs:
        bomb.update()
    all_bombs = [bomb for bomb in all_bombs if bomb.timer > 0]

class Bomb():
    babies_abandoned = 0
    image = pygame.image.load(config.bomb.image)
    def __init__(self, victim):
        self.victim = victim
        self.timer = frame_seconds(config.bomb.explode_time)
        all_bombs.append(self)
    
    def update(self):
        self.victim.web()
        self.timer -= 1
        if self.timer == 0:
            self.victim.kill() #so for some reason the wasp vanishes right away. We have no idea why
            self.spawn_babies()
    
    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(bottomleft = self.victim.rect.center))
        
    def spawn_babies(self):
        for i in range(random.randint(config.bomb.babies_made_min, config.bomb.babies_made_max)):
            baby = flingable.Flingable("spiderling", self.victim.rect.center)
            force = Vec2d(random.randint(config.bomb.baby_spray_min, config.bomb.baby_spay_max), 0)
            force.angle = random.randint(0, 359)
            baby.fling(force) #best line of code ever written
            self.babies_abandoned += 1 #second best line of code ever written
        