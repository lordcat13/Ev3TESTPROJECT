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

RightButton_pressed = False
LeftButton_pressed = False
MiddleButton_Pressed = False

SpeedMultiplier = 1

# placeholders for functions
def MiddleButton():
    print("MiddleButtonPressed!")
    FollowLineMode()
def LeftButton():
    print("LeftButtonPressed!")
    SpeedMultiplier -= 1
def RightButton():
    print("RightButtonPressed!")
    SpeedMultiplier += 1

def CheckButtons():
    while True:
        sleep(0.2)
        if Button.CENTER in ev3.buttons.pressed() and not MiddleButton_Pressed:
            MiddleButton()
            MiddleButton_Pressed = True
        else:
            MiddleButton_Pressed = False
        if Button.LEFT in ev3.buttons.pressed() and not LeftButton_pressed:
            LeftButton()
            LeftButton_pressed = True
        else:
            LeftButton_pressed = False
        if Button.CENTER in ev3.buttons.pressed() and not RightButton_pressed:
            RightButton()
            RightButton_pressed = True
        else:
            RightButton_pressed = False

threading.Thread(target=CheckButtons).start

def CheckReflection():
  #  print(lightSensor_One.reflection())
   # print(lightSensor_Two.reflection())
   # print(lightSensor_Three.reflection())
   # print(lightSensor_Four.reflection())
   print("yes")

# PID shit (there no acctual ID thought )

def PID_regulator():

    # turns out we have only 2 sensors
    W2 = lightSensor_Two.reflection()
    W3 = lightSensor_Three.reflection()
    
    RightSide = W2
    LeftSide  = W3

    DeltaError =  RightSide - LeftSide

    BaseSpeed = 75

    SpeedL = BaseSpeed + DeltaError
    SpeedR = BaseSpeed - DeltaError

    LeftMotor.run(SpeedL * SpeedMultiplier)
    RightMotor.run(SpeedR * SpeedMultiplier )
    ev3.screen.clear
    ev3.screen.draw_text(0,0, SpeedMultiplier, text_color="Black")
    

def FollowLineMode():
    while True:
        PID_regulator