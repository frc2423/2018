import magicbot
import wpilib
import ctre
from components.drive_train import DriveTrain
from robotpy_ext.common_drivers import navx


class MyRobot(magicbot.MagicRobot):

    driveTrain = DriveTrain

    def createObjects(self):
        '''Create motors and stuff here'''
        self.br_motor = ctre.CANTalon(10)
        self.bl_motor = ctre.CANTalon(50)
        self.fl_motor = ctre.CANTalon(30)
        self.fr_motor = ctre.CANTalon(40)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)
        self.joy1 = wpilib.Joystick(1)

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)
        self.gyro = navx.AHRS.create_spi()

        self.shooter = wpilib.Relay(1)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        self.driveTrain.arcade_drive(self.joy1.getX(), self.joy1.getY())
if __name__ == '__main__':
    wpilib.run(MyRobot)