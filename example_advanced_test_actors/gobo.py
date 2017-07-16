from pydojo import *

class Gobo(Actor):

    def update(self):
        if ticks() > 2000:
            self.forward(3)

    def collision(self, other, point):
        print("Hello there!")
