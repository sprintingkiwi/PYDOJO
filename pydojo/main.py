import pygame, math, random, os, subprocess, sys, gc, time

pygame.init()

# CONSTANTS
LIBRARY_VERSION = 1.7

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

SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'gif', 'bmp']


# Class for Game Info
class GameInfo():
    def __init__(self):
        self.framerate = 60


game_info = GameInfo()


def framerate(fps):
    game_info.framerate = fps


# OBJECTS FOR DATA STORAGE
class EventsStorage():
    def __init__(self):
        self.CHECK = False
        self.list = []


events_storage = EventsStorage()


class MouseState():
    def __init__(self):
        self.leftdown = False
        self.centraldown = False
        self.rightdown = False
        self.pos = pygame.mouse.get_pos()
        self.x = self.pos[0]
        self.y = self.pos[1]


MOUSE = MouseState()


class ScreenInfo():
    def __init__(self):
        self.screen = None
        self.resolution = [800, 600]
        self.pen_surface = pygame.Surface([32, 32])
        self.has_background = False
        self.bg_color = BLACK
        self.backgrounds = {}
        self.background = None


screen_info = ScreenInfo()


class ActorsInfo():
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


def CreatePenSurface():
    path = (os.path.dirname(sys.modules[__name__].__file__))
    path = os.path.join(path, 'pensurface.png')
    screen_info.pen_surface = pygame.image.load(path).convert_alpha()
    screen_info.pen_surface = pygame.transform.scale(screen_info.pen_surface, screen_info.resolution)


# SCREEN
def screen(w, h, fullscreen=False):
    screen_info.resolution = [w, h]
    if fullscreen:
        screen_info.screen = pygame.display.set_mode([w, h], pygame.FULLSCREEN)
    else:
        screen_info.screen = pygame.display.set_mode([w, h])
    # Create surface for turtle drawings
    CreatePenSurface()
    # Get screen center
    CENTER.x = screen_info.resolution[0] / 2
    CENTER.y = screen_info.resolution[1] / 2


def SCREEN(*args):
    screen(*args)


def fill(color):
    screen_info.has_background = False
    screen_info.bg_color = color


def clear():
    CreatePenSurface()


def find_file_name(path):
    words = path.split('/')
    name = words[-1]
    return name.split('.')[0]


def background(path):
    screen_info.has_background = True
    screen_info.background = pygame.image.load(path).convert_alpha()
    screen_info.background = pygame.transform.scale(screen_info.background,
                                                    screen_info.resolution)
    screen_info.backgrounds[find_file_name(path)] = screen_info.background
    screen_info.screen.blit(screen_info.background, (0, 0))


def loadbackground(path):
    background(path)


def setbackground(name):
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


# Actors-to-transform_image GROUP
actors_to_draw = pygame.sprite.LayeredUpdates()


# One of the most important functions
def update():

    # DRAW
    # Transform Actor's images
    for actor in actors_to_draw:
        actor.transform_image()
    # Draw screen base color if needed
    if not screen_info.has_background:
        screen_info.screen.fill(screen_info.bg_color)
    # Draw background if needed
    if screen_info.has_background:
        actors_to_draw.clear(screen_info.screen, screen_info.background)
    # Draw the visible-Actors group
    actors_to_draw.draw(screen_info.screen)
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
            quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                quit()
    # Refresh mouse position
    MOUSE.pos = pygame.mouse.get_pos()
    MOUSE.x = MOUSE.pos[0]
    MOUSE.y = MOUSE.pos[1]

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
            actors_to_draw.add(actor)
    # Gliding
    process_gliding()


def UPDATE():
    update()


def Clock():
    return pygame.time.Clock()


def wait(ms):
    pygame.time.wait(ms)


def ticks():
    return pygame.time.get_ticks()


