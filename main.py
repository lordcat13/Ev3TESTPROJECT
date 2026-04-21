#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep
import threading

# Create your objects here.
ev3 = EV3Brick()

# Motors :3
LeftMotor = Motor(Port.C)
RightMotor = Motor(Port.B)


# LightSensors :O
lightSensor_One = ColorSensor(Port.S1)
lightSensor_Two = ColorSensor(Port.S2)
lightSensor_Three = ColorSensor(Port.S3)
lightSensor_Four = ColorSensor(Port.S4)

ColorSensors = {
    "SecondColorSensor": lightSensor_Two,
    "ThirdColorSensor": lightSensor_Three
    
}

RightButton_pressed = False
LeftButton_pressed = False
MiddleButton_Pressed = False

Calibrated = False

ColorSensors_Data = {
    "FirstColorSensor": { "MaxBlack": 0,  "Maxwhite": 0},
    "SecondColorSensor":{ "MaxBlack": 0,  "Maxwhite": 0},
    "ThirdColorSensor": { "MaxBlack": 0,  "Maxwhite": 0},
    "FourthColorSensor":{ "MaxBlack": 0,  "Maxwhite": 0},
    "FifthColorSensor": { "MaxBlack": 0,  "Maxwhite": 0},
}


SpeedMultiplier = 1



# placeholders for functions
def MiddleButton():
    print("MiddleButtonPressed!")
    if not Calibrated:
        Calibrate
    else:
        FollowLineMode
def LeftButton():
    print("LeftButtonPressed!")
    SpeedMultiplier -= 1
def RightButton():
    print("RightButtonPressed!")
    SpeedMultiplier += 1

def CheckButtons():
    global MiddleButton_Pressed, RightButton_pressed, LeftButton_pressed, SpeedMultiplier
    MiddleButtonS = False, RightButtonS = False, LeftButtonS = False
    while True:
        if Button.CENTER in ev3.buttons.pressed() and not MiddleButtonS:
            MiddleButtonS = True
            MiddleButton_Pressed = True
            sleep(0.05)
            MiddleButton_Pressed = False
        elif not Button.CENTER in ev3.buttons.pressed():
            MiddleButtonS = False


        if Button.RIGHT in ev3.buttons.pressed() and not RightButtonS:
            RightButtonS = True
            RightButton_pressed = True
            SpeedMultiplier += 1
            sleep(0.05)
            RightButton_pressed = False
        elif not Button.RIGHT in ev3.buttons.pressed():
            RightButtonS = False


        if Button.LEFT in ev3.buttons.pressed() and not LeftButtonS:
            LeftButtonS = True
            LeftButton_pressed = True
            SpeedMultiplier -= 1
            sleep(0.05)
            LeftButton_pressed = False
        elif not Button.LEFT in ev3.buttons.pressed():
             LeftButtonS = False


        sleep(0.05)



CheckButtonsTheard = threading.Thread(target=CheckButtons)
CheckButtonsTheard.daemon = True
CheckButtonsTheard.start

Prev_error = 0
Integral = 0


def PID_regulator() -> None:

    # turns out we have only 2 sensors
    W2 = GetCalibrated_Values(lightSensor_Two.reflection(), ColorSensors_Data["SecondColorSensor"]["MaxBlack"],ColorSensors_Data["SecondColorSensor"]["MaxWhite"] )
    W3 = GetCalibrated_Values(lightSensor_Three.reflection(), ColorSensors_Data["ThirdColorSensor"]["MaxBlack"], ColorSensors_Data["ThirdColorSensor"]["MaxWhite"])
    
    RightSide = W2
    LeftSide  = W3


    DeltaError =  RightSide - LeftSide
  
    BaseSpeed = 75

    SpeedL = BaseSpeed + DeltaError
    SpeedR = BaseSpeed - DeltaError

    LeftMotor.run(SpeedL * SpeedMultiplier)
    RightMotor.run(-SpeedR * SpeedMultiplier )
    ev3.screen.clear()
    ev3.screen.draw_text(0,0, SpeedMultiplier)
    



def Calibrate() -> None:
    global MiddleButton_Pressed
    offset = 10
    ev3.screen.draw_text(10, 10, "Put Color Sensors on Black")

    while not  MiddleButton_Pressed:
        sleep(0.05)
    ev3.screen.clear()

    for i in ColorSensors:
        ColorSensors_Data[++i]["MaxBlack"] = ColorSensors[i].reflection
        ev3.screen.draw_text(10, offset, ColorSensors[i].reflection)
        offset -= 10
    
    while not  MiddleButton_Pressed:
        sleep(0.05)

    ev3.screen.clear()
    ev3.screen.draw_text(10,10, "Put Color Sensors on White")

    while not  MiddleButton_Pressed:
        sleep(0.05)

    ev3.screen.clear()
    
    for i in ColorSensors:
        ColorSensors_Data[++i]["MaxWhite"] = ColorSensors[i].reflection
        ev3.screen.draw_text(10, offset, ColorSensors[i].reflection)
        offset -= 10
    
    ev3.screen.draw_text(10,10, "All done!")
    sleep(0.5)
    ev3.screen.clear()

    FollowLineMode()

    



def GetCalibrated_Values(raw: int, MinValue: int, MaxValue: int) -> int: 
    
   

    calibrated =  (raw - MinValue) / (MaxValue - MinValue) * 100
    return max(0, min(100, calibrated))   





def FollowLineMode():
    while True:
        PID_regulator

while not MiddleButton_Pressed:
    sleep(0.01)

Calibrate()

# this code is fucking mess never wish someone to try undestand it :sob: