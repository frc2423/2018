
import wpilib

class Arms:

    def __init__(self):
        self.left_arm = wpilib.Spark(0)
        self.right_arm = wpilib.Spark(1)

        self.left_speed = 0
        self.right_speed = 0

    def set_speed(self, speed):
        self.left_speed = speed
        self.right_speed = speed

    def set_left_right(self, speed):
        self.left_speed = speed

    def set_right_speed(self, speed):
        self.right_speed = speed

    def execute(self):
        self.left_arm.set(self.left_speed)
        self.right_arm.set(self.right_speed)
