import pygame
import rice_rocks
import random
import math

# init pygame
pygame.init()

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
rock_num = 0
game_over = True
rock_vel_increment = 1	
angle_vel = 0.05		# ship's angle velocity
missile_vel_scale = 5	# missile's scale factor to multiply forward vector
ship_vel_scale = 0.99	# ship's friction factor
ship_acc_scale = 0.1	# ship's acceleration scale factor

# init screen, fps and quit flag
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
quit = False

# load resources
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
debris_info = rice_rocks.ImageInfo([320, 240], [640, 480])
debris_image = pygame.image.load("Resources\\Images\\debris2_blue.png")
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = rice_rocks.ImageInfo([400, 300], [800, 600])
nebula_image = pygame.image.load("Resources\\Images\\nebula_blue.f2014.png")
# splash image
splash_info = rice_rocks.ImageInfo([200, 150], [400, 300])
splash_image = pygame.image.load("Resources\\Images\\splash.png")
# ship image
ship_info = rice_rocks.ImageInfo([45, 45], [90, 90], 35)
ship_image = pygame.image.load("Resources\\Images\\double_ship.png")
# missile image - shot1.png, shot2.png, shot3.png
missile_info = rice_rocks.ImageInfo([5,5], [10, 10], 3, 50)
missile_image = pygame.image.load("Resources\\Images\\shot2.png")
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = rice_rocks.ImageInfo([45, 45], [90, 90], 40)
asteroid_image = pygame.image.load("Resources\\Images\\asteroid_blue.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = rice_rocks.ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = pygame.image.load("Resources\\Images\\explosion_alpha.png")
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = pygame.mixer.Sound("Resources\\Sounds\\soundtrack.mp3")
missile_sound = pygame.mixer.Sound("Resources\\Sounds\\missile.mp3")
pygame.mixer.Sound.set_volume(missile_sound, 0.5)
ship_thrust_sound = pygame.mixer.Sound("Resources\\Sounds\\thrust.mp3")
explosion_sound = pygame.mixer.Sound("Resources\\Sounds\\explosion.mp3")

# init game components
my_ship = rice_rocks.Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 4.71, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# set a timer to spawn rocks
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

# main loop
while not quit:
    screen.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# quit event
            quit = True
        elif event.type == pygame.USEREVENT + 1:# timer event            
            if rock_num < 12:
                flag = True
                while(flag):
                    max_vel = 10 + score // 100 * rock_vel_increment	# increase rock vel every hundred score
                    rock = rice_rocks.Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], 
                                  [random.randrange(-max_vel, max_vel) * 0.1, random.randrange(-max_vel, max_vel) * 0.1], 
                                  0, 
                                  random.randrange(-10, 10) * 0.01, 
                                  asteroid_image, 
                                  asteroid_info)
                    if not rock.collide(my_ship):
                        flag = False
                rock_group.add(rock)
                rock_num += 1
        elif event.type == pygame.KEYDOWN:# keydown event
            if event.key == pygame.K_UP:
                my_ship.set_thrust(True)
            elif event.key == pygame.K_LEFT:
                my_ship.set_angle_vel(-angle_vel)
            elif event.key == pygame.K_RIGHT:
                my_ship.set_angle_vel(angle_vel)
            elif event.key == pygame.K_SPACE:
                my_ship.shoot()
        elif event.type == pygame.KEYUP:# keyup event
            if event.key == pygame.K_UP:
                my_ship.set_thrust(False)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                my_ship.set_angle_vel(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:# mousedown event
            if event.button == 1:
                if game_over:
                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                    soundtrack.play()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()