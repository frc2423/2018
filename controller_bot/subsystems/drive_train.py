from robotpy_ext.common_drivers import navx
import ctre
import wpilib

class Drive_Train:


    def __init__(self):
        self.gyro = navx.AHRS.create_spi()

        br, fr, bl, fl = (1, 7, 2, 5)

        self.br_motor = ctre.wpi_talonsrx.WPI_TalonSRX(br)
        self.bl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(bl)
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fl)
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fr)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)


        self.speed = 0
        self.turn_rate = 0

    def get_angle(self):
        return self.gyro.getAngle()

    def set_speed(self, speed):
        self.speed = speed

    def set_turn_rate(self, turn_rate):
        self.turn_rate = turn_rate

    def set(self, speed, turn_rate):
        self.speed = speed
        self.turn_rate = turn_rate

    def execute(self):
        self.robot_drive.arcadeDrive(self.turn_rate, self.speed)

