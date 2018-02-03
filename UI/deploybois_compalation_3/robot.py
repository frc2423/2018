import ctre
import magicbot
import wpilib

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.motor = ctre.wpi_talonsrx.WPI_TalonSRX(10)

    def teleopInit(self):
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        self.motor.set(.5)
if __name__ == '__main__':
    wpilib.run(MyRobot)