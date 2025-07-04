from controller import Robot, Camera


robot = Robot()
# get the time step of the current world.
TIME_STEP = 8
MAX_SPEED = 6.28



def detect_color(camera):
    """Detects color from the center pixel of the camera image."""
    image = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()
    
    center_x = width // 2
    center_y = height // 2
    r = camera.imageGetRed(image, width, center_x, center_y)
    g = camera.imageGetGreen(image, width, center_x, center_y)
    b = camera.imageGetBlue(image, width, center_x, center_y)

    if r > 190 and g < 45 and b < 45:
        return "Red"
    elif r > 190 and g > 190 and b < 45:
        return "Yellow"
    elif r > 190 and g < 45 and b > 190:
        return "Pink"
    elif r < 45 and g > 190 and b < 45:
        return "Green"
    elif 170 < r < 200 and 120 < g < 140 and 45 < b < 65:
        return "Brown"
    else:
        return None

def control_leds(color, led1, led2):
    """Controls LEDs based on the detected color."""
    if color in ["Red", "Yellow", "Pink", "Green", "Brown"]:
        print(f"Detected color: {color}")
        led1.set(1)
        led2.set(1)
    else:
        led1.set(0)
        led2.set(0)
        

# Run for the calculated turn time
def right_turn() :
    left_motor.setVelocity(1)
    right_motor.setVelocity(-1)
    start_time1 = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if robot.getTime() - start_time1 >= turn_time:
            break
            
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)

# Stop the robot

    
    
def left_turn() :
    left_motor.setVelocity(-1)
    right_motor.setVelocity(1)
    start_time1 = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if robot.getTime() - start_time1 >= turn_time:
            break
            
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)


def forward() :
    left_motor.setVelocity(6.28)
    right_motor.setVelocity(6.28)
    
def backward() :
    left_motor.setVelocity(-6.28)
    right_motor.setVelocity(-6.28)

def brake() :
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)
    
def go_straight() :
    while robot.step(TIME_STEP) != -1:
        forward()
        color = detect_color(camera)
        control_leds(color, led1, led2)
        print(list_ps[3].getValue())
        if list_ps[3].getValue() > 116 :
            brake()
            break

def move_to_next_cell() :
    forward() 
    start_time1 = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if robot.getTime() - start_time1 > 1.983:
            brake()
            break

def align() :
    left_motor.setVelocity(0.3)
    right_motor.setVelocity(-0.3)
    while robot.step(TIME_STEP) != -1:
        coefficient = (list_ps[0].getValue() - list_ps[5].getValue())/list_ps[0].getValue()
        print(list_ps[0].getValue(),list_ps[5].getValue())
        print(abs(coefficient - 0))
        if abs(coefficient) < 0.01 and list_ps[0].getValue() > 250 :
            brake()
            break

 


# def run_robot(robot):
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)

right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)


# Speeds
wheel_speed = 2.0  # m/s
wheel_base = 0.053  # Distance between e-puck wheels in meters
turn_time = 2.225  # Time for 90-degree turn

list_ps = []
for ind in [0, 1, 2, 5, 6, 7]: 
    sensor_name = 'ps' + str(ind)
    list_ps.append(robot.getDevice(sensor_name))
    list_ps[-1].enable(TIME_STEP)

camera = robot.getDevice('camera')
camera.enable(TIME_STEP)

led1 = robot.getDevice('led6')
led2 = robot.getDevice('led2')



# while robot.step(TIMESTEP) != -1:
    # left_speed = MAX_SPEED
    # right_speed = MAX_SPEED

    # for ps in list_ps:
        # if ps.getValue() < 40:
            # left_speed = -MAX_SPEED
                

# while robot.step(TIME_STEP) != -1:
    # brake()
    # print(list_ps[1].getValue(),list_ps[2].getValue())
       

#move_to_next_cell()
# go_straight()
# red_yellow()
# yellow_pink()

# align()
move_to_next_cell()
left_turn()
move_to_next_cell()
move_to_next_cell()
left_turn()
move_to_next_cell()
right_turn()
move_to_next_cell()
# color = detect_color(camera)
# control_leds(color, led1, led2)



        # left_motor.setVelocity(left_speed)
        # right_motor.setVelocity(right_speed)

# if _name_ == "_main_":
    # my_robot = Robot()
    # run_robot(my_robot)