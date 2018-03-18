import magicbot
import wpilib
import ctre
from components.drive_train import DriveTrain
from components.arms import Arms
from components.elevator import Elevator
from robotpy_ext.common_drivers import navx
import wpilib.drive
from networktables import NetworkTables


class MyRobot(magicbot.MagicRobot):

    arms = Arms
    driveTrain = DriveTrain
    elevator = Elevator

    def createObjects(self):

        self.init_drive_train()
        self.init_arms()
        self.init_elevator()

        self.button10_prev = False

        self.joystick = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        self.table = NetworkTables.getTable("limelight")

    def disabledInit(self):
        self.table.putNumber("ledMode", 1)

    def autonomousInit(self):
        self.table.putNumber("ledMode", 0)
    def init_drive_train(self):
        #fl, bl, fr, br = (30, 40, 50, 10)  # practice bot
        br, fr, bl, fl = (1, 7, 2, 5)  # on competition robot

        self.br_motor = ctre.wpi_talonsrx.WPI_TalonSRX(br)
        self.bl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(bl)
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fl)
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(fr)
        self.fr_motor.setInverted(True)
        self.br_motor.setInverted(True)

        self.gyro = navx.AHRS.create_spi()

        driveTrain = self.driveTrain

        def set_pid_turn_rate(turn_rate):
            driveTrain.turn_rate = turn_rate
            pass

        self.drive_train_pid = wpilib.PIDController(.1, 0, 0, self.gyro, set_pid_turn_rate)

        self.robot_drive = wpilib.RobotDrive(self.fl_motor, self.bl_motor, self.fr_motor, self.br_motor)

    def init_arms(self):
        self.l_arm = wpilib.Spark(0)
        self.r_arm = wpilib.Spark(1)


    def init_elevator(self):

        self.elevator_motor = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.elevator_follower = ctre.wpi_talonsrx.WPI_TalonSRX(10)
        self.elevator_follower.follow(self.elevator_motor)



        #self.elevator_encoder = wpilib.Encoder(0, 1)

        elevator = self.elevator
        def elevator_position(speed):
            elevator.speed = speed
            pass

        self.elevator_pid = wpilib.PIDController(.1, 0, 0, self.elevator_follower.getQuadraturePosition, elevator_position)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.arm_speed = 0
        self.turn_rate = 0
        self.robot_speed = 0
        self.br_motor.setQuadraturePosition(0, 0)
        self.fl_motor.setQuadraturePosition(0, 0)
        self.table.putNumber("ledMode", 0)

    def teleopPeriodic(self):
        #print("encoder value", self.elevator_follower.getQuadraturePosition())
        # ELEVATOR CODE
        print("gyro: ", self.gyro.getAngle())
        if self.joystick2.getRawButton(2):
            self.elevator.down()
        elif self.joystick2.getRawButton(3):
            self.elevator.up()
        else:
            self.elevator.stop()

        button10_cur = self.joystick2.getRawButton(10)
        acc_toggle_btn_clicked = not self.button10_prev and button10_cur

        if acc_toggle_btn_clicked:
            self.driveTrain.toggle_acc()

        self.button10_prev = button10_cur


        # DRIVE TRAIN CODE
        self.robot_speed = self.joystick.getY()
        self.turn_rate = self.joystick.getX()

        self.driveTrain.arcade(self.turn_rate * .8, self.robot_speed)


        # ARM CODE
        if self.joystick2.getTrigger():
            if self.joystick2.getY() > 0:
                self.arms.intake()
            elif self.joystick2.getY() < 0:
                self.arms.outtake()
        else:
            self.arms.stop()






if __name__ == '__main__':
    wpilib.run(MyRobot)