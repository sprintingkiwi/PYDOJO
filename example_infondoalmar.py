from pydojo import *

# CREATE GAME DISPLAY
screen(800, 600)

background('example_asset/backgrounds/sea.png')

# CREATE SHARK ACTOR
shark = Actor('example_asset/characters/shark1.png')
shark.rotate('flip')

# CREATE FISH
fish = Actor('example_asset/characters/fish1.png')
fish.point(60)
fish.bounce = True
fish.rotation = 'flip'

# MAIN LOOP
while True:

    # print shark.direction, shark.heading, shark.actual_scale

    # SHARK MOVEMENT
    if key(RIGHT):
        shark.point(90)
        shark.forward(3)
    if key(LEFT):
        shark.point(-90)
        shark.forward(3)
    if key(UP):
        shark.point(0)
        shark.forward(3)
    if key(DOWN):
        shark.point(180)
        shark.forward(3)

    # FISH MOVEMENT
    fish.forward(10)
    # print(fish.direction, fish.heading)
    # update screen and events queue
    update()
