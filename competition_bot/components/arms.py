import wpilib
import wpilib.drive
from robotpy_ext.common_drivers import navx

class Arms:

    l_arm : wpilib.Spark
    r_arm : wpilib.Spark

    def __init__(self):
        self.l_arm_speed = 0
        self.r_arm_speed = 0

    def intake(self):
        self.l_arm_speed = .4
        self.r_arm_speed = -.4

    def outtake(self):
        self.l_arm_speed = -.4
        self.r_arm_speed = .4

    def stop(self):
        self.l_arm_speed = -.25
        self.r_arm_speed = .25

    def execute(self):
        # run the sparks
        self.l_arm.set(self.l_arm_speed)
        self.r_arm.set(self.r_arm_speed)



