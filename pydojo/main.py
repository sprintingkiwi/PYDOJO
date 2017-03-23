import pygame, math, random, os, subprocess, sys
from pyfirmata import *
from serial import *
from time import sleep, time

pygame.init()

# CONSTANTS
LIBRARY_VERSION = 1.3

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

# OBJECTS FOR DATA STORAGE
class EventsStorage():
    def __init__(self):
        self.CHECK = False
        self.LIST = []


eventsStorage = EventsStorage()


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
        self.penSurface = pygame.Surface([32, 32])
        self.hasBackground = False
        self.bgColor = BLACK
        self.colorFilled = False

    def createBackground(self, *args):
        self.background = Actor(*args)
        self.background.layer = -100
        self.background.scale(self.resolution[0], self.resolution[1])
        self.hasBackground = True


screenInfo = ScreenInfo()


class ActorsInfo():
    def __init__(self):
        self.actorsList = []
        self.drawList = []
        self.pausedActorsList = []
        self.hiddenActorsList = []
        self.counts = []


actorsInfo = ActorsInfo()

# Screen Center Constant
CENTER = pygame.sprite.Sprite()


# SCREEN
def screen(w, h, fullscreen=False):
    screenInfo.resolution = [w, h]
    if fullscreen:
        screenInfo.screen = pygame.display.set_mode([w, h], pygame.FULLSCREEN)
    else:
        screenInfo.screen = pygame.display.set_mode([w, h])
    # Create surface for turtle drawings
    path = (os.path.dirname(sys.modules[__name__].__file__))
    path = os.path.join(path, 'pensurface.png')
    screenInfo.penSurface = pygame.image.load(path).convert_alpha()
    screenInfo.penSurface = pygame.transform.scale(screenInfo.penSurface, screenInfo.resolution)
    CENTER.x = screenInfo.resolution[0] / 2
    CENTER.y = screenInfo.resolution[1] / 2


def SCREEN(*args):
    screen(*args)


def enableBackground():
    if screenInfo.colorFilled:
        actorsInfo.actorsList.append(screenInfo.background)
        screenInfo.colorFilled = False


def disableBackground():
    if not screenInfo.colorFilled and screenInfo.hasBackground:
        actorsInfo.actorsList.remove(screenInfo.background)
        screenInfo.colorFilled = True


def fill(color):
    screenInfo.bgColor = color
    disableBackground()


def background(*args):
    screenInfo.createBackground(*args)
    enableBackground()


def loadbackground(*args):
    if not screenInfo.hasBackground:
        screenInfo.createBackground(*args)
    else:
        screenInfo.background.load(*args)
        # screenInfo.background.setcostume(screenInfo.background.cosnumber + 1)


def setbackground(*args):
    screenInfo.background.setcostume(*args)
    enableBackground()


defaultClock = pygame.time.Clock()


# One of the most important functions
def update():
    # Refresh the event list
    eventsStorage.LIST = pygame.event.get()
    # Refresh mouse position
    MOUSE.pos = pygame.mouse.get_pos()
    MOUSE.x = MOUSE.pos[0]
    MOUSE.y = MOUSE.pos[1]
    # Manage the time for hide and pause methods
    actualTime = pygame.time.get_ticks()
    # Compute actors pauses
    for actor in actorsInfo.pausedActorsList:
        deltaTime = actualTime - actor.startPauseTime
        if deltaTime >= actor.pauseTime:
            actor.paused = False
            actorsInfo.pausedActorsList.remove(actor)
    # Compute actors hide time
    for actor in actorsInfo.hiddenActorsList:
        deltaTime = actualTime - actor.startHideTime
        if deltaTime >= actor.hideTime:
            actor.hidden = False
            actorsInfo.hiddenActorsList.remove(actor)
            actorsInfo.drawList.append(actor)
    # Order Actor's list by layer
    actorsInfo.drawList.sort(key=lambda x: x.layer)
    # Draw screen base color
    screenInfo.screen.fill(screenInfo.bgColor)
    # Draw Actors (and Background)
    for actor in actorsInfo.drawList:
        actor.draw()
    # Draw the turtle drawings surface
    screenInfo.screen.blit(screenInfo.penSurface, [0, 0])
    # refresh the pygame screen
    pygame.display.update()
    defaultClock.tick(60)


def UPDATE():
    update()


def Clock():
    return pygame.time.Clock()


def wait(ms):
    pygame.time.wait(ms)


def ticks():
    return pygame.time.get_ticks()


