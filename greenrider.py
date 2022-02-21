#!/usr/bin/env python2
from greenrider_lib.robot_control import RobotControl
from greenrider_lib.robot_control import Vector3D
import time

robot = RobotControl("greenrider")
time.sleep(5)

waitingPosition = Vector3D(0,0,5)                 # position to wait while object is moving on belt
pickupPosition = Vector3D(0,0,0)                  # position to move to for picking up object
canBinPosition = Vector3D(-1.31,1.97,0.49)       # position for dropping into the can bin
bottleBinPosition = Vector3D(-1.31,-1.97,0.49)   # position for dropping into the box bin
boxBinPosition = Vector3D(-1.31,0.0,0.49)        # position for dropping into the bottle bin

timePickupObject = 3.0                           # time to move to pickup_position
timeMoveConveyerBelt = 14.85                    # time to wait for conveyer belt
timeMoveToBin = 5.0                             # time to move to a bin

# def fonk yaz
def waitForObject():
    noObject = True
    while noObject:
        image = robot.image_data()
        for i in range(0,image.width):
            for j in range(0,image.height):
                red = image.data[j*image.width*3 + i*3 + 0]
                green = image.data[j*image.width*3 + i*3 + 1]
                blue = image.data[j*image.width*3 + i*3 + 2]
                if red + green + blue > 0:
                    noObject = False
    time.sleep(1.2)



#Your Code Starts Here

while robot.is_ok():
    robot.start_conveyor(True)
    robot.new_object()
    robot.set_position(waitingPosition)
    robot.sleep(3.0)
    waitForObject()
    robot.start_conveyor(False)
    robot.sleep(2.0)
    image = robot.image_data()

    sumRed = 0
    sumGreen = 0
    sumBlue = 0

for i in range(0,image.width):
    for j in range(0,image.height):
        red = image.data[j*image.width*3 + i*3 + 0]
        green = image.data[j*image.width*3 + i*3 + 1]
        blue = image.data[j*image.width*3 + i*3 + 2]
        sumRed = sumRed + red
        sumGreen = sumGreen + green
        sumBlue = sumBlue + blue

colors = [sumRed, sumGreen, sumBlue]
print(colors)

boxType = ""
binPosition = waitingPosition
if max(colors) == sumRed:
    print("This is a Box!")
    boxType = "Box"
    binPosition = boxBinPosition
elif max(colors) == sumGreen:
    print("This is a Bottle!")
    boxType = "Bottle"
    binPosition = bottleBinPosition
else:
    print("This is a Can")
    boxType = "Can"
    binPosition = canBinPosition

robot.grip(True)
robot.set_position(pickupPosition)
robot.sleep(2.0)
robot.set_position(waitingPosition)
robot.sleep(2.0)
robot.set_position(binPosition)
robot.sleep(3.0)
robot.grip(False)
robot.sleep(1)