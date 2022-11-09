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
    
    def translate_camera(self, slice_counter: int) -> None:
        print(f"Move camera to new z position: {Z_POSITIONS[slice_counter]}")
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
    if supervisor.receiver.getQueueLength() > 0:
        msg = supervisor.receiver.getData().decode("utf-8")
        supervisor.receiver.nextPacket()
        sample_number = msg.split(":")[-1]
        # translate camera to initial position
        supervisor.translate_camera(0)
    supervisor.receiver.setChannel(CAMERA_CHANNEL)
    if supervisor.receiver.getQueueLength() > 0:
        msg = supervisor.receiver.getData().decode("utf-8")
        supervisor.receiver.nextPacket()
        slice_number = msg.split(":")[-1]
        if slice_number < len(Z_POSITIONS):
            # move camera to next z position
            supervisor.translate_camera(slice_number)
        else:
            print("Finished capturing all slices")
            supervisor.emitter.setChannel(DISPLAY_CHANNEL)
            msg = "Finished capturing all slices of sample: {sample_number}"
            supervisor.emitter.send(bytes(msg, "utf-8"))
    i += 1
