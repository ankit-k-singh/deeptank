import numpy as np
import cv2
import sys

if __name__ == '__main__':

    videoFile = "/Users/therold/Downloads/Himmelsdorf_480_cut.mp4"
    cap = cv2.VideoCapture(videoFile)

    if not cap.isOpened():
        sys.exit(1)

    while True:

        ret, frame = cap.read()
        if not ret: break


        # HSV
        redLower = (161, 70, 180)  # RGB = (166, 41, 76)
        redUpper = (243, 184, 255) # RGB = (222, 60, 76)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, redLower, redUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            for cnt in cnts:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            #c = max(cnt, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                M = cv2.moments(cnt)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                #if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)


        cv2.imshow("mask", mask)
        cv2.imshow("orignal", frame)
        cv2.moveWindow("orignal", 650, 50)
        prvs = next

        fps = 40
        key = cv2.waitKey(1000 / fps) # time to wait between frames, in mSec

        # stop on ESC
        if key == 27: break

    cap.release()
    cv2.destroyAllWindows()