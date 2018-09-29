import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.drive_train import DriveTrain
from components.direction_pid import Direction_Pid


class LeftSideSequence(AutonomousStateMachine):
    MODE_NAME = 'LeftSideSequence'
    DEFAULT = False


    driveTrain = DriveTrain
    direction_pid = Direction_Pid


    @state(first = True)
    def stopped_at_position_1(self):
        self.next_state('driving_to_posiion_2')

    @state()
    def driving_to_posiion_2(self):
        # state body
        self.driveTrain.drive_to(0, 4)

        # transition
        if self.driveTrain.at_position(0, 4):
            if self.get_switch_side() is 'left':
                self.next_state('driving_to_position_6')
            else:
                self.next_state("driving_to_position_3")


    @state()
    def driving_to_posiion_3(self):
        pass

    @state()
    def driving_to_posiion_4(self):
        pass

    @state()
    def driving_to_posiion_5(self):
        pass

    def driving_to_position_6(self):
        self.driveTrain.drive_to(2, 4)

        if self.driveTrain().at_position(2, 4):
            self.next_state("drop")


        pass

    @state()
    def drop(self):
        pass



    @timed_state(duration=8, next_state='do_nothing')
    def forward(self):
        '''This happens first'''
        self.direction_pid.set_angle(0)
        self.driveTrain.set_speed(-.5)

    @timed_state(duration=5)
    def do_nothing(self):
        '''This happens second'''
        self.direction_pid.disable()
        self.driveTrain.stop()