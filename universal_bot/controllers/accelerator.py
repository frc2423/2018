from wpilib.timer import Timer

class Accelerator:


    def __init__(self, acceleration, dead_zone = 0):
        # ft/s^2
        self.acceleration = acceleration
        self.current_value = 0
        self.desired_value = 0
        self.dead_zone = dead_zone
        self.previous_time = None

    def set_desired(self, value):
        self.desired_value = value


    def get(self):
        # calculate how much time has passed since get was called
        current_time = Timer.getFPGATimestamp()
        dt = 0 if self.previous_time is None else current_time - self.previous_time


        desired_direction = 1 if self.desired_value > 0 else -1
        current_direction = 1 if self.current_value > 0 else -1

        # If we want to travel in opposite directions we won't accelerate to that direction, making contols more responsive
        if desired_direction is not current_direction:
            self.current_value = 0

        if abs(self.current_value) < abs(self.dead_zone) < abs(self.desired_value):
            self.current_value = self.dead_zone * desired_direction

        if abs(self.current_value) < abs(self.desired_value):
            self.current_value += self.acceleration * dt * desired_direction
        else:
            self.current_value = self.desired_value


        self.previous_time = current_time

        return self.current_value



