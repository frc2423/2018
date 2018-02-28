import magicbot
import wpilib
import ctre
from robotpy_ext.common_drivers import navx
import wpilib.drive


class MyRobot(magicbot.MagicRobot):

    def createObjects(self):

        self.joystick = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        self.init_drive_train()



    def init_drive_train(self):
        fl, bl, fr, br = (30, 40, 50, 10) # practice bot
        # br, fr, bl, fl = (1, 7, 2, 5)  # on competition robot

        self.br_motor = ctre.wpi_talonsrx.WPI_TalonSRX(br)
        self.bl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(bl)
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fl)
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fr)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)
        #self.robot_drive = wpilib.RobotDrive(self.bl_motor, self.br_motor)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):



        # DRIVE TRAIN CODE
        self.robot_speed = self.joystick.getY()
        self.turn_rate = self.joystick.getX()

        if self.joystick.getTrigger():
            #self.fl_motor.set(.5)
            #self.fr_motor.set(.5)
            self.robot_drive.arcadeDrive(self.turn_rate, self.robot_speed)
        else:
            self.robot_drive.arcadeDrive(self.turn_rate * .75, self.robot_speed * .75)
            #self.fl_motor.set(0)
            #self.fr_motor.set(0)







if __name__ == '__main__':
    wpilib.run(MyRobot)