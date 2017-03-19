from pydojo import *

# CREATE GAME DISPLAY
screen(1920, 1080)

uga = Actor()
uga.goto(CENTER)
uga.pendown()
uga.pencolor = WHITE

p = 10

# MAIN LOOP
while True:

    # MOVE THE TURTLE
    uga.forward(p)
    uga.right(88)
    p = p + 5

    # DRAW IMAGES
    fill(BLACK)
    uga.draw()

    # UPDATE SCREEN
    update()

    # WAIT
    wait(10)
