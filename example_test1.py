from pydojo import *

# create game display
screen(1280, 720)

dyno = Actor('example_asset/characters/dinosaur1.png')
dyno.scale(0.8)
dyno.goto(800, 0)
dyno.rotation = 'flip'

star = Actor('example_asset/characters/seastar1.png', 'felice')
star.load('example_asset/characters/seastar2.png', 'triste')
star.scale(180, 180)
star.goto(600, 500)

testo = Text('ciao', color=GREEN, italic=True)
print(testo.costumes)
testo.setfontsize(48)
testo.setbold(True)
testo.goto(100, 100)
testo.scale(2)

# dyno.roll = False

hey = Sound('example_asset/sounds/hey.wav')

while True:
    # testo.scale(0.9)

    # print(actorsInfo.drawList)

    if dyno.click():
        print('funziona')
        hey.play()
        print(dyno.getcostume())
        save(ticks(), "time_dyno")

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
    testo.right(1)
    dyno.point(MOUSE)
    dyno.forward(3)
    if keydown(G):
    #     dyno.pendown()
    #     dyno.gorand()
        dyno.glide(testo)

    if keydown(W):
        print(dyno.x, dyno.y)

    star.left(1)
    # print(dyno.direction)

    if dyno.collide(star):
        # print(dyno.collide(star))
        star.setcostume(1)
        print('dyno ha toccato star')
        # hey.play()
        dyno.hide(2)

    if dyno.collide(testo):
        testo.write('toccato')

    if keydown(F):
        star.setcostume('felice')

    if keydown(D):
        dyno.show()

    if keydown(B):
        terminate()

    fill(PINK)

    # update screen and events queue
    update()
