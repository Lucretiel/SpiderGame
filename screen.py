'''
Created on Sep 16, 2011

@author: Nathan West
'''

import pygame
import random
from vec2d import Vec2d
import config
from turtle import Vec2D

random.seed()

def frame_seconds(seconds):
    #converts a number of seconds into a number of frames
    return int(seconds * config.display.frame_rate)

class Background:
    def __init__(self, image, offset):
        self.image = image
        self.offset = offset

class Screen:
    def __init__(self):
        self.offset = 0
        self.dimensions = self.width, self.height = 1260, 980
        self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN if config.display.fullscreen else 0)
        background_file = open(config.display.backgrounds_file)
        self.backgrounds = [pygame.image.load(config.assets_folder + line.rstrip()).convert_alpha() for line in background_file]
        self.background_buffer = [Background(random.choice(self.backgrounds), 0)]
        
    def get_rect(self):
        return self.screen.get_rect(left = -self.offset)
    def paralax(self):
        return self.offset / config.display.paralax_factor
    
    def update(self):
        self.offset -= config.display.pixels_per_frame
        #if the last frame in the buffer extends past the end, make a new frame
        if self.paralax() + self.background_buffer[-1].offset + self.background_buffer[-1].image.get_rect().width < self.width:
            self.background_buffer.append(Background(random.choice(self.backgrounds), self.background_buffer[-1].offset + self.background_buffer[-1].image.get_rect().width))
        #if the first frame of the buffer is off the screen, remove it
        if self.paralax() + self.background_buffer[0].offset + self.background_buffer[0].image.get_rect().width < 0:
            self.background_buffer.pop(0)
        
    def draw(self):
        #blit at paralax offset, centered vertically
        for background in self.background_buffer:
            self.screen.blit(background.image, background.image.get_rect(left = background.offset + self.paralax()))
    def blit(self, source, dest, area=None, special_flags = 0):
        return self.screen.blit(source, dest + Vec2d(self.offset, 0), area, special_flags)
    
    def blit_UI(self, source, dest, area=None, special_flags = 0):
        return self.screen.blit(source, dest, area, special_flags)
    
    def line(self, color, start, end, thickness):
        if thickness != 1:
            return pygame.draw.line(self.screen, color, start + Vec2d(self.offset, 0), end + Vec2d(self.offset, 0), thickness)
        else:
            return pygame.draw.aaline(self.screen, color, start + Vec2d(self.offset, 0), end + Vec2D(self.offset, 0))
        
    def reset(self):
        self.offset = 0
        self.background_buffer = [Background(random.choice(self.backgrounds), 0)]