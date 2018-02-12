import wpilib
import wpilib.drive
from robotpy_ext.common_drivers import navx

class Elevator:

    elevator : wpilib.CANTalon
    pid : wpilib.PIDController
    distance_per_tick = 5


    def __init__(self):
        self.speed = 0
        self.setpoint = 0

    def elevator_position(self):


    def execute(self):