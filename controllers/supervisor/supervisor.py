import sys 
sys.path.append("/mnt/data1/max/microscope")

from controller import Supervisor, Emitter
from scripts.constants import Z_POSITIONS, DISPLAY_CHANNEL, CAMERA_CHANNEL


class SupervisorRobot:
    def __init__(self) -> None:
        self.robot = Supervisor()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.emitter = self.robot.getDevice("emitter")
        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(self.timestep)
        self.camera_node = self.robot.getFromDef("CAMERA")
        self.translation_field = self.camera_node.getField("translation")
        self.counter = 0
    
    def translate_camera(self) -> None:
        print(f"Move camera to new z position: {Z_POSITIONS[image_counter]}")
        new_z_position = Z_POSITIONS[self.counter]
        new_camera_position = [0, 0.2, new_z_position]
        self.translation_field.setSFVec3f(new_camera_position)
        msg = f"Supervisor: {self.counter}"
        self.emitter.set_channel(CAMERA_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))
        self.counter += 1


i = 0
prev_slice_counter = -1
image_counter = 0
slice_counter = 0
supervisor = SupervisorRobot()
while supervisor.robot.step(timestep) != -1:
    # translate camera to first position
    if i == 20:
        supervisor.translate_camera()
        prev_slice_counter = 0
    # waiting for camera before moving to next position
    supervisor.receiver.set_channel(CAMERA_CHANNEL)
    if supervisor.receiver.getDataSize() > 0:
        msg = supervisor.receiver.getData().decode()
        if msg.split(":")[0] == "Camera":
            slice_counter = int(msg.split(":")[-1])
            if slice_counter > prev_slice_counter and slice_counter < len(Z_POSITIONS):
                supervisor.translate_camera()
                prev_slice_counter = slice_counter
            elif slice_counter == len(Z_POSITIONS):
                prev_slice_counter = 0
                image_counter += 1
                msg = f"Supervisor: {image_counter}"
                supervisor.emitter.set_channel(DISPLAY_CHANNEL)
                supervisor.emitter.send(bytes(msg, "utf-8"))
    supervisor.receiver.set_channel(DISPLAY_CHANNEL)
    if supervisor.receiver.getDataSize() > 0:
        msg = supervisor.receiver.getData().decode()
        if int(msg.split(":")[-1]) == image_counter:
            

    i += 1
