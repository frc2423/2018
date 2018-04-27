import wpilib

class Arms:


    def __init__(self):
        self.l_arm = wpilib.Spark(0)
        self.r_arm = wpilib.Spark(1)
        self.l_arm_speed = 0
        self.r_arm_speed = 0

    def intake(self):
        self.l_arm_speed = -.6
        self.r_arm_speed = .6

    def outtake(self):
        self.l_arm_speed = .7
        self.r_arm_speed = -.7

    def stop(self):
        self.l_arm_speed = -.25
        self.r_arm_speed = .25

    def execute(self):
        # run the sparks
        self.l_arm.set(self.l_arm_speed)
        self.r_arm.set(self.r_arm_speed)