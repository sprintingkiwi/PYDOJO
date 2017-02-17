from pydojo import *

# inizializzo
pygame.init()
width = 800
height = 600
SCREEN(width, height)

bianco = [255, 255, 255]

#gameGAMEPAD0_control = False
#try:
    ## creo un oggetto Joystick
    #GAMEPAD0 = pygame.joystick.Joystick(0)
    ## inizializzo il joystick
    #GAMEPAD0.init()
    #gameGAMEPAD0_control = True
#except:
    #print("no GamePad found...")

gobo = Actor('example_library/gobo.png')
gobo.goto(width/2, height/2)

os.system('sudo rfcomm bind /dev/rfcomm0  00:15:83:35:86:A2 1')
uno = Arduino('/dev/rfcomm0')
#uno = Arduino('/dev/ttyACM0')

rightPwm = uno.get_pin('d:5:p')
leftPwm = uno.get_pin('d:10:p')
RF = uno.get_pin('d:7:o')
RB = uno.get_pin('d:6:o')
LF = uno.get_pin('d:9:o')
LB = uno.get_pin('d:8:o')

RF.write(True)
RB.write(False)
LF.write(True)
LB.write(False)

direction = "forward"

def shutdown():
    RF.write(False)
    RB.write(False)
    LF.write(False)
    LB.write(False)
    rightPwm.write(0)
    leftPwm.write(0)

def power_right_motor(value=1):
    if direction == "forward":
            RF.write(True)
            RB.write(False)
    elif direction == "back":
            RF.write(False)
            RB.write(True)
    rightPwm.write(value)
    
def power_left_motor(value=1):
    if direction == "forward":
        LF.write(True)
        LB.write(False)
    elif direction == "back":
        LF.write(False)
        LB.write(True)
    leftPwm.write(value)
    
def shutdown_right_motor():
    rightPwm.write(0)
    RF.write(False)
    RB.write(False)
    
def shutdown_left_motor():
    leftPwm.write(0)
    LF.write(False)
    LB.write(False)

while True:

    # KEYBOARD CONTROL
    if keydown(ESCAPE):
        shutdown()
        quit()

    if keydown(RIGHT):
        power_right_motor()
        
    if keyup(RIGHT):
        shutdown_right_motor()

    if keydown(LEFT):
        power_left_motor()

    if keyup(LEFT):
        shutdown_left_motor()

    if keydown(UP):
        direction = 'forward'
    if keydown(DOWN):
        direction = 'back'


    # GAMEPAD CONTROL
    horizontal = axis('left', 'horizontal')

    if horizontal > 0.2:
        #rightPwm.write(0.9)
        pass
    if horizontal < -0.2:
        #leftPwm.write(0.9)
        pass
        
    if buttondown(0):
        if direction == 'forward':
            direction = 'back'
        elif direction == 'back':
            direction = 'forward'    
    if buttondown(4):
        power_left_motor()
    if buttondown(5):
        power_right_motor()
    if not buttondown(4):
        shutdown_left_motor()
    if not buttondown(5):
        shutdown_right_motor()


    gobo.draw()
    sleep(0.01)
    UPDATE()
