from pydojo import *
screen(800, 600)

apple = Actor('example_asset/characters/apple.png')
apple.layer = 10
apple.scale(0.5)
apple.hide()

food = []

for i in range(10):
    m = clone(apple)
    m.gorand()
    m.show()
    food.append(m)

print food

while True:

    for f in food:
        f.hide()

    update()