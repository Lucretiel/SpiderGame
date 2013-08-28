'''
Created on Sep 16, 2011

@author: Nathan West
'''

import pygame
from vec2d import Vec2d
import config
import movement
from movement import distance
from screen import frame_seconds
import venom
import flingable
import wasp
import frog
import bomb
import music

pygame.font.init()

#spider position states
class movement_states:
    no_movement = 0; #generally not used. Could be used during some kind of cutscene
    free_movement = 1;
    web_movement = 2;
    
class Charge:
    bar = pygame.image.load(config.spider.bar_image)
    border = pygame.image.load(config.spider.border_image)
    def __init__(self):
        self.charge = 0
        self.center = config.spider.bar_center
    
    def update(self):
        self.charge += 1.0/frame_seconds(config.spider.venom_regen_time)
        if self.charge > 1:
            self.charge = 1.0
    
    def draw(self, screen):
        clip_rect = self.bar.get_rect()
        clip_rect.width *= self.charge
        screen.blit_UI(self.bar, self.bar.get_rect(center = self.center), clip_rect)
        screen.blit_UI(self.border, self.border.get_rect(center = self.center))
    
    def fire(self):
        if self.charge > config.spider.min_venom_charge:
            self.charge -= config.spider.min_venom_charge
            return True
        return False
    
    def reset(self):
        self.charge = 0
