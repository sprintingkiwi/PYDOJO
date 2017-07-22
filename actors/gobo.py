from pydojo import *

class Gobo(Actor):

    def update(self):
        self.goto(MOUSE)

    def collision(self, other, point):
        print("Hello there!")
