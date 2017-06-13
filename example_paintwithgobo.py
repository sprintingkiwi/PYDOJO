from pydojo import *
# CREATE GAME DISPLAY
screen(800, 600)

# Create an Actor object
gobo = Actor('example_asset/characters/gobo.png')


# MAIN LOOP
while True:

    # Actor movement
    gobo.goto(MOUSE)
    gobo.stamp()
    gobo.right(5)

    # Keyboard keys behaviour
    if keydown(C):
        # Clear the screen
        clear()
    if keydown(L):
        # Color the background
        fill(LAVENDER)
    if keydown(P):
        fill(PINK)
    if key(SPACE):
        fill(colorscale(5))

    # UPDATE SCREEN
    update()
