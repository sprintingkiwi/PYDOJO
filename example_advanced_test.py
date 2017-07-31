from pydojo import *
from actors.gobo import *
from actors.pyco import *
from actors.arrow import *

# CREATE GAME DISPLAY
screen(800, 600)

# setup()

pyco = Pyco('example_asset/characters/pyco1.png')
gobo = Gobo('example_asset/characters/gobo.png')
arrow = Arrow()

# MAIN LOOP
gameover = False
while not gameover:

    mainloop()
