'''
Created on Sep 17, 2011

@author: Nathan West
'''
import pygame
#Rule of thumb for the config file: no executable code. Only define constants
#that will be loaded later, like numbers and strings. If a string is a txt file,
#end its name with _file. If it's an image file, and its name with _image

#General
assets_folder = "Assets/"
#Display
class display:
    resolution = width, height = 1260, 980
    frame_rate = 30
    backgrounds_file = assets_folder + "Backgrounds.txt"
    pixels_per_frame = 1
    paralax_factor = 2
    fullscreen = True
#Controls
class controls:
    venom = pygame.K_f
    bomb = pygame.K_d
    web_shift = pygame.K_SPACE
#Spider
class spider:
    starting_postion = 100, 100
    starting_lives = 3
    invuln_time = 3
    invuln_blink_rate = 5 #frames per blink
    dead_time = 3
    infinite_lives = True
    
    min_enemy_web_time = 1
    web_ball_image = assets_folder + "Items/webBall.png"
    web_ball_rotation_rate = 40
    
    venom_speed = 40
    venom_regen_time = 5 #seconds to get from 0 to full
    min_venom_charge = .25 #float, 0-1, required to fire venom
    border_image = assets_folder + "bar.png"
    bar_image = assets_folder + "innerBar.png"
    bar_center = (display.width/2, 900)
    class free_movement:
        speed = 6
        file = assets_folder + "FreeSpiderFrames.txt"
        frames_per_frame = 3
        
    class web_movement:
        speed = 10
        file = assets_folder + "WebSpiderFrames.txt"
        frames_per_frame = 3
#Webbing
class web:
    color = 255, 255, 255
    thickness = 1
    web_spray_image = assets_folder + "Dudes/Spider/EndWeb.png"

#Frog
class frog:
    head_file = assets_folder + "FrogHeadFrames.txt"
    body_image = assets_folder + "Dudes/Enemies/Frog/frogBody.png"
    webbed_image = assets_folder + "Dudes/Enemies/Frog/webbedClosed copy.png"
    webbed_body_image = assets_folder + "Dudes/Enemies/Frog/frogBodyWebbed.png"
    tongue_tip = assets_folder + "Dudes/Enemies/Frog/Tongue.png"
    tongue_color = (255, 0, 0)
    tongue_thickness = 15
    fire_range = 1000
    time_aiming = 3
    time_charging = 1
    time_shooting = .25
    head_center = 18, 18
    time_webbed = 3

#Wasp
class wasp:
    file = assets_folder + "WaspFrames.txt"
    velocicty = (-3, 3)
    #move_time is in frames
    move_time = 60
    #move_time is the amount of time it takes for the wasp to move from the bottom to the top, and visa versa
    frame_rate = 1
    web_time = 3
    death_jump = (0, -5)
    
#Hand
class hand:
    file = assets_folder + "HandFrames.txt"
    move = 100
    vel = 6
    life_span = 120
    clock = 100
    start_frame = 5300
    spawn_clock = 150
    
#Bird
class bird:
    bird_file = assets_folder + "BirdFrames.txt"
    hp = 10
    frame_rate = 1
    yaccl = -0.25

#object
class object:
    gravity = (0, 1) #woo omnidirectional gravity
    max_force = 500
    force_division_factor = 10
    
class bomb:
    image = assets_folder + "Dudes/Spider/eggSac.png"
    explode_time = 2
    babies_made_min = 20
    babies_made_max = 40
    baby_spray_min = 5
    baby_spay_max = 35