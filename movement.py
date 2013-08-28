'''
Created on Sep 10, 2011

@author: nathan
'''

import pygame
from vec2d import Vec2d #an incredible file I found online that implements a fully-featured 2d vector that is fully compatibly with pygame.
import math
import config

#simple distance finder
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

all_webs = list()
all_regions = list()
all_region_types = dict()

def clear():
    global all_webs
    global all_regions
    all_webs = []
    all_regions = []

def update_movement(screen):
    global all_webs
    global all_regions
    all_webs = [web for web in all_webs if screen.get_rect().collidepoint(web.start) or screen.get_rect().collidepoint(web.end)]
    all_regions = [region for region in all_regions if region.get_rect().right > screen.get_rect().left]

class Web:
    end_image = pygame.image.load(config.web.web_spray_image)
    def __init__(self, start, end):
        self.start = Vec2d(start)
        self.end = Vec2d(end)
        all_webs.append(self)
    def draw(self, screen):
        screen.line(config.web.color, self.start, self.end, config.web.thickness)
        screen.blit(self.end_image, self.end_image.get_rect(center=self.end))
    def vector(self):
        return self.end - self.start
    def collide_box(self):
        rect = pygame.rect.Rect(self.start, self.vector())
        rect.normalize()
        return rect
    def get_point(self, dist):
        vec = self.vector()
        vec.length = dist
        return self.start + vec
    
#A walkable region reperesents a single varient of a region. They are instanced
#in the game by the WalkableRegionInstance class
class WalkableRegionType():
    def __init__(self, name, image_file, region_rect = None):
        self.image = pygame.image.load(config.assets_folder + image_file)
        self.rect = pygame.Rect(region_rect if region_rect is not None else self.image.get_rect())
        all_region_types[name] = self

class WalkableRegion():
    def __init__(self, region_name, **kwargs):
        self.region = all_region_types[region_name]
        self.location = Vec2d(self.region.image.get_rect(**kwargs).topleft)
        self.adjacencies = [region for region in all_regions if region.get_rect().colliderect(self.get_rect())]
        for adj in self.adjacencies:
            adj.adjacencies.append(self)
        all_regions.append(self)
    
    #superfunction- binds the spider to either this or an adjacent region
    def constrain_spider_movement(self, spider):
        if self.get_rect().collidepoint(spider.rect.center):
            return
        for adj in self.adjacencies:
            if adj.get_rect().collidepoint(spider.rect.center):
                spider.parent = adj
                return
        #constrain
        if spider.rect.centerx < self.get_rect().left:
            spider.rect.centerx = self.get_rect().left
        elif spider.rect.centerx > self.get_rect().right:
            spider.rect.centerx = self.get_rect().right
        if spider.rect.centery > self.get_rect().bottom:
            spider.rect.centery = self.get_rect().bottom
        elif spider.rect.centery < self.get_rect().top:
            spider.rect.centery = self.get_rect().top
            
    def get_rect(self):
        return pygame.rect.Rect(self.location + self.region.rect.topleft, self.region.rect.size)
        
    def draw(self, screen):
        screen.blit(self.region.image, self.location)