def pausable(func):
    def wrapper(self, *args):
        if not self.paused:
            return func(self, *args)
    return wrapper


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
        if path is None:
            path = (os.path.dirname(sys.modules[__name__].__file__))
            path = os.path.join(path, 'turtle.png')
            print path
        actorsInfo.actorsList.append(self)
        actorsInfo.drawList.append(self)
        pygame.sprite.Sprite.__init__(self)
        # Actor coordinates
        self.x = 0.0
        self.x = screenInfo.resolution[0] / 2
        self.y = 0.0
        self.y = screenInfo.resolution[1] / 2
        # Actor angle direction
        self.direction = 90
        # image orientation
        self.heading = 0
        self.layer = 0
        self.actualScale = 1
        self.count = 0
        self.paused = False
        self.hidden = False
        self.pauseTime = 0.0
        self.hideTime = 0.0
        self.startPauseTime = 0.0
        self.startHideTime = 0.0
        # load actor image
        self.costumes = []
        self.costume = ''
        self.cosnumber = 0
        self.originalCostumes = []
        self.coscount = 0
        # if path is not None:
        self.load(path, cosname)
        # rotation style
        self.rotate = True
        self.rotation = 360
        self.needToFlip = 'left'
        # needs to transform image?
        self.transform = False
        self.penState = 'up'
        self.pencolor = RED
        self.pensize = 1
        self.needToStamp = False

    # find costume name from image path
    def findCostumeName(self, path):
        words = path.split('/')
        costume = words[-1]
        return costume.split('.')[0]

    # update rect as the image changes
    def updateRect(self):
        self.rect = self.costumes[self.cosnumber][1].get_rect()
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.size = self.costumes[self.cosnumber][1].get_size()
        self.width = self.costumes[self.cosnumber][1].get_width()
        self.height = self.costumes[self.cosnumber][1].get_height()
        self.actualScale = [self.width, self.height]

    # load Actor's image
    def load(self, path, cosname=None):
        if cosname is None:
            self.costume = self.findCostumeName(path)
        else:
            self.costume = cosname
        img = pygame.image.load(path).convert_alpha()
        if len(self.costumes) > 0:
            img = pygame.transform.scale(img, self.actualScale)
        self.costumes.append([self.costume, img])
        self.originalCostumes.append([self.costume, img])
        self.mask = pygame.mask.from_surface(self.costumes[self.cosnumber][1])
        self.updateRect()

    def loadcostume(self, path, cosname=None):
        self.load(path, cosname)

    def loadfolder(self, path):
        pass

    def setcostume(self, newcostume):
        if type(newcostume) is int:
            self.cosnumber = newcostume
        elif type(newcostume) is str:
            for cos in self.costumes:
                if cos[0] == newcostume:
                    self.cosnumber = self.costumes.index(cos)
        self.updateRect()

    def getcostume(self):
        return self.costume

    def nextcostume(self, pause=1):
        if self.coscount > pause:
            if self.cosnumber < len(self.costumes) - 1:
                self.setcostume(self.cosnumber + 1)
            else:
                self.setcostume(0)
            self.coscount = 0
        self.coscount += 1

    def setposition(self, pos=0, y=0):
        if pos is float:
            self.x = pos
            self.y = y
        else:
            self.x = pos[0]
            self.y = pos[1]

    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

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

    # @hideaway
    def draw(self, rect=None):
        # If the image changed the transform functions apply
        if self.rotate:
            # Full 360 rotation style
            if self.rotation == 360:
                self.costumes[self.cosnumber][1] = pygame.transform.rotate(self.costumes[self.cosnumber][1], -self.heading)
                self.updateRect()
            # Horizontal Flip rotation style
            elif self.rotation == 'flip':
                if self.direction < 0 or self.direction > 180:
                    if self.needToFlip == 'left':
                        self.flip('horizontal')
                        self.needToFlip = 'right'
                if self.direction > 0 and self.direction < 180:
                    if self.needToFlip == 'right':
                        self.flip('horizontal')
                        self.needToFlip = 'left'
        # Blit the image to the screen
        screenInfo.screen.blit(self.costumes[self.cosnumber][1],
                               ((self.x - self.width / 2),
                                (self.y - self.height / 2)),
                               rect)
        # Stamp in the turtle drawing surface
        if self.needToStamp:
            screenInfo.penSurface.blit(self.costumes[self.cosnumber][1],
                                       ((self.x - self.width / 2),
                                        (self.y - self.height / 2)),
                                       rect)
            self.needToStamp = False
        # And then the original image is loaded
        if self.rotate:
            self.costumes[self.cosnumber][1] = self.originalCostumes[self.cosnumber][1]

    @pausable
    def goto(self, x, y=0):
        if type(x) is int:
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
        self.updateRect()

    @pausable
    def gorand(self,
               rangex=[0, screenInfo.resolution[0]],
               rangey=[0, screenInfo.resolution[1]]):
        self.x = random.randint(rangex[0], rangex[1])
        self.y = random.randint(rangey[0], rangey[1])
        self.updateRect()

    def pendown(self):
        self.penState = 'down'

    def penup(self):
        self.penState = 'up'

    @pausable
    def forward(self, steps):
        if self.penState == 'down':
            startX = self.x
            startY = self.y
            for i in range(steps):
                pygame.draw.circle(screenInfo.penSurface,
                                   self.pencolor,
                                   [int(startX), int(startY)],
                                   self.pensize)
                # pygame.display.update()
                startX = self.x + i * math.sin(math.radians(self.direction))
                startY = self.y + i * -math.cos(math.radians(self.direction))
        self.x = round(self.x + steps * math.sin(math.radians(self.direction)))
        self.y = round(self.y + steps * -math.cos(math.radians(self.direction)))
        self.updateRect()

    @pausable
    def right(self, angle):
        self.direction = (self.direction + angle) % 360
        self.heading = self.direction - 90
        if self.rotate:
            self.transform = True

    @pausable
    def left(self, angle):
        self.direction = (self.direction - angle) % 360
        self.heading = self.direction - 90
        if self.rotate:
            self.transform = True

    @pausable
    def stamp(self):
        if not self.needToStamp:
            self.needToStamp = True

    @pausable
    def point(self, target):
        # set heading as angle
        if type(target) is int and type(target) is not str:
            angle = target % 360
            self.direction = angle
            self.heading = angle - 90
        # point at coordinate
        elif type(target) is list and type(target) is not str:
            angle = -math.atan2(self.x - target[0], self.y - target[1])
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
            for cos in self.originalCostumes:
                cos[1] = pygame.transform.flip(cos[1], True, False)
        if direction == 'vertical':
            for cos in self.costumes:
                cos[1] = pygame.transform.flip(cos[1], False, True)
            for cos in self.originalCostumes:
                cos[1] = pygame.transform.flip(cos[1], False, True)
        self.updateRect()

    def scale(self, w, h=None):
        if h is not None:
            for cos in self.costumes:
                cos[1] = pygame.transform.scale(cos[1], (w, h))
            for cos in self.originalCostumes:
                cos[1] = pygame.transform.scale(cos[1], (w, h))
            self.actualScale = [w, h]
            self.updateRect()
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
            for event in eventsStorage.LIST:
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
            for event in eventsStorage.LIST:
                if event.type == pygame.MOUSEBUTTONUP:
                    MOUSE.rightdown = False

    # Mask collision
    @hideaway
    def mcollide(self, target):
        result = pygame.sprite.collide_mask(self, target)
        if result is not None:
            return True
            # print(result)

    # Rect collision
    @hideaway
    def collide(self, target):
        if not target.hidden:
            return self.rect.colliderect(target.rect)

    @hideaway
    def collidepoint(self, point):
        if point == MOUSE:
            return self.rect.collidepoint([MOUSE.x, MOUSE.y])
        else:
            return self.rect.collidepoint(point)

    # pause actor's actions (da completare)
    def pause(self, t=-1):
        self.paused = True
        if t >= 0:
            actorsInfo.pausedActorsList.append(self)
            self.pauseTime = t * 1000
            self.startPauseTime = pygame.time.get_ticks()

    def unpause(self):
        self.paused = False
        actorsInfo.pausedActorsList.remove(self)

    @hideaway
    def hide(self, t=-1):
        self.hidden = True
        actorsInfo.drawList.remove(self)
        if t >= 0:
            actorsInfo.hiddenActorsList.append(self)
            self.hideTime = t * 1000
            self.startHideTime = pygame.time.get_ticks()

    def show(self):
        if self.hidden:
            self.hidden = False
            try:
                actorsInfo.hiddenActorsList.remove(self)
            except:
                print(actorsInfo.hiddenActorsList)
            actorsInfo.drawList.append(self)
        else:
            pass


