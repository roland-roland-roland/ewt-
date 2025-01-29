#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.10

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import threading

import json
import os

stop_flag = threading.Event()
driver = None

class ConfigReader:
    def __init__(self,path):
        self.path = path
        with open(self.path) as f:
            self.dic = json.load(f)

    def save(self):
        with open(self.path) as f:
            json.dump(self.path)

    def rd_default_drv_path(self):
        return self.dic["default_drv_path"]

    def rd_element_target(self,key):
        if key in self.dic["ele_target"]:
            return self.dic["ele_target"][key]
        return None
    def rd_scene_url(self,key):
        return self.dic["scene_url"]

def convert_duration_to_seconds(duration):
    parts = duration.split(':')
    minutes = int(parts[0])
    seconds = int(parts[1]) if len(parts) > 1 else 0
    total_seconds = minutes * 60 + seconds
    return total_seconds


def switch_to_new_window(driver, wait):
    original_window = driver.current_window_handle
    wait.until(EC.number_of_windows_to_be(2))
    new_window = (lambda x = None: [ window for window in x if window != original_window ])(driver.window_handles)[0]
    driver.switch_to.window(new_window)
    return original_window

def get_video_duration(wait, xpath):
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    duration_str = element.text.split(' ')[-1]
    return convert_duration_to_seconds(duration_str)


def check_and_click_element(driver, xpath):
    pass
# WARNING: Decompyle incomplete


def element_detection_thread(driver, xpath):
    check_and_click_element(driver, xpath)


def main():
    global driver,config_obj
    try:
        config_obj = ConfigReader("config.json")
        driver_path = config_obj.rd_default_drv_path()

        user_name = input('请输入账号:')
        user_password = input('请输入密码:')
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(service=service,options=options)
        actions = ActionChains(driver)
        url = config_obj.rd_scene_url()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        driver.maximize_window()
        input_box = wait.until(EC.element_to_be_clickable((By.ID, config_obj.rd_element_target("UsernameBox"))))
        input_box.send_keys(user_name)
        input_box = driver.find_element(By.ID, config_obj.rd_element_target("PasswordBox"))
        input_box.send_keys(user_password)

        cssr = ""
        for i in config_obj.rd_element_target("ClickableObject"):
            cssr+=i

        config_obj.rd_element_target("ClickableObject")
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,cssr)))
        button.click()
    except PermissionError:
        print("Access Denied.Please check your access.")
    except FileNotFoundError:
        print("Could not load config file!")
    except Exception as e:
        print("Unknown Error.")
if __name__ == "__main__":
    main()
