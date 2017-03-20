from pydojo import *

screen(1280, 720)
fill(LAVENDER)

uga = Actor()
uga.pendown()
uga.pensize = 10

while True:
    uga.forward(10)
    uga.right(10)

    if keydown(ESCAPE):
        quit()

    update()
    wait(10)