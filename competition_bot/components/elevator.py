import wpilib
import wpilib.drive
import ctre
from robotpy_ext.common_drivers import navx

class Elevator:

    elevator_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    elevator_pid : wpilib.PIDController
    distance_per_tick = 5
    elevator_encoder : wpilib.Encoder
    TICKS_TO_TOP = 1000

    def __init__(self):
        self.speed = 0
        self.setpoint = 0

    def setup(self):
        self.elevator_pid.setOutputRange(-1, 1)
        self.elevator_pid.setInputRange(0, self.TICKS_TO_TOP)

    def elevator_position(self, speed ):
        self.speed = speed

    def execute(self):
        self.elevator_motor.set(self.speed)

    def up(self):
        self.elevator_pid.disable()
        self.speed = 0.5

    def down(self):
        self.elevator_pid.disable()
        self.speed = -0.4

    def stop(self):
        self.elevator_pid.enable()
        self.speed = 0
        self.elevator_pid.setSetpoint(self.elevator_encoder.get())

    def get_height(self):
        pos = self.elevator_encoder.get()
        feet = pos / self.distance_per_tick
        return feet

    def set_height(self, height):
        ticks = height * self.distance_per_tick
        if self.elevator_pid.getSetpoint() != ticks or not self.elevator_pid.isEnabled():
            self.elevator_pid.enable()
            self.elevator_pid.setSetpoint(ticks)