def clone(target):
    # clonedActor = copy.copy(target)
    # actors_info.actors_list.append(clonedActor)
    # clonedActor.update_rect()
    # if not target.hidden:
    #     actors_to_draw.add(clonedActor)
    # return clonedActor
    cloned_actor = Actor(target.path)
    cloned_actor.scale(target.actual_scale[0], target.actual_scale[1])
    cloned_actor.x = target.x
    cloned_actor.y = target.y
    # Actor angle direction
    cloned_actor.direction = target.direction
    # image orientation
    cloned_actor.heading = target.heading
    cloned_actor.layer = target.layer
    cloned_actor.count = 0
    cloned_actor.paused = False
    cloned_actor.hidden = target.hidden
    cloned_actor.pause_time = 0.0
    cloned_actor.hide_time = 0.0
    cloned_actor.start_pause_time = 0.0
    cloned_actor.start_hide_time = 0.0
    # load actor image
    cloned_actor.costumes = target.costumes
    cloned_actor.costume = target.costume
    cloned_actor.cosnumber = target.cosnumber
    cloned_actor.original_costumes = target.original_costumes
    cloned_actor.coscount = 0
    # if path is not None:
    cloned_actor.actual_scale = [cloned_actor.width, cloned_actor.height]
    # rotation style
    cloned_actor.rotate = target.rotate
    cloned_actor.rotation = target.rotation
    cloned_actor.need_to_flip = target.need_to_flip
    # needs to transform image?
    cloned_actor.transform = target.transform
    cloned_actor.pen_state = target.pen_state
    cloned_actor.pencolor = target.pencolor
    cloned_actor.pensize = target.pensize
    cloned_actor.need_to_stamp = target.need_to_stamp
    cloned_actor.bounce = target.bounce
    cloned_actor.tag = target.tag
    cloned_actor.gliding = False
    return cloned_actor


def distance(a, b):
    return math.hypot(b.x - a.x, b.y - a.y)


def getactors(tag=None):
    tagged_actors_list = []
    for obj in gc.get_objects():
        if isinstance(obj, Actor):
            if tag is None:
                tagged_actors_list.append(obj)
            elif tag is str:
                if obj.tag == tag:
                    tagged_actors_list.append(obj)
    return tagged_actors_list


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


def terminate():
    subprocess.Popen(['python', '/home/pi/PYGB/main.py'], cwd='/home/pi/')
    pygame.quit()
    sys.exit()


