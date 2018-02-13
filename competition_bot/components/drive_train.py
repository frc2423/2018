import wpilib
import wpilib.drive
from robotpy_ext.common_drivers import navx
import ctre

class DriveTrain:

    robot_drive : wpilib.RobotDrive
    gyro : navx.AHRS
    br_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    fl_motor : ctre.wpi_talonsrx.WPI_TalonSRX


    def __init__(self):
        self.turn_rate = 0
        self.speed = 0

    def execute(self):
        self.robot_drive.arcadeDrive(self.turn_rate, self.speed)

    def forward(self):
        self.turn_rate = 0
        self.speed = -0.5

    def backward(self):
        self.turn_rate = 0
        self.speed = 0.5

    def stop(self):
        self.turn_rate = 0
        self.speed = 0

    def turn(self):
        self.turn_rate = 0.5
        self.speed = 0

    def getAngle(self):
        return self.gyro.getAngle()

    def resetGyro(self):
        self.gyro.reset()

    def arcade(self, turn_rate, speed):
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
