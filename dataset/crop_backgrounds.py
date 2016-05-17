import numpy as np
import cv2
import os
import random
import argparse

def crop_backgrounds(args):

    OUTPUT_SHAPE = (299, 299)
    frame_counter = 0

    for file_name in os.listdir(args.backgrounds_dir):

        if not file_name.endswith((".png", ".jpeg")):
            continue

        file_path = os.path.join(args.backgrounds_dir, file_name)

        background_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        aspect_ratio = background_image.shape[1] / background_image.shape[0]

        for i in range(10):
            # Down-size background and randomly crop background to mach output shape of 299x299
            image = cv2.resize(background_image, (OUTPUT_SHAPE[0] * aspect_ratio, OUTPUT_SHAPE[0]))

            offset_x = random.randint(0, image.shape[1] - OUTPUT_SHAPE[1])
            image = image[0:0 + OUTPUT_SHAPE[1], offset_x:offset_x + OUTPUT_SHAPE[0]]

            # And save it
            save_dir = args.output_dir
            new_file_name = "background_{}.png".format(frame_counter)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            cv2.imwrite(os.path.join(save_dir, new_file_name), image)
            frame_counter += 1


if __name__ == '__main__':
    # Combine the previously downloaded tank images with a background and crop
    # them fit to the Inception network

    PARSER = argparse.ArgumentParser(description='Process some integers.')
    PARSER.add_argument('--backgrounds_dir', '-b', metavar='Input directory', type=str, help='Input background image directory.')
    PARSER.add_argument('--output_dir', '-o', metavar='Output directory', type=str, help='Output image directory.')
    args = PARSER.parse_args()

    crop_backgrounds(args)
