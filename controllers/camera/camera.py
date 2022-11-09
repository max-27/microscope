"""display controller."""
import sys 
sys.path.append("/mnt/data1/max/microscope")

from controller import Robot, Receiver, Emitter
import PIL.Image
import struct
import cv2
import io 
import os

from scripts.get_root import ROOT_PATH
from scripts.constants import Z_POSITIONS, CAMERA_CHANNEL


class CameraRobot:
    def __init__(self) -> None:
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.camera = self.robot.getDevice("camera")
        self.camera.enable(self.timestep)
        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(self.timestep)
        self.emitter = self.robot.getDevice("emitter")

    def adjust_focal_distance(self, focal_distance: float) -> None:
        self.camera.setFocalDistance(focal_distance)
    
    def capture_image(self, counter: int) -> None:
        file_name = os.path.join(ROOT_PATH, "images", f"sample{counter}_{Z_POSITIONS[counter]}.jpg")
        self.camera.saveImage(filename=file_name, quality=100)
        msg = f"Next position slice position: {counter+1}"
        self.emitter.setChannel(CAMERA_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))
        

i = 0
camera = CameraRobot()
while camera.robot.step(32) != -1:
    camera.receiver.setChannel(CAMERA_CHANNEL)
    if camera.receiver.getQueueLength() > 0:
        msg = camera.receiver.getData().decode("utf-8")
        print(msg)
        camera.receiver.nextPacket()
        slice_number = int(msg.split(":")[-1])
        camera.capture_image(slice_number)
    i += 1
 