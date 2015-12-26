import pygame
import rice_rocks
import random
import math

WIDTH = 800
HEIGHT = 600

# init pygame
pygame.init()
pygame.mixer.init()

# init screen, fps and quit flag
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
quit = False

# load resources
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
debris_info = rice_rocks.ImageInfo([320, 240], [640, 480])
debris_image = pygame.image.load("Resources\\Images\\debris2_blue.png").convert()
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = rice_rocks.ImageInfo([400, 300], [800, 600])
nebula_image = pygame.image.load("Resources\\Images\\nebula_blue.f2014.png").convert()
# splash image
splash_info = rice_rocks.ImageInfo([200, 150], [400, 300])
splash_image = pygame.image.load("Resources\\Images\\splash.png").convert()
# ship image
ship_info = rice_rocks.ImageInfo([45, 45], [90, 90], 35)
ship_image = pygame.image.load("Resources\\Images\\double_ship.png").convert()
# missile image - shot1.png, shot2.png, shot3.png
missile_info = rice_rocks.ImageInfo([5,5], [10, 10], 3, 50)
missile_image = pygame.image.load("Resources\\Images\\shot2.png").convert()
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = rice_rocks.ImageInfo([45, 45], [90, 90], 40)
asteroid_image = pygame.image.load("Resources\\Images\\asteroid_blue.png").convert()
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = rice_rocks.ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = pygame.image.load("Resources\\Images\\explosion_alpha.png").convert()
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = pygame.mixer.Sound("Resources\\Sounds\\soundtrack.ogg")
missile_sound = pygame.mixer.Sound("Resources\\Sounds\\missile.ogg")
pygame.mixer.Sound.set_volume(missile_sound, 0.5)
ship_thrust_sound = pygame.mixer.Sound("Resources\\Sounds\\thrust.ogg")
explosion_sound = pygame.mixer.Sound("Resources\\Sounds\\explosion.ogg")

# init game components
game = rice_rocks.Game(WIDTH, HEIGHT, ship_image, ship_info, 3)

# main loop
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# quit event
            quit = True
        elif event.type == pygame.USEREVENT + 1:# timer event            
            game.rock_spawn(asteroid_image, asteroid_info)
        elif event.type == pygame.KEYDOWN:# keydown event
            if event.key == pygame.K_UP:
                game.my_ship.set_thrust(True, ship_thrust_sound)
            elif event.key == pygame.K_LEFT:
                game.my_ship.set_angle_vel(-game.angle_vel)
            elif event.key == pygame.K_RIGHT:
                game.my_ship.set_angle_vel(game.angle_vel)
            elif event.key == pygame.K_SPACE:
                game.my_ship.shoot(game.missile_group, game.missile_vel_scale, missile_image, missile_info, missile_sound)
        elif event.type == pygame.KEYUP:# keyup event
            if event.key == pygame.K_UP:
                game.my_ship.set_thrust(False, ship_thrust_sound)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                game.my_ship.set_angle_vel(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:# mousedown event
            if event.button == 1:
                if game.game_over:
                    game.game_over = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                    soundtrack.play()
    screen.fill(0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()