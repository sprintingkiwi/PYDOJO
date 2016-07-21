import pygame, math, random, time, os
import thread
import threading
#, types, inspect
pygame.init()

#COLORS
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

#some useful variables
mouse = "mouse"


class Actor(pygame.sprite.Sprite):
    def __init__(self, path=None):
        pygame.sprite.Sprite.__init__(self)
        #Actor coordinates
        self.x = 0.0
        self.y = 0.0
        #Actor angle direction
        self.direction = 0
        if path is not None:
            self.load(path)
        #rotation style
        self.rotate = True
        #needs to transform image?
        self.transform = False

    #find costume name from image path
    def costume_name(self, path):
        words = path.split("/")
        lenpath = len(words)
        costume = words[lenpath - 1]
        self.costume = costume.split(".")[0]

    #update rect as the image changes
    def update_rect(self):
        self.rect = self.image.get_rect()
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.size = self.image.get_size()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    #load Actor's image
    def load(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.original_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.update_rect()
        self.costume_name(path)

    def setposition(self, pos):
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

    def draw(self, surface, rect=None):
        #if the image changed the transform functions apply
        if self.transform is True:
            self.transform = False
            self.image = pygame.transform.rotate(self.image, -self.direction)
            self.update_rect()
            surface.blit(self.image,
                         ((self.x - self.width / 2),
                         (self.y - self.height / 2)),
                         rect)
            #and then the original image is loaded
            self.image = self.original_image
        else:
            surface.blit(self.image,
                        ((self.x - self.width / 2), (self.y - self.height / 2)),
                        rect)

    def goto(self, x, y=0):
        if type(x) is int:
            self.x = x
            self.y = y

        elif x == "mouse":
            pos = pygame.mouse.get_pos()
            self.x = pos[0]
            self.y = pos[1]

        self.update_rect()

    def gorand(self, rangex=[0, 800], rangey=[0, 600]):
        self.x = random.randint(rangex[0], rangex[1])
        self.y = random.randint(rangey[0], rangey[1])
        self.update_rect()

    def forward(self, steps):
        self.x = round(self.x + steps * math.sin(math.radians(self.direction)))
        self.y = round(self.y + steps * -math.cos(math.radians(self.direction)))
        self.update_rect()

    def right(self, angle):
        self.direction = (self.direction + angle) % 360
        if self.rotate:
            self.transform = True

    def left(self, angle):
        self.direction = (self.direction - angle) % 360
        if self.rotate:
            self.transform = True

    def point(self, target):
        #set heading as angle
        if type(target) is int and type(target) is not str:
            self.direction = target % 360
        #point at coordinate
        elif type(target) is list and type(target) is not str:
            angle = -math.atan2(self.x - target[0], self.y - target[1])
            angle = angle * (180 / math.pi)
            self.direction = angle
        #point at mouse pointer
        elif target == "mouse":
            mousepos = pygame.mouse.get_pos()
            angle = -math.atan2(self.x - mousepos[0], self.y - mousepos[1])
            angle = angle * (180 / math.pi)
            self.direction = angle
        #point at target
        else:
            angle = -math.atan2(self.x - target.x, self.y - target.y)
            angle = angle * (180 / math.pi)
            self.direction = angle
        if self.rotate:
            self.transform = True

    def flip(self, direction):
        if direction == "horizontal":
            self.image = pygame.transform.flip(self.image, True, False)
        if direction == "vertical":
            self.image = pygame.transform.flip(self.image, False, True)
        self.update_rect()

    def scale(self, w, h=None):
        if h is not None:
            self.image = pygame.transform.scale(self.image, (w, h))
            self.original_image = self.image
            self.update_rect()
        else:
            width = int(self.width * w)
            height = int(self.height * w)
            self.scale(width, height)

    #check if mouse has clicked the Actor
    def click(self, option="down"):
        mousepos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if not MOUSE.leftdown:
            if self.rect.collidepoint(mousepos) and buttons[0] == 1:
                MOUSE.leftdown = True
                return True
        else:
            for event in EVENTS.LIST:
                if event.type == pygame.MOUSEBUTTONUP and \
                       event.button == 1 and \
                       self.rect.collidepoint(mousepos):
                    MOUSE.leftdown = False

    def rclick(self, option="down"):
        mousepos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if not MOUSE.leftdown:
            if self.rect.collidepoint(mousepos) and buttons[2] == 1:
                MOUSE.leftdown = True
                return True
        else:
            for event in EVENTS.LIST:
                if event.type == pygame.MOUSEBUTTONUP and \
                       event.button == 1 and \
                       self.rect.collidepoint(mousepos):
                    MOUSE.leftdown = False

    #Mask collision
    def mcollide(self, target):
        result = pygame.sprite.collide_mask(self, target)
        if result is not None:
            return True
        #print(result)

    #Rect collision
    def collide(self, target):
        return self.rect.colliderect(target.rect)


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
        self.update_text()

    def update_text(self):
        self.font = pygame.font.SysFont(self.name,
                                        self.fontsize,
                                        self.bold,
                                        self.italic)
        self.image = self.font.render(self.string, True, self.color)
        self.update_rect()

    def write(self, string):
        self.string = str(string)
        self.update_text()

    def setfontsize(self, fontsize):
        self.fontsize = fontsize
        self.update_text()

    def setbold(self, bold):
        self.bold = bold
        self.update_text()

    def setitalic(self, italic):
        self.italic = italic
        self.update_text()

    def color(self, color):
        self.color = color
        self.update_text()


class Rect(Actor):
    def __init__(self, size=[32, 32], color=[255, 0, 0], line_width=0):
        self.x = 0.0
        self.y = 0.0
        self.size = size
        self.color = color
        self.line_width = line_width
        self.update_rect()
        self.direction = 0
        self.transform = False
        self.rotate = False

    def update_rect(self):
        self.rect = pygame.Rect(int(self.x),
                                int(self.y),
                                self.size[0],
                                self.size[1])
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def draw(self, surface):
        pygame.draw.rect(surface,
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
        self.update_rect()
        self.direction = 0
        self.transform = False
        self.rotate = False

    def update_rect(self):
        self.rect = pygame.Rect(int(self.x),
                                int(self.y),
                                self.radius * 2,
                                self.radius * 2)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def draw(self, surface):
        pygame.draw.circle(surface,
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


#SCREEN
def Screen(w, h):
    return pygame.display.set_mode([w, h])

def UPDATE():
    EVENTS.LIST = pygame.event.get()
    pygame.display.update()


#EVENTS:

#KEYBOARD KEYS
UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT


def keydown(key):
    if pygame.key.get_pressed()[key]:
        return True



class Events():
    def __init__(self):
        self.CHECK = False
        self.LIST = []
EVENTS = Events()

class Mouse():
    def __init__(self):
        self.leftdown = False
        self.centraldown = False
        self.rightdown = False
MOUSE = Mouse()




#def keydown(key):
    #for event in pygame.event.get():
        #if event.type == pygame.KEYDOWN:
            #if event.key == key:
                #return True



########################################

#Multi-Thread recipe
#class Operation(threading._Timer):
    #def __init__(self, *args, **kwargs):
        #threading._Timer.__init__(self, *args, **kwargs)
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

#timer = Manager()
#timer.add_operation(events, 0.01)



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


