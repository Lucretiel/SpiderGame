import pygame
from vec2d import Vec2d
import config
import music

all_flingable_types = dict()
all_flingables = list()
all_flung = list()

def clear():
    global all_birds
    global all_flingables
    all_birds = []
    all_flingables = []

def update_flingables(screen):
    global all_flung
    for fling in all_flung:
        fling.update(screen)
    all_flung = [x for x in all_flung if screen.get_rect().colliderect(x.get_rect())]

class FlingableType:
    def __init__(self, name, image_file, webbed_image_file):
        self.image = pygame.image.load(config.assets_folder + image_file)
        if webbed_image_file is not None:
            self.webbed = pygame.image.load(config.assets_folder + webbed_image_file)
        all_flingable_types[name] = self
    
class Flingable():  
    def __init__(self, type, loc):
        self.type = all_flingable_types[type]
        self.location = Vec2d(loc)
        self.velocity = None
        self.webbed = False
        all_flingables.append(self)
        
    def grab(self):
        self.webbed = True
    
    def fling(self, force):
        self.velocity = Vec2d(force)
        all_flingables.remove(self)
        all_flung.append(self)
        
    def update(self, screen):
        if self.velocity is not None:
            self.location += self.velocity
            self.velocity += config.object.gravity
    
    def draw(self, screen):
        if self.webbed == False:
            image = self.type.image
            if self.velocity is not None:
                image = pygame.transform.rotate(image, self.velocity.angle)
            screen.blit(image, image.get_rect(center = self.location))
        else:
            image = self.type.webbed
            if self.velocity is not None:
                image = pygame.transform.rotate(image, self.velocity.angle)
            screen.blit(image, image.get_rect(center = self.location))
    
    def get_rect(self):
        return self.type.image.get_rect(center = self.location)