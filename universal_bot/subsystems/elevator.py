import ctre
import wpilib

class Elevator:
    ELEVATOR_HEIGHT = 5
    TICKS_TO_TOP = 4320
    DISTANCE_PER_TICK = ELEVATOR_HEIGHT / TICKS_TO_TOP

    def __init__(self):
        self.elevator_motor = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.elevator_follower = ctre.wpi_talonsrx.WPI_TalonSRX(10)
        self.elevator_follower.follow(self.elevator_motor)

    def execute(self):
        self.elevator_motor.set(self.speed)

    def set_speed(self, speed):
        self.speed = -speed

    def get_height(self):
        pos = self.get_encoder()
        feet = pos * self.DISTANCE_PER_TICK
        return feet

    def is_max_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return top == 1

    def is_min_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return bottom == 1

    def get_encoder(self):
        return -self.elevator_follower.getQuadraturePosition()

    def set_encoder(self, ticks):
        self.elevator_follower.setQuadraturePosition(-ticks, 0)

    def ticks_to_feet(self, ticks):
        return self.DISTANCE_PER_TICK * ticks
