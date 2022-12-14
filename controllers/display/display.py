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
        self.receiver.setChannel(DISPLAY_CHANNEL)

    def display_img(self) -> None:
        img = self.load_image()
        h, w, c = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA).tolist()

        ir = self.display.imageNew(img, Display.BGRA, w, h)
        self.display.imagePaste(ir, 0, 0, False)
        self.display.imageDelete(ir)
        msg = f"Displaying sample number: {self.counter}"
        self.emitter.setChannel(DISPLAY_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))


i = 0
display = DisplayRobot("/home/maf4031/Downloads")
while display.robot.step(32) != -1:
    if i == 4:
        display.display_img()
    if display.receiver.getQueueLength() > 0:
        msg = display.receiver.getData().decode("utf-8")
        print(msg)
        display.receiver.nextPacket()
        if display.counter < len(display):
            display.display_img()
        else:
            display.emitter.setChannel(SUPERVISOR_CHANNEL)
            display.emitter.send(bytes("0", "utf-8"))
            break
    i += 1
 