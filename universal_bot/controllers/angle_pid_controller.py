import wpilib

class Angle_Pid_Controller:


    P = .1
    I = 0
    D = 0

    def __init__(self, get_angle, tolerance = 1):
        self.turn = 0
        def pid_output(output):
            self.turn = output

        self.angle_pid = wpilib.PIDController(self.P, self.I, self.D, get_angle, pid_output)
        self.angle_pid.setOutputRange(-1, 1)
        self.angle_pid.setInputRange(-180, 180)
        self.angle_pid.setAbsoluteTolerance(tolerance)
        self.angle_pid.setContinuous(True)

    def enable(self):
        self.angle_pid.enable()

    def disable(self):
        self.angle_pid.disable()

    def is_enabled(self):
        return self.angle_pid.isEnabled()

    def get_turn(self):
        return self.turn

    def set_angle(self, angle):

        if self.angle_pid.getSetpoint() != angle or not self.is_enabled():
            self.enable()
            self.angle_pid.setSetpoint(angle)

    def on_target(self):
        return self.angle_pid.onTarget()