# ACTOR CLASS
class Actor(pygame.sprite.Sprite):
    def __init__(self, path=None, cosname=None):
        super(Actor, self).__init__()
        if path is None:
            path = (os.path.dirname(sys.modules[__name__].__file__))
            path = os.path.join(path, 'turtle.png')
        actors_info.actors_list.append(self)
        # actors_info.draw_list.append(self)
        actors_to_draw.add(self)
        # pygame.sprite.Sprite.__init__(self)
        # Actor coordinates
        self.x = 0.0
        self.x = screen_info.resolution[0] / 2
        self.y = 0.0
        self.y = screen_info.resolution[1] / 2
        # Actor angle direction
        self.direction = 90
        # image orientation
        self.heading = 0
        self.layer = 0
        self.actual_scale = [100, 100]
        self.count = 0
        self.paused = False
        self.hidden = False
        self.pause_time = 0.0
        self.hide_time = 0.0
        self.start_pause_time = 0.0
        self.start_hide_time = 0.0
        # load actor image
        self.costumes = []
        self.costume = ''
        self.cosnumber = 0
        self.original_costumes = []
        self.coscount = 0
        self.path = path
        self.load(path, cosname)
        # rotation style
        self.rotate = True
        self.rotation = 360
        self.need_to_flip = 'left'
        # needs to transform image?
        self.transform = False
        self.pen_state = 'up'
        self.pencolor = RED
        self.pensize = 1
        self.need_to_stamp = False
        self.bounce = False
        self.tag = "untagged"
        self.gliding = False
        self.sliding_costumes = False
        self.animations = {}

    # find costume name from image path
    def find_costume_name(self, path):
        words = path.split('/')
        costume = words[-1]
        return costume.split('.')[0]

    # update rect as the image changes
    def update_rect(self):
        self.rect = self.costumes[self.cosnumber][1].get_rect()
        self.update_position()
        self.size = self.costumes[self.cosnumber][1].get_size()
        self.width = self.costumes[self.cosnumber][1].get_width()
        self.height = self.costumes[self.cosnumber][1].get_height()
        self.image = self.costumes[self.cosnumber][1]
        # self.mask = pygame.mask.from_surface(self.image)

    def update_position(self):
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    # load Actor's image
    def load(self, path, cosname=None):
        if path[-3:] in SUPPORTED_IMAGE_FORMATS:
            if cosname is None:
                self.costume = self.find_costume_name(path)
            else:
                self.costume = cosname
            self.rawImg = pygame.image.load(path).convert_alpha()
            # if len(self.costumes) > 0:
            #     self.rawImg = pygame.transform.scale(self.rawImg, self.actual_scale)
            self.costumes.append([self.costume, self.rawImg])
            self.original_costumes.append([self.costume, self.rawImg])
            # Generate Rect and other stuff
            self.rect = self.costumes[self.cosnumber][1].get_rect()
            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)
            self.size = self.costumes[self.cosnumber][1].get_size()
            self.width = self.costumes[self.cosnumber][1].get_width()
            self.height = self.costumes[self.cosnumber][1].get_height()
            # image attribute for pygame sprite/group methods
            self.image = self.costumes[self.cosnumber][1]
            self.actual_scale = [self.width, self.height]
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
        for f in os.listdir(path):
            if f.split('.')[1] in SUPPORTED_IMAGE_FORMATS:
                self.load(os.path.join(path, f))

    def setcostume(self, newcostume):
        if type(newcostume) is int:
            self.cosnumber = newcostume
        elif type(newcostume) is str:
            for cos in self.costumes:
                if cos[0] == newcostume:
                    self.cosnumber = self.costumes.index(cos)
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
            self.cosnumber = first
        if self.coscount > pause:
            if self.cosnumber < last:
                self.setcostume(self.cosnumber + interval)
            else:
                self.setcostume(first)
            self.coscount = 0
        self.coscount += 1

    def setx(self, x):
        self.x = x
        self.update_position()

    def sety(self, y):
        self.y = y
        self.update_position()

    def getposition(self):
        return [self.x, self.y]

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def setdirection(self, angle):
        self.direction = angle

    def getdirection(self):
        return self.direction

    def transform_image(self, rect=None):
        # If the image changed the transform functions apply
        if self.rotate:
            # Full 360 rotation style
            if self.rotation == 360 and self.transform:
                self.costumes[self.cosnumber][1] = pygame.transform.rotate(self.costumes[self.cosnumber][1], -self.heading)
                self.update_rect()
            # Horizontal Flip rotation style
            elif self.rotation == 'flip':
                if self.direction < 0 or self.direction > 180:
                    if self.need_to_flip == 'left':
                        self.flip('horizontal')
                        self.need_to_flip = 'right'
                if self.direction > 0 and self.direction < 180:
                    if self.need_to_flip == 'right':
                        self.flip('horizontal')
                        self.need_to_flip = 'left'
        # Blit the image to the screen
        # screen_info.screen.blit(self.costumes[self.cosnumber][1],
        #                         ((self.x - self.width / 2),
        #                         (self.y - self.height / 2)),
        #                         rect)
        # Stamp in the turtle drawing surface
        if self.need_to_stamp:
            screen_info.pen_surface.blit(self.costumes[self.cosnumber][1],
                                         ((self.x - self.width / 2),
                                        (self.y - self.height / 2)),
                                         rect)
            self.need_to_stamp = False
        # And then the original image is loaded
        if self.rotate:
            self.costumes[self.cosnumber][1] = self.original_costumes[self.cosnumber][1]

    # @pausable
    def goto(self, x=None, y=None):
        if type(x) is int or type(x) is float:
            # if x is None:
            #     x = self.x
            # if y is None:
            #     y = self.y
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
        self.update_position()

    def pendown(self):
        self.pen_state = 'down'

    def penup(self):
        self.pen_state = 'up'

    def bounceOnEdge(self):
        if self.y > screen_info.resolution[1] or self.y < 0:
            self.direction = (180 - self.direction) % 360
            self.heading = self.direction - 90
            if self.rotate:
                self.transform = True
        if self.x > screen_info.resolution[0] or self.x < 0:
            self.direction = (0 - self.direction) % 360
            self.heading = self.direction - 90
            if self.rotate:
                self.transform = True

    # @pausable
    def forward(self, steps):
        if self.pen_state == 'down':
            startX = self.x
            startY = self.y
            for i in range(abs(steps)):
                pygame.draw.circle(screen_info.pen_surface,
                                   self.pencolor,
                                   [int(startX), int(startY)],
                                   self.pensize)
                # pygame.display.update()
                startX = self.x + i * math.sin(math.radians(self.direction))
                startY = self.y + i * -math.cos(math.radians(self.direction))
        self.x = round(self.x + steps * math.sin(math.radians(self.direction)))
        self.y = round(self.y + steps * -math.cos(math.radians(self.direction)))
        if self.bounce:
            self.bounceOnEdge()
        self.update_position()

    def back(self, steps):
        self.forward(-steps)

    # @pausable
    def right(self, angle):
        self.direction = (self.direction + angle) % 360
        self.heading = self.direction - 90
        if self.rotate:
            self.transform = True

    # @pausable
    def left(self, angle):
        self.direction = (self.direction - angle) % 360
        self.heading = self.direction - 90
        if self.rotate:
            self.transform = True

    def roll(self, angle):
        self.heading += angle
        if self.rotate:
            self.transform = True

    # @pausable
    def stamp(self):
        if not self.need_to_stamp:
            self.need_to_stamp = True

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
        if self.rotate:
            self.transform = True

    def flip(self, direction):
        if direction == 'horizontal':
            for cos in self.costumes:
                cos[1] = pygame.transform.flip(cos[1], True, False)
            for cos in self.original_costumes:
                cos[1] = pygame.transform.flip(cos[1], True, False)
        if direction == 'vertical':
            for cos in self.costumes:
                cos[1] = pygame.transform.flip(cos[1], False, True)
            for cos in self.original_costumes:
                cos[1] = pygame.transform.flip(cos[1], False, True)
        self.update_rect()

    def scale(self, w, h=None):
        if h is not None:
            for cos in self.costumes:
                cos[1] = pygame.transform.scale(cos[1], (w, h))
            for cos in self.original_costumes:
                cos[1] = pygame.transform.scale(cos[1], (w, h))
            self.actual_scale = [w, h]
            self.update_rect()
        else:
            width = int(self.width * w)
            height = int(self.height * w)
            self.scale(width, height)

    # check if the mouse has clicked the Actor
    def click(self, option='down'):
        mousepos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if not MOUSE.leftdown:
            if self.rect.collidepoint(mousepos) and buttons[0] == 1:
                MOUSE.leftdown = True
                return True
        else:
            for event in events_storage.list:
                if event.type == pygame.MOUSEBUTTONUP:
                    MOUSE.leftdown = False

    def rclick(self, option='down'):
        mousepos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if not MOUSE.rightdown:
            if self.rect.collidepoint(mousepos) and buttons[2] == 1:
                MOUSE.rightdown = True
                return True
        else:
            for event in events_storage.list:
                if event.type == pygame.MOUSEBUTTONUP:
                    MOUSE.rightdown = False

    # Mask collision
    @hideaway
    def collide(self, target):
        if isinstance(target, Actor):
            if not target.hidden:
                self.update_position()
                target.update_position()
                # result = pygame.sprite.groupcollide(self.sprite_group,
                #                                     target.sprite_group,
                #                                     False,
                #                                     False,
                #                                     pygame.sprite.collide_mask)
                # if len(result) > 0:
                #     # print(target.costume)
                #     return True
                result = pygame.sprite.collide_mask(self, target)
                if result is not None:
                    return True
        elif type(target) is list:
            for a in target:
                if self.collide(a):
                    return True
        elif type(target) is str:
            for obj in gc.get_objects():
                if isinstance(obj, Actor):
                    if obj.tag == target:
                        if self.collide(obj):
                            return True

    # Rect collision
    @hideaway
    def rectcollide(self, target):
        self.update_position()
        target.update_position()
        if not target.hidden:
            return self.rect.colliderect(target.rect)

    @hideaway
    def collidepoint(self, point):
        self.update_position()
        if point == MOUSE:
            return self.rect.collidepoint([MOUSE.x, MOUSE.y])
        else:
            return self.rect.collidepoint(point)

    # pause actor's actions (da completare)
    def pause(self, t=-1):
        self.paused = True
        if t >= 0:
            actors_info.paused_actors_list.append(self)
            self.pause_time = t * 1000
            self.start_pause_time = pygame.time.get_ticks()

    def unpause(self):
        self.paused = False
        actors_info.paused_actors_list.remove(self)

    @hideaway
    def hide(self, t=-1):
        if not self.hidden:
            self.hidden = True
            actors_to_draw.remove(self)
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
            actors_to_draw.add(self)
        else:
            pass


