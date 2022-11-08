"""display controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Display
import cv2

# create the Robot instance.

robot = Robot()
timestep = int(robot.getBasicTimeStep())

camera = robot.getDevice("camera")
camera.enable(timestep)

distance_sensor = robot.getDevice("distance sensor")
distance_sensor.enable(timestep)

def adjust_focal_distance(focal_distance: float):
    camera.setFocalDistance(focal_distance)

def get_curr_distance():
    return distance_sensor.getValue()/1000

i = 0
while robot.step(32) != -1:
    print(get_curr_distance())
    i += 1
 