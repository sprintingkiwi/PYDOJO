from pydojo import *
from actors.gobo import Gobo

class Arrow(Actor):

    def setup(self):
        self.target = find(Gobo)

    def update(self):
        self.point(self.target)

    def collision(self, other, point):
        pass
