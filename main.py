'''
Created on Sep 11, 2011

@author: Nathan West
'''

import pygame
from vec2d import Vec2d
import config
import movement
from spider import Spider
import screen
import frog
import wasp
import stinger
import venom
import flingable
import bird
import bomb
import music
import hand

#loading screen
screen = screen.Screen()
loading = pygame.image.load("Assets/loadingScreen.png")
screen.blit_UI(loading, (0, 0))
pygame.display.flip()

main_menu = pygame.image.load("Assets/titleScreen.png")
instructions = pygame.image.load("Assets/Instructions.png")
victory = pygame.image.load("Assets/YouWin.png")
start_rect = pygame.Rect(561, 745, 172, 80)
instructions_rect = pygame.Rect(543, 820, 213, 64)
victory_rect = pygame.Rect(8000, 96, 364, 229)
#===============================================================================
#ASSETS LOAD
#===============================================================================
movement.WalkableRegionType("tree1", "World/Foreground/treeTrunk.png")                        
movement.WalkableRegionType("tree2", "World/Foreground/tree2.png", (84, 0, 133, 980))         
movement.WalkableRegionType("tree3", "World/Foreground/tree3.png", (84, 0, 133, 980))       
movement.WalkableRegionType("tree4", "World/Foreground/HugeTrunk copy.png")  
movement.WalkableRegionType("bathroom", "World/Foreground/foreground (1).png")               
movement.WalkableRegionType("bathroom toothbrush", "World/Foreground/foreground (2).png")               
movement.WalkableRegionType("bathroom sink", "World/Foreground/foreground (3).png")               
movement.WalkableRegionType("bathroom window", "World/Foreground/foreground (4).png")               
movement.WalkableRegionType("hallway1", "World/Foreground/foreground (5).png")                
movement.WalkableRegionType("hallway2", "World/Foreground/foreground (6).png")                
movement.WalkableRegionType("hallway3", "World/Foreground/foreground (7).png")                
movement.WalkableRegionType("kitchen1", "World/Foreground/foreground (8).png")                
movement.WalkableRegionType("kitchen1", "World/Foreground/foreground (9).png")                
movement.WalkableRegionType("kitchen1", "World/Foreground/foreground (10).png")
movement.WalkableRegionType("window", "World/Foreground/foreground (15).png")  
movement.WalkableRegionType("tree branch", "World/Foreground/treeBranch.png", (0, 80, 420, 75))
movement.WalkableRegionType("web bridge", "World/Foreground/webBridge.png")
movement.WalkableRegionType("respawn", "Dudes/Spider/largeWeb.png")

flingable.FlingableType("acorn", "Items/acorn.png", "Items/acorn_webbed.png")
flingable.FlingableType("rock", "Items/rock.png", "Items/rock_webbed.png")
flingable.FlingableType("male spider", "Items/maleSpider.png", "Items/maleSpiderWebbed.png")
flingable.FlingableType("spiderling", "Dudes/Spider/babySpider1.png", None)
flingable.FlingableType("branch", "World/Decals/branch.png", "World/Decals/webbedBranch.png")

