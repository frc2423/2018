
from controllers.controller import Controller

class Acceleration_Controller(Controller):

    def __init__(self, acc, min_speed = 0, max_speed = 1, default_value = 0):
        self.acc = acc
        self.set_output('speed', default_value)
        self.set_target('speed', default_value)
        self.min_speed = min_speed
        self.max_speed = max_speed

    def calculate_outputs(self, dt):
        self.set_output('speed', self._get_speed(dt))

    def _get_speed(self, dt):
        target_speed = self.get_target('speed')
        cur_speed = self.get_output('speed')
        target_direction = 1 if target_speed > 0 else -1
        cur_direction = 1 if cur_speed > 0 else -1

        # If we reverse directions, reset to 0
        if target_direction != cur_direction:
            return 0
        # If we want to be above our min speed but we're currently below it, set the speed to the min
        # speed instead of accelerating to it.
        elif abs(cur_speed) < abs(target_speed):
            low = self.min_speed * target_direction
            speed = cur_speed + self.acc * dt * target_direction
            high = self.max_speed * target_direction
            return self._bound(low, high, speed)
        else:
            return target_speed

    def _bound(self, low, high, value):
        if abs(value) < abs(low):
            return low
        elif abs(high) > abs(value):
            return high
        return value

    def set(self, value):
        return self.set_target('speed', value)

    def get(self):
        return self.get_output('speed')

