import sys, os, py_compile, subprocess, time, pickle, imp


def compile_and_execute():
    name = sys.argv[0].split('/')[-1]
    extension = name.split('.')[1]
    if extension == 'py':
        print('Compiling ' + name)
        py_compile.compile(name)
        pycname = name.split('.')[0] + '.pyc'
        print('Executing ' + pycname)
        subprocess.call(['python', pycname])
        time.sleep(0.1)
        # print('Removing ' + pycname)
        # os.remove(pycname)
        quit()

# Uncomment to enable compiled mode
#compile_and_execute()

import pygame, math, random, copy, gc

pygame.init()

# CONSTANTS
LIBRARY_VERSION = 3.0

# Colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
CYAN = [0, 255, 255]
YELLOW = [255, 255, 0]
MAGENTA = [255, 0, 255]
PINK = [255, 192, 203]
TURQUOISE = [64, 224, 208]
ORANGE = [255, 165, 0]
SILVER = [192, 192, 192]
GREY = [128, 128, 128]
VIOLET = [238, 130, 238]
PURPLE = [128, 0, 128]
TOMATO = [255, 99, 71]
BEIGE = [245, 245, 220]
LAVENDER = [230, 230, 250]

COLORS = [RED,
          GREEN,
          BLUE,
          YELLOW,
          BLACK,
          WHITE,
          CYAN,
          YELLOW,
          MAGENTA,
          PINK,
          TURQUOISE,
          ORANGE,
          SILVER,
          GREY,
          VIOLET,
          PURPLE,
          TOMATO,
          BEIGE,
          LAVENDER]

SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

# ADVANCED_MODE = False

# Collisions results
COLLISION = pygame.sprite.Sprite()

# Class for Game Info
class GameInfo:
    def __init__(self):
        self.framerate = 60
        self.tagged_actors = {}


game_info = GameInfo()


def framerate(fps):
    game_info.framerate = fps


# OBJECTS FOR DATA STORAGE
class EventsStorage():
    def __init__(self):
        self.CHECK = False
        self.list = []


events_storage = EventsStorage()


class MouseState:
    def __init__(self):
        self.left = False
        self.leftdown = False
        self.leftup = False
        self.central = False
        self.centraldown = False
        self.centralup = False
        self.right = False
        self.rightdown = False
        self.rightup = False
        self.position = pygame.mouse.get_pos()
        self.x = self.position[0]
        self.y = self.position[1]
        self.hidden = False

    def hide(self):
        pygame.mouse.set_visible(False)
        self.hidden = True

    def show(self):
        pygame.mouse.set_visible(True)
        self.hidden = False

    def update_events(self):
        self.position = pygame.mouse.get_pos()
        self.x = MOUSE.position[0]
        self.y = MOUSE.position[1]
        buttons = pygame.mouse.get_pressed()
        # Left
        if buttons[0] == 0 and self.left is True:
            self.leftup = True
        else:
            self.leftup = False
        if self.leftdown is True:
            self.leftdown = False
        if self.left is False:
            self.leftdown = bool(buttons[0])
        self.left = bool(buttons[0])
        # Central
        if buttons[1] == 0 and self.central is True:
            self.centralup = True
        else:
            self.centralup = False
        if self.centraldown is True:
            self.centraldown = False
        if self.central is False:
            self.centraldown = bool(buttons[1])
        self.central = bool(buttons[1])
        # Right
        if buttons[2] == 0 and self.right is True:
            self.rightup = True
        else:
            self.rightup = False
        if self.rightdown is True:
            self.rightdown = False
        if self.right is False:
            self.rightdown = bool(buttons[2])
        self.right = bool(buttons[2])


MOUSE = MouseState()


class ScreenInfo:
    def __init__(self):
        self.screen = None
        self.resolution = [800, 600]
        self.pen_surface = pygame.Surface([32, 32])
        self.has_background = False
        self.bg_color = BLACK
        self.backgrounds = {}
        self.background = None


screen_info = ScreenInfo()


class ActorsInfo:
    def __init__(self):
        self.actors_list = []
        self.draw_list = []
        self.paused_actors_list = []
        self.hidden_actors_list = []
        self.glide_list = []
        self.counts = []


actors_info = ActorsInfo()

# Screen Center Constant
CENTER = pygame.sprite.Sprite()


def create_pen_surface():
    path = (os.path.dirname(sys.modules[__name__].__file__))
    path = os.path.join(path, 'pensurface.png')
    screen_info.pen_surface = pygame.image.load(path).convert_alpha()
    screen_info.pen_surface = pygame.transform.scale(screen_info.pen_surface, screen_info.resolution)


class ColorsInfo:
    def __init__(self):
        self.color_scale_phase = 'g_up'
        self.r = 255
        self.g = 0
        self.b = 0


colors_info = ColorsInfo()


def colorscale(interval=1):
    if colors_info.color_scale_phase == 'g_up':
        if colors_info.g + interval <= 255:
            colors_info.g += interval
        else:
            colors_info.color_scale_phase = 'r_down'
    elif colors_info.color_scale_phase == 'r_down':
        if colors_info.r - interval >= 0:
            colors_info.r -= interval
        else:
            colors_info.color_scale_phase = 'b_up'
    elif colors_info.color_scale_phase == 'b_up':
        if colors_info.b + interval <= 255:
            colors_info.b += interval
        else:
            colors_info.color_scale_phase = 'g_down'
    elif colors_info.color_scale_phase == 'g_down':
        if colors_info.g - interval >= 0:
            colors_info.g -= interval
        else:
            colors_info.color_scale_phase = 'r_up'
    elif colors_info.color_scale_phase == 'r_up':
        if colors_info.r + interval <= 255:
            colors_info.r += interval
        else:
            colors_info.color_scale_phase = 'b_down'
    elif colors_info.color_scale_phase == 'b_down':
        if colors_info.b - interval >= 0:
            colors_info.b -= interval
        else:
            colors_info.color_scale_phase = 'g_up'
    return [colors_info.r, colors_info.g, colors_info.b]



# SCREEN
def screen(w, h, fullscreen=False):
    screen_info.resolution = [w, h]
    if fullscreen:
        screen_info.screen = pygame.display.set_mode([w, h], pygame.FULLSCREEN)
    else:
        screen_info.screen = pygame.display.set_mode([w, h])
    # Create surface for turtle drawings
    create_pen_surface()
    # Get screen center
    CENTER.x = screen_info.resolution[0] / 2
    CENTER.y = screen_info.resolution[1] / 2


def SCREEN(*args):
    screen(*args)


def fill(color):
    screen_info.has_background = False
    screen_info.bg_color = color


