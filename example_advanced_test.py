from pydojo import *
from example_advanced_test_actors.gobo import *
from example_advanced_test_actors.pyco import *

# CREATE GAME DISPLAY
screen(800, 600)

pyco = Pyco('example_asset/characters/pyco1.png')
gobo = Gobo('example_asset/characters/gobo.png')

# MAIN LOOP
gameover = False
while not gameover:

    check_collisions()

    ACTORS.update()

    update()
