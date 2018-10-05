
import wpilib
from components.drive_train import DriveTrain
from robotpy_ext.common_drivers import navx


class Direction_Pid:

    P = .1
    I = 0
    D = 0
    driveTrain : DriveTrain
    #gyro: navx.AHRS

    def setup(self):
        self.turn_rate = 0

        def pid_output(turn_rate):
            self.turn_rate = turn_rate

        def pid_input():
            return 0
            #return self.gyro.getAngle()

        self.direction_pid = wpilib.PIDController(self.P, self.I, self.D, pid_input, pid_output)
        self.direction_pid.setOutputRange(-1, 1)
        self.direction_pid.setInputRange(-180, 180)
        self.direction_pid.setContinuous(True)

    def disable(self):
        self.direction_pid.disable()

    def execute(self):
        if self.isEnabled():
            self.driveTrain.set_turn_rate(self.turn_rate)

    def isEnabled(self):
        return self.direction_pid.isEnabled()

    def get_turn_rate(self):
        return self.turn_rate

    def set_angle(self, angle):

        self.direction_pid.setEnabled(True)

        if self.direction_pid.getSetpoint() != angle or not self.isEnabled():
            self.direction_pid.enable()
            self.direction_pid.setSetpoint(angle)

    def on_target(self):
        error_degrees = self.direction_pid.getError()
        return abs(error_degrees) < 1

    def get_angle(self):
        angle = 0
        #angle = self.gyro.getAngle()
        return angle
