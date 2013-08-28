import pygame

all_bullets = list()

def clear():
    global all_bullets
    all_bullets = []
    
def update_bullets(screen):
    global all_bullets
    for bullet in all_bullets:
        bullet.update(screen)
    all_bullets = [x for x in all_bullets if x.rect.right > screen.get_rect().left and x.dead is False]

class Stinger():

    def __init__(self, loc):
        self.image = pygame.image.load("Assets/Dudes/Enemies/Wasp/stinger.png").convert_alpha()
        self.rect = self.image.get_rect(midright = (loc[0] + 80, loc[1] + 25))
        self.xvel = 50
        self.dead = False

        all_bullets.append(self)
        
    def update(self, screen):
        self.rect.left -= self.xvel
        
    def kill(self):
        self.dead = True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)