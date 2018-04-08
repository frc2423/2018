import ctre

class Elevator:

    elevator_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    ELEVATOR_HEIGHT = 5
    TICKS_TO_TOP = 4320
    DISTANCE_PER_TICK = ELEVATOR_HEIGHT / TICKS_TO_TOP
    elevator_follower : ctre.wpi_talonsrx.WPI_TalonSRX
    MAX_SPEED = .25
    MIN_SPEED = -.8

    def __init__(self):
        self.speed = 0

    def is_max_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return top == 1

    def is_min_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return bottom == 1

    def execute(self):

        if self.speed < self.MIN_SPEED:
            self.speed = self.MIN_SPEED

        if self.speed > self.MAX_SPEED:
            self.speed = self.MAX_SPEED

        self.elevator_motor.set(self.speed)

    def set_speed(self, speed):
        self.speed = speed

    def up(self):
        if self.is_max_height():
            self.stop()
            self.set_encoder(self.TICKS_TO_TOP)
        else:
            self.speed = -.8

    def down(self):
        if self.is_min_height():
            self.stop()
            self.set_encoder(0)
        else:
            self.speed = 0.25

    def stop(self):
        self.speed = -0.3 if not self.is_min_height() else 0

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
