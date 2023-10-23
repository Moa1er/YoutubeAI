from selenium import webdriver
from selenium.webdriver.common.keys import Keys # pip install selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
import pickle

def upload_tiktok_vid(vid_title, vid_tags, vid_path):
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tiktok.com/@tiktalk_trend")
    time.sleep(5)
    cookies = pickle.load(open("selenium_script/cookies.pkl", "rb"))
    time.sleep(5)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    upload_url = "https://www.tiktok.com/creator-center/upload?from=upload"
    driver.get(upload_url)
    time.sleep(5)
    iframe_element = driver.find_element(By.CSS_SELECTOR,'iframe[data-tt="Upload_index_iframe"]')
    driver.switch_to.frame(iframe_element)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @accept='video/*' and @class='jsx-2834184006']")))
    element.send_keys(os.getcwd() + "/" + vid_path)
    time.sleep(30)
    span_element = driver.find_element(By.XPATH, "//span[@data-text='true']")
    action = ActionChains(driver)
    action.move_to_element(span_element).click()
    time.sleep(5)
    # Simulate pressing the 'End' key to move cursor to the end of text
    action.send_keys(Keys.END)
    # Now simulate holding 'Shift' and pressing 'Home' to select all text from end to start
    action.key_down(Keys.SHIFT).send_keys(Keys.HOME).key_up(Keys.SHIFT)
    # Now simulate pressing 'Backspace' to clear selected text
    action.send_keys(Keys.BACKSPACE)
    action.send_keys(vid_title).perform()
    for i in range(len(vid_tags)):
        tag_action = ActionChains(driver)
        tag_action.send_keys(vid_tags[i]).perform()
        time.sleep(3)
        enter_action = ActionChains(driver)
        enter_action.send_keys(Keys.ENTER).perform()
        
    time.sleep(5)
    upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='css-y1m958']")))
    upload_btn.click()
    time.sleep(300)
    driver.close()


