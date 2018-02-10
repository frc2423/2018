import wpilib

class Shooter:

    shooter = wpilib.relay(1)

    def __init__(self):
        self.direction = self.shooter.Value.kOff;

    def execute(self):
        self.shooter.set(self.direction)

    def forward(self):
        self.direction = self.shooter.Value.kForward

    def reverse(self):
        self.direction = self.shooter.Value.kReverse

    def stop(self):
        self.direction = self.shooter.Value.kOff