"""display controller."""
from controller import Robot, Receiver
import cv2

robot = Robot()
timestep = int(robot.getBasicTimeStep())

receiver = robot.getDevice("receiver")
receiver.enable(timestep)

camera = robot.getDevice("camera")
camera.enable(timestep)

def adjust_focal_distance(focal_distance: float):
    camera.setFocalDistance(focal_distance)

i = 0
t = 0
while robot.step(32) != -1:
    if receiver.getQueueLength() != 0 and t==0:
        msg = receiver.getData()
        print(msg)
        t =1
    i += 1
 