

######################################################
# COLLISIONS, ROTATION AND UPDATE
from pydojo import *
screen(1280, 720)
t = Actor('example_asset/characters/terrain.png')
t.right(90)
t.tag('ostacolo')

gobo = Actor('example_asset/characters/gobo.png')
gobo.scale(0.5)
gobo.goto(800, 500)
gobo.rotate('flip')

spawntime = Timer(500)

while True:

    if key(RIGHT):
        gobo.point(90)
        gobo.forward(10)
    if key(LEFT):
        gobo.point(-90)
        gobo.forward(10)

    if keydown(SPACE):
        gobo.jump()


    # if spawntime.get():
    #     spawn(gobo, speed=10, direction=MOUSE)


    # if keydown(N):
    #     execute('example_test1.py')
    # if gobo.collide('ostacolo'):
    #     print('collision')
    #     quit()
    # if keydown(SPACE):
    #     t.roll(30)

    # for i in range(20):
    #     gobo.scale(1.11)
    #     update()
    # for i in range(20):
    #     gobo.scale(0.9)
    #     update()

    update()
######################################################

######################################################
# CLONE

# apple = Actor('example_asset/characters/apple.png')
# apple.layer = 10
# apple.scale(0.5)
# apple.hide()
#
# food = []
#
# for i in range(10):
#     m = clone(apple)
#     m.gorand()
#     m.show()
#     food.append(m)
#
# print food
#
# while True:
#
#     for f in food:
#         f.forward(1)
#
#     update()
######################################################