import ctre

import wpilib



class Elevator:
    elevator_motor: ctre.wpi_talonsrx.WPI_TalonSRX
    ELEVATOR_HEIGHT = 5
    TICKS_TO_TOP = 4320
    DISTANCE_PER_TICK = ELEVATOR_HEIGHT / TICKS_TO_TOP
    elevator_follower: ctre.wpi_talonsrx.WPI_TalonSRX
    MAX_SPEED = .25
    MIN_SPEED = -.8

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

    def get_encoder(self):
        return -self.elevator_follower.getQuadraturePosition()

    def set_encoder(self, ticks):
        self.elevator_follower.setQuadraturePosition(-ticks, 0)

    def ticks_to_feet(self, ticks):
        return self.DISTANCE_PER_TICK * ticks
