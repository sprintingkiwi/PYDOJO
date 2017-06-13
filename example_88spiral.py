from pydojo import *

# CREATE GAME DISPLAY
screen(1920, 1080)

uga = Actor()
uga.pendown()
uga.setpencolor(ORANGE)

p = 10

# MAIN LOOP
while True:

    # MOVE THE TURTLE
    uga.forward(p)
    uga.right(88)
    p = p + 20
    uga.changepencolor(20)

    # UPDATE SCREEN
    update()
