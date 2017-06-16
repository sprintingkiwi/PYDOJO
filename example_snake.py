from pydojo import *

width = 1280
height = 720
screen(width, height)

head = Actor('example_asset/characters/square.png')
head.speed = 5
head.scale(0.5)
head.tag('snake')
head.setlayer(2)

tail = []
tailcoords = []
food = []

apple = Actor('example_asset/characters/apple.png')
apple.setlayer(1)
apple.scale(0.5)
apple.hide()

for i in range(10):
    m = clone(apple)
    m.gorand()
    while m.collide('t'):
        m.gorand()
    m.show()
    m.tag('food')
    food.append(m)

while True:

    # Controls
    if key(RIGHT):
        head.right(5)
    if key(LEFT):
        head.left(5)

    # Boundaries
    if head.y < 0:
        head.goto(head.x, height)
    if head.x < 0:
        head.goto(width, head.y)
    if head.y > height:
        head.goto(head.x, 0)
    if head.x > width:
        head.goto(0, head.y)

    # Eating food
    for f in food:
        if f.collide(head):
            for i in range(10):
                t = clone(head)
                t.tag('snake')
                t.layer = 2
                tail.append(t)
            f.hide()
            food.remove(f)

    # Manage Head
    head.forward(head.speed)

    # Manage Tail
    tailcoords.insert(0, [head.x, head.y])
    for pezzo in tail:
        pezzo.goto(tailcoords[tail.index(pezzo)])

    update()
