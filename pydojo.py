import pygame, math, random, time, os
from time import sleep
#import thread
#import threading
#, types, inspect
pygame.init()

#COLORS
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

#useful variables
mouse = "mouse"


#Objects for saving data
class EventsStorage():
    def __init__(self):
        self.CHECK = False
        self.LIST = []
eventsStorage = EventsStorage()


class Mouse():
    def __init__(self):
        self.leftdown = False
        self.centraldown = False
        self.rightdown = False
        self.pos = pygame.mouse.get_pos()
        self.x = self.pos[0]
        self.y = self.pos[1]
MOUSE = Mouse()


class ScreenInfo():
    def __init__(self):
        self.screen = None
        self.resolution = []
screenInfo = ScreenInfo()


class ActorsInfo():
    def __init__(self):
        self.actorsList = []
        self.counts = []
actorsInfo = ActorsInfo()


#SCREEN
def SCREEN(w, h):
    screenInfo.resolution = [w, h]
    screenInfo.screen = pygame.display.set_mode([w, h])


def fill(color):
    screenInfo.screen.fill(color)


# one of the most important functions
def UPDATE():
    # refresh the event list
    eventsStorage.LIST = pygame.event.get()
    # refresh mouse position
    MOUSE.pos = pygame.mouse.get_pos()
    MOUSE.x = MOUSE.pos[0]
    MOUSE.y = MOUSE.pos[1]
    # manage the time for hide and pause methods
    actualTime = pygame.time.get_ticks()
    for actor in actorsInfo.actorsList:
        deltaTime = actualTime - actor.startPauseTime
        if deltaTime >= actor.pauseTime:
            actor.paused = False
        deltaTime = actualTime - actor.startHideTime
        if deltaTime >= actor.hideTime:
            actor.hidden = False
    # refresh the pygame screen
    pygame.display.update()


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