class Text(Actor):
    def __init__(self,
                 string='Text',
                 name='Liberation Serif',
                 fontsize=32, bold=False,
                 italic=False,
                 color=[0, 0, 0]):
        self.string = str(string)
        self.name = name
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.color = color
        Actor.__init__(self)

    def update_text(self):
        self.font = pygame.font.SysFont(self.name,
                                        self.fontsize,
                                        self.bold,
                                        self.italic)
        img = self.font.render(self.string, True, self.color)
        self.costumes[self.cosnumber][1] = img
        self.original_costumes[self.cosnumber][1] = img
        self.update_rect()

    def load(self, path, cosname):
        self.costumes.append([self.costume, None])
        self.original_costumes.append([self.costume, None])
        self.update_text()

    def write(self, string):
        self.string = str(string)
        self.update_text()

    def setfontsize(self, fontsize):
        self.fontsize = fontsize
        self.update_text()

    def setbold(self, bold=True):
        self.bold = bold
        self.update_text()

    def setitalic(self, italic=True):
        self.italic = italic
        self.update_text()

    def color(self, color):
        self.color = color
        self.update_text()


# SUONI
def load(path):
    pygame.mixer.music.load(path)


def play():
    pygame.mixer.music.play()


def Sound(path):
    s = pygame.mixer.Sound(path)
    return s


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
def key(key):
    if pygame.key.get_pressed()[key]:
        return True


