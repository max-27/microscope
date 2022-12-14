"""display controller."""
import sys 
sys.path.append("/mnt/data1/max/microscope")

from controller import Robot, Receiver, Emitter
import PIL.Image
from pathlib import Path
import struct
import cv2
import io 
import os

from scripts.get_root import ROOT_PATH, DATA_PATH
from scripts.constants import Z_POSITIONS, CAMERA_CHANNEL, DISPLAY_CHANNEL


class CameraRobot:
    def __init__(self) -> None:
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.camera = self.robot.getDevice("camera")
        self.camera.enable(self.timestep)
        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(self.timestep)
        self.receiver.setChannel(CAMERA_CHANNEL)
        self.emitter = self.robot.getDevice("emitter")
        self.emitter.setChannel(CAMERA_CHANNEL)
        self.dir = DATA_PATH
        Path(self.dir).mkdir(parents=True, exist_ok=True)
        self.num_dir = self.count_dir()

    def adjust_focal_distance(self, focal_distance: float) -> None:
        print("Set focal distance to:", focal_distance)
        self.camera.setFocalDistance(0.05)
    
    def capture_image(self, slice_counter: int, sample_num: int) -> None:
        folder_path = os.path.join(self.dir, f"run_{self.num_dir}", f"sample{sample_num}")
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        file_name = os.path.join(folder_path, f"{Z_POSITIONS[slice_counter]}.jpg")
        self.camera.saveImage(filename=file_name, quality=100)
        msg = f"Next position index: {slice_counter+1}"
        self.emitter.send(bytes(msg, "utf-8"))
    
    def count_dir(self) -> int:
        """Count subdirectories"""
        return len([obj for obj in os.listdir(self.dir) if not os.path.isfile(obj) and obj[0] != "."])   
        

i = 0
camera = CameraRobot()
while camera.robot.step(32) != -1:
    if i == 4:
        camera.adjust_focal_distance(abs(Z_POSITIONS[0]))
    if camera.receiver.getQueueLength() > 0:
        msg = camera.receiver.getData().decode("utf-8")
        camera.receiver.nextPacket()
        if msg == "0":
            break
        else:
            slice_number = int(msg.split(":")[-1])
            sample_num = int(msg.split(":")[1])
            camera.capture_image(slice_number, sample_num)
    i += 1
 