import magicbot
import ctre
import wpilib
from networktables import NetworkTables
class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.table = NetworkTables.getTable("limelight")

        self.br_motor = ctre.CANTalon(10)
        self.bl_motor = ctre.CANTalon(50)
        self.fl_motor = ctre.CANTalon(30)
        self.fr_motor = ctre.CANTalon(40)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)
        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.turn_rate = 0
        self.speed = 0
        self.saved_turn_rate = 0


    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''

        tx = self.table.getNumber('tx', None)
        ty = self.table.getNumber('ty', None)
        ta = self.table.getNumber('ta', None)
        ts = self.table.getNumber('ts', None)
        tv = self.table.getNumber('tv', None)

        if tv == 0:
            self.speed = 0
            if self.saved_turn_rate != 0:
                self.turn_rate = (self.saved_turn_rate)
            else:
                self.turn_rate = 0
        else:
            self.turn_rate = tx / 27 if tx is not None else 0
            self.speed = -.4
            self.saved_turn_rate = self.turn_rate

        self.robot_drive.arcadeDrive(self.turn_rate, self.speed)

        print('tx, ty: ', tx, ty)
        print("saved_turn_rate: ", self.saved_turn_rate)

        if tv == 1:
            print("target acquired")
        else :
            print("no target")




if __name__ == '__main__':
    wpilib.run(MyRobot)

