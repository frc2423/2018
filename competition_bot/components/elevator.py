import wpilib
import wpilib.drive
import ctre
from robotpy_ext.common_drivers import navx

class Elevator:

    elevator_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    pid : wpilib.PIDController
    distance_per_tick = 5


    def __init__(self):
        self.speed = 0
        self.setpoint = 0

    def elevator_position(self):
        pass

    def execute(self):
        self.elevator_motor.set(self.speed)