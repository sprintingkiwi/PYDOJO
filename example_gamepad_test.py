from pydojo import *

SCREEN(800, 600)

# creo un oggetto Joystick
pad = pygame.joystick.Joystick(0)
# inizializzo il joystick
pad.init()

while True:
    
    for event in pygame.event.get():
        print(event)
