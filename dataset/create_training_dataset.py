import numpy as np
import cv2
import os
import random

def create_training_data(tank_name):

    file_dir = os.path.join("images", "tanks", tank_name)
    if not os.path.exists(file_dir):
        print "Ups, missing directory for {0}".format(file_dir)

    for file_name in os.listdir(file_dir):

        print file_name
        image = cv2.imread(os.path.join(file_dir, file_name), cv2.IMREAD_COLOR)
        background_image = cv2.imread(random.choice(BACKGROUNDS), cv2.IMREAD_COLOR)

        # Resize background to mach tank shape
        image_width = int(image.shape[1])
        image_height = int(image.shape[0])
        background_image = cv2.resize(background_image, (image_width, image_height))

        # add tank image to the background
        x_offset = random.randint(-50, 50)
        y_offset = random.randint(-100, 10)
        transformation = np.float32([[1,0, x_offset],[0,1, y_offset]])
        image = cv2.warpAffine(image, transformation, (image_width, image_height), borderValue=[255, 255, 255])
        mask = image > 200
        image[mask] = background_image[mask]

        # And save it
        save_dir = os.path.join("images", "training_data", tank_name)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        cv2.imwrite(os.path.join(save_dir, file_name), image)

if __name__ == '__main__':
    # Combine the previously downloaded tank images with a background and crop
    # them fit the Inception network

    BACKGROUNDS = [os.path.join("backgrounds", image) for image in os.listdir("backgrounds") if image.endswith("png")]
    TANK_NAMES = [line.strip('\n') for line in open("tanks_blitz.txt", "r")]

    for tank_name in TANK_NAMES:
        create_training_data(tank_name)