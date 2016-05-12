import numpy as np
import cv2
import os
import random
import argparse

def combine_tanks_backgrounds(tank_name, args):

    OUTPUT_SHAPE = (299, 299)
    frame_counter = 0
    file_dir = os.path.join(args.tanks_dir, tank_name)
    if not os.path.exists(file_dir):
        print "Ups, missing directory for {0}".format(file_dir)

    for file_name in os.listdir(file_dir):

        image = cv2.imread(os.path.join(file_dir, file_name), cv2.IMREAD_COLOR)

        # Create 5 slightly different versions of the tank
        for i in range(5):
            background_image = cv2.imread(random.choice(BACKGROUNDS), cv2.IMREAD_COLOR)

            # Resize tank image to fit the 299x299 shape of the net and crop center
            # of image for a square image
            offset_x = random.randint(0, 0)
            offset_y = random.randint(20, 100)
            scale_factor = random.uniform(0.23, 0.27)

            transformation = np.float32([[scale_factor, 0, -120 + offset_x],[0, scale_factor, offset_y]])
            square_image = cv2.warpAffine(image, transformation, OUTPUT_SHAPE, borderValue=[255, 255, 255])

            # Randomly crop background to mach output shape of 299x299
            image_size_diff = np.subtract(background_image.shape[:2], OUTPUT_SHAPE)
            rand_x = random.randint(0, image_size_diff[1])
            rand_y = random.randint(0, image_size_diff[0])
            background_image = background_image[rand_y:rand_y + OUTPUT_SHAPE[1], rand_x:rand_x + OUTPUT_SHAPE[0]]

            # add tank image to the background
            mask = square_image > 200
            square_image[mask] = background_image[mask]

            # And save it
            save_dir = os.path.join(args.output_dir, tank_name)
            new_file_name = "{0}_{1}.png".format(tank_name, frame_counter)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            cv2.imwrite(os.path.join(save_dir, new_file_name), square_image)
            frame_counter += 1

    print "Done combining ", tank_name

if __name__ == '__main__':
    # Combine the previously downloaded tank images with a background and crop
    # them fit to the Inception network

    PARSER = argparse.ArgumentParser(description='Process some integers.')
    PARSER.add_argument('--tanks_dir', '-i', metavar='Input directory', type=str, help='Input tank image directory.')
    PARSER.add_argument('--backgrounds_dir', '-b', metavar='Input directory', type=str, help='Input background image directory.')
    PARSER.add_argument('--output_dir', '-o', metavar='Output directory', type=str, help='Output image directory.')
    args = PARSER.parse_args()

    BACKGROUNDS = [os.path.join("backgrounds", image) for image in os.listdir(args.backgrounds_dir) if image.endswith("png")]
    TANK_NAMES = [line.strip('\n') for line in open("tanks_blitz.txt", "r")]

    for tank_name in TANK_NAMES:
        combine_tanks_backgrounds(tank_name, args)