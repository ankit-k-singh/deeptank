from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image

import time
import StringIO

def get_images_for_tank(name, driver):

  driver.get("http://tanks.gg/wot/tank/{0}#tab:model".format(name))

  try:
    # Wait for site to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "turret-control")))

    # Remove unwanted UI elements
    hideJS = "arguments[0].style.visibility='hidden'; arguments[0].style.display='none'"
    driver.execute_script(hideJS, driver.find_element_by_css_selector("#model .left-panel"));
    driver.execute_script(hideJS, driver.find_element_by_css_selector("#model .right-panel"));
    driver.execute_script(hideJS, driver.find_element_by_css_selector("#model .loadout"));
    driver.execute_script(hideJS, driver.find_element_by_css_selector("#model .turret-control"));
    driver.execute_script(hideJS, driver.find_element_by_css_selector("#armor-tip"));
    driver.execute_script("document.getElementById('viewer-div').style.background = 'white';", driver.find_element_by_css_selector("#viewer-div"))

    # Switch visual model to 'collision' for correctly textured 3D models
    collisionDropdownXPath = "//*[@id=\"model\"]/div[1]/div[1]/div[1]/a"
    visualModeXPath = "//*[@id=\"model\"]/div[1]/div[1]/div[1]/ul/li[3]/a"
    driver.find_element_by_xpath(collisionDropdownXPath).click()
    driver.find_element_by_xpath(visualModeXPath).click()

    # Wait for the 3D model to load
    time.sleep(5) # seconds

    # canvas = driver.find_element_by_css_selector("#viewer-div")
    # offset_by_degree = 180 / 360
    # (ActionChains(driver)
    #   # .click_and_hold(canvas)
    #   # .move_by_offset(i * offset_by_degree, 0)
    #   # .release()
    #   .drag_and_drop_by_offset(canvas, i, 0)
    #   .perform()
    # )

    # Move the Mouse / Rotate Camera
    for i in range(0, 360):

      rotationPerTick = 0.02
      rotateCameraJS = "tgg.wot.components.TankDetails.modelViewer.azimuth = tgg.wot.components.TankDetails.modelViewer.azimuth + {0};".format(rotationPerTick)
      driver.execute_script(rotateCameraJS);

      # Save a screenshot of the website
      screen = driver.get_screenshot_as_png()
      image = Image.open(StringIO.StringIO(screen))
      image = image.crop((350, 430, 500 + 1800, 430 + 700))
      image.save("images/{0}_{1}.png".format(name, i), "PNG")

    print "Done with {0}".format(name)

  except Exception as e:
    print "Ups ", e
    pass


if __name__ == '__main__':




  driver = webdriver.Chrome()
  driver.set_window_size(1440, 900)
  driver.maximize_window();

  tank_names = [line.strip('\n') for line in open("tanks_blitz.txt", "r")]

  #for tank_name in tank_names:
  get_images_for_tank(tank_names[0], driver)

  driver.close()