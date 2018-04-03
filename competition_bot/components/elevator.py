import wpilib
import wpilib.drive
import ctre
from robotpy_ext.common_drivers import navx

class Elevator:

    elevator_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    elevator_pid : wpilib.PIDController
    distance_per_tick = 5
    TICKS_TO_TOP = 1000
    elevator_follower : ctre.wpi_talonsrx.WPI_TalonSRX
    def __init__(self):
        self.speed = 0
        self.setpoint = 0

    def setup(self):
        self.elevator_pid.setOutputRange(-1, 1)
        self.elevator_pid.setInputRange(0, self.TICKS_TO_TOP)

    def elevator_position(self, speed):
        self.speed = speed


    def is_max_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return top == 1

    def is_min_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return bottom == 1

    def execute(self):
        if self.is_max_height():
            print('max height')
        elif self.is_min_height():
            print('min height')


        self.elevator_motor.set(self.speed)

    def up(self):
        self.elevator_pid.disable()
        if self.is_max_height():
            self.stop()
        else:
            self.speed = -1

    def down(self):
        self.elevator_pid.disable()
        if self.is_min_height():
            self.stop()
        else:
            self.speed = 0.3

    def stop(self):
        print('stoooped!')
        #self.elevator_pid.enable()
        self.speed = -0.3 if not self.is_min_height() else 0
        #self.elevator_pid.setSetpoint(self.elevator_follower.getQuadraturePosition())

    def get_height(self):
        pos = self.elevator_encoder.get()
        feet = pos / self.distance_per_tick
        return feet

    def set_height(self, height):
        ticks = height * self.distance_per_tick
        if self.elevator_pid.getSetpoint() != ticks or not self.elevator_pid.isEnabled():
            self.elevator_pid.enable()
            self.elevator_pid.setSetpoint(ticks)