def clear():
    create_pen_surface()


def find_file_name(path):
    words = path.split('/')
    name = words[-1]
    return name.split('.')[0]


def background(path):
    screen_info.has_background = True
    screen_info.background = pygame.image.load(path).convert()
    screen_info.background = pygame.transform.scale(screen_info.background,
                                                    screen_info.resolution)
    screen_info.backgrounds[find_file_name(path)] = screen_info.background
    screen_info.screen.blit(screen_info.background, (0, 0))


def loadbackground(path):
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.scale(bg, screen_info.resolution)
    screen_info.backgrounds[find_file_name(path)] = bg


def setbackground(name):
    screen_info.has_background = True
    screen_info.background = screen_info.backgrounds[name]
    screen_info.screen.blit(screen_info.background, (0, 0))


default_clock = pygame.time.Clock()


# GLIDING
def process_gliding():
    for item in actors_info.glide_list:
        item[0].point(item[1], item[2])
        if (abs(int(item[0].x) - item[1]) > 5) or (abs(int(item[0].y) - item[2]) > 5):
            item[0].forward(item[3])
        else:
            item[0].goto(item[1], item[2])
            item[0].gliding = False
            actors_info.glide_list.remove(item)


# Actors-to-transform_rotate_image GROUP
ACTORS = pygame.sprite.LayeredUpdates()


def Clock():
    return pygame.time.Clock()


def wait(ms):
    pygame.time.wait(ms)


def ticks():
    return pygame.time.get_ticks()


# def copy_cos_dict(target):
#     newdict = target.copy()
#     for k in newdict:
#         newdict[k]['image'] = target[k]['image'].copy()
#     print 'DEBUG CLONE DICT'
#     # print newdict['age_uke\\age_uke_011']['image'] is target['age_uke\\age_uke_011']['image'].copy()
#     return newdict


def clone(target):
    # clonedActor = copy.copy(target)
    # actors_info.actors_list.append(clonedActor)
    # clonedActor.update_rect()
    # if not target.hidden:
    #     ACTORS.add(clonedActor)
    # return clonedActor
    cloned_actor = Actor(target.path)
    cloned_actor.x = target.x
    cloned_actor.y = target.y
    # Actor angle direction
    cloned_actor.direction = target.direction
    # image orientation
    cloned_actor.heading = target.heading
    # cloned_actor.layer = target.layer
    ACTORS.change_layer(cloned_actor, target.layer)
    cloned_actor.count = 0
    cloned_actor.paused = False
    if target.hidden:
        cloned_actor.hide()
    cloned_actor.pause_time = 0.0
    cloned_actor.hide_time = 0.0
    cloned_actor.start_pause_time = 0.0
    cloned_actor.start_hide_time = 0.0
    # load actor image
    cloned_actor.costumes = copy.deepcopy(target.costumes)
    cloned_actor.costume = target.costume
    cloned_actor.cosnumber = target.cosnumber

    # Cloning dict cos by name
    # cloned_actor.costumes_by_name = copy_cos_dict(target.costumes_by_name)
    cloned_actor.costumes_by_name = {}
    for k in target.costumes_by_name:
        img = target.costumes_by_name[k]['image'].copy()
        num = target.costumes_by_name[k]['number']
        cloned_actor.costumes_by_name[k] = {'image': img, 'number': num}

    # Cloning dict cos by number
    cloned_actor.costumes_by_number = {}
    for k in target.costumes_by_number:
        img = target.costumes_by_number[k]['image'].copy()
        name = target.costumes_by_number[k]['name']
        cloned_actor.costumes_by_number[k] = {'image': img, 'name': name}

    # Cloning original costumes dict
    # print 'DEBUG CLONING COS BY NAME'
    # print cloned_actor.costumes_by_name['age_uke\\age_uke_013']['image'] is target.costumes_by_name['age_uke\\age_uke_013']['image']
    # print 'DEBUG CLONING COS BY NNUMBER'
    # print cloned_actor.costumes_by_number[3] is target.costumes_by_number[3]
    cloned_actor.original_costumes = {}
    for k in target.original_costumes:
        cloned_actor.original_costumes[k] = target.original_costumes[k].copy()
    # print 'DEBUG CLONING ORIGINALS'
    # print cloned_actor.original_costumes['age_uke\\age_uke_013'] is target.original_costumes['age_uke\\age_uke_013']

    cloned_actor.animations = copy.deepcopy(target.animations)
    cloned_actor.animation = copy.deepcopy(target.animation)
    # cloned_actor.original_costumes = target.original_costumes
    cloned_actor.coscount = 0
    # if path is not None:
    # cloned_actor.actual_scale = [cloned_actor.width, cloned_actor.height]
    # rotation style
    # cloned_actor.roll = target.roll
    cloned_actor.rotation = target.rotation
    cloned_actor.hor_direction = target.hor_direction
    # needs to need_to_transform image?
    cloned_actor.need_to_rotate = target.need_to_rotate
    # cloned_actor.need_to_scale = target.need_to_scale
    cloned_actor.penstate = target.penstate
    cloned_actor.pencolor = list(target.pencolor)
    cloned_actor.pensize = target.pensize
    cloned_actor.pencolor_scale_phase = target.pencolor_scale_phase
    cloned_actor.pen_r = target.pen_r
    cloned_actor.pen_g = target.pen_g
    cloned_actor.pen_b = target.pen_b
    # cloned_actor.need_to_stamp = target.need_to_stamp
    # cloned_actor.bounce = target.bounce
    # cloned_actor.tags = list(target.tags)
    for tag in target.tags:
        cloned_actor.tag(tag)
    cloned_actor.gliding = False
    # cloned_actor.scale(target.actual_scale[0], target.actual_scale[1])
    cloned_actor.transform_rotate_image()
    return cloned_actor


def distance(a, b):
    return math.hypot(b.x - a.x, b.y - a.y)


def getactors(tag=None):
    if tag is not None:
        if tag in game_info.tagged_actors:
            return game_info.tagged_actors[tag]
        else:
            print('DEBUG: tag not in dictionary')
            return []
    else:
        return ACTORS
    # tagged_actors_list = []
    # for obj in gc.get_objects():
    #     if isinstance(obj, Actor):
    #         if tag is None:
    #             tagged_actors_list.append(obj)
    #         elif tag is str:
    #             if tag in obj.tags:
    #                 tagged_actors_list.append(obj)
    # return tagged_actors_list


def write(string='Text',
          position=None,
          name='Liberation Serif',
          fontsize=32,
          bold=False,
          italic=False,
          color=[255, 0, 0]):
    t = Text(string, name, fontsize, bold, italic, color)
    if position is not None:
        t.goto(position)