# detect the single pression of a key
def keydown(key):
    for event in events_storage.list:
        if event.type == pygame.KEYDOWN:
            if event.key == key:
                return True


# detect the release of a key
def keyup(key):
    for event in events_storage.list:
        if event.type == pygame.KEYUP:
            if event.key == key:
                return True


# GAMEPAD
gamepadCount = pygame.joystick.get_count()
gamepads = []
for gamepadID in range(pygame.joystick.get_count()):
    # add gamepad to list
    gamepads.append(pygame.joystick.Joystick(gamepadID))
    # initialize gamepad
    gamepads[gamepadID].init()


# try:
#     # creo un oggetto Joystick
#     _pad0 = pygame.joystick.Joystick(0)
#     # inizializzo il joystick
#     _pad0.init()
# except:
#     print('no GamePad found...')

def buttondown(btn, pad=0):
    global gamepadCount, gamepads
    if gamepadCount > 0:
        return gamepads[pad].get_button(btn)
    else:
        print('no gamepad found...')


def axis(hand, direction, pad=0):
    global gamepadCount, gamepads
    if gamepadCount > 0:
        if hand == 'left':
            if direction == 'horizontal':
                return gamepads[pad].get_axis(0)
            elif direction == 'vertical':
                return gamepads[pad].get_axis(1)
        elif hand == 'right':
            if direction == 'horizontal':
                return gamepads[pad].get_axis(3)
            elif direction == 'vertical':
                return gamepads[pad].get_axis(4)
    else:
        print('no gamepad found...')


def trigger(hand, pad=0):
    global gamepadCount, gamepads
    if gamepadCount > 0:
        if hand == 'left':
            raw = gamepads[pad].get_axis(2)
            value = (raw + 1) / 2
            return value
        if hand == 'right':
            raw = gamepads[pad].get_axis(5)
            value = (raw + 1) / 2
            return value
