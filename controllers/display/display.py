"""display controller."""
import sys 
sys.path.append("/mnt/data1/max/microscope")

import cv2
from controller import Robot, Display, Emitter, Receiver

from scripts.dataloader import DataLoader
from scripts.constants import SUPERVISOR_CHANNEL, DISPLAY_CHANNEL


class DisplayRobot(DataLoader):
    def __init__(self, dir: str) -> None:
        super().__init__(dir=dir)
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.display = self.robot.getDevice("display")
        self.emitter = self.robot.getDevice("emitter")
        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(self.timestep)

    def display_img(self) -> None:
        img = self.load_image()
        h, w, c = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA).tolist()

        ir = self.display.imageNew(img, Display.BGRA, w, h)
        self.display.imagePaste(ir, 0, 0, False)
        self.display.imageDelete(ir)
        msg = f"Display: {self.counter}"
        self.emitter.set_channel(DISPLAY_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))


i = 0
pre_image_counter = 0
display = DisplayRobot("/home/maf4031/Downloads")
while display.robot.step(32) != -1:
    if i == 4:
        display.display_img()
    # wait for supervisor to display next image
    display.receiver.set_channel(DISPLAY_CHANNEL)
    if display.receiver.getDataSize() > 0:
        msg = display.receiver.getData().decode()
        image_counter = int(msg.split(":")[-1])
        if image_counter > pre_image_counter:
            display.display_img()
            pre_image_counter = image_counter
            image_counter += 1
    i += 1
 