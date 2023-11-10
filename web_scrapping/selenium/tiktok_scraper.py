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
    time.sleep(2)
    cookies = pickle.load(open("web_scrapping/selenium/cookies_tiktalk.pkl", "rb"))
    time.sleep(2)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    upload_url = "https://www.tiktok.com/creator-center/upload?from=upload"
    driver.get(upload_url)
    wait = WebDriverWait(driver, 100)
    iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'iframe[data-tt="Upload_index_iframe"]')))
    driver.switch_to.frame(iframe_element)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @accept='video/*' and @class='jsx-2834184006']")))
    element.send_keys(os.getcwd() + "/" + vid_path)
    span_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-text='true']")))
    # span_element = driver.find_element(By.XPATH, "//span[@data-text='true']")
    action = ActionChains(driver)
    action.move_to_element(span_element).click()
    time.sleep(2)
    # Simulate pressing the 'End' key to move cursor to the end of text
    action.send_keys(Keys.END)
    # Now simulate holding 'Shift' and pressing 'Home' to select all text from end to start
    action.key_down(Keys.SHIFT).send_keys(Keys.HOME).key_up(Keys.SHIFT)
    # Now simulate pressing 'Backspace' to clear selected text
    action.send_keys(Keys.BACKSPACE)
    action.send_keys(vid_title).perform()   
    tag_fyp_enter = ActionChains(driver)
    tag_fyp_enter.send_keys(Keys.ENTER).perform()
    tag_fyp = ActionChains(driver)
    tag_fyp.send_keys(" #fyp").perform()
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'jsx-1584741129 hash-view-count mentionSuggestionsEntryText')]")))
    tag_fyp_enter = ActionChains(driver)
    tag_fyp_enter.send_keys(Keys.ENTER).perform()
    tag_fyp = ActionChains(driver)
    tag_fyp.send_keys(" #fypage").perform()
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'jsx-1584741129 hash-view-count mentionSuggestionsEntryText')]")))
    tag_fyp_enter = ActionChains(driver)
    tag_fyp_enter.send_keys(Keys.ENTER).perform()
    tag_fyp = ActionChains(driver)
    tag_fyp.send_keys(" #trending ").perform()
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'jsx-1584741129 hash-view-count mentionSuggestionsEntryText')]")))
    tag_fyp_enter = ActionChains(driver)
    tag_fyp_enter.send_keys(Keys.ENTER).perform()
    for i in range(len(vid_tags)):
        tag_action = ActionChains(driver)
        tag_action.send_keys(vid_tags[i]).perform()
        try:
            view_count_propositions = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'jsx-1584741129 hash-view-count mentionSuggestionsEntryText')]")))
            view_count_propositions = [s.text.replace(" views", "") for s in view_count_propositions]
            best_tag_idx = find_max_idx(view_count_propositions)
            for i in range(0, best_tag_idx):
                press_down = ActionChains(driver)
                press_down.send_keys(Keys.ARROW_DOWN).perform()
        except:
            pass
        enter_action = ActionChains(driver)
        enter_action.send_keys(Keys.ENTER).perform()
        
    time.sleep(10)
    upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='css-y1m958']")))
    upload_btn.click()
    time.sleep(100)
    driver.close()


# Define the function to convert the string numbers with suffixes to float values
def convert_to_number(s):
    # Check for the suffix and convert accordingly
    if "Add" in s:
        return 0.0
    elif s.endswith('B'):
        return float(s[:-1]) * 1e9
    elif s.endswith('M'):
        return float(s[:-1]) * 1e6
    elif s.endswith('K'):
        return float(s[:-1]) * 1e3
    else:
        return float(s)

# Define the function to find the index of the maximum number in the list
def find_max_idx(lst):
    # Convert all strings to numbers
    numbers = [convert_to_number(s) for s in lst]
    # Return the index of the maximum number
    return numbers.index(max(numbers))