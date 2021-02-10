from pydojo import *
# CREATE GAME DISPLAY
screen(1600, 900)

turtle = Actor()
turtle.hide()

turtles = []

time = 0

# MAIN LOOP
while True:

    clear()

    if ticks() - time > 100:
        t = clone(turtle)
        t.point(random.randint(-180, 180))
        t.tag('turtle')
        t.speed = random.randint(1, 10)
        t.pendown()
        turtles.append(t)
        time = ticks()

    for t in getactors('turtle'):
        t.changepencolor(random.randint(1, 100))
        t.forward(t.speed)
        t.bounce()
        t.setdirection(random.randint(t.direction - 10, t.direction + 10))
        if t.collide('turtle'):
            t.point(random.randint(-180, 180))

    # UPDATE SCREEN
    update()