class Camera:
    def __init__(self):
        self.target = None
        self.old_x = 0
        self.old_y = 0
        self.following = False
        self.others = None
        self.on_the_edge = False
        self.dx = 0
        self.dy = 0
        self.hor_position = None
        self.ver_position = None

    def scroll_x(self, target):
        if target.x != self.old_x:
            self.dx = self.old_x - target.x
            target.setx(self.old_x)
            for a in self.others:
                a.setx(a.x + self.dx)

    def scroll_y(self, target):
        if target.y != self.old_y:
            self.dy = self.old_y - target.y
            target.sety(self.old_y)
            for a in self.others:
                a.sety(a.y + self.dy)

    def follow(self, target, ground=None):
        self.target = target
        self.others = ACTORS.copy()
        self.others.remove(target)
        if not self.following:
            self.old_x = target.x
            self.old_y = target.y
            self.following = True
        else:
            if ground is not None:
                if self.on_the_edge:
                    self.following = False

                    # self.old_x = target.x
                    # self.old_y = target.y
                    if self.hor_position == 'left':
                        if target.x >= screen_info.resolution[0]/2:
                            self.on_the_edge = False
                            dx = target.x - screen_info.resolution[0]/2
                            target.setx(screen_info.resolution[0]/2)
                            for a in self.others:
                                a.setx(a.x - dx)
                    elif self.hor_position == 'right':
                        if target.x <= screen_info.resolution[0]/2:
                            self.on_the_edge = False
                            dx = target.x - screen_info.resolution[0]/2
                            target.setx(screen_info.resolution[0]/2)
                            for a in self.others:
                                a.setx(a.x - dx)
                    if self.ver_position == 'up':
                        if target.y >= screen_info.resolution[1]/2:
                            self.on_the_edge = False
                            dy = target.y - screen_info.resolution[1]/2
                            target.setx(screen_info.resolution[1]/2)
                            for a in self.others:
                                a.sety(a.y - dy)
                    elif self.ver_position == 'down':
                        if target.y <= screen_info.resolution[1]/2:
                            self.on_the_edge = False
                            dy = target.y - screen_info.resolution[1]/2
                            target.setx(screen_info.resolution[1]/2)
                            for a in self.others:
                                a.sety(a.y - dy)
                else:
                    if not 0 < ground.x < ground.width/2:
                        self.on_the_edge = True
                        if 225 < target.direction < 315:
                            self.hor_position = 'left'
                        elif 45 < target.direction < 135:
                            self.hor_position = 'right'
                    else:
                        self.hor_position = None
                        self.scroll_x(target)
                    if not 0 < ground.y < ground.height/2:
                        if 315 < target.direction <= 360 or 0 <= target.direction < 45:
                            self.ver_position = 'up'
                        elif 135 < target.direction < 225:
                            self.ver_position = 'down'
                    else:
                        self.ver_position = None
                        self.scroll_y(target)

            else:
                self.scroll_x(target)
                self.scroll_y(target)



CAMERA = Camera()


class Timer:
    def __init__(self, ms):
        self.start = ticks()
        self.delta_time = ms

    def get(self):
        if ticks() - self.start > self.delta_time:
            self.start = ticks()
            return True


spawned_actors = pygame.sprite.Group()


def spawn(actor, speed=None, direction=None, position=None, target=None, setup_behavior=None, update_behavior=None, autoshow=True):
    spawned = clone(actor)
    spawned.spawn_speed = speed
    if direction is not None:
        spawned.point(direction)
    if position is not None:
        if position == 'random':
            spawned.gorand()
        else:
            spawned.goto(position)
    spawned.spawn_target = target
    spawned.spawn_setup = setup_behavior
    spawned.spawn_update = update_behavior
    if spawned.hidden and autoshow:
        spawned.show()
    if setup_behavior is not None:
        setup_behavior(spawned)
    spawned.spawn_update = update_behavior
    spawned_actors.add(spawned)
    return spawned


def tagcollide(tag1, tag2):
    for a in getactors(tag1):
        for b in getactors(tag2):
            if Actor.collide(a, b):
                COLLISION.object1 = a
                COLLISION.object2 = b
                return True


# def randombetween(a, b, *args):
#     if a is int and b is int:
#         return random.randint(a, b)
#     else:
#         for i in args:
#
#         roll = random.randint(0, 1)
#         if


# def pausable(func):
#     def wrapper(self, *args):
#         if not self.paused:
#             return func(self, *args)
#     return wrapper


def hideaway(func):
    def wrapper(self, *args):
        if not self.hidden:
            return func(self, *args)
    return wrapper


def execute(path):
    name = path.split('/')[-1]
    extension = name.split('.')[1]
    if extension == 'py':
        print('Compiling ' + name)
        py_compile.compile(name)
        pycname = name.split('.')[0] + '.pyc'
        print('Executing ' + pycname)
        subprocess.call(['python', pycname])
        # quit()
    else:
        print('DEBUG - execute: Not a Python script. Aborting...')


def fullscreen():
    pygame.display.toggle_fullscreen()


jumping_actors = pygame.sprite.Group()


def process_jumps():
    for a in jumping_actors:
        if a.jump_phase == 'up':
            if a.y > a.jump_starty - a.jump_height:
                a.sety(a.y - a.jump_step)
            else:
                a.jump_phase = 'down'
        elif a.jump_phase == 'down':
            if a.y < a.jump_originaly:
                a.sety(a.y + a.jump_step)
            else:
                a.jumping = False
                a.jump_count = 0
                a.sety(a.jump_originaly)


def save(data, tag):
    datafile = open("savedata.p", "w")
    if os.stat("savedata.p").st_size == 0:
        datadict = {}
    else:
        datadict = pickle.load(datafile)
    datadict[tag] = data
    pickle.dump(datadict, datafile)
    print(tag + " saved")


def load(tag):
    datafile = open("savedata.p", "rb")
    data = pickle.load(datafile)[tag]
    return data


def terminate():
    # PYGB support (to do)
    if False:
        subprocess.Popen(['python', '/home/pi/PYGB/main.py'], cwd='/home/pi/')
    # QUIT
    pygame.quit()
    sys.exit()
    quit()