#ACTOR CLASS
class Actor(pygame.sprite.Sprite):
    def __init__(self, path=None, cosname=None):
        actorsInfo.actorsList.append(self)
        pygame.sprite.Sprite.__init__(self)
        #Actor coordinates
        self.x = 0.0
        self.y = 0.0
        #Actor angle direction
        self.direction = 0
        #image orientation
        self.heading = 0
        self.count = 0
        self.paused = False
        self.hidden = False
        self.pauseTime = 0.0
        self.hideTime = 0.0
        self.startPauseTime = 0.0
        self.startHideTime = 0.0
        #load actor image
        self.costumes = []
        self.costume = ""
        self.cosnumber = 0
        self.originalCostumes = []
        self.coscount = 0
        #if path is not None:
        self.load(path, cosname)
        #rotation style
        self.rotate = True
        #needs to transform image?
        self.transform = False

    #find costume name from image path
    def findCosname(self, path):
        words = path.split("/")
        costume = words[-1]
        return costume.split(".")[0]

    #update rect as the image changes
    def updateRect(self):
        self.rect = self.costumes[self.cosnumber][1].get_rect()
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.size = self.costumes[self.cosnumber][1].get_size()
        self.width = self.costumes[self.cosnumber][1].get_width()
        self.height = self.costumes[self.cosnumber][1].get_height()

    #load Actor's image
    def load(self, path, cosname=None):
        if cosname is None:
            self.costume = self.findCosname(path)
        else:
            self.costume = cosname
        img = pygame.image.load(path).convert_alpha()
        self.costumes.append([self.costume, img])
        self.originalCostumes.append([self.costume, img])
        self.mask = pygame.mask.from_surface(self.costumes[self.cosnumber][1])
        self.updateRect()

    def loadcostume(self, path, cosname=None):
        self.load(path, cosname)

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

    def nextcostume(self, pause):
        if self.coscount > pause:
            self.setcostume(self.costume + 1)
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

    @hideaway
    def draw(self, rect=None):
        #if the image changed the transform functions apply
        #if self.transform is True:
            #self.transform = False
        if self.rotate is True:
            self.costumes[self.cosnumber][1] = pygame.transform.rotate(self.costumes[self.cosnumber][1], -self.heading)
            self.updateRect()
            screenInfo.screen.blit(self.costumes[self.cosnumber][1],
                         ((self.x - self.width / 2),
                         (self.y - self.height / 2)),
                         rect)
            #and then the original image is loaded
            self.costumes[self.cosnumber][1] = self.originalCostumes[self.cosnumber][1]
        else:
            screenInfo.screen.blit(self.costumes[self.cosnumber][1],
                        ((self.x - self.width / 2), (self.y - self.height / 2)),
                        rect)

    @pausable
    def goto(self, x, y=0):
        if type(x) is int:
            self.x = x
            self.y = y

        elif x == "mouse":
            pos = pygame.mouse.get_pos()
            self.x = pos[0]
            self.y = pos[1]

        else:
            self.x = x.x
            self.y = x.y

        self.updateRect()

    @pausable
    def gorand(self, rangex=[0, 800], rangey=[0, 600]):
        self.x = random.randint(rangex[0], rangex[1])
        self.y = random.randint(rangey[0], rangey[1])
        self.updateRect()

    @pausable
    def forward(self, steps):
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
    def point(self, target):
        #set heading as angle
        if type(target) is int and type(target) is not str:
            angle = target % 360
            self.direction = angle
            self.heading = angle - 90
        #point at coordinate
        elif type(target) is list and type(target) is not str:
            angle = -math.atan2(self.x - target[0], self.y - target[1])
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        #point at mouse pointer
        elif target == "mouse":
            mousepos = pygame.mouse.get_pos()
            angle = -math.atan2(self.x - mousepos[0], self.y - mousepos[1])
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        #point at target
        else:
            angle = -math.atan2(self.x - target.x, self.y - target.y)
            angle = angle * (180 / math.pi)
            self.direction = angle
            self.heading = angle - 90
        if self.rotate:
            self.transform = True

    def flip(self, direction):
        if direction == "horizontal":
            self.costumes[self.cosnumber][1] = pygame.transform.flip(self.costumes[self.cosnumber][1], True, False)
        if direction == "vertical":
            self.costumes[self.cosnumber][1] = pygame.transform.flip(self.costumes[self.cosnumber][1], False, True)
        self.updateRect()

    def scale(self, w, h=None):
        if h is not None:
            for cos in self.costumes:
                cos[1] = pygame.transform.scale(cos[1], (w, h))
            for cos in self.originalCostumes:
                cos[1] = pygame.transform.scale(cos[1], (w, h))
            self.updateRect()
        else:
            width = int(self.width * w)
            height = int(self.height * w)
            self.scale(width, height)

    #check if the mouse has clicked the Actor
    def click(self, option="down"):
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

    def rclick(self, option="down"):
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

    #Mask collision
    def mcollide(self, target):
        result = pygame.sprite.collide_mask(self, target)
        if result is not None:
            return True
        #print(result)

    #Rect collision
    def collide(self, target):
        return self.rect.colliderect(target.rect)

    def collidepoint(self, point):
        if point == MOUSE:
            return self.rect.collidepoint([MOUSE.x, MOUSE.y])
        else:
            return self.rect.collidepoint(point)

    #pause actor's actions (da completare)
    def pause(self, t):
        self.paused = True
        self.pauseTime = t * 1000
        self.startPauseTime = pygame.time.get_ticks()

    def hide(self, t):
        self.hidden = True
        self.hideTime = t * 1000
        self.startHideTime = pygame.time.get_ticks()

    def show(self):
        self.hidden = False



