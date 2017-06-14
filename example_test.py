from pydojo import *
screen(1000, 800)

while True:

    update()

######################################################
# COLLISIONS, ROTATION AND UPDATE

# t = Actor('example_asset/characters/terrain.png')
# t.right(90)
#
# gobo = Actor('example_asset/characters/gobo.png')
# gobo.scale(0.5)
# gobo.goto(800, 500)
#
# while True:
#
#     if gobo.collide(t):
#         print('collision')
#         quit()
#
#     if keydown(SPACE):
#         t.roll(30)
#
#     update()
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