class Text(Actor):
    def __init__(self,
                 string,
                 name='Liberation Serif',
                 fontsize=32, bold=False,
                 italic=False,
                 color=[0, 0, 0]):
        Actor.__init__(self)
        self.string = str(string)
        self.name = name
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.color = color
        self.updateText()

    def updateText(self):
        self.font = pygame.font.SysFont(self.name,
                                        self.fontsize,
                                        self.bold,
                                        self.italic)
        img = self.font.render(self.string, True, self.color)
        self.costumes[self.cosnumber][1] = img
        self.originalCostumes[self.cosnumber][1] = img
        self.updateRect()

    def load(self, path, cosname):
        self.costumes.append([self.costume, None])
        self.originalCostumes.append([self.costume, None])

    def write(self, string):
        self.string = str(string)
        self.updateText()

    def setfontsize(self, fontsize):
        self.fontsize = fontsize
        self.updateText()

    def setbold(self, bold=True):
        self.bold = bold
        self.updateText()

    def setitalic(self, italic=True):
        self.italic = italic
        self.updateText()

    def color(self, color):
        self.color = color
        self.updateText()


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
    for event in eventsStorage.LIST:
        if event.type == pygame.KEYDOWN:
            if event.key == key:
                return True


# detect the release of a key
def keyup(key):
    for event in eventsStorage.LIST:
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
