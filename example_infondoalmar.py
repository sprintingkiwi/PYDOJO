from pydojo import *

# CREATE GAME DISPLAY
screen(1920, 1080)

background('example_library/sea.png')

# CREATE SHARK ACTOR
shark = Actor('example_library/shark1.png')
shark.scale(0.2)
shark.rotation = 'flip'

# CREATE FISH
fish = Actor('example_library/fish1.png')
fish.scale(0.2)
fish.point(60)
fish.bounce = True
fish.rotation = 'flip'

print(CENTER.x, CENTER.y)
print(screenInfo.resolution)

# MAIN LOOP
while True:

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
    print(fish.direction, fish.heading)
    # update screen and events queue
    update()