class Spider():
    free_movement_frames = list()
    web_movement_frames = list()
    f32 = pygame.font.Font(None, 32)

    
    def __init__(self, parent):
        anim = open(config.spider.free_movement.file)
        self.free_movement_frames = [pygame.image.load(config.assets_folder + frame.rstrip()) for frame in anim]
        anim = open(config.spider.web_movement.file)
        self.web_movement_frames = [pygame.image.load(config.assets_folder + frame.rstrip()) for frame in anim]
        anim.close()
        self.web_ball = pygame.image.load(config.spider.web_ball_image)
        
        self.rect = self.free_movement_frames[0].get_rect(center = config.spider.starting_postion)
        self.movement_target = Vec2d(config.spider.starting_postion)
        self.movement = False
        self.movement_state = movement_states.free_movement
        self.parent = parent
        self.position_on_web = 0 #used for web movement
        self.angle = 0
        self.frame = 0
        
        self.charge = Charge()
        
        self.fling_object = None
        
        self.lives = config.spider.starting_lives
        self.invuln = 0
        self.dead_time = 0 #countdown timer
        self.blink_time = 0
        self.respawn_location = None
        
        self.web_enemy = None
        self.web_enemy_time = 0
        self.min_web_enemy_time = frame_seconds(config.spider.min_enemy_web_time)
        self.web_ball_angle = 0
            
    def switch_movement_state(self):
        if(self.movement_state == movement_states.free_movement):
            #attempt to grab a web
            for web in movement.all_webs:
                if self.rect.collidepoint(web.start):
                    self.movement_state = movement_states.web_movement
                    self.rect.center = web.start
                    self.parent = web
                    self.position_on_web = 0
                    self.angle = web.vector().get_angle_between((0, -1))
                    break
                elif self.rect.collidepoint(web.end):
                    self.movement_state = movement_states.web_movement
                    self.rect.center = web.end
                    self.parent = web
                    self.position_on_web = web.vector().length
                    self.angle = web.vector().get_angle_between((0, -1))
                    break
        else:
            for region in movement.all_regions:
                if region.get_rect().colliderect(self.rect):
                    self.movement_state = movement_states.free_movement
                    self.parent = region
                    break
                    
    def try_create_web(self, location):
        for region in movement.all_regions:
            if region.get_rect().collidepoint(location):
                new_web = movement.Web(self.rect.center, location)
                self.movement_state = movement_states.web_movement
                self.rect.center = new_web.start
                self.parent = new_web
                self.position_on_web = 0
                return
    
    def proccess_event(self, event):
        if not self.dead():
            if event.type == pygame.KEYDOWN:
                if event.key == config.controls.web_shift:
                    self.switch_movement_state()
                elif event.key == config.controls.venom:
                    self.shoot()
                elif event.key == config.controls.bomb:
                    for buzzy in wasp.all_wasps:
                        if buzzy.webbed is True and buzzy.rect.colliderect(self.rect):
                            bomb.Bomb(buzzy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.movement = True
                elif event.button == 3:
                    for x in flingable.all_flingables:
                        if x.get_rect().collidepoint(event.pos):
                            self.fling_object = x
                            x.grab()
                            break
                    for enemy in frog.all_frogs + wasp.all_wasps:
                        if enemy.rect.collidepoint(event.pos):
                            self.web_enemy = enemy
                            break
                    if self.fling_object is None and self.web_enemy is None:
                        self.try_create_web(event.pos) 
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.movement = False
                elif event.button == 3:
                    if self.fling_object is not None:
                        self.fling(event.pos)
                    if self.web_enemy is not None:
                        self.web_enemy = None
                        self.web_enemy_time = 0
            elif event.type == pygame.MOUSEMOTION:
                self.movement_target = Vec2d(event.pos)
            
    def fling(self, target):
        if target is None:
            target = Vec2d(self.fling_object.location)
        else:
            target = Vec2d(target)
        force = (target - self.fling_object.location)/config.object.force_division_factor
        if force.length >= config.object.max_force:
            force.length = config.object.max_force
        self.fling_object.fling(force)
        music.play_whip()
        self.fling_object = None
        
    def invulnerable(self):
        return self.invuln > 0
    
    def dead(self):
        return self.dead_time > 0
    
    def update(self):
        self.web_ball_angle += config.spider.web_ball_rotation_rate
        if self.invuln > 0:
            self.invuln -= 1
            self.blink_time += 1
            if self.blink_time == config.spider.invuln_blink_rate:
                self.blink_time = -config.spider.invuln_blink_rate
            if self.invuln == 0:
                self.blink_time = 0
        if self.dead_time > 0:
            self.dead_time -= 1
            if self.dead_time == 0:
                self.respawn()
        else:
            self.charge.update()
            if self.web_enemy is not None:
                self.web_enemy_time += 1
                if self.web_enemy_time >= self.min_web_enemy_time:
                    self.web_enemy.web()
            if self.movement:
                movement_vector = self.movement_target - self.rect.center
                if self.movement_state == movement_states.free_movement:
                    dist = min(config.spider.free_movement.speed, distance(self.rect.center, self.movement_target))
                    if dist > 0:
                        movement_vector.length = dist
                    self.angle = movement_vector.get_angle_between((0, -1))
                    self.rect.center += movement_vector
                    #collision
                    self.parent.constrain_spider_movement(self)
                else:
                    true_movement = movement_vector.projection(self.parent.vector())
                    if true_movement.length > config.spider.web_movement.speed:
                        true_movement.length = config.spider.web_movement.speed
                    
                    #determine which way along the web to move. Test both x and y;
                    #otherwise bugs occur with perfectly vertical or horizontal lines
                    if (cmp(true_movement.x, 0) == cmp(self.parent.vector().x, 0) and
                            cmp(true_movement.y, 0) == cmp(self.parent.vector().y, 0)):
                        self.position_on_web += true_movement.length
                    else:
                        self.position_on_web -= true_movement.length
                    
                    if self.position_on_web < 0:
                        self.position_on_web = 0
                    elif self.position_on_web > self.parent.vector().length:
                        self.position_on_web = self.parent.vector().length
                    
                    self.angle = true_movement.get_angle_between((0, -1))
                    self.rect.center = self.parent.get_point(self.position_on_web)
    def draw(self, screen):
        if self.fling_object is not None:
            screen.line(config.web.color, self.rect.center, self.movement_target, config.web.thickness)
            screen.line(config.web.color, self.movement_target, self.fling_object.location, config.web.thickness)
            
        if self.web_enemy is not None:
            screen.line(config.web.color, self.rect.center, Vec2d(self.web_enemy.rect.center), config.web.thickness)
            rotated = pygame.transform.rotate(self.web_ball, self.web_ball_angle)
            screen.blit(rotated, rotated.get_rect(center = self.web_enemy.rect.center))
        
        if not self.dead() and self.blink_time >= 0:
            image = None
            if(self.movement == True):
                self.frame += 1
            if self.movement_state == movement_states.free_movement:
                image = self.free_movement_frames[int(self.frame/3)%len(self.free_movement_frames)]
            else:
                image = self.web_movement_frames[int(self.frame/3)%len(self.web_movement_frames)]
                
            rotated = pygame.transform.rotate(image, self.angle)
            screen.blit(rotated, rotated.get_rect(center = self.rect.center))
            self.charge.draw(screen)
            
        lives_image = self.f32.render("Lives = %d"%self.lives, 1, (255,255,255))
        screen.blit_UI(lives_image, (20,20))
        
    #note that it is possible to kill an invulnerable spider
    def kill(self):
        self.dead_time = frame_seconds(config.spider.dead_time)
        if not config.spider.infinite_lives:
            self.lives -= 1
        self.invuln = frame_seconds(config.spider.invuln_time) + self.dead_time
        if self.fling_object is not None:
            self.fling(None)
        if self.web_enemy is not None:
            self.web_enemy = None
            self.web_enemy_time = 0
        self.respawn_location = self.rect.center + Vec2d(self.dead_time, 0)
        self.rect.center = 0, 0
    
    def respawn(self):
        self.rect.center = self.respawn_location
        movement.WalkableRegion("respawn", center = self.respawn_location)
        self.switch_movement_state()
        self.blink_time = -config.spider.invuln_blink_rate
        self.charge.reset()
        
    def shoot(self):
        if self.charge.fire():
            music.play_venom()
            dir = Vec2d(config.spider.venom_speed, 0)
            dir.angle = self.angle * -1 - 90
            venom.Venom(self.rect.center, dir)