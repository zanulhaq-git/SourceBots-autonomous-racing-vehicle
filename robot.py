import time
import math
from sbot import Robot
robot = Robot()

motors = robot.motor_boards["SRO-AAV-GRC"].motors

POWERCONST = 0.9 # accounts for difference in motor speed

def getPowers(): return [-1 * motors[0].power, -1 * motors[1].power/POWERCONST]

#powers = [leftPower, rightPower]
def setPowers(powers): 
    motors[0].power = -1 * powers[0] 
    motors[1].power = -1 * powers[1] * POWERCONST

def findMarkerById(markers, id):
    for marker in markers:
        if(marker.id == id): return marker
    return False

def powerForTime(powers, seconds):
    a = time.time() + seconds 
    while time.time() < a:
        setPowers(powers)

def rotateOnSpot(direction, power, seconds):
    setPowers([0,0])
    t_end = time.time() + seconds
    while time.time() < t_end:
        if(direction == "left"):
            setPowers([power*-1,power])
        elif(direction == "right"):
            setPowers([power,power*-1])
    setPowers([0,0])

#could add support for multiple ids
def approachMarker(markerId, stopDistance, spinDirection):
    rotations = 0
    while True:
        markers = robot.camera.see() #should be 6/7
        marker = findMarkerById(markers, markerId)
        time.sleep(0.5)
        if(marker):
            setPowers([0.3,0.3]) #to test
            if(marker.distance < stopDistance): break
            else:
                t_end = time.time() + 0.3 * marker.distance/1000
                while time.time() < t_end:
                    basePower = 0.4 #to test
                    angle = convertAzimuth(math.degrees(marker.azimuth)) #-180 to 180
                    powerChange = 0.7 * (angle/180) #to test
                    if(angle < 0): setPowers([basePower + powerChange, basePower - powerChange])
                    elif(angle > 0): setPowers([basePower - powerChange, basePower + powerChange])
        else: 
            rotateOnSpot(spinDirection, 0.4, 0.1)
            rotations+=1
            if(rotations == 4 and spinDirection=="left"): 
                powerForTime([0.4,0.4], 2)
                rotations = 0
                break
            elif(rotations == 16 and spinDirection=="right"):
                powerForTime([0.4,0.4], 1)
                rotations = 0
                break
            else: pass



#hardcoded - to test
def firstCanTurn():
    #rotateOnSpot("right", 0.6, 0.1)
    powerForTime([0.74,1], 2.05)

def secondCanTurn():
    powerForTime([0.5,0.5], 1) #to test
    powerForTime([0.5,0.8], 2) #to test

def gameRoutine():
    while True:
        firstCanTurn()
        powerForTime([0.4,0.4], 0.75)
        powerForTime([0.55,1], 2)
        powerForTime([0.4,0.4], 0.95)
        setPowers([0,0])
        approachMarker(3, 700, "left")
        approachMarker(4, 700, "right")
        rotateOnSpot("right", 0.6, 0.1)
        powerForTime([0.4,0.4], 1.1)
        setPowers([0,0])
        approachMarker(6, 1000, "right")
        firstCanTurn()

def newGameRoutine():
    while True:
        firstCanTurn()
        powerForTime([0.4,0.4], 0.75)
        powerForTime([0.55,1], 2)
        powerForTime([0.4,0.4], 0.95)
        approachMarker(3, 700, "left")
        approachMarker(4, 700, "right")
        #pray the repetitions save us



newGameRoutine()

def convertAzimuth(azimuth):
    if(azimuth > 180): return (azimuth-360)
    return azimuth

#====================TESTS====================#
def testPower(power, seconds):
    t_end = time.time() + seconds
    while time.time() < t_end:
        setPowers([power,power]) 

def testApproach(stopDistance):
    while True:
        markers = robot.camera.see()
        time.sleep(0.5)
        if(len(markers)):
            marker = markers[0]
            print("test")
            print(marker.distance)
            if(marker.distance < stopDistance): break
            else:
                t_end = time.time() + 0.3 * marker.distance/1000
                while time.time() < t_end:
                    basePower = 0.4 #to test
                    angle = convertAzimuth(math.degrees(marker.azimuth)) #-180 to 180
                    powerChange = 0.7 * (angle/180) #to test
                    if(angle < 0): setPowers([basePower + powerChange, basePower - powerChange])
                    elif(angle > 0): setPowers([basePower - powerChange, basePower + powerChange])
        else: rotateOnSpot("right", 0.4, 0.1)




# def testApproach(stopDistance):
#     while True:
#         markers = robot.camera.see()
#         if(len(markers)):
#             marker = markers[0]
#             print("test")
#             print(marker.distance)
#             if(marker.distance < stopDistance): break
#             else:
#                 t_end = time.time() + 0.4
#                 while time.time() < t_end:
#                     setPowers([0.3, 0.3])
#                 basePower = 0.3 #to test
#                 angle = convertAzimuth(math.degrees(marker.azimuth)) #-180 to 180
#                 powerChange = (angle/180) #to test
#                 if(angle < 0): setPowers([basePower + powerChange, basePower - powerChange])
#                 elif(angle > 0): setPowers([basePower - powerChange, basePower + powerChange])
#         else: rotateOnSpot("right", 0.3, 0.2)