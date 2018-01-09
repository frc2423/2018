#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import ctre
from networktables import NetworkTables


class MyRobot(wpilib.IterativeRobot):


    def robotInit(self):
        self.sd = NetworkTables.getTable("SmartDashboard")


    def teleopPeriodic(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)