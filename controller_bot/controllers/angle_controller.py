
import wpilib

class Angle_Controller:

    def __init__(self, P=1, I=0, D=0, tolerance=5):
        self.set_output('turn_rate', 0)
        self.set_target('turn_rate', 0)

        self.pid = wpilib.PIDController(P, I, D, self._pid_source, self._pid_output)
        self.pid.setAbsoluteTolerance(tolerance)
        self.pid.setContinuous(True)
        self.pid.setInputRange(-180, 180)
        self.pid.setOutputRange(-1, 1)

        self.angle_feedback = lambda: 0
        self.turn_rate = 0

    def set_target_angle(self, angle):
        self.pid.setSetpoint(angle)

    def set_angle_feedback(self, angle_feedback):
        self.angle_feedback = angle_feedback

    def get_turn_rate(self):
        return self.turn_rate

    def on_target(self):
        return self.pid.onTarget()

    def _pid_source(self):
        return self.angle_feedback()

    def _pid_output(self, turn_rate):
        self.turn_rate = turn_rate