# One of the most important functions
def update():

    # JUMPS
    process_jumps()

    # Manage spawned objects
    for spawned in spawned_actors:
        if spawned.spawn_target is not None:
            spawned.point(spawned.spawn_target)
        if spawned.spawn_speed is not None:
            spawned.forward(spawned.spawn_speed)
        if spawned.spawn_update is not None:
            spawned.spawn_update(spawned)

    # DRAW
    # Transform Actor's images
    # for actor in ACTORS:
    #     actor.transform_rotate_image()
    # Draw screen base color if needed
    if not screen_info.has_background:
        screen_info.screen.fill(screen_info.bg_color)
    # Draw background if needed
    else:
        ACTORS.clear(screen_info.screen, screen_info.background)
    # Draw the visible-Actors group
    ACTORS.draw(screen_info.screen)
    # Draw the turtle drawings surface
    screen_info.screen.blit(screen_info.pen_surface, [0, 0])
    # Refresh the Pygame screen
    pygame.display.update()

    # framerate
    default_clock.tick(game_info.framerate)

    # EVENTS
    # Refresh the event list
    events_storage.list = pygame.event.get()
    # Close pygame window when X icon clicked or ESCAPE pressed
    for e in events_storage.list:
        if e.type == pygame.QUIT:
            terminate()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                terminate()
    # Refresh mouse position
    MOUSE.update_events()

    # OTHER
    # Manage the time for hide and pause methods
    actual_time = pygame.time.get_ticks()
    # Compute actors pauses
    # for actor in actorsInfo.pausedActorsList:
    #     delta_time = actual_time - actor.start_pause_time
    #     if delta_time >= actor.pause_time:
    #         actor.paused = False
    #         actorsInfo.pausedActorsList.remove(actor)
    # Compute actors hide time
    for actor in actors_info.hidden_actors_list:
        delta_time = actual_time - actor.start_hide_time
        if delta_time >= actor.hide_time:
            actor.hidden = False
            actors_info.hidden_actors_list.remove(actor)
            # actors_info.draw_list.append(actor)
            ACTORS.add(actor)
    # Gliding
    process_gliding()


def UPDATE():
    update()


# def setup():
#     # gobo = imp.load_source('gobo', 'actors/gobo.py')
#     # gobo.Gobo('example_asset/characters/gobo.png')
#     # try:
#     items = os.listdir('actors')
#
#     actors_classes = {}
#
#     for item in items:
#
#         if item.split('.')[-1] == 'py':
#             print item
#             actors_classes[str(item)] = imp.load_source(str(item), 'actors/' + str(item))
#
#     # except:
#     #     print('actors directory not found')

def check_collisions():
    others = ACTORS.copy()
    for a in ACTORS:
        others.remove(a)
        for o in others:
            point = pygame.sprite.collide_mask(a, o)
            if point is not None:
                a.collision(o, point)
                o.collision(a, point)


def mainloop():
    check_collisions()
    ACTORS.update()
    update()


def find(actor_class):
    for a in ACTORS:
        if type(a) is actor_class:
            return a