#===============================================================================
# LEVEL LOAD
#===============================================================================
spider = None
frames = 0
def load_level():
    screen.blit_UI(loading, (0, 0))
    pygame.display.flip()
    global spider
    global frames
    frames = 0
    movement.clear()
    bird.clear()
    bomb.clear()
    flingable.clear()
    frog.clear()
    hand.clear()
    stinger.clear()
    venom.clear()
    wasp.clear()
    screen.reset()
    
    start_region = movement.WalkableRegion("tree4", topleft = (0, 0))
    movement.WalkableRegion("tree branch", center = (1085, 360))
    movement.WalkableRegion("web bridge", center = (2125, 810))
    movement.WalkableRegion("web bridge", center = (2695, 107))
    movement.WalkableRegion("web bridge", center = (4135, 660))
    movement.WalkableRegion("tree branch", center = (4785, 295))
    movement.WalkableRegion("tree branch", center = (4785, 510))
    movement.WalkableRegion("tree branch", center = (4785, 725))
    movement.WalkableRegion("tree2", topleft = (520, 0))
    movement.WalkableRegion("tree3", topleft = (725, 0))
    movement.WalkableRegion("tree1", topleft = (1205, 0))
    movement.WalkableRegion("tree1", topleft = (1680, 0))
    movement.WalkableRegion("tree1", topleft = (2235, 0))
    movement.WalkableRegion("tree4", topleft = (2810, 0))
    movement.WalkableRegion("tree3", topleft = (3320, 0))
    movement.WalkableRegion("tree1", topleft = (3735, 0))
    movement.WalkableRegion("tree4", topleft = (4207, 0))
    movement.WalkableRegion("tree4", topleft = (4915, 0))
    movement.WalkableRegion("bathroom toothbrush", topleft = (5357, 0))
    movement.WalkableRegion("bathroom sink", topleft = (6268, 0))
    movement.WalkableRegion("bathroom window", topleft = (7362, 0))
    movement.WalkableRegion("window", topleft = (5357, 0))
    
    flingable.Flingable("rock", (645, 410))
    flingable.Flingable("acorn", (1310, 140))
    flingable.Flingable("acorn", (1403, 175))
    flingable.Flingable("acorn", (1482, 205))
    flingable.Flingable("acorn", (1400, 267))
    flingable.Flingable("rock", (1310, 635))
    flingable.Flingable("rock", (1430, 665))
    flingable.Flingable("branch", (1430, 735))
    flingable.Flingable("rock", (1807, 293))
    flingable.Flingable("rock", (1770, 410))
    flingable.Flingable("acorn", (1870, 450))
    flingable.Flingable("acorn", (2395, 205))
    flingable.Flingable("rock", (2460, 710))
    flingable.Flingable("branch", (2410, 535))
    flingable.Flingable("acorn", (2935, 230))
    flingable.Flingable("rock", (3075, 330))
    flingable.Flingable("rock", (2945, 500))
    flingable.Flingable("acorn", (3105, 505))
    flingable.Flingable("rock", (3040, 700))
    flingable.Flingable("acorn", (3475, 335))
    flingable.Flingable("rock", (3805, 325))
    flingable.Flingable("rock", (3960, 460))
    flingable.Flingable("rock", (3840, 615))
    flingable.Flingable("rock", (4345, 390))
    flingable.Flingable("rock", (4540, 500))
    flingable.Flingable("branch", (4435, 720))
    
    wasp.Wasp(1100,235)
    wasp.Wasp(1155,500)
    wasp.Wasp(1255,265)
    wasp.Wasp(1940,165)
    wasp.Wasp(1940,320)
    wasp.Wasp(1940,410)
    wasp.Wasp(1940,775)
    wasp.Wasp(2372,320)
    wasp.Wasp(2640,475)
    wasp.Wasp(2760,630)
    wasp.Wasp(2815,355)
    wasp.Wasp(2865,805)
    wasp.Wasp(3685,680)
    wasp.Wasp(4105,345)
    wasp.Wasp(4490,205)
    wasp.Wasp(4665,555)
    wasp.Wasp(4785,725)
    wasp.Wasp(4940,610)
    wasp.Wasp(4995,270)
    wasp.Wasp(5100,470)
    wasp.Wasp(5195,730)
    wasp.Wasp(6135,760)
    wasp.Wasp(6770,360)
    wasp.Wasp(7320,280)
    wasp.Wasp(7640,700)
    
    high = -10, 10
    med = -15, 15
    low = -18, 18
    bird.Bird((2675, 100), med, -.25)
    bird.Bird((3705, 100), high, -.25)
    bird.Bird((3925, 100), low, -.25)
    bird.Bird((4635, 100), low, -.25)
    bird.Bird((4995, 100), med, -.25)
    bird.Bird((5315, 100), high, -.25)
    
    frog.Frog((1850, 980))
    frog.Frog((3250, 980)) 
    frog.Frog((3915, 980)) 
    frog.Frog((4455, 980)) 
    frog.Frog((4788, 980)) 
    frog.Frog((5135, 980)) 
    
    spider = Spider(start_region)
    music.music_begin()
    music.play_music()

#===============================================================================
# GAME RUN
#===============================================================================

stop = False
timer = pygame.time.Clock()
menu = 0 #0 = main, 1 = instructions, 2 = game, 3 = victory

