import pygame
from vec2d import Vec2d
import config
from screen import frame_seconds
import music

all_birds = list()

def clear():
    global all_birds
    all_birds = []
    
def update_birds(screen):
    global all_birds
    for enemy in all_birds:
        enemy.update(screen)
    all_birds = [x for x in all_birds if x.rect.colliderect(screen.get_rect()) or x.moving == False]

class Bird():
    def __init__(self, position, velocity, yaccel):
        anim = open(config.bird.bird_file)
        self.images = [pygame.image.load(config.assets_folder + frame.rstrip()) for frame in anim]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = position)
        self.hp = config.bird.hp
        self.angle = 0
        self.vel = Vec2d(velocity)
        self.yaccl = yaccel
        self.frames = config.bird.frame_rate
        self.frame = 0
        self.frame_clock = 0
        self.moving = False
        all_birds.append(self)

    def update(self, screen):
        if self.rect.centerx < screen.get_rect().right:
            self.moving = True
            music.play_bird()
        if self.moving == True:
            self.vel.y += self.yaccl
            self.rect += self.vel
            self.angle = self.vel.angle * -1 + 205
            
            if self.frame_clock < self.frames:
                self.frame = 0
            else:
                self.frame = 1
            self.frame_clock += 1
            if self.frame_clock == (self.frames *2):
                self.frame_clock = 0
            
            self.image = self.images[self.frame]
        

    def draw (self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        screen.blit(rotated, rotated.get_rect(center = self.rect.center))  
        #screen.blit(self.image, self.rect)