# ACTOR CLASS
class Actor(pygame.sprite.Sprite):
    def __init__(self, path=None, cosname=None):
        super(Actor, self).__init__()
        if path is None:
            path = (os.path.dirname(sys.modules[__name__].__file__))
            path = os.path.join(path, 'turtle.png')
        actors_info.actors_list.append(self)
        ACTORS.add(self)
        # Actor coordinates
        self.x = 0.0
        self.x = screen_info.resolution[0] / 2
        self.y = 0.0
        self.y = screen_info.resolution[1] / 2
        # Actor angle direction
        self.direction = 90
        # image orientation
        self.heading = 0
        #self.layer = 0
        self.count = 0
        self.paused = False
        self.hidden = False
        self.pause_time = 0.0
        self.hide_time = 0.0
        self.start_pause_time = 0.0
        self.start_hide_time = 0.0
        self.costumes = []
        self.costumes_by_name = {}
        self.costumes_by_number = {}
        self.original_costumes = {}
        # self.costume = ''
        # self.cosnumber = 0
        self.coscount = 0
        self.rotation = 360
        self.hor_direction = 'right'
        self.need_to_rotate = False
        self.penstate = 'up'
        self.pencolor = RED
        self.pensize = 10
        self.pencolor_scale_phase = 'g_up'
        self.pen_r = 255
        self.pen_g = 0
        self.pen_b = 0
        self.tags = []
        self.gliding = False
        self.sliding_costumes = False
        self.animations = {}
        self.animation = {'name': '', 'state': ''}
        self.rect = None
        self.size = None
        self.width = None
        self.height = None
        # self.raw_img = None
        self.jump_step = 0
        self.jumping = False
        self.jump_count = 0
        self.jump_starty = 0
        self.jump_originaly = 0
        self.jump_phase = ""
        self.path = path
        self.load(path, cosname)
        self.costume = self.costumes_by_number[0]['name']
        self.cosnumber = 0
        self.image = self.costumes_by_name[self.costume]['image']
        self.update_rect()
        # self.actual_scale = [self.width, self.height]
        self.setup()

    # find costume name from image path
    def find_costume_name(self, path):
        words = path.split('/')
        costume = words[-1]
        return costume.split('.')[0]

    # update rect as the image changes
    def update_rect(self):
        self.rect = self.image.get_rect()
        self.update_position()
        self.size = self.image.get_size()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_position(self):
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    # load Actor's image
    def load(self, path, cosname=None):
        if path[-3:] in SUPPORTED_IMAGE_FORMATS:
            # Find costume name
            if cosname is None:
                cosname = self.find_costume_name(path)
            # Update Actor costumes list
            self.costumes.append(cosname)
            # Find costume number ID
            cosnumber = len(self.costumes) - 1
            # Load Image:
            raw_img = pygame.image.load(path).convert_alpha()
            # Update Original Costumes (reloading)
            self.original_costumes[cosname] = pygame.image.load(path).convert_alpha()
            # Update costumes name dictionary
            self.costumes_by_name[cosname] = {'image': raw_img, 'number': cosnumber}
            # Update costumes number dictionary
            self.costumes_by_number[cosnumber] = {'image': raw_img, 'name': cosname}
            # Update attributes
            # self.costume = cosname
            # self.cosnumber = cosnumber
        else:
            try:
                self.loadfolder(path)
                print('Loading folder of costumes instead: ' + path)
            except:
                print('Image not supported')
                quit()

    def loadcostume(self, path, cosname=None):
        self.load(path, cosname)

    def loadfolder(self, path):
        files_list = os.listdir(path)
        for f in files_list:
            if f[-3:] not in SUPPORTED_IMAGE_FORMATS:
                files_list.remove(f)
        files_list = sorted(files_list, key=str.lower)
        anim_name = path.split('/')[-1].split('.')[0]
        anim_begin = len(self.costumes)
        anim_end = anim_begin + len(files_list) - 1
        self.animations[anim_name] = {'begin': anim_begin, 'end': anim_end}
        for f in files_list:
            if f.split('.')[1] in SUPPORTED_IMAGE_FORMATS:
                self.load(os.path.join(path, f))

    def setcostume(self, newcostume):
        if type(newcostume) is int:
            self.cosnumber = newcostume
            self.image = self.costumes_by_number[newcostume]['image']
            self.costume = self.costumes_by_number[newcostume]['name']
        elif type(newcostume) is str:
            # for cos in self.costumes:
            #     if cos[0] == newcostume:
            #         self.cosnumber = self.costumes.index(cos)
            self.costume = newcostume
            self.image = self.costumes_by_name[newcostume]['image']
            self.cosnumber = self.costumes_by_name[newcostume]['number']
        # self.image = self.costumes[self.cosnumber][1]
        if self.need_to_rotate:
            self.transform_rotate_image()
        else:
            self.update_rect()

    def getcostume(self):
        return self.costume

    def nextcostume(self, pause=10, costumes=None):
        if self.coscount > pause:
            if costumes is not None:
                first_costume = costumes[0]
                last_costume = costumes[1]
                if self.cosnumber < last_costume:
                    self.setcostume(self.cosnumber + 1)
                else:
                    self.setcostume(first_costume)
            else:
                if self.cosnumber < len(self.costumes) - 1:
                    self.setcostume(self.cosnumber + 1)
                else:
                    self.setcostume(0)
            self.coscount = 0
        self.coscount += 1

    def slidecostumes(self, first=None, last=None, pause=10, interval=1):
        if first is None:
            first = 0
        if last is None:
            last = len(self.costumes) - 1
        if self.cosnumber < first or self.cosnumber > last:
            self.setcostume(first)
        if self.coscount > pause:
            if self.cosnumber < last:
                self.setcostume(self.cosnumber + interval)
            else:
                self.setcostume(first)
            self.coscount = 0
        self.coscount += 1

    def play(self, animation, fps=15, loop=True, interval=1):
        anim = self.animations[animation]
        pause = 1000 / fps
        if self.animation['name'] != animation:
            self.animation['name'] = animation
            self.animation['state'] = 'playing'
            self.coscount = ticks()
            # if self.cosnumber < anim['begin'] or self.cosnumber > anim['end']:
            self.setcostume(anim['begin'])
        if self.animation['state'] != 'ended':
            if ticks() - self.coscount > pause:
                if self.cosnumber + interval <= anim['end']:
                    self.setcostume(self.cosnumber + interval)
                else:
                    if loop:
                        self.setcostume(anim['begin'])
                        return 'ended'
                    else:
                        self.animation['state'] = 'ended'
                        return 'ended'
                self.coscount = ticks()

    def setx(self, x):
        self.x = x
        self.update_position()

    def sety(self, y):
        self.y = y
        self.update_position()

    def changex(self, delta_x):
        self.x = self.x + delta_x
        self.update_position()

    def changey(self, delta_y):
        self.y = self.y + delta_y
        self.update_position()

    def getposition(self):
        return [self.x, self.y]

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def setdirection(self, angle):
        self.direction = angle
        self.transform_rotate_image()

    def getdirection(self):
        return self.direction

    # @pausable
    def goto(self, x=None, y=None):
        if type(x) is int or type(x) is float:
            self.x = x
            self.y = y
        elif type(x) is list or type(x) is tuple:
            self.x = x[0]
            self.y = x[1]
        elif x == 'mouse':
            pos = pygame.mouse.get_pos()
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = x.x
            self.y = x.y
        if self.penstate == 'down':
            pygame.draw.circle(screen_info.pen_surface,
                               self.pencolor,
                               [int(self.x), int(self.y)],
                               self.pensize)
        self.update_position()

    def setposition(self, *args):
        self.goto(*args)

    def glide(self, x, y=None, speed=10):
        if not self.gliding:
            destx = x
            desty = y
            if y is None:
                destx = x.x
                desty = x.y
            actors_info.glide_list.append([self, destx, desty, speed])
            self.gliding = True

    # @pausable
    def gorand(self,
               rangex=None,
               rangey=None):
        if rangex is None:
            rangex = [0, screen_info.resolution[0]]
        if rangey is None:
            rangey = [0, screen_info.resolution[1]]
        self.x = random.randint(rangex[0], rangex[1])
        self.y = random.randint(rangey[0], rangey[1])
        if self.penstate == 'down':
            pygame.draw.circle(screen_info.pen_surface,
                               self.pencolor,
                               [int(self.x), int(self.y)],
                               self.pensize)
        self.update_position()

    def pendown(self):
        self.penstate = 'down'
        pygame.draw.circle(screen_info.pen_surface,
                           self.pencolor,
                           [int(self.x), int(self.y)],
                           self.pensize)

    def penup(self):
        self.penstate = 'up'

    def setpensize(self, size):
        self.pensize = size

    def setpencolor(self, r=0, g=0, b=0):
        if type(r) is list or type(r) is tuple:
            self.pencolor = r
        else:
            self.pencolor = [r, g, b]

    def colorscale(self, interval=1):
        if self.pencolor_scale_phase == 'g_up':
            if self.pen_g + interval <= 255:
                self.pen_g += interval
            else:
                self.pencolor_scale_phase = 'r_down'
        elif self.pencolor_scale_phase == 'r_down':
            if self.pen_r - interval >= 0:
                self.pen_r -= interval
            else:
                self.pencolor_scale_phase = 'b_up'
        elif self.pencolor_scale_phase == 'b_up':
            if self.pen_b + interval <= 255:
                self.pen_b += interval
            else:
                self.pencolor_scale_phase = 'g_down'
        elif self.pencolor_scale_phase == 'g_down':
            if self.pen_g - interval >= 0:
                self.pen_g -= interval
            else:
                self.pencolor_scale_phase = 'r_up'
        elif self.pencolor_scale_phase == 'r_up':
            if self.pen_r + interval <= 255:
                self.pen_r += interval
            else:
                self.pencolor_scale_phase = 'b_down'
        elif self.pencolor_scale_phase == 'b_down':
            if self.pen_b - interval >= 0:
                self.pen_b -= interval
            else:
                self.pencolor_scale_phase = 'g_up'
        return [self.pen_r, self.pen_g, self.pen_b]

    def changepencolor(self, interval=1):
        self.setpencolor(self.colorscale(interval))

    def bounce(self):
        if self.y > screen_info.resolution[1] or self.y < 0:
            self.direction = (180 - self.direction) % 360
            self.heading = self.direction - 90
            if self.rotation is not False:
                self.transform_rotate_image()
        if self.x > screen_info.resolution[0] or self.x < 0:
            self.direction = (0 - self.direction) % 360
            self.heading = self.direction - 90
            if self.rotation is not False:
                self.transform_rotate_image()

    # @pausable
    def forward(self, steps):
        if self.penstate == 'down':
            start_x = self.x
            start_y = self.y
            for i in range(abs(steps)):
                pygame.draw.circle(screen_info.pen_surface,
                                   self.pencolor,
                                   [int(start_x), int(start_y)],
                                   self.pensize)
                # pygame.display.update()
                start_x = self.x + i * math.sin(math.radians(self.direction))
                start_y = self.y + i * -math.cos(math.radians(self.direction))
        self.x = round(self.x + steps * math.sin(math.radians(self.direction)))
        self.y = round(self.y + steps * -math.cos(math.radians(self.direction)))
        # if self.bounce:
        #     self.bounce_on_edge()
        self.update_position()

    def back(self, steps):
        self.forward(-steps)

    def backward(self, steps):
        self.forward(-steps)

    def jump(self, height=100, step=10, jumps=1):
        if self.jump_count < jumps:
            self.jump_count += 1
            self.jump_height = height
            self.jump_step = step
            self.jumping = True
            self.jump_starty = self.y
            if self.jump_count == 1:
                self.jump_originaly = self.y
            self.jump_phase = 'up'
            jumping_actors.add(self)

    def transform_rotate_image(self):
        self.need_to_rotate = True
        # If the image changed the transform roll functions apply
        # First, restore original image
        # self.image = self.costumes_by_name[self.costume]['image']
        # Then roll it:
        # Full 360 rotation style
        if self.rotation == 360:
            self.image = pygame.transform.rotate(self.costumes_by_name[self.costume]['image'], -self.heading)
        # Horizontal Flip rotation style
        elif self.rotation == 'flip':
            if self.direction < 0 or self.direction > 180:
                self.hor_direction = 'left'
            elif 0 < self.direction < 180:
                self.hor_direction = 'right'
            if self.hor_direction == 'left':
                self.image = pygame.transform.flip(self.costumes_by_name[self.costume]['image'], True, False)
            elif self.hor_direction == 'right':
                self.image = self.costumes_by_name[self.costume]['image']
            # if self.direction < 0 or self.direction > 180:
            #     if self.need_to_flip == 'left':
            #         self.flip('horizontal')
            #         self.need_to_flip = 'right'
            # if 0 < self.direction < 180:
            #     if self.need_to_flip == 'right':
            #         self.flip('horizontal')
            #         self.need_to_flip = 'left'
        # In the end update the rect
        self.update_rect()
        # Stamp in the turtle drawing surface
        # if self.need_to_stamp:
        #     self.need_to_stamp = False
        # And then the original image is loaded
        # self.costumes[self.cosnumber][1] = self.original_costumes[self.cosnumber][1]

    # @pausable
    def right(self, angle):
        self.direction = (self.direction + angle) % 360
        self.heading = self.direction - 90
        self.transform_rotate_image()

    # @pausable
    def left(self, angle):
        self.direction = (self.direction - angle) % 360
        self.heading = self.direction - 90
        self.transform_rotate_image()

    def roll(self, angle):
        self.heading += angle
        original_rotation_style = self.rotation
        self.rotate(360)
        self.transform_rotate_image()
        self.rotate(original_rotation_style)

    def rotate(self, style):
        self.rotation = style

    # @pausable
    def stamp(self):
        # if not self.need_to_stamp:
        #     self.need_to_stamp = True
        screen_info.pen_surface.blit(self.image,
                                     ((self.x - self.width / 2),
                                      (self.y - self.height / 2)),
                                     None)

    # @pausable
    def point(self, target, y=None):
        # set heading as angle
        if type(target) is int and type(target) is not str and y is None:
            angle = target % 360
            self.direction = angle
            self.heading = angle - 90
        # point at coordinate
        elif type(target) is list and type(target) is not str:
            angle = -math.atan2(self.x - target[0], self.y - target[1])
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        elif y is not None:
            angle = -math.atan2(self.x - target, self.y - y)
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        # point at mouse pointer
        elif target == 'mouse':
            mousepos = pygame.mouse.get_pos()
            angle = -math.atan2(self.x - mousepos[0], self.y - mousepos[1])
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        # point at target
        else:
            angle = -math.atan2(self.x - target.x, self.y - target.y)
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        self.transform_rotate_image()

    def flip(self, direction):
        if direction == 'horizontal':
            # for name in self.costumes_by_name:
            #     self.costumes_by_name[name]['image'] = pygame.transform.flip(self.original_costumes[name], True, False)
            #     self.costumes_by_number[self.costumes_by_name[name]['number']]['image'] = pygame.transform.flip(self.original_costumes[name], True, False)
            for d in [self.costumes_by_name, self.costumes_by_number]:
                for k in d:
                    d[k]['image'] = pygame.transform.flip(d[k]['image'], True, False)
            for k in self.original_costumes:
                self.original_costumes[k] = pygame.transform.flip(self.original_costumes[k], True, False)
        if direction == 'vertical':
            # for name in self.costumes_by_name:
            #     self.costumes_by_name[name]['image'] = pygame.transform.flip(self.original_costumes[name], False, True)
            #     self.costumes_by_number[self.costumes_by_name[name]['number']]['image'] = pygame.transform.flip(self.original_costumes[name], False, True)
            for d in [self.costumes_by_name, self.costumes_by_number]:
                for k in d:
                    d[k]['image'] = pygame.transform.flip(d[k]['image'], False, True)
            for k in self.original_costumes:
                self.original_costumes[k] = pygame.transform.flip(self.original_costumes[k], False, True)
        self.transform_rotate_image()

    def scale(self, w, h=None):
        # self.need_to_scale = True
        if h is None:
            width = int(self.width * w)
            height = int(self.height * w)
        else:
            width = w
            height = h
        self.image = pygame.transform.scale(self.original_costumes[self.costume], (width, height))
        for name in self.costumes_by_name:
            if h is None:
                width = int(self.costumes_by_name[name]['image'].get_rect().width * w)
                height = int(self.costumes_by_name[name]['image'].get_rect().height * w)
            self.costumes_by_name[name]['image'] = pygame.transform.scale(self.original_costumes[name], (width, height))
            self.costumes_by_number[self.costumes_by_name[name]['number']]['image'] = pygame.transform.scale(self.original_costumes[name], (width, height))
        if self.need_to_rotate:
            self.transform_rotate_image()
        else:
            self.update_rect()
        # self.actual_scale = [self.image.get_rect().width, self.image.get_rect().height]

    def setlayer(self, layer):
        #self.layer = layer
        ACTORS.change_layer(self, layer)
        if not self.hidden:
            ACTORS.change_layer(self, layer)

    def tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            if tag not in game_info.tagged_actors:
                game_info.tagged_actors[tag] = []
            game_info.tagged_actors[tag].append(self)

    def untag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            if tag in game_info.tagged_actors:
                game_info.tagged_actors[tag].remove(self)
                if not game_info.tagged_actors[tag]:
                    del game_info.tagged_actors[tag]
        else:
            print('DEBUG: The actor was not tagged that way')

    # check if the mouse has clicked the Actor
    def click(self):
        if self.collidepoint(MOUSE.position) and MOUSE.leftdown is True:
            return True
        else:
            return False
        # else:
        #     for event in events_storage.list:
        #         if event.type == pygame.MOUSEBUTTONUP:
        #             MOUSE.leftdown = False

    def centralclick(self):
        if self.collidepoint(MOUSE.position) and MOUSE.centraldown is True:
            return True
        else:
            return False

    def rightclick(self):
        if self.collidepoint(MOUSE.position) and MOUSE.rightdown is True:
            return True
        else:
            return False

    # Mask collision
    @hideaway
    def collide(self, target):
        if isinstance(target, Actor):
            if not target.hidden:
                self.update_position()
                target.update_position()
                result = pygame.sprite.collide_mask(self, target)
                if result is not None:
                    COLLISION.point = result
                    COLLISION.object = target
                    return True
                else:
                    return False
        elif type(target) is list:
            for a in target:
                if self.collide(a):
                    return True
        elif type(target) is str:
            if target in game_info.tagged_actors:
                otherslist = list(game_info.tagged_actors[target])
                if self in otherslist:
                    otherslist.remove(self)
                for a in otherslist:
                    if self.collide(a):
                        return True
            else:
                print('DEBUG: Tag does not exist')

    # Rect collision
    @hideaway
    def rectcollide(self, target):
        self.update_position()
        target.update_position()
        if not target.hidden:
            return self.rect.colliderect(target.rect)

    @hideaway
    def collidepoint(self, x=0, y=0):
        self.update_position()
        if type(x) is list or type(x) is tuple:
            return self.rect.collidepoint(x)
        else:
            return self.rect.collidepoint(x, y)

    # pause actor's actions (wip)
    # def pause(self, t=-1):
    #     self.paused = True
    #     if t >= 0:
    #         actors_info.paused_actors_list.append(self)
    #         self.pause_time = t * 1000
    #         self.start_pause_time = pygame.time.get_ticks()
    #
    # def unpause(self):
    #     self.paused = False
    #     actors_info.paused_actors_list.remove(self)

    @hideaway
    def hide(self, t=-1):
        if not self.hidden:
            self.hidden = True
            ACTORS.remove(self)
            if t >= 0:
                actors_info.hidden_actors_list.append(self)
                self.hide_time = t * 1000
                self.start_hide_time = pygame.time.get_ticks()
        else:
            pass

    def show(self):
        if self.hidden:
            self.hidden = False
            if self in actors_info.hidden_actors_list:
                try:
                    actors_info.hidden_actors_list.remove(self)
                except:
                    print('errore strano')
                    print(actors_info.hidden_actors_list)
            ACTORS.add(self)
            ACTORS.change_layer(self, self.layer)
        else:
            pass

    def kill(self):
        super(Actor, self).kill()
        self.hide()

    def setup(self):
        pass

    @hideaway
    def collision(self, other, point):
        pass


