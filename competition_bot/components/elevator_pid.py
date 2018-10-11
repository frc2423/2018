
import wpilib
from components.elevator import Elevator


class Elevator_Pid:

    P = .1
    I = 0
    D = 0
    elevator : Elevator

    def setup(self):
        self.speed = 0

        def pid_output(speed):
            self.speed = speed

        def pid_input():
            return -self.elevator.get_encoder()

        self.elevator_pid = wpilib.PIDController(self.P, self.I, self.D, pid_input, pid_output)
        self.elevator_pid.setOutputRange(-1, 1)
        self.elevator_pid.setInputRange(-self.elevator.TICKS_TO_TOP, 0)

    def disable(self):
        self.elevator_pid.disable()

    def execute(self):
        if self.on_target():
            self.disable()

        if self.isEnabled():
            self.elevator.set_speed(self.speed)

    def isEnabled(self):
        return self.elevator_pid.isEnabled()

    def get_speed(self):
        return self.speed

    def set_height(self, height):
        ticks = -height / self.elevator.DISTANCE_PER_TICK
        self.elevator_pid.setEnabled(True)

        if self.elevator_pid.getSetpoint() != ticks or not self.isEnabled():
            self.elevator_pid.enable()
            self.elevator_pid.setSetpoint(ticks)

    def on_target(self):
        error = self.elevator_pid.getError()
        feet = self.elevator.ticks_to_feet(error)
        return abs(feet) < 3/12

    def get_height(self):
        pos = self.elevator.get_encoder()
        feet = pos * self.DISTANCE_PER_TICK
        return feet
