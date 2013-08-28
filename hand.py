import pygame
import config
from vec2d import Vec2d
from movement import distance
import music

all_hands = list()
spawn_clock = config.hand.spawn_clock

def clear():
    global all_hands
    all_hands = []

def update_hands(spider, frames):
    global all_hands
    global spawn_clock
    if frames >= config.hand.start_frame:
        spawn_clock -=1
        if spawn_clock <= 0:
            Hand(spider.rect.center)
            spawn_clock = config.hand.spawn_clock
    all_hands = [x for x in all_hands if x.vanish == False]
    for current in all_hands:
        current.update(spider)


class Hand():

    def __init__(self, loc):
        anim = open(config.hand.file)
        self.images = [pygame.image.load(config.assets_folder + frame.rstrip()).convert_alpha() for frame in anim]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = loc)
        self.shadow_clock = config.hand.clock
        self.move_clock = config.hand.move
        self.exist_clock = config.hand.life_span
        self.vel = config.hand.vel
        self.vanish = False
        self.down = False
        
        all_hands.append(self)
        
    def update(self, spider):
        self.move_clock -=1
        self.shadow_clock -= 1
        self.exist_clock -=1
       
        
        if self.move_clock >= 0:
            movement_vector = Vec2d(spider.rect.center) - self.rect.center
            dist = min(self.vel, distance(self.rect.center, spider.rect.center))
            if dist > 0:
                movement_vector.length = dist
                self.angle = movement_vector.get_angle_between((0, -1))
                self.rect.center += movement_vector
        
        if self.shadow_clock <= 0:
            self.down = True
            self.image = self.images[1]
            music.play_hand()
        
        if self.exist_clock <= 0:
            self.vanish = True
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)