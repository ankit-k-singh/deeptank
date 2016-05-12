import numpy as np
import cv2
import sys
import time
import argparse
from os.path import join, basename, abspath
import os
from glob import glob

def list_videos(directory):
    files = []
    for ext in ('*.mp4', '*.mkv', '*.mov', '*.avi'):
        files.extend(glob(join(directory, ext)))

    return files

def extract_backgrounds(args):

    for video_file in list_videos(args.input_dir):

        print "Processing %s" % video_file
        video_name = basename(video_file)[:-4]

        # Open the video and read it frame by frame
        cap = cv2.VideoCapture(video_file)
        if not cap.isOpened():
            print "Ups. Something went wrong."
            sys.exit(1)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        video_duration = frame_count / fps

        start_time = total_elapsed_time_start = time.time()
        frame_counter = 0
        total_elapsed_time = 0


        while True:

            ret, frame = cap.read()
            if not ret: break

            # Only capture a frame every 1 second
            now = time.time()
            elapsed_time = now - start_time

            if elapsed_time > args.threshold:

                # Allow the user to skip X seconds at the beginning/end of the
                # video clip
                total_elapsed_time = now - total_elapsed_time_start
                if total_elapsed_time > (video_duration - args.skip_end): break
                if total_elapsed_time < args.skip_start: continue

                # Crop frame to exclude user's vehicle + GUI
                frame = frame[0:1200, 0:2750]

                file_name = join(args.output_dir, "%s_%s.png" % (video_name, frame_counter))
                cv2.imwrite(file_name, frame)

                frame_counter += 1
                start_time = time.time()


        print "Extracted %s background frames" % frame_counter
        cap.release()


if __name__ == '__main__':
    # Extract 'background' frames from a video. Background image should not show
    # any tanks just the 'map' aka background.

    PARSER = argparse.ArgumentParser(description='Process some integers.')
    PARSER.add_argument('--input_dir', '-i', metavar='Input directory', type=str, help='Input image directory.')
    PARSER.add_argument('--output_dir', '-o', metavar='Output directory', type=str, default="backgrounds", help='Output image directory.')
    PARSER.add_argument('--skip_start', '-s', metavar='Skip Seconds', type=int, default=0, help='Skip x seconds at start of video.')
    PARSER.add_argument('--skip_end', '-e', metavar='Skip Seconds', type=int, default=0, help='Skip x seconds at end of video.')
    PARSER.add_argument('--threshold', '-t', metavar='Threshold', type=float, default=1, help='Time between consecutive frame in seconds.')

    args = PARSER.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    extract_backgrounds(args)