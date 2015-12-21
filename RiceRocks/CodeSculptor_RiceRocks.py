# program template for Spaceship
import simplegui
import math
import random

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

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

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
    
def rock_spawner():
    """timer handler that spawns a rock """
    global rock_num
    if rock_num < 12:
        flag = True
        while(flag):
            max_vel = 10 + score // 100 * rock_vel_increment	# increase rock vel every hundred score
            rock = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], 
                          [random.randrange(-max_vel, max_vel) * 0.1, random.randrange(-max_vel, max_vel) * 0.1], 
                          0, 
                          random.randrange(-10, 10) * 0.01, 
                          asteroid_image, 
                          asteroid_info)
            if not rock.collide(my_ship):
                flag = False
        rock_group.add(rock)
        rock_num += 1

def key_down(key):
    """key_down handler"""
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_angle_vel(-angle_vel)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(angle_vel)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def key_up(key):
    """key_up handler"""
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)

def mouse_handler(position):
    """mouse click event handler"""
    global game_over
    if game_over:
        game_over = False
        timer.start()
        soundtrack.rewind()
        soundtrack.play()
     
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
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 4.71, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()