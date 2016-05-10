import numpy as np
import cv2
import sys
import time
import argparse
from os.path import join, basename, abspath
from glob import glob

lib_path = abspath("..")
sys.path.append(lib_path)
from video_analysis import ObjectTracker

def list_videos(directory):
    files = []
    for ext in ('*.mp4', '*.mkv'):
        files.extend(glob(join(directory, ext)))

    return files

def extract_backgrounds(args):

    THRESHOLD = 1 # seconds
    object_tracker = ObjectTracker()

    for video_file in list_videos(args.input_dir):

        video_file = "samples/Dragon Review.mkv"
        print "Processing %s" % video_file
        video_name = basename(video_file)[:-4]

        # Open the video and read it frame by frame
        cap = cv2.VideoCapture(video_file)
        if not cap.isOpened():
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
            elapsed_time = time.time() - start_time
            print elapsed_time

            if elapsed_time > THRESHOLD:

                # Allow the user to skip X seconds at the beginning/end of the
                # video clip
                total_elapsed_time = time.time() - total_elapsed_time_start
                if total_elapsed_time > (video_duration - args.skip_end): break
                if total_elapsed_time < args.skip_start: continue

                # Only save frames that dont show any tanks
                if object_tracker.contains_tank(frame) == 0:

                    file_name = join(args.output_dir, "%s_%s.png" % (video_name, frame_counter))
                    print "saving", file_name
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
    PARSER.add_argument('--output_dir', '-o', metavar='Output directory', type=str, help='Output image directory.')
    PARSER.add_argument('--skip_start', '-s', metavar='Skip Seconds', type=int, default=0, help='Skip x seconds at start of video.')
    PARSER.add_argument('--skip_end', '-e', metavar='Skip Seconds', type=int, default=0, help='Skip x seconds at end of video.')

    args = PARSER.parse_args()
    extract_backgrounds(args)