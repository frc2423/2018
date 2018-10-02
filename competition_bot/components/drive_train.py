import wpilib
import wpilib.drive
from robotpy_ext.common_drivers import navx
import ctre
from wpilib.timer import Timer
import math


class DriveTrain:
    # These measurements are in inches
    WHEEL_RADIUS = 3
    DRIVE_BASE = 28

    # In degrees
    THRESHOLD_ANGLE = 5

    # In inches
    THRESHOLD_DISTANCE = 12

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

    def drive_to(self, desired_x, desired_y):

        # change from feet to inches
        desired_x *= 12
        desired_y *= 12

        desired_angle = math.atan2(desired_x - self.x_pos, desired_y - self.y_pos) * 180 / math.pi
        distance = math.sqrt((desired_x - self.x_pos) ** 2 + (desired_y - self.y_pos) ** 2)

        angle_distance = desired_angle - self.get_angle_from_encoders()
        if angle_distance > 180:
            angle_distance -= 360
        elif angle_distance < -180:
            angle_distance += 360

        if angle_distance > DriveTrain.THRESHOLD_ANGLE:
            self.robot_drive.arcadeDrive(.5, 0)
        elif angle_distance < -DriveTrain.THRESHOLD_ANGLE:
            self.robot_drive.arcadeDrive(-.5, 0)
        elif distance > DriveTrain.THRESHOLD_DISTANCE:
            self.robot_drive.arcadeDrive(0, -.5)
        else:
            self.robot_drive.arcadeDrive(0, 0)

    def calculate_odometry(self):

        # get how much time has passed
        dt = 0.02

        left_angular_pos = self.get_left_angular_pos()
        right_angular_pos = self.get_right_angular_pos()

        # calculate angular velocities of the wheels
        left_angular_vel = (left_angular_pos - self.prev_left_angular_pos) / dt
        right_angular_vel = (right_angular_pos - self.prev_right_angular_pos) / dt

        # calculate the velocity of the robot
        vel = (left_angular_vel + right_angular_vel) * DriveTrain.WHEEL_RADIUS / 2

        # calculate angular velocity and use it to calculate the new heading of the robot
        angular_vel = (left_angular_vel - right_angular_vel) * DriveTrain.WHEEL_RADIUS / DriveTrain.DRIVE_BASE
        self.angle += angular_vel * dt

        # Update the robot's position
        self.x_pos += vel * math.sin(self.angle) * dt
        self.y_pos += vel * math.cos(self.angle) * dt

        # save these values so we can take the difference between them. We want to measure
        # the difference in order to calculate the angular velocity.
        self.prev_left_angular_pos = left_angular_pos
        self.prev_right_angular_pos = right_angular_pos

    def reset_odometry(self):
        self.fl_motor.setQuadraturePosition(0, 0)
        self.br_motor.setQuadraturePosition(0, 0)
        self.x_pos = 0
        self.y_pos = 0
        self.angle = 0
        self.prev_left_angular_pos = self.get_left_angular_pos()
        self.prev_right_angular_pos = self.get_right_angular_pos()

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

    def get_angle_from_encoders(self):
        '''Returns an angle between -180 and 180'''
        angle_degrees = (self.angle % (math.pi * 2)) * (180 / math.pi)
        if angle_degrees < -180:
            return angle_degrees + 360
        elif angle_degrees > 180:
            return angle_degrees - 360
        else:
            return angle_degrees

    def get_position(self):
        return self.x_pos / 12, self.y_pos / 12

    def get_left_angular_pos(self):
      encoder_value = self.fl_motor.getQuadraturePosition()
      ticks_per_turn = -1000
      return 2 * math.pi * encoder_value / ticks_per_turn


    def get_right_angular_pos(self):
        encoder_value = self.br_motor.getQuadraturePosition()
        ticks_per_turn = 1440
        return 2 * math.pi * encoder_value / ticks_per_turn