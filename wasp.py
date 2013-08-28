import pygame
import stinger
import config
from screen import frame_seconds
from vec2d import Vec2d
import music

all_wasps = list()

def clear():
    global all_wasps
    all_wasps = []

def update_wasps(screen):
    global all_wasps
    for enemy in all_wasps:
        enemy.update(screen)
    all_wasps = [x for x in all_wasps if x.rect.colliderect(screen.get_rect()) or x.moving == False]


class Wasp():
    images = [pygame.image.load(config.assets_folder + frame.rstrip()) for frame in open(config.wasp.file)]
    def __init__(self, xloc, yloc):
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = (xloc, yloc))
        self.vel = Vec2d(config.wasp.velocicty)
        self.bullet_clock = 0
        self.move_clock = 0
        self.frame = 0
        self.frame_clock = 0
        self.dead = False
        self.webbed = False
        self.moving = False
        self.web_clock = frame_seconds(config.wasp.web_time)
        
        self.move_time = config.wasp.move_time
        self.frames = config.wasp.frame_rate
        all_wasps.append(self)

        
    def update(self, screen):
        if self.rect.left < screen.get_rect().right:
            self.moving = True
            music.play_wasp()
        if self.moving == True:
            self.bullet_clock += 1
            if not self.dead:
                #movement   
                if self.webbed == False:
                    self.move_clock += 1
                    if self.move_clock == self.move_time:
                        self.vel.y *= -1
                        self.move_clock = 0
                    self.rect += self.vel
                
                #frames
                if self.webbed == False:
                    if self.frame_clock < self.frames:
                        self.frame = 0
                    else:
                        self.frame = 1
                    self.frame_clock +=1
                    if self.frame_clock == (self.frames *2):
                        self.frame_clock = 0
                #Webbed ends below
                else:
                    self.frame = 3
                    self.web_clock -= 1
                    if self.web_clock <= 0:
                        self.webbed = False
                self.image = self.images[self.frame]
                
                #shoot
                if self.webbed == False:
                    if self.bullet_clock >= 8:
                        self.image = self.images[2]
                        if self.bullet_clock >= 10:
                            self.bullet_clock = 0
                            stinger.Stinger(self.rect.midleft)
            else:
                self.rect += self.vel
                self.vel += config.object.gravity
    
    def draw(self, screen):
         screen.blit(self.image, self.rect)
         
    def kill(self):
        self.dead = True
        self.moving = True
        #pop into air
        self.vel += config.wasp.death_jump
    
    def web(self):
        self.webbed = True
        self.web_clock = frame_seconds(config.wasp.web_time)