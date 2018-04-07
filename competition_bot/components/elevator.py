import wpilib
import wpilib.drive
import ctre
from robotpy_ext.common_drivers import navx

class Elevator:

    elevator_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    elevator_pid : wpilib.PIDController
    ELEVATOR_HEIGHT = 5
    TICKS_TO_TOP = 4320
    DISTANCE_PER_TICK = ELEVATOR_HEIGHT / TICKS_TO_TOP
    elevator_follower : ctre.wpi_talonsrx.WPI_TalonSRX
    MAX_SPEED = .25
    MIN_SPEED = -.8
    def __init__(self):
        self.speed = 0
        self.setpoint = 0

    def setup(self):
        self.elevator_pid.setOutputRange(-1, 1)
        self.elevator_pid.setInputRange(-self.TICKS_TO_TOP, 0)


    def elevator_position(self, speed):
        self.speed = speed


    def is_max_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return top == 1

    def is_min_height(self):
        bottom, top = self.elevator_follower.getLimitSwitchState()
        return bottom == 1

    def execute(self):

        if self.on_target():
            self.elevator_pid.disable()

        if self.is_max_height():
            #print('max height')
            pass
        elif self.is_min_height():
            #print('min height')
            pass

        if self.speed < self.MIN_SPEED:
            self.speed = self.MIN_SPEED

        if self.speed > self.MAX_SPEED:
            self.speed = self.MAX_SPEED


        self.elevator_motor.set(self.speed)

    def up(self):
        self.elevator_pid.disable()

        if self.is_max_height():
            self.stop()
            self.set_encoder(self.TICKS_TO_TOP)
        else:
            self.speed = -.8

    def down(self):
        self.elevator_pid.disable()
        if self.is_min_height():
            self.stop()
            self.set_encoder(0)
        else:
            self.speed = 0.25

    def stop(self):
        #self.elevator_pid.enable()
        self.speed = -0.3 if not self.is_min_height() else 0
        #self.elevator_pid.setSetpoint(self.elevator_follower.getQuadraturePosition())

    def get_height(self):
        pos = self.get_encoder()
        feet = pos * self.DISTANCE_PER_TICK
        return feet

    def set_height(self, height):
        ticks = -height / self.DISTANCE_PER_TICK
        self.elevator_pid.setEnabled(True)


        #print('ticks: ', ticks)

        if self.elevator_pid.getSetpoint() != ticks or not self.elevator_pid.isEnabled():
            self.elevator_pid.enable()
            self.elevator_pid.setSetpoint(ticks)

    def get_encoder(self):
        return -self.elevator_follower.getQuadraturePosition()

    def set_encoder(self, ticks):
        self.elevator_follower.setQuadraturePosition(-ticks, 0)

    def ticks_to_feet(self, ticks):
        return self.DISTANCE_PER_TICK * ticks

    def on_target(self):
        error = self.elevator_pid.getError()
        feet = self.ticks_to_feet(error)
        print('error feet: ', feet)
        return abs(feet) < 3/12

    def is_pid_enabled(self):
        return self.elevator_pid.isEnabled()