import cv2
import numpy as np
import time
import os
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

def get_images_for_tank(tank_name, DRIVER, done_callback):

    DRIVER.get("http://tanks.gg/wot/tank/{0}#tab:model".format(tank_name))

    try:
        # Wait for site to load
        WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "turret-control")))

        # Remove unwanted UI elements
        hide_js = "arguments[0].style.visibility='hidden'; arguments[0].style.display='none'"
        DRIVER.execute_script(hide_js, DRIVER.find_element_by_css_selector("#model .left-panel"))
        DRIVER.execute_script(hide_js, DRIVER.find_element_by_css_selector("#model .right-panel"))
        DRIVER.execute_script(hide_js, DRIVER.find_element_by_css_selector("#model .loadout"))
        DRIVER.execute_script(hide_js, DRIVER.find_element_by_css_selector("#model .turret-control"))
        DRIVER.execute_script(hide_js, DRIVER.find_element_by_css_selector("#armor-tip"))
        DRIVER.execute_script("document.getElementById('viewer-div').style.background = 'white';", DRIVER.find_element_by_css_selector("#viewer-div"))

        # Switch visual model to 'collision' for correctly textured 3D models
        collision_dropdown_xpath = "//*[@id=\"model\"]/div[1]/div[1]/div[1]/a"
        visual_mode_xpath = "//*[@id=\"model\"]/div[1]/div[1]/div[1]/ul/li[3]/a"
        DRIVER.find_element_by_xpath(collision_dropdown_xpath).click()
        DRIVER.find_element_by_xpath(visual_mode_xpath).click()

        # Wait for the 3D model to load
        time.sleep(5) # seconds

        rotation_per_tick = 0.1
        pitch_angle = {
            'FPV': 1.57,
            'ISO': 1.75
        }

        # Move the Mouse / Rotate Camera
        for p_key, p_angle in pitch_angle.iteritems():

            rotate_camera_x_js = "tgg.wot.components.TankDetails.modelViewer.azimuth = tgg.wot.components.TankDetails.modelViewer.azimuth + {0};".format(rotation_per_tick)
            rotate_camera_y_js = "tgg.wot.components.TankDetails.modelViewer.zenith = {0};".format(p_angle)
            reset_camera_x_js = "tgg.wot.components.TankDetails.modelViewer.azimuth = 4.7"

            DRIVER.execute_script(reset_camera_x_js)
            DRIVER.execute_script(rotate_camera_y_js)

            for i in range(0, 60):

                DRIVER.execute_script(rotate_camera_x_js)

                # Save a screenshot of the website
                np_array = np.fromstring(DRIVER.get_screenshot_as_png(), np.uint8)
                image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                # Crop image
                image = image[430:430 + 750, 350:500 + 1800]

                # And save it
                save_dir = os.path.join(args.output_dir, tank_name)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                cv2.imwrite(os.path.join(save_dir, "{0}_{1}_{2}.png".format(tank_name, p_key, i)), image)

        print "Done with {0}".format(tank_name)
        done_callback(DRIVER)

    except TimeoutException as exception:
        print "Ups ", exception


def download_next_tank(driver):

    if len(TANK_NAMES) > 0:
        tank_name = TANK_NAMES.pop()

        get_images_for_tank(tank_name, driver, download_next_tank)

if __name__ == '__main__':

    DRIVER = webdriver.Chrome()
    DRIVER.set_window_size(1440, 900)
    DRIVER.maximize_window()

    PARSER = argparse.ArgumentParser(description='Process some integers.')
    PARSER.add_argument('--output_dir', '-o', metavar='Output directory', default="tanks", type=str, help='Output image directory.')
    args = PARSER.parse_args()

    TANK_NAMES = [line.strip('\n') for line in open("tanks_blitz.txt", "r")]
    TANK_NAMES.reverse()

    # Recursively download all tanks
    download_next_tank(DRIVER)

    DRIVER.close()