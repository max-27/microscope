from controller import Supervisor, Emitter

robot = Supervisor()
emitter = robot.getDevice("emitter")
timestep = int(robot.getBasicTimeStep())

camera_node = robot.getFromDef("CAMERA")
translation_field = camera_node.getField("translation")
new_camera_position = [0, 0.2, -0.211]
while robot.step(timestep) != -1:
    translation_field.setSFVec3f(new_camera_position)
    emitter.send(b"success")
