"""display controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Display
import cv2

# create the Robot instance.

robot = Robot()
display = robot.getDevice("display")
timestep = int(robot.getBasicTimeStep())

path_to_img = "/home/maf4031/Downloads/test_img.jpg"

image = cv2.imread(path_to_img)
print("Size of image:", image.shape)


def display_img(img):
    h, w, c = img.shape
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA).tolist()

    ir = display.imageNew(img, Display.BGRA, w, h)
    display.imagePaste(ir, 0, 0, False)
    #display.imageDelete(ir)

i = 0
while robot.step(32) != -1:
        
    if i == 20:
        display_img(image)
       
    i += 1
 