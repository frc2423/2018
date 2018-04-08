import wpilib
import wpilib.drive
from robotpy_ext.common_drivers import navx
import ctre
from wpilib.timer import Timer


class DriveTrain:

    robot_drive : wpilib.RobotDrive
    gyro : navx.AHRS
    br_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    fl_motor : ctre.wpi_talonsrx.WPI_TalonSRX
    ACC = 0.5
    TURN_ACC = 1.2

    def __init__(self):
        self.min_speed = 0.3
        self.min_turn_rate = 0.2

    def on_enable(self):
        self.speed = 0
        self.previous_time = None
        self.cur_speed = 0
        self.des_speed = 0
        self.cur_turn_rate = 0
        self.des_turn_rate = 0
        self.acc_toggle = True
        print("on_enable")

    def toggle_acc(self):
        self.acc_toggle = not self.acc_toggle

    def execute(self):
        current_time = Timer.getFPGATimestamp()
        dt = 0 if self.previous_time is None else current_time - self.previous_time


        self.cur_speed = self.accelerate(self.cur_speed, self.des_speed, dt, self.min_speed, self.ACC)
        self.cur_turn_rate = self.accelerate(self.cur_turn_rate, self.des_turn_rate, dt, self.min_turn_rate, self.TURN_ACC)
        self.robot_drive.arcadeDrive(self.cur_turn_rate, self.cur_speed)

        self.previous_time = current_time


    def accelerate(self, cur_speed, des_speed, dt, min_speed, ACC):

        if cur_speed * des_speed < 0:
            cur_speed = 0
        if des_speed > 0.3 and cur_speed < min_speed:
            cur_speed = min_speed
        elif des_speed < -0.3 and cur_speed > -min_speed:
            cur_speed = -min_speed

        direction = 1 if des_speed > 0 else -1
        if abs(cur_speed) < abs(des_speed):
            cur_speed = cur_speed + ACC * dt * direction
        if abs(cur_speed) > abs(des_speed):
            cur_speed = des_speed

        return cur_speed




    def turn_pid_off(self):
        self.drive_train_pid.disable()

    def stop(self):
        self.des_turn_rate = 0
        self.des_speed = 0

    def turn_right(self):
        self.des_turn_rate = 0.5
        self.des_speed = 0

    def turn_left(self):
        self.des_turn_rate = -0.5
        self.des_speed = 0

    def set_turn_rate(self, turn_rate):
        self.des_turn_rate = turn_rate

    def set_speed(self, speed):
        self.des_speed = speed

    def getAngle(self):
        return self.gyro.getAngle()

    def resetGyro(self):
        self.gyro.reset()

    def arcade(self, turn_rate, speed):
        self.des_turn_rate = turn_rate
        self.des_speed = speed

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