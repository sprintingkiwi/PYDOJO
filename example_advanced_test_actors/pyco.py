from pydojo import *

class Pyco(Actor):

    def setup(self):
        self.touched_gobo = False
        self.setx(100)

    def update(self):
        if key(RIGHT) and not self.touched_gobo:
            self.point(90)
            self.forward(10)

    def collision(self, other, point):
        if other.costume == "gobo":
            self.touched_gobo = True
            print("Hello Gobo!")