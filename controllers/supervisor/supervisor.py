import sys 
sys.path.append("/mnt/data1/max/microscope")

from controller import Supervisor, Emitter
from scripts.constants import Z_POSITIONS, DISPLAY_CHANNEL, CAMERA_CHANNEL
import time

class SupervisorRobot:
    def __init__(self) -> None:
        self.robot = Supervisor()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.emitter = self.robot.getDevice("emitter")
        self.receiver = self.robot.getDevice("receiver")
        self.receiver1 = self.robot.getDevice("receiver(1)")
        self.receiver.enable(self.timestep)
        self.camera_node = self.robot.getFromDef("CAMERA")
        self.translation_field = self.camera_node.getField("translation")
    
    def translate_camera(self, slice_counter: int) -> None:
        new_z_position = Z_POSITIONS[slice_counter]
        new_camera_position = [0, 0.2, new_z_position]
        self.translation_field.setSFVec3f(new_camera_position)
        msg = f"Moved camera to position: {slice_counter}"
        self.emitter.setChannel(CAMERA_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))


i = 0
supervisor = SupervisorRobot()
while supervisor.robot.step(32) != -1:
    supervisor.receiver.setChannel(DISPLAY_CHANNEL)
    time.sleep(.5)
    if supervisor.receiver.getQueueLength() > 0:
        msg = supervisor.receiver.getData().decode()
        supervisor.receiver.nextPacket()
        print(msg)
        slice_counter = int(msg.split(":")[-1])
        supervisor.translate_camera(slice_counter)
    supervisor.receiver.setChannel(CAMERA_CHANNEL)
    time.sleep(0.5)
    if supervisor.receiver.getQueueLength() > 0:
        msg = supervisor.receiver.getData().decode()
        print(msg)
    i += 1
