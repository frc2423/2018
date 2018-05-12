#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from subsystems.drive_train import Drive_Train
from subsystems.arms import Arms
from subsystems.elevator import Elevator

from controllers.accelerator import Accelerator
from controllers.elevator_pid_controller import Elevator_Pid_Controller

from controllers.angle_pid_controller import Angle_Pid_Controller



class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.drive_train = Drive_Train()
        self.arms = Arms()
        self.elevator = Elevator()

        self.joystick = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)


        self.speed_accelerator = Accelerator(1)
        self.turn_rate_accelerator = Accelerator(1)

        self.elevator_pid = Elevator_Pid_Controller(self.elevator.get_encoder, self.elevator.TICKS_TO_TOP, self.elevator.ELEVATOR_HEIGHT)

        self.angle_pid = Angle_Pid_Controller(self.drive_train.get_angle)



    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):

        # drive train code
        turn_rate = 0
        speed = 0

        if self.joystick.getRawButton(10):
            self.angle_pid.set_angle(0)
            turn_rate = self.angle_pid.get_turn()
        elif self.joystick.getRawButton(11):
            self.angle_pid.set_angle(180)
            turn_rate = self.angle_pid.get_turn()
        else:
            self.speed_accelerator.set_desired(self.joystick.getY())
            self.turn_rate_accelerator.set_desired(self.joystick.getX())
            speed = self.speed_accelerator.get()
            turn_rate = self.turn_rate_accelerator.get()

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
            self.elevator_pid.disable()
            self.elevator_speed = -.5
        elif self.joystick2.getRawButton(3):
            self.elevator_pid.disable()
            self.elevator_speed = 0.5
        elif not self.elevator_pid.is_enabled():
            self.elevator_speed = 0
        elif self.elevator_pid.is_enabled():
            self.elevator_speed = self.elevator_pid.get_speed()

        if self.elevator_pid.on_target():
            self.elevator_pid.disable()

        if self.joystick2.getRawButton(11) or self.joystick2.getRawButton(6):
            self.elevator_pid.set_height(1.7)
        elif self.joystick2.getRawButton(10) or self.joystick2.getRawButton(7):
            self.elevator_pid.set_height(-.5)


        if self.elevator.is_min_height():
            self.elevator.reset_encoder_min()
        elif self.elevator.is_max_height():
            self.elevator.reset_encoder_max()

        elevator_min = -.5
        elevator_max = .5
        elevator_feedforward = 0 if self.elevator.is_min_height() else .3

        if self.elevator.is_max_height():
            elevator_max = 0
        if self.elevator.is_min_height():
            elevator_min = 0

        self.elevator.set_speed(self.clamp(self.elevator_speed, elevator_min, elevator_max) + elevator_feedforward)

        # execute subsystems
        self.drive_train.execute()
        self.arms.execute()
        self.elevator.execute()

    def clamp(self, value, min, max):
        if value < min:
            return min
        elif value > max:
            return max
        else:
            return value


if __name__ == "__main__":
    wpilib.run(MyRobot)