#!/usr/bin/env python3

import pathfinder as pf
import math
from robotpy_ext.common_drivers import navx
#from components.drive_train import DriveTrain


gyro = navx.AHRS

if __name__ == '__main__':
    points = [
        pf.Waypoint(-4, -1, math.radians(-45.0)),
        pf.Waypoint(-2, -2, 0),
        pf.Waypoint(0, 0, 0),
    ]

    info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                                   dt=0.05,  # 50ms
                                   max_velocity=1.7,
                                   max_acceleration=2.0,
                                   max_jerk=60.0)

    '''
    # Wheelbase Width = 0.5m
    modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)

    # Do something with the new Trajectories...
    left = modifier.getLeftTrajectory()
    right = modifier.getRightTrajectory()

    wheel_diameter = .1524

    left.configureEncoder(encoder_position, 1000, wheel_diameter)
    left.configurePIDVA(1.0, 0.0, 0.0, 1 / max_velocity, 0)
    right.configureEncoder(encoder_position, 1000, wheel_diameter)
    right.configurePIDVA(1.0, 0.0, 0.0, 1 / max_velocity, 0)

    left_output = left.calculate(encoder_position)
    right_output = right.calculate(encoder_position)

    gyro_heading = gyro.getAngle()
    desired_heading = pf.r2d(left.getHeading()) '''


   #  use pid controller to control turn rate.