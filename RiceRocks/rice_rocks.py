# program template for Spaceship
import math
import random

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

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(sprite_group, canvas):
    """update and draw a group of sprites"""
    for sprite in set(sprite_group):
        if sprite.update():
            sprite_group.discard(sprite)
        else:
            sprite.draw(canvas)

def group_collide(group, other_object):
    """judge if a group of sprites has collision with another object"""
    flag = False
    for sprite in set(group):
        if sprite.collide(other_object):
            group.discard(sprite)
            explosion_group.add(Sprite(sprite.get_position(), 
                                       [0, 0], 
                                       0, 
                                       0, 
                                       explosion_image, 
                                       explosion_info, 
                                       explosion_sound))
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
        
    def set_thrust(self, flag):
        self.thrust = flag
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
    
    def shoot(self):
        forward_vector = angle_to_vector(self.angle)
        missile_group.add(Sprite([self.pos[0] + self.radius * forward_vector[0], self.pos[1] + self.radius * forward_vector[1]], 
                          [forward_vector[0] * missile_vel_scale + self.vel[0], forward_vector[1] * missile_vel_scale + self.vel[1]], 
                          self.angle, 
                          0, 
                          missile_image, 
                          missile_info, 
                          missile_sound))
    
    def draw(self,canvas):
        if not self.thrust:
            canvas.draw_image(self.image, 
                              self.image_center, 
                              self.image_size, 
                              self.pos, 
                              self.image_size, 
                              self.angle)
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
     
def new_game():
    """initialize a new game"""
    global my_ship, rock_group, missile_group, lives, score, rock_num
    timer.stop()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 4.71, ship_image, ship_info)
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    lives = 3
    score = 0
    rock_num = 0    