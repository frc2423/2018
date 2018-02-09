import magicbot
import wpilib
import ctre
from components.drive_train import DriveTrain
from robotpy_ext.common_drivers import navx
import wpilib.drive


class MyRobot(magicbot.MagicRobot):

    driveTrain = DriveTrain

    def createObjects(self):
        #fl, bl, fr, br = (30, 50, 40, 10) # practice bot
        br, fr, bl, fl = (1, 7, 2, 5) #on competition robot

        self.br_motor = ctre.wpi_talonsrx.WPI_TalonSRX(br)
        self.bl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(bl)
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fl)
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fr)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)

        self.l_arm = wpilib.Spark(0)
        self.r_arm = wpilib.Spark(1)

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)

        self.gyro = navx.AHRS.create_spi()

        self.shooter = wpilib.Relay(1)
        self.joystick = wpilib.Joystick(0)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.arm_speed = .30

    def teleopPeriodic(self):

        self.driveTrain.arcade(self.joystick.getX(), self.joystick.getY())

        if self.joystick.getRawButtonPressed(5):
            self.arm_speed += .02
        elif self.joystick.getRawButtonPressed(4):
            self.arm_speed -= .02

        print(self.arm_speed)

        if self.joystick.getRawButton(3):
            self.l_arm.set(self.arm_speed)
            self.r_arm.set(-self.arm_speed)
        elif self.joystick.getRawButton(2):
            self.l_arm.set(-self.arm_speed)
            self.r_arm.set(self.arm_speed)
        else:
            self.l_arm.set(0)
            self.r_arm.set(0)




if __name__ == '__main__':
    wpilib.run(MyRobot)