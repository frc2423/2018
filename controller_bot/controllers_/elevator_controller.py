
from controllers.controller import Controller
import wpilib

class Angle_Controller(Controller):

    def __init__(self, P=1, I=0, D=0, TOLERANCE=0, ELEVATOR_TOP=1000, DISTANCE_PER_TICK=1):
        self.set_output('turn_rate', 0)
        self.set_target('turn_rate', 0)

        self.DISTANCE_PER_TICK = DISTANCE_PER_TICK

        self.pid = wpilib.PIDController(P, I, D, self._pid_source, self._pid_output)
        self.pid.setAbsoluteTolerance(TOLERANCE)
        self.pid.setInputRange(0, ELEVATOR_TOP)
        self.pid.setOutputRange(-1, 1)

    def set_height(self, height):
        self.set_target('height', height)

        ticks = height / self.elevator.DISTANCE_PER_TICK
        self.pid.setEnabled(True)

        if self.pid.getSetpoint() != ticks:
            self.pid.setSetpoint(ticks)

    def set_encoder_feedback(self, get_encoder_value):
        self.set_feedback('encoder', callback=get_encoder_value)

    def get_speed(self):
        return self.get_output('speed')

    def on_target(self):
        return self.pid.onTarget()

    def _pid_source(self):
        encoder = self.get_feedback('encoder')
        return encoder if encoder is not None else 0

    def _pid_output(self, speed):
        self.set_output('speed', speed)

    def calculate_outputs(self, dt):
        pass