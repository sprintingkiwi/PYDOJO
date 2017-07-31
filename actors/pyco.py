from pydojo import *
from gobo import Gobo

class Pyco(Actor):

    def setup(self):
        self.touched_gobo = False
        self.setx(100)
        self.testtimer = Timer(2000)
        self.rotate('flip')

    def update(self):

        if key(RIGHT):
            self.point(90)
            self.forward(10)
        if key(LEFT):
            self.point(-90)
            self.forward(10)

        if keydown(SPACE):
            self.jump()

        if self.testtimer.get():
            print("It is test time!")

    def collision(self, other, point):
        if type(other) is Gobo:
            self.touched_gobo = True
            print("Hello Gobo!")