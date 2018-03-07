import wpilib
import wpilib.drive
from robotpy_ext.common_drivers import navx
import ctre

class DriveTrain:

    robot_drive : wpilib.RobotDrive
    gyro : navx.AHRS
    drive_train_pid : wpilib.PIDController
    br_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    fl_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    ACC = 0.3

    def setup(self):
        self.drive_train_pid.setOutputRange(-1, 1)
        self.drive_train_pid.setInputRange(-360, 360)

    def __init__(self):
        self.turn_rate = 0
        self.speed = 0

    def execute(self):
        #set dt to 0 for first time run
        current_time = self.wpilib.Timer.getFPGATimestamp()
        dt = current_time - self.previous_time
        if self.cur_speed * self.des_speed < 0:
            self.cur_speed = 0
        direction = 1 if self.des_speed > 0 else -1
        if abs(self.cur_speed) < abs(self.des_speed):
            self.cur_speed = self.cur_speed + self.ACC * dt * direction
        if abs(self.cur_speed) > abs(self.des_speed):
            self.cur_speed = self.des_speed


        self.robot_drive.arcadeDrive(self.turn_rate, self.speed)
        self.previous_time = current_time

    def set_pid_turn_rate(self, turn_rate):
        self.turn_rate = turn_rate

    def forward(self):
        self.speed = -.5
        if not self.drive_train_pid.isEnabled():
            self.drive_train_pid.enable()
            self.drive_train_pid.setSetpoint(self.gyro.getAngle())

    def backward(self):
        self.speed = .5
        if not self.drive_train_pid.isEnabled():
            self.drive_train_pid.enable()
            self.drive_train_pid.setSetpoint(self.gyro.getAngle())


    def turn_pid_off(self):
        self.drive_train_pid.disable()

    def stop(self):
        self.turn_pid_off()
        self.turn_rate = 0
        self.speed = 0

    def turn_right(self):
        self.turn_pid_off()
        self.turn_rate = 0.5
        self.speed = 0

    def turn_left(self):
        self.turn_pid_off()
        self.turn_rate = -0.5
        self.speed = 0

    def getAngle(self):
        return self.gyro.getAngle()

    def resetGyro(self):
        self.gyro.reset()

    def arcade(self, turn_rate, speed):
        self.turn_pid_off()
        self.turn_rate = turn_rate
        self.speed = speed

    def get_left_distance(self):
        ticks_per_foot = -630.8
        pos = self.fl_motor.getQuadraturePosition()
        feet = pos / ticks_per_foot
        return feet
        # br: 912.6/ft
    def get_right_distance(self):
        pos = self.br_motor.getQuadraturePosition()
        ticks_per_foot = 912.6
        feet = pos / ticks_per_foot
        return feet

    def set_speed(self, speed):
        self.des_speed = speed
