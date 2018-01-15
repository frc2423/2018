import magicbot
import wpilib

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        pass

    def teleopInit(self):
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''

if __name__ == '__main__':
    wpilib.run(MyRobot)