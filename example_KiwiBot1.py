from pydojo import *

# inizializzo
pygame.init()
width = 800
height = 600
SCREEN(width, height)

gobo = Actor('example_library/gobo.png')
gobo.goto(width/2, height/2)

os.system('sudo rfcomm bind /dev/rfcomm0  00:15:83:35:86:A2 1')
uno = Arduino('/dev/rfcomm0')
#uno = Arduino('COM6')

rightPwm = uno.get_pin('d:5:p')
leftPwm = uno.get_pin('d:10:p')
RF = uno.get_pin('d:7:o')
RB = uno.get_pin('d:6:o')
LF = uno.get_pin('d:9:o')
LB = uno.get_pin('d:8:o')
clacson = uno.get_pin('d:3:p')

RF.write(True)
RB.write(False)
LF.write(True)
LB.write(False)

direction = 'forward'

def complete_shutdown():
    RF.write(False)
    RB.write(False)
    LF.write(False)
    LB.write(False)
    rightPwm.write(0)
    leftPwm.write(0)

def power_right_motor(value=1):
    if direction == 'forward':
            RF.write(True)
            RB.write(False)
    elif direction == 'back':
            RF.write(False)
            RB.write(True)
    rightPwm.write(value)
    
def power_left_motor(value=1):
    if direction == 'forward':
        LF.write(True)
        LB.write(False)
    elif direction == 'back':
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
    
def honk(value=1):
    clacson.write(value)

while True:

    # KEYBOARD CONTROL
    if keydown(ESCAPE) or buttondown(6):
        complete_shutdown()
        terminate()

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
        
    # reverse gear
    if buttondown(0):
        direction = 'back'
    else:
        direction = 'forward'
    
    # low-level motor control    
    if buttondown(4):
        power_left_motor()
    if buttondown(5):
        power_right_motor()
    if not buttondown(4):
        shutdown_left_motor()
    if not buttondown(5):
        shutdown_right_motor()
        
    # high-level motor control
    if horizontal > 0.2:
        #rightPwm.write(0.9)
        pass
    if horizontal < -0.2:
        #leftPwm.write(0.9)
        pass

    #clacson
    if buttondown(2):
        honk(1)
    else:
        honk(0)

    gobo.draw()
    sleep(0.01)
    UPDATE()
