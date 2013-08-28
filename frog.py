import pygame
from vec2d import Vec2d
import config
from screen import frame_seconds
import music

all_frogs = list()
tongues = list()

def clear():
    global all_frogs
    global tongues
    all_frogs = []
    tongues = []

def update_frogs(screen, spider):
    global all_frogs
    for ugly in all_frogs:
        ugly.update(spider)
    all_frogs = [ugly for ugly in all_frogs if ugly.rect.right > screen.get_rect().left]
class directions:
    left = 0;
    right = 1;

class shoot_states:
    aiming = 1 #on cooldown
    charging = 2 #head angle locked
    shooting = 3 #tongue shooting

class Frog():
    def __init__(self, location):		
        anim = open(config.frog.head_file)
        images = [pygame.image.load(config.assets_folder + frame.rstrip()) for frame in anim]
        web_image = pygame.image.load(config.frog.webbed_image)
        self.head = Frog.Head(images, web_image, config.frog.head_center)
        self.image = pygame.image.load(config.frog.body_image)
        self.web_image = pygame.image.load(config.frog.webbed_body_image)
        self.rect = self.image.get_rect(midbottom = location)
        self.head.rect.center = self.rect.topleft + Vec2d(self.head.rect.size)/2
        self.hp = 10
        
        self.frames = 0
        self.aim_time = frame_seconds(config.frog.time_aiming)
        self.charge_time = frame_seconds(config.frog.time_charging)
        self.shoot_time = frame_seconds(config.frog.time_shooting)
        self.shoot_clock = self.aim_time
        
        self.direction = directions.left
        self.shooting_state = shoot_states.aiming
        self.target_location = Vec2d(0, 0)
        self.range = config.frog.fire_range
        
        self.tongue = None
        
        self.webbed = 0
        
        all_frogs.append(self)

    def update(self, spider):
        self.frames += 1
        
        if self.webbed > 0:
            self.webbed -= 1
        else:
            if self.shoot_clock > 0:
                self.shoot_clock -= 1
            
            #state proccessing
            if self.shooting_state == shoot_states.aiming:
                #find target
                self.target_location = Vec2d(spider.rect.center)
                
                #change facing if nessesary
                if self.rect.centerx < self.target_location.x:
                    self.direction = directions.right
                    self.head.rect.centerx = self.rect.right - (self.head.rect.width / 2)
                    self.head.rect.centery = self.rect.top + (self.head.rect.height / 2)
                    #self.head.rotation_center_offset.x = -abs(self.head.rotation_center_offset.x)
                else:
                    self.direction = directions.left
                    self.head.rect.center = self.rect.topleft + Vec2d(self.head.rect.size)/2
                    #self.head.rotation_center_offset.x = abs(self.head.rotation_center_offset.x)
                
                #find target vector
                target_vector = (self.target_location - self.head.rect.center + self.head.rotation_center_offset)
                
                #determine angle
                self.head.angle = target_vector.angle
                if self.direction == directions.left:
                    self.head.angle = 180.0 - self.head.angle
                else:
                    self.head.angle *= -1
                
                #STATE CHANGE: if in range and off cooldown, begin charging
                if target_vector.length <= self.range and self.shoot_clock == 0:
                    self.shooting_state = shoot_states.charging
                    self.shoot_clock = self.charge_time
                    music.play_frog()
            elif self.shooting_state == shoot_states.charging:
                #begin charging. Charge is a countdown float
                self.head.charge = float(self.shoot_clock) / self.charge_time
                
                #STATE CHANGE: when charge is complete, shoot
                if self.shoot_clock == 0:
                    self.shooting_state = shoot_states.shooting
                    self.shoot_clock = self.shoot_time
                    self.tongue = Frog.Tongue(self.head.rect.center + self.head.rotation_center_offset, self.target_location, self.shoot_time)
                    self.head.charge = 0
            elif self.shooting_state == shoot_states.shooting:
                #Update Tongue
                self.tongue.update()
                if self.shoot_clock == 0:
                    self.shooting_state = shoot_states.aiming
                    self.shoot_clock = self.aim_time
                    tongues.remove(self.tongue)
                    self.tongue = None
                    self.head.charge = 1.0 
                
    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.destroy = True

    def draw(self, screen):
        if self.tongue is not None:
            self.tongue.draw(screen)
        self.head.draw(screen, self.direction, self.webbed)
        if self.direction == directions.left:
            if self.webbed > 0:
                screen.blit(self.web_image, self.rect)
            else:
                screen.blit(self.image, self.rect)
        else:
            if self.webbed > 0:
                screen.blit(pygame.transform.flip(self.web_image, True, False), self.rect)
            else:
                screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
            
    def web(self):
        if self.shooting_state != shoot_states.shooting:
            self.webbed = frame_seconds(config.frog.time_webbed)
            self.shooting_state = shoot_states.aiming
            self.shoot_clock = 0
        
    class Head():
        def __init__(self, images, webbed, center):
            self.images = images
            self.web_image = webbed
            self.rect = images[0].get_rect()
            self.rotation_center_offset = Vec2d(center) #this is relative to the center
            self.angle = 0
            self.charge = 1.0 #countdown timer
            
        def draw(self, screen, direction, web):
            charge = 1.0 - self.charge
            if web > 0:
                image = self.web_image
            else:
                image = self.images[min(len(self.images)-1, int(charge * len(self.images)))]
            
            if direction == directions.right:
                image = pygame.transform.flip(image, True, False)
                
            screen.blit(image, self.rect)
        
    class Tongue():
        image = pygame.image.load(config.frog.tongue_tip)
        def __init__(self, origin, target, time):
            self.origin = Vec2d(origin)
            self.tongue_vec = target - origin
            self.time = time/2
            self.frame = 0
            self.extending = True
            tongues.append(self)
        def update(self):
            if self.extending:
                self.frame += 1
            else:
                self.frame -= 1
            
            if self.frame >= self.time:
                self.extending = False
        def draw(self, screen):
            tongue_vec = self.tongue_vec * (float(self.frame)/self.time)
            screen.line(config.frog.tongue_color, self.origin, self.origin + tongue_vec, config.frog.tongue_thickness)
            rotated = pygame.transform.rotate(self.image, -tongue_vec.angle)
            screen.blit(rotated, rotated.get_rect(center = self.origin + tongue_vec))
            
        def get_rect(self):
            tongue_vec = self.tongue_vec * (float(self.frame)/self.time)
            return self.image.get_rect(center = self.origin + tongue_vec)