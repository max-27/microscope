import cv2
import glob
import os
import numpy as np


class DataLoader:
    def __init__(self, dir: str, data_type: str = "jpg"):
        self.dir = dir
        self.images = glob.glob(os.path.join(self.dir, f"*.{data_type}"))
        if self.__len__() == 0:
            self.images = glob.glob(os.path.join(self.dir, f"*.{data_type.upper()}"))
        if self.__len__() == 0:
            raise ValueError(f"Provided directory does not contain any images of type {data_type}")
        self.counter = 0
    
    def __len__(self):
        return len(self.images)
    
    def load_image(self):
        # if self.counter < len(self.images):
        if self.counter < 1:  #TODO Remove me!
            img_name = self.images[self.counter]
            self.counter += 1
            return cv2.imread(img_name)
        else:
            raise IndexError("All images have been loaded")

if __name__ == "__main__":
    d = DataLoader("/mnt/data1/max/microscope/images")
    print(d.load_image())