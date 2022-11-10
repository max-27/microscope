import sys 
sys.path.append("/mnt/data1/max/microscope")

from controller import Supervisor, Emitter
from scripts.constants import Z_POSITIONS, DISPLAY_CHANNEL, CAMERA_CHANNEL, SUPERVISOR_CHANNEL


class SupervisorRobot:
    def __init__(self) -> None:
        self.robot = Supervisor()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.emitter = self.robot.getDevice("emitter")
        self.receiver_display = self.robot.getDevice("receiver_display")
        self.receiver_display.enable(self.timestep)
        self.receiver_display.setChannel(DISPLAY_CHANNEL)
        self.receiver_camera = self.robot.getDevice("receiver_camera")
        self.receiver_camera.enable(self.timestep)
        self.receiver_camera.setChannel(CAMERA_CHANNEL)
        self.receiver_super = self.robot.getDevice("receiver_super")
        self.receiver_super.enable(self.timestep)
        self.receiver_super.setChannel(SUPERVISOR_CHANNEL)
        self.camera_node = self.robot.getFromDef("CAMERA")
        self.translation_field = self.camera_node.getField("translation")
    
    def translate_camera(self, slice_counter: int, sample_num: int) -> None:
        new_z_position = Z_POSITIONS[slice_counter]
        new_camera_position = [0, 0.2, new_z_position]
        self.translation_field.setSFVec3f(new_camera_position)
        msg = f"Sample number: {sample_num}: Moved camera to position: {slice_counter}"
        self.emitter.setChannel(CAMERA_CHANNEL)
        self.emitter.send(bytes(msg, "utf-8"))


i = 0
supervisor = SupervisorRobot()
while supervisor.robot.step(32) != -1:
    if supervisor.receiver_display.getQueueLength() > 0:
        msg = supervisor.receiver_display.getData().decode()
        supervisor.receiver_display.nextPacket()
        print(msg)
        sample_counter = int(msg.split(":")[-1])
        supervisor.translate_camera(0, sample_counter)
    if supervisor.receiver_camera.getQueueLength() > 0:
        msg = supervisor.receiver_camera.getData().decode()
        supervisor.receiver_camera.nextPacket()
        print(msg)
        z_position_index = int(msg.split(":")[-1])
        if z_position_index < len(Z_POSITIONS):
            supervisor.translate_camera(z_position_index, sample_counter)
        else:
            supervisor.emitter.setChannel(DISPLAY_CHANNEL)
            msg = f"Load next image: {sample_counter+1}"
            supervisor.emitter.send(bytes(msg, "utf-8"))
    if supervisor.receiver_super.getQueueLength() > 0:
        msg = supervisor.receiver_super.getData().decode()
        supervisor.receiver_super.nextPacket()
        if msg == "0":
            supervisor.emitter.setChannel(CAMERA_CHANNEL)
            supervisor.emitter.send(bytes("0", "utf-8"))
            break
    i += 1
