#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from subsystems.drive_train import Drive_Train
from subsystems.arms import Arms
from subsystems.elevator import Elevator




class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.drive_train = Drive_Train()
        self.arms = Arms()
        self.elevator = Elevator()

        self.joystick = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)



    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):

        # drive train code
        turn_rate = self.joystick.getX()
        speed = self.joystick.getY()
        self.drive_train.arcade(turn_rate, speed)

        # arms code
        if self.joystick2.getTrigger():
            if self.joystick2.getY() > 0:
                self.arms.intake()
            elif self.joystick2.getY() < 0:
                self.arms.outtake()
        else:
            self.arms.stop()


        # elevator code
        if self.joystick2.getRawButton(2):
            self.elevator.set_speed(-.5)
        elif self.joystick2.getRawButton(3):
            self.elevator.set_speed(.5)
        else:
            self.elevator.set_speed(0)


        # execute subsystems
        self.drive_train.execute()
        self.arms.execute()
        self.elevator.execute()

if __name__ == "__main__":
    wpilib.run(MyRobot)