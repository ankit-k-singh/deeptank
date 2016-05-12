import numpy as np
import cv2
import os
import random
import argparse

def combine_tanks_backgrounds(tank_name, args):

    frame_counter = 0
    file_dir = os.path.join(args.tanks_dir, tank_name)
    if not os.path.exists(file_dir):
        print "Ups, missing directory for {0}".format(file_dir)

    for file_name in os.listdir(file_dir):

        image = cv2.imread(os.path.join(file_dir, file_name), cv2.IMREAD_COLOR)
        image_width = int(image.shape[1])
        image_height = int(image.shape[0])

        # Create 5 slightly different versions of the tank
        for i in range(5):
            background_image = cv2.imread(random.choice(BACKGROUNDS), cv2.IMREAD_COLOR)

            # Randomly crop background to mach tank image shape
            image_size_diff = np.subtract(background_image.shape, image.shape)
            rand_x = random.randint(0, image_size_diff[1])
            rand_y = random.randint(0, image_size_diff[0])
            background_image = background_image[rand_y:rand_y + image_height, rand_x:rand_x + image_width]

            # add tank image to the background
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-100, 10)
            transformation = np.float32([[1,0, x_offset],[0,1, y_offset]])
            modified_image = cv2.warpAffine(image, transformation, (image_width, image_height), borderValue=[255, 255, 255])
            mask = modified_image > 200
            modified_image[mask] = background_image[mask]

            # And save it
            save_dir = os.path.join(args.output_dir, tank_name)
            new_file_name = "{0}_{1}.png".format(tank_name, frame_counter)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            cv2.imwrite(os.path.join(save_dir, new_file_name), modified_image)
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