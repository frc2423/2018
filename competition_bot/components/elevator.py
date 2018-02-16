import wpilib
import wpilib.drive
import ctre
from robotpy_ext.common_drivers import navx

class Elevator:

    elevator_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    pid : wpilib.PIDController
    distance_per_tick = 5
    elevator_encoder : wpilib.Encoder

    def __init__(self):
        self.speed = 0
        self.setpoint = 0

    def elevator_position(self, speed ):
        self.speed = speed
    def execute(self):
        self.elevator_motor.set(self.speed)

    def up(self):
        self.pid.disable()
        self.speed = 0.5

    def down(self):
        self.pid.disable()
        self.speed = -0.4

    def stop(self):
        self.pid.enable()
        self.speed = 0
        self.pid.setSetpoint(self.elevator_encoder.get())

    def get_height(self):
        pos = self.elevator_encoder.get()
        feet = pos / self.distance_per_tick
        return feet

    def set_height(self, height):
        ticks = height * self.distance_per_tick
        if self.pid.getSetpoint() != ticks or not self.pid.isEnabled():
            self.pid.enable()
            self.pid.setSetpoint(ticks)