class Text(Actor):
    def __init__(self,
                 string='Text',
                 name='Liberation Serif',
                 fontsize=32, bold=False,
                 italic=False,
                 color=[255, 0, 0]):
        self.string = str(string)
        self.name = name
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.color = color
        self.need_to_scale_text = False
        Actor.__init__(self)

    def update_text(self):
        self.font = pygame.font.SysFont(self.name,
                                        self.fontsize,
                                        self.bold,
                                        self.italic)
        self.image = self.font.render(self.string, True, self.color)
        # self.costumes[0] = ["text", self.image]
        # self.costumes[0][1] = self.image
        # Update costumes name dictionary
        self.costumes_by_name['text'] = {'image': self.image, 'number': 0}
        # Update costumes number dictionary
        self.costumes_by_number[0] = {'image': self.image, 'name': 'text'}
        self.original_costumes = {'text': self.image}
        if self.need_to_rotate:
            self.transform_rotate_image()
        else:
            self.update_rect()

    def load(self, path, cosname=None):
        self.costume = 'text'
        self.costumes.append([0, 'text'])
        # self.costumes.append(["text", None])
        # Update costumes name dictionary
        self.costumes_by_name['text'] = {'image': None, 'number': 0}
        # Update costumes number dictionary
        self.costumes_by_number[0] = {'image': None, 'name': 'text'}
        self.original_costumes = {'text': None}
        self.update_text()
        # self.image = self.font.render(self.string, True, self.color)
        # self.costumes.append(["text", self.image])

    def write(self, string):
        self.string = str(string)
        self.update_text()
        if self.need_to_scale_text:
            self.scale(self.need_to_scale_text[0], self.need_to_scale_text[1])

    def setfontsize(self, fontsize):
        self.fontsize = fontsize
        self.update_text()

    def setbold(self, bold=True):
        self.bold = bold
        self.update_text()

    def setitalic(self, italic=True):
        self.italic = italic
        self.update_text()

    def setcolor(self, color):
        self.color = color
        self.update_text()

    def scale(self, w, h=None):
        if h is None:
            self.fontsize = int(self.fontsize * w)
            self.write(self.string)
        else:
            Actor.scale(self, w, h)
            self.need_to_scale_text = (w, h)



