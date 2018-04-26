#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from subsystems.arms import Arms
from subsystems.drive_train import Drive_Train
from subsystems.elevator import Elevator


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        # subsystems
        self.arms = Arms()
        self.drive_train = Drive_Train()
        self.elevator = Elevator()

        # controllers
        self.

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopPeriodic(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)