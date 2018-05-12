import wpilib

class Elevator_Pid_Controller:


    P = .1
    I = 0
    D = 0

    def __init__(self, get_encoder, TICKS_TO_TOP = 1000, HEIGHT = 5, tolerance = .25, feedforward = 0):
        self.speed = 0
        self.feedforward = feedforward
        self.TICKS_TO_TOP = TICKS_TO_TOP
        self.DISTANCE_PER_TICK = HEIGHT / TICKS_TO_TOP

        def pid_output(output):
            self.speed = output + self.feedforward

        self.elevator_pid = wpilib.PIDController(self.P, self.I, self.D, get_encoder, pid_output)
        self.elevator_pid.setOutputRange(-1, 1)
        self.elevator_pid.setInputRange(0, self.TICKS_TO_TOP)
        self.elevator_pid.setAbsoluteTolerance(self.distance_to_ticks(tolerance))

    def enable(self):
        self.elevator_pid.enable()

    def disable(self):
        self.elevator_pid.disable()

    def is_enabled(self):
        return self.elevator_pid.isEnabled()

    def get_speed(self):
        return self.speed

    def set_height(self, height):
        ticks = self.distance_to_ticks(height)

        if self.elevator_pid.getSetpoint() != ticks or not self.is_enabled():
            self.enable()
            self.elevator_pid.setSetpoint(ticks)

    def on_target(self):
        return self.elevator_pid.onTarget()

    def get_height(self):
        pos = self.get_encoder()
        feet = pos * self.DISTANCE_PER_TICK
        return feet


    def ticks_to_distance(self, ticks):
        return self.DISTANCE_PER_TICK * ticks

    def distance_to_ticks(self, distance):
        return distance / self.DISTANCE_PER_TICK