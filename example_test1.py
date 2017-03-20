from pydojo import *

# create game display
screen(1280, 720)

dyno = Actor('example_library/dinosaur1.png')
dyno.scale(0.2)
dyno.goto(500, 300)

star = Actor('example_library/seastar1.png', 'felice')
star.load('example_library/seastar2.png', 'triste')
star.scale(100, 200)
star.goto(600, 500)

a = Text('ciao', color=GREEN, italic=True)
print(a.costumes)
a.setfontsize(48)
a.setbold(True)
a.goto(100, 100)

# dyno.rotate = False

# r = Rect(size=[32, 32], color=BLUE)
# r.goto(400, 250)
#
# c = Circle(radius=64, line_width=20)
# c.goto(500, 400)

hey = Sound('example_library/hey.wav')

print(actorsInfo.actorsList)

while True:

    if dyno.click():
        print('funziona')
        hey.play()
        print(dyno.getcostume())

    if keydown(RIGHT):
        print('destra')
        star.point(90)
        star.forward(5)

    if keydown(LEFT):
        print('sinistra')
        star.point(-90)
        star.forward(5)

    # dyno.direction = 90
    # dyno.left(1)
    a.right(1)
    # r.right(10)
    # c.left(5)
    dyno.goto(MOUSE)
    # r.point('mouse')
    dyno.forward(10)
    # r.forward(2)
    # c.forward(20)
    # dyno.gorand()

    # if asize > 10:
    # asize = 0.1
    # asize += 0.1
    ##    a.scale(0.2)

    if dyno.collide(star):
        print(dyno.collide(star))
        star.setcostume(1)
        # hey.play()
        dyno.hide(2)

    if star.costume == 'triste' and not star.collide(dyno):
        star.setcostume('felice')

    if keydown(D):
        dyno.show()

    fill(PINK)
    a.draw()
    star.draw()
    dyno.draw()
    # r.draw()
    # c.draw()

    # update screen and events queue
    update()

    # wait
    sleep(0.01)
