import numpy as np
import cv2
import os

class ObjectTracker(object):

    def __init__(self):

        self.gui_mask = cv2.imread(os.path.join(os.path.dirname(__file__), "gui_mask.png"), cv2.IMREAD_GRAYSCALE)

        self.redLower = (161, 100, 150)  # RGB = (166, 41, 76)
        self.redUpper = (243, 184, 255) # RGB = (222, 60, 76)

        self.threshold = 30

    def __process_frame__(self, frame):
        # Apply a mask to hide all GUI elements
        frame = cv2.bitwise_and(frame, frame, mask=self.gui_mask)

        # Convert to HSV and find all red elements within a range
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.redLower, self.redUpper)

        # mask = cv2.erode(mask, None, iterations=2)
        # mask = cv2.dilate(mask, None, iterations=2)

        # cv2.imshow("sdfsdf", mask)
        # cv2.waitKey(1)

        return mask


    def contains_tank(self, frame):
        mask = self.__process_frame__(frame)

        print len(mask[mask == 255]) > self.threshold, len(mask[mask == 255])
        return len(mask[mask == 255]) > self.threshold


    def get_regions(self, frame):

        mask = self.__process_frame__(frame)

        # Find contours in the mask
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        return [cv2.boundingRect(cnt) for cnt in cnts]