class Text(Actor):
    def __init__(self,
                 string,
                 name="Liberation Serif",
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


class Rect(Actor):
    def __init__(self, size=[32, 32], color=[255, 0, 0], line_width=0):
        self.x = 0.0
        self.y = 0.0
        self.size = size
        self.color = color
        self.line_width = line_width
        self.updateRect()
        self.direction = 0
        self.transform = False
        self.rotate = False
        self.paused = False
        self.hidden = False

    def updateRect(self):
        self.rect = pygame.Rect(int(self.x),
                                int(self.y),
                                self.size[0],
                                self.size[1])
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    @hideaway
    def draw(self):
        pygame.draw.rect(screenInfo.screen,
                             self.color,
                             self.rect,
                             self.line_width)


class Circle(Actor):
    def __init__(self, color=[255, 0, 0], radius=32, line_width=0):
        self.x = 0.0
        self.y = 0.0
        self.radius = int(radius)
        self.color = color
        self.line_width = int(line_width)
        self.updateRect()
        self.direction = 0
        self.transform = False
        self.rotate = False
        self.paused = False
        self.hidden = False

    def updateRect(self):
        self.rect = pygame.Rect(int(self.x),
                                int(self.y),
                                self.radius * 2,
                                self.radius * 2)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    @hideaway
    def draw(self):
        pygame.draw.circle(screenInfo.screen,
                           self.color,
                           [self.rect.centerx, self.rect.centery],
                           self.radius,
                           self.line_width)


#SUONI
def load(path):
    pygame.mixer.music.load(path)


def play():
    pygame.mixer.music.play()


def Sound(path):
    s = pygame.mixer.Sound(path)
    return s


#EVENTS:

#KEYBOARD KEYS
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

#detect the pression of a key
def keydown(key):
    if pygame.key.get_pressed()[key]:
        return True

#detect the release of a key
def keyup(key):
    for event in eventsStorage:
        if event.type == pygame.KEYUP:
            if event.key == key:
                return True






#class KeyStorage():
    #def __init__(self):
        #self.dictionary = dict
#key_storage = KeyStorage()




#def keydown(key):
    #for event in pygame.event.get():
        #if event.type == pygame.KEYDOWN:
            #if event.key == key:
                #return True



########################################

#Multi-Thread recipe
#class Operation(threading._pauseTime):
    #def __init__(self, *args, **kwargs):
        #threading._pauseTime.__init__(self, *args, **kwargs)
        #self.setDaemon(True)

    #def run(self):
        #while True:
            #self.finished.clear()
            #self.finished.wait(self.interval)
            #if not self.finished.isSet():
                #self.function(*self.args, **self.kwargs)
            #else:
                #return
            #self.finished.set()

#class Manager(object):

    #ops = []

    #def add_operation(self, operation, interval, args=[], kwargs={}):
        #op = Operation(interval, operation, args, kwargs)
        #self.ops.append(op)
        #thread.start_new_thread(op.run, ())

    #def stop(self):
        #for op in self.ops:
            #op.cancel()
        #self._event.set()


#def events():
    #pygame.event.get()
    #print("sto andando")

#pauseTime = Manager()
#pauseTime.add_operation(events, 0.01)



#######################################

#class Screen():

    #def __init__(self, w, h):
        #self.s = pygame.display.set_mode([w, h])

    #def update(self):
        #pygame.display.update()

    #def __getattr__(self, name):
        #print(self.s)
        #if hasattr(self[0], name):
            #def fn(*args):
                #getattr(self.s, name)(*args)
            #return fn
        #else:
            #raise AttributeError


#def Screen(w, h):

    #class MySurf(pygame.Surface):

        #def __init__(self):
            #super(MySurf, self).__init__((w, h))

        #def update(self):
            #pygame.display.update()

        ##@classmethod
        ##def convert_to_MySurf(cls, obj):
            ##obj.__class__ = MySurf

    #s = pygame.display.set_mode([w, h])
    #print(s)

    #myS = MySurf()
    #for n, v in inspect.getmembers(s):
        #setattr(myS, n, v);


    ##MySurf.convert_to_MySurf(s)
    ##print(s)

    #return myS


