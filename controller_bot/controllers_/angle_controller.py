
from controllers.controller import Controller
import wpilib

class Angle_Controller(Controller):

    def __init__(self, P=1, I=0, D=0, tolerance=5):
        self.set_output('turn_rate', 0)
        self.set_target('turn_rate', 0)

        self.pid = wpilib.PIDController(P, I, D, self._pid_source, self._pid_output)
        self.pid.setAbsoluteTolerance(tolerance)
        self.pid.setContinuous(True)
        self.pid.setInputRange(-180, 180)
        self.pid.setOutputRange(-1, 1)

    def set_target_angle(self, angle):
        self.pid.setSetpoint(angle)
        self.set_target('angle', angle)

    def set_angle_feedback(self, get_angle):
        self.set_feedback('angle', callback=get_angle)

    def get_turn_rate(self):
        return self.get_output('turn_rate')

    def on_target(self):
        return self.pid.onTarget()

    def calculate_outputs(self, dt):
        pass

    def _pid_source(self):
        angle = self.get_feedback('angle')
        return angle if angle is not None else 0

    def _pid_output(self, turn_rate):
        self.set_output('turn_rate', turn_rate)