import wpilib
from robotpy_ext.common_drivers import navx
import ctre

class Drive_Train:

    def __init__(self):
        # fl, bl, fr, br = (30, 40, 50, 10)  # practice bot
        br, fr, bl, fl = (1, 7, 2, 5)  # on competition robot

        self.br_motor = ctre.wpi_talonsrx.WPI_TalonSRX(br)
        self.bl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(bl)
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fl)
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fr)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)

        self.gyro = navx.AHRS.create_spi()

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)

        self.speed = 0
        self.turn_rate = 0

    def stop(self):
        self.turn_rate = 0
        self.speed = 0

    def set_turn_rate(self, turn_rate):
        self.turn_rate = turn_rate

    def set_speed(self, speed):
        self.speed = speed

    def get_angle(self):
        return self.gyro.getAngle()

    def reset_gyro(self):
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

    def execute(self):
        self.robot_drive.arcadeDrive(self.turn_rate, self.speed)