while stop == False:
    if menu == 2:
        #Draw
        screen.draw()
        for region in movement.all_regions:
            region.draw(screen)
        for web in movement.all_webs:
            web.draw(screen)
        for item in flingable.all_flingables:
            item.draw(screen)
        for item in flingable.all_flung:
            item.draw(screen)
        for ugly in frog.all_frogs:
            ugly.draw(screen)
        for buzzy in wasp.all_wasps:
            buzzy.draw(screen)
        for doom in bomb.all_bombs:
            doom.draw(screen)
        for humming in bird.all_birds:
            humming.draw(screen)
            
        spider.draw(screen)
        for bullet in stinger.all_bullets:
            bullet.draw(screen)
        for shot in venom.all_shots:
            shot.draw(screen)
        for smash in hand.all_hands:
            smash.draw(screen)
            
        pygame.display.flip()
        
        #events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                menu = 0
                music.stop_music()
            else:
                #convert mouse coordinates if needed
                event2 = event
                #this is the most unpythonic code ever written. It has to be done, as event objects are immutable
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    event2 = pygame.event.Event(event.type, pos = event.pos - Vec2d(screen.offset, 0), button = event.button) #compensate for  screen movement
                elif event.type == pygame.MOUSEMOTION:
                    event2 = pygame.event.Event(event.type, pos = event.pos - Vec2d(screen.offset, 0))
                spider.proccess_event(event2)
        
        #logic
        screen.update()
        spider.update()
        frog.update_frogs(screen, spider)
        bird.update_birds(screen)
        wasp.update_wasps(screen)
        stinger.update_bullets(screen)
        venom.update_shots(screen)
        flingable.update_flingables(screen)
        bomb.update_bombs()
        hand.update_hands(spider, frames)
        movement.update_movement(screen)
        
        #kill wasps and stingers with flingables
        for x in flingable.all_flung:
            #needs to be a while loop 
            for pointy in stinger.all_bullets:
                if pointy.rect.colliderect(x.get_rect()):
                    pointy.kill()
            for buzzy in wasp.all_wasps:
                if x.get_rect().colliderect(buzzy.rect):
                    buzzy.kill()
        
        #kill spider with stingers 
        collide = spider.rect.collidelist(stinger.all_bullets)
        if collide != -1:
            stinger.all_bullets[collide].kill()
            if not spider.invulnerable():
                spider.kill()
        
        #kill spider with frog tongue
        for sticky in frog.tongues:
            if sticky.get_rect().colliderect(spider.rect) and not spider.invulnerable():
                spider.kill()
                
        #kill spider with wasps
        for evil in wasp.all_wasps:
            if evil.rect.colliderect(spider.rect) and not spider.invulnerable() and not evil.webbed and not evil.dead:
                spider.kill()
        
        #kill spider with hands
        for smash in hand.all_hands:
            if smash.rect.colliderect(spider.rect) and not spider.invulnerable() and smash.down:
                spider.kill()
        
        #kill wasps with venom
        for burning in venom.all_shots:
            for buzzy in wasp.all_wasps:
                if burning.rect.colliderect(buzzy.rect):
                    buzzy.kill()
                    burning.kill()
                    
        #kill spider with birds
        for humming in bird.all_birds:
            if humming.rect.colliderect(spider.rect) and not spider.invulnerable():
                spider.kill()
        
        #kill spider with screen
        if not screen.get_rect().colliderect(spider.rect) and not spider.invulnerable():
            spider.kill()
            
        if spider.lives == 0:
            menu = 0
            music.stop_music()
            
        if victory_rect.collidepoint(spider.rect.center):
            menu = 0
            music.stop_music()
            
        timer.tick(config.display.frame_rate)
        frames += 1
    elif menu == 0:
        #main menu
        screen.blit_UI(main_menu, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    load_level()
                    menu = 2
                elif instructions_rect.collidepoint(event.pos):
                    menu = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True
        timer.tick(config.display.frame_rate)
    elif menu == 1:
        #instructions screen
        screen.blit_UI(instructions, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                menu = 0
        timer.tick(config.display.frame_rate)
    #===========================================================================
    # elif menu == 3:
    #    screen.blit_UI(victory, (0, 0))
    #    pygame.display.flip()
    #    for event in pygame.event.get():
    #        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
    #            menu = 0
    #    timer.tick(config.display.frame_rate)
    #===========================================================================
