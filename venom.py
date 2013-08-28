import pygame
import music
    
all_shots = list()

def clear():
    global all_shots
    all_shots = []
    
def update_shots(screen):
    global all_shots
    for shot in all_shots:
        shot.update(screen)
    all_shots = [x for x in all_shots if x.rect.colliderect(screen.get_rect())]

class Venom():

    def __init__(self, loc, direction):
        self.image = pygame.image.load("Assets/Dudes/Spider/acid1.png").convert_alpha()
        self.rect = self.image.get_rect(center = loc)
        self.velocity = direction

        all_shots.append(self)
        
    def update(self, screen):
        self.rect += self.velocity
        
    def kill(self):
        all_shots.remove(self)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)