# SUONI
def musicload(path):
    pygame.mixer.music.load(path)


def musicplay(loops=0, start=0.0):
    pygame.mixer.music.play(loops, start)


# def Sound(path):
#     s = pygame.mixer.Sound(path)
#     return s

class Sound(pygame.mixer.Sound):
    def __init__(self, path):
        super(Sound, self).__init__(path)
        self.volume = self.get_volume() * 100
        self.lenght = self.get_length()

    def setvolume(self, volume):
        self.volume = volume
        v = volume / 100.0
        self.set_volume(v)

    def volumeup(self, value):
        if 0 <= self.volume + value <= 100:
            self.setvolume(self.volume + value)

    def volumedown(self, value):
        if 0 <= self.volume - value <= 100:
            self.setvolume(self.volume - value)


# EVENTS:

# KEYBOARD KEYS
UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
BACKSPACE = pygame.K_BACKSPACE
TAB = pygame.K_TAB
CLEAR = pygame.K_CLEAR
RETURN = pygame.K_RETURN
PAUSE = pygame.K_PAUSE
ESCAPE = pygame.K_ESCAPE
SPACE = pygame.K_SPACE
EXCLAIM = pygame.K_EXCLAIM
QUOTEDBL = pygame.K_QUOTEDBL
HASH = pygame.K_HASH
DOLLAR = pygame.K_DOLLAR
AMPERSAND = pygame.K_AMPERSAND
QUOTE = pygame.K_QUOTE
LEFTPAREN = pygame.K_LEFTPAREN
RIGHTPAREN = pygame.K_RIGHTPAREN
ASTERISK = pygame.K_ASTERISK
PLUS = pygame.K_PLUS
COMMA = pygame.K_COMMA
MINUS = pygame.K_MINUS
PERIOD = pygame.K_PERIOD
SLASH = pygame.K_SLASH
ZERO = pygame.K_0
ONE = pygame.K_1
TWO = pygame.K_2
THREE = pygame.K_3
FOUR = pygame.K_4
FIVE = pygame.K_5
SIX = pygame.K_6
SEVEN = pygame.K_7
EIGHT = pygame.K_8
NINE = pygame.K_9
COLON = pygame.K_COLON
SEMICOLON = pygame.K_SEMICOLON
LESS = pygame.K_LESS
EQUALS = pygame.K_EQUALS
GREATER = pygame.K_GREATER
QUESTION = pygame.K_QUESTION
AT = pygame.K_AT
LEFTBRACKET = pygame.K_LEFTBRACKET
BACKSLASH = pygame.K_BACKSLASH
RIGHTBRACKET = pygame.K_RIGHTBRACKET
CARET = pygame.K_CARET
UNDERSCORE = pygame.K_UNDERSCORE
BACKQUOTE = pygame.K_BACKQUOTE
A = pygame.K_a
B = pygame.K_b
C = pygame.K_c
D = pygame.K_d
E = pygame.K_e
F = pygame.K_f
G = pygame.K_g
H = pygame.K_h
I = pygame.K_i
J = pygame.K_j
K = pygame.K_k
L = pygame.K_l
M = pygame.K_m
N = pygame.K_n
O = pygame.K_o
P = pygame.K_p
Q = pygame.K_q
R = pygame.K_r
S = pygame.K_s
T = pygame.K_t
U = pygame.K_u
V = pygame.K_v
W = pygame.K_w
X = pygame.K_x
Y = pygame.K_y
Z = pygame.K_z
DELETE = pygame.K_DELETE
INSERT = pygame.K_INSERT
HOME = pygame.K_HOME
END = pygame.K_END
PAGEUP = pygame.K_PAGEUP
PAGEDOWN = pygame.K_PAGEDOWN
F1 = pygame.K_F1
F2 = pygame.K_F2
F3 = pygame.K_F3
F4 = pygame.K_F4
F5 = pygame.K_F5
F6 = pygame.K_F6
F7 = pygame.K_F7
F8 = pygame.K_F8
F9 = pygame.K_F9
F10 = pygame.K_F10
F11 = pygame.K_F11
F12 = pygame.K_F12
F13 = pygame.K_F13
F14 = pygame.K_F14
F15 = pygame.K_F15
NUMLOCK = pygame.K_NUMLOCK
CAPSLOCK = pygame.K_CAPSLOCK
SCROLLOCK = pygame.K_SCROLLOCK
RSHIFT = pygame.K_RSHIFT
LSHIFT = pygame.K_LSHIFT
RCTRL = pygame.K_RCTRL
LCTRL = pygame.K_LCTRL
RALT = pygame.K_RALT
LALT = pygame.K_LALT
RMETA = pygame.K_RMETA
LMETA = pygame.K_LMETA
LSUPER = pygame.K_LSUPER
RSUPER = pygame.K_RSUPER
PRINT = pygame.K_PRINT
EURO = pygame.K_EURO


# detect the continuous pression of a key
def key(keycode):
    if pygame.key.get_pressed()[keycode]:
        return True


# detect the single pression of a key
def keydown(keycode):
    for event in events_storage.list:
        if event.type == pygame.KEYDOWN:
            if event.key == keycode:
                return True


# detect the release of a key
def keyup(keycode):
    for event in events_storage.list:
        if event.type == pygame.KEYUP:
            if event.key == keycode:
                return True


def anykeydown():
    for event in events_storage.list:
        if event.type == pygame.KEYDOWN:
            return True
        else:
            return False


# GAMEPAD
class GamePadManager:
    def __init__(self):
        self.gamepad_count = pygame.joystick.get_count()
        self.gamepads = []
        for gamepadID in range(self.gamepad_count):
            # add gamepad to list
            self.gamepads.append(pygame.joystick.Joystick(gamepadID))
            # initialize gamepad
            self.gamepads[gamepadID].init()
        self.no_gamepad_found = False

gamepad_manager = GamePadManager()

# gamepadCount = pygame.joystick.get_count()
# gamepads = []
# for gamepadID in range(pygame.joystick.get_count()):
#     # add gamepad to list
#     gamepads.append(pygame.joystick.Joystick(gamepadID))
#     # initialize gamepad
#     gamepads[gamepadID].init()


def buttondown(btn, pad=0):
    if gamepad_manager.gamepad_count > 0:
        return gamepad_manager.gamepads[pad].get_button(btn)
    elif not gamepad_manager.no_gamepad_found:
        print('no gamepad found...')
        gamepad_manager.no_gamepad_found = True


def axis(hand, direction, pad=0):
    if gamepad_manager.gamepad_count > 0:
        if hand == 'left':
            if direction == 'horizontal':
                return gamepad_manager.gamepads[pad].get_axis(0)
            elif direction == 'vertical':
                return gamepad_manager.gamepads[pad].get_axis(1)
        elif hand == 'right':
            if direction == 'horizontal':
                return gamepad_manager.gamepads[pad].get_axis(3)
            elif direction == 'vertical':
                return gamepad_manager.gamepads[pad].get_axis(4)
    elif not gamepad_manager.no_gamepad_found:
        print('no gamepad found...')
        gamepad_manager.no_gamepad_found = True


def trigger(hand, pad=0):
    if gamepad_manager.gamepad_count > 0:
        if hand == 'left':
            raw = gamepad_manager.gamepads[pad].get_axis(2)
            value = (raw + 1) / 2
            return value
        if hand == 'right':
            raw = gamepad_manager.gamepads[pad].get_axis(5)
            value = (raw + 1) / 2
            return value
    elif not gamepad_manager.no_gamepad_found:
        print('no gamepad found...')
        gamepad_manager.no_gamepad_found = True
