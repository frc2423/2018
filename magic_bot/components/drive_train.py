import wpilib
from robotpy_ext.common_drivers import navx

class DriveTrain:

    robot_drive = wpilib.RobotDrive
    gyro = navx.AHRS

    def __init__(self):
        self.turn_rate = 0
        self.speed = 0

    def execute(self):
        self.robot_drive.arcadeDrive(self.turn_rate, self.speed)

    def forward(self):
        self.turn_rate = 0
        self.speed = 0.5

    def backward(self):
        self.turn_rate = 0
        self.speed = -0.5

    def stop(self):
        self.turn_rate = 0
        self.speed = 0

    def turn(self):
        self.turn_rate = 0.5
        self.speed = 0

    def getAngle(self):
        return self.gyro.getAngle()

    def arcade_drive(self, turn_rate, speed):
        self.turn_rate = turn_rate
        self.speed = speed