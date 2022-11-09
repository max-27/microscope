import cv2
import glob
import os
import numpy as np


class DataLoader:
    def __init__(self, dir: str):
        self.dir = dir
        self.images = glob.glob(os.path.join(self.dir, "*.jpg"))
        self.counter = 0
    
    def __len__(self):
        return len(self.images)
    
    def load_image(self):
        if self.counter < len(self.images):
            img_name = self.images[self.counter]
            self.counter += 1
            return cv2.imread(img_name)
        else:
            raise IndexError("All images have been loaded")

if __name__ == "__main__":
    d = DataLoader("/mnt/data1/max/microscope/images")
    print(d.load_image())