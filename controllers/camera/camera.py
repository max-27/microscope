"""display controller."""
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
        msg = f"Camera: {counter+1}"
        self.emitter.set_channel(CAMERA_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))
        

i = 0
prev_slice_counter = -1
camera = CameraRobot()
while camera.robot.step(32) != -1:
    if camera.receiver.getDataSize() > 0:
        msg = camera.receiver.getData().decode()
        if msg.split(":")[0] == "Supervisor":
            slice_counter = int(msg.split(":")[-1])
            if slice_counter > prev_slice_counter and slice_counter < len(Z_POSITIONS):
                print(f"Capture image at z position: {Z_POSITIONS[slice_counter]}")
                camera.capture_image(slice_counter)
                prev_slice_counter = slice_counter
            elif slice_counter == len(Z_POSITIONS):
                prev_slice_counter = 0
    i += 1
 