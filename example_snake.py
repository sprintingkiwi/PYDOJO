from pydojo import *
screen(1100, 1100)

head = Actor('example_asset/characters/square.png')
head.speed = 5
head.size = 30
head.pensize = 10
head.scale(0.5)

tail = []
tailcoords = []
food = []

apple = Actor('example_asset/characters/apple.png')
apple.layer = -1
apple.scale(0.5)
apple.hide()

for i in range(10):
    m = clone(apple)
    m.gorand()
    m.show()
    m.tag = 'food'
    food.append(m)

while True:

    # Controls
    if key(RIGHT):
        head.right(5)
    if key(LEFT):
        head.left(5)

    # Boundaries
    if head.y < 0:
        head.goto(head.x, 1100)
    if head.x < 0:
        head.goto(1100, head.y)
    if head.y > 1100:
        head.goto(head.x, 0)
    if head.x > 1100:
        head.goto(0, head.y)

    # Eating food
    for f in food:
        if f.collide(head):
            for i in range(10):
                tail.append(clone(head))
            f.hide()
            food.remove(f)

    # Manage Head
    head.forward(head.speed)

    # Manage Tail
    tailcoords.insert(0, [head.x, head.y])
    for pezzo in tail:
        pezzo.goto(tailcoords[tail.index(pezzo)])

    update()
