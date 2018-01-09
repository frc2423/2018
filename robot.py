#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import ctre
from networktables import NetworkTables


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.br_motor = ctre.CANTalon(1)
        self.bl_motor = ctre.CANTalon(3)
        self.fl_motor = ctre.CANTalon(2)
        self.fr_motor = ctre.CANTalon(0)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)



        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)


        self.shooter = wpilib.Relay(1)
        self.feeder = wpilib.Relay(2)

        self.gyro = wpilib.ADXRS450_Gyro()

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)
        self.table = NetworkTables.getTable('SmartDashboard')


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0

    def autonomousPeriodic(self):
        pass

    def teleopPeriodic(self):
        self.robot_drive.arcadeDrive(self.r_joy)


        if True or self.table.getBoolean('controls_enable', False):
            turn_rate = self.l_joy.getY()
            speed = self.l_joy.getX()
            self.robot_drive.arcadeDrive(speed, turn_rate)
            if self.l_joy.getTrigger():
                self.shooter.set(wpilib.Relay.Value.kForward)
            else:
                self.shooter.set(wpilib.Relay.Value.kOff)

            if self.l_joy.getRawButton(1):
                self.feeder.set(wpilib.Relay.Value.kForward)
            else:
                self.feeder.set(wpilib.Relay.Value.kOff)
        else:
            pass

if __name__ == "__main__":
    wpilib.run(MyRobot)