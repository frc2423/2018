from wpilib.timer import Timer

class Controller:

    def __init__(self):
        self.feedback = {}
        self.target = {}
        self.output = {}
        self._prev_time = None

    def calculate_outputs(self, dt):
        '''
        Override this function. This function is meant to calculate the latest output values
        based on the target and feedback values. This function is not meant to be directly called.
        Call the run function instead to will calculate dt and pass it in calculate_outputs.
        '''
        raise NotImplementedError

    def run(self):
        '''

        :return:
        '''
        current_time = Timer.getFPGATimestamp()
        dt = 0 if self._prev_time is None else current_time - self._prev_time
        self._prev_time = current_time

        self.calculate_outputs(dt)


    def set_output(self, name, value):
        '''
        Call this function to set the current output value.
        :param name:
        :param value:
        :return:
        '''
        self.output[name] = value

    def get_output(self, name):
        '''
        Gets the latest output value.
        :param name:
        :return:
        '''
        return None if name not in self.output else self.output[name]

    def get_feedback(self, name):
        if name not in self.feedback:
            return None

        feedback = self.feedback[name]

        return feedback() if callable(feedback) else feedback

    def get_target(self, name):
        return None if name not in self.target else self.target[name]

    def set_target(self, name, value):
        '''
        :param name:
        :param value:
        :return:
        '''
        self.target[name] = value

    def set_feedback(self, name, value = None, callback = None):
        '''
        Provides feedback from a sensor. You can either call this function and pass in the value
        of the sensor every time it changes, or pass in a callback which provides the most up to date
        value of the sensor. If a callback is provided this function only needs to be called once unless
        the callback needs to change.
        :param name
        :param value: The current value of the sensor.
        :param callback: A function which returns the most up to date value of the sensor.
        '''

        self.feedback[name] = value if value is not None else callback



    def reset_dt(self):
        self._prev_time = None

