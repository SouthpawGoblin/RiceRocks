# program template for Spaceship
import pygame
import math
import random

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def set_angle_vel(self, vel):
        self.angle_vel = vel
        
    def set_thrust(self, flag, sound):
        self.thrust = flag
        if self.thrust:
            sound.play()
        else:
            sound.stop()
    
    def shoot(self, missile_group, missile_vel_scale, missile_image, missile_info, missile_sound):
        forward_vector = angle_to_vector(self.angle)
        missile_group.add(Game.Sprite([self.pos[0] + self.radius * forward_vector[0], self.pos[1] + self.radius * forward_vector[1]], 
                            [forward_vector[0] * missile_vel_scale + self.vel[0], forward_vector[1] * missile_vel_scale + self.vel[1]], 
                            self.angle, 
                            0, 
                            missile_image, 
                            missile_info, 
                            missile_sound))
    
    def draw(self, screen):
        if not self.thrust:
            im = pygame.transform.rotate(self.image, (self.angle / math.pi) * 180)
            screen.blit(self.image, (self.pos[0] - self.image_center[0], self.pos[1] - self.image_center[1]))
        else:
            canvas.draw_image(self.image, 
                                [self.image_center[0] + self.image_size[0], self.image_center[1]], 
                                self.image_size, 
                                self.pos, 
                                self.image_size, 
                                self.angle)

    def update(self):
        dimension = 2
        forward_vector = angle_to_vector(self.angle)
        for i in range(dimension):
            if self.thrust:
                self.vel[i] += forward_vector[i] * ship_acc_scale
            self.vel[i] *= ship_vel_scale
            self.pos[i] += self.vel[i]
            self.pos[i] %= [WIDTH, HEIGHT][i]
        self.angle += self.angle_vel 
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius()

    def draw(self, canvas):
        im_center = []
        if self.animated:
            im_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
        else:
            im_center = self.image_center                         
        canvas.draw_image(self.image, 
                            im_center, 
                            self.image_size, 
                            self.pos, 
                            self.image_size, 
                            self.angle)
    
    def update(self):
        dimension = 2
        for i in range(dimension):
            self.pos[i] += self.vel[i]
            self.pos[i] %= [WIDTH, HEIGHT][i]
        self.angle += self.angle_vel
        self.age += 1
        return True if self.age >= self.lifespan else False

class Game:
    def __init__(self, wid, ht, init_ship_im, init_ship_info, max_life=3):
        self.__max_life = max_life
        self.width = wid
        self.height = ht
        self.my_ship = Ship([wid / 2, ht / 2], [0, 0], 4.71, init_ship_im, init_ship_info)
        self.rock_group = set([])
        self.missile_group = set([])
        self.explosion_group = set([])
        self.score = 0
        self.lives = max_life
        self.time = 0
        self.rock_num = 0
        self.game_over = True
        self.rock_vel_increment = 1	
        self.angle_vel = 0.05		# ship's angle velocity
        self.missile_vel_scale = 5	# missile's scale factor to multiply forward vector
        self.ship_vel_scale = 0.99	# ship's friction factor
        self.ship_acc_scale = 0.1	# ship's acceleration scale factor

    def process_sprite_group(sprite_group, screen):
        """update and draw a group of sprites"""
        for sprite in set(sprite_group):
            if sprite.update():
                sprite_group.discard(sprite)
            else:
                sprite.draw(screen)

    def group_collide(group, other_object, expl_im, expl_info, expl_sound):
        """judge if a group of sprites has collision with another object"""
        flag = False
        for sprite in set(group):
            if sprite.collide(other_object):
                group.discard(sprite)
                explosion_group.add(Sprite(sprite.get_position(), 
                                           [0, 0], 
                                           0, 
                                           0, 
                                           expl_im, 
                                           expl_info, 
                                           expl_sound))
                flag = True
        return flag

    def group_group_collide(group1, group2):
        """calculate how many collisions does two group of sprites have"""
        count = 0
        for sprite in set(group1):
            if group_collide(group2, sprite):
                count += 1
                group1.discard(sprite)
        return count



    def rock_spawn(self, asteroid_image, asteroid_info):
        """spawn a rock and adds it to the rock_group"""
        if self.rock_num < 12:
            flag = True
            while(flag):
                max_vel = 10 + self.score // 100 * self.rock_vel_increment	# increase rock vel every hundred score
                rock = Sprite([random.randrange(self.width), random.randrange(self.height)], 
                                [random.randrange(-max_vel, max_vel) * 0.1, random.randrange(-max_vel, max_vel) * 0.1], 
                                0, 
                                random.randrange(-10, 10) * 0.01, 
                                asteroid_image, 
                                asteroid_info)
                if not rock.collide(self.my_ship):
                    flag = False
            self.rock_group.add(rock)
            self.rock_num += 1
              
    def draw(canvas):
        """draw handler"""
        global time, lives, score, rock_num, game_over
   
        # animiate background
        time += 1
        wtime = (time / 4) % WIDTH
        center = debris_info.get_center()
        size = debris_info.get_size()
        canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
        canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))   
    
        # draw ship
        my_ship.draw(canvas)
    
        if game_over:
            new_game()
            canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        else:
            # update ship
            my_ship.update()

            process_sprite_group(rock_group, canvas)
            process_sprite_group(missile_group, canvas)
            process_sprite_group(explosion_group, canvas)

            if group_collide(rock_group, my_ship):
                rock_num -= 1
                lives -= 1

            collide_num = group_group_collide(missile_group, rock_group)
            rock_num -= collide_num
            score += 10 * collide_num

            if lives < 1:
                game_over = True
            
        # draw text
        canvas.draw_text("Lives: " + str(lives), [WIDTH - 120, 24], 24, "White")
        canvas.draw_text("Score: " + str(score), [0, 24], 24, "White")  
     
    def new_game(self):
        """initialize a new game"""
        self.my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 4.71, ship_image, ship_info)
        self.rock_group = set([])
        self.missile_group = set([])
        self.explosion_group = set([])
        self.lives = 3
        self.score = 0
        self.rock_num = 0    