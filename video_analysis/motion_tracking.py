import numpy as np
import cv2
import sys
import math

if __name__ == '__main__':

    videoFile = "snapshots/snap_%d.png"
    cap = cv2.VideoCapture(videoFile)

    if not cap.isOpened():
        sys.exit(1)


    frame_counter = 0
    num_columns = 5
    fps = 100
    grid_width = 1280
    grid_height = 720

    image_grid = np.zeros((grid_height, grid_width, 3), np.uint8)
    image_grid_mask = np.zeros((grid_height, grid_width), np.uint8)

    while True:

        ret, frame = cap.read()
        if not ret: break

        # HSV
        redLower = (161, 100, 150)  # RGB = (166, 41, 76)
        redUpper = (243, 184, 255) # RGB = (222, 60, 76)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, redLower, redUpper)

        # mask = cv2.erode(mask, None, iterations=2)
        # mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            for cnt in cnts:
                rect = cv2.boundingRect(cnt)

                #cv2.putText(frame, "%s, %s" % (rect[2], rect[3]), (rect[0], rect[1] + 5), 1, 1, (0, 255, 255))
                if float(rect[2] / rect[3] + 0.001) > 3.5:
                    cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]) , (0, 255, 255), 2)

        # render frame into a lager image grid
        width = int(grid_width / float(num_columns))
        height = int(grid_height / float(grid_width) * width)
        column = (frame_counter % num_columns) * width
        row = frame_counter / num_columns * height

        image_grid[row:row + height, column:column + width] = cv2.resize(frame, (width, height))
        image_grid_mask[row:row + height, column:column + width] = cv2.resize(mask, (width, height))

        # time to wait between frames, in mSec
        # relevant for videos
        key = cv2.waitKey(1000 / fps)

        # stop on ESC
        if key == 27: break
        if key == 32: cv2.waitKey(0)

        frame_counter += 1


    cv2.imshow("mask", image_grid_mask)
    cv2.imshow("orignal", image_grid)
    cv2.moveWindow("orignal", 650, 50)
    cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()