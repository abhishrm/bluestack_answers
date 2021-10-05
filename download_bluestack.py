from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import configparser
import re
import os

import pyautogui

from pathlib import Path

# The below code reads the data from the config file
config_parser = configparser.ConfigParser()
config_parser.read(['./config_file.ini'])

# The below url is read from config filr from where bluestack installed need to be downloaded
url = config_parser.get('section', 'url')

# The below line reads the location from config file to which exe installer need to be installed
user_defined_download_location = config_parser.get('section', 'user_defined_download_location')

##The below code reads the chromedriver exe file which is needed fot selenium
executable_file_path = config_parser.get('section', 'executable_file_path')

element_locator = """//*[@data-animation='Retry / Download']"""


def invoke_the_chrome_and_access_the_url(executable_file_path, url, element_locator):
    # Invoke the driver
    # driver = webdriver.Chrome(executable_path=executable_file_path,options=chromeOptions)
    driver = webdriver.Chrome(executable_path=executable_file_path)
    driver.get(url)
    return driver


def click_the_download_button_on_web_page(driver, element_locator):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, element_locator))
        )

        element[1].click()
    except Exception as e:
        print("\n\n Element download button failed due to exception ", e)
        assert False, "Failed due to exception :{}".format(e)


driver = invoke_the_chrome_and_access_the_url(executable_file_path, url, element_locator)

click_the_download_button_on_web_page(driver, element_locator)

flag = None
file_name_of_blue_stack_installer = None
# The below code will check for 120 seconds whether the exe file is getting downloaded with in 120 seconds
for i in range(15):
    try:

        for root, dirs, files in os.walk(user_defined_download_location):

            for i in files:
                if re.search('BlueStacksinstaller', i, re.IGNORECASE):
                    file_name_of_blue_stack_installer = i
                    print("Found the downloaded bluestack exe file ", file_name_of_blue_stack_installer)
                    flag = True
                    break

            if flag is True:
                print("Will break out")
                break

    except Exception as e:
        print("Finding the exe file under user_defined_download_location failed due to error :{}  ", e)
    if flag is True:
        print("Found the downloaded bluestack exe file ", file_name_of_blue_stack_installer)
        break
    time.sleep(1)

if file_name_of_blue_stack_installer is None:
    assert False, "Not able to find the exe file the program tried to download under location with in 15 seconds ".format(
        user_defined_download_location)
time.sleep(10)

path = user_defined_download_location + '/' + file_name_of_blue_stack_installer

print("Program will now invoke the exe file :{} from path :{} ".format(file_name_of_blue_stack_installer,
                                                                       user_defined_download_location))
os.startfile(path)

print("Wait for 5 seconds")
time.sleep(5)

# The below library will send the tab button which will move the control to Install button on GUI screen
pyautogui.press('tab')
# The below button will press enter on the Install button and hence installation should get started
pyautogui.press('enter')

t1 = datetime.datetime.now()
raise_flag = None
for i in range(300):
    os.system('wmic /output:InstalledSoftwareList.txt product get name,version')
    with open("InstalledSoftwareList.txt", 'r') as f1:

        lines = f1.readlines()
        for line in lines:

            if re.search('BlueStacks', line):
                print("Software :{} found in list of system installed software, means it is installed ".format(line))
                raise_flag = True
                t2 = datetime.datetime.now()
                break

    if raise_flag is True:
        break

    time.sleep(1)
    if i == 299:
        assert False, "timeout, Not able to see installed Bluestack software in the system after checking system for 5 minutes"

all_time = t2 - t1
print("Time taken for software installation ", all_time)






