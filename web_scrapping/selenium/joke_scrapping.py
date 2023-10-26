from selenium import webdriver
from selenium.webdriver.common.keys import Keys # pip install selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.page_load_strategy = 'none'
options.add_experimental_option("detach", True)
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.get("https://upjoke.com/abrupt-jokes")


# stops to load the window after it find the joke-wrapper class
wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "joke-wrapper")))
driver.execute_script("window.stop();")

#takes all the joke divs
divs_with_class = driver.find_elements(By.CLASS_NAME, "joke-wrapper")

xpath_string_btn = "//button[contains(@onclick, \"this.parentNode.parentNode.nextElementSibling.classList.remove('offensive'); this.parentNode.parentNode.style.display = 'none';\")]"
buttons = driver.find_elements(By.XPATH, xpath_string_btn)
for button in buttons:
    button.click()

read_more_xpath = "//button[contains(@onclick, \"this.previousSibling.remove();\") and contains(@onclick, \"this.nextSibling.innerHTML = restOfLongJokes[\") and contains(@onclick, \"this.nextSibling.style.display=''; this.remove();\")]"
read_more_buttons = driver.find_elements(By.XPATH, read_more_xpath)
for button in read_more_buttons:
    button.click()

jokes = []
for div in divs_with_class:
    title = div.find_element(By.CLASS_NAME, "joke-title").text
    body = div.find_element(By.CLASS_NAME, "joke-body").text
    joke = title + body
    jokes.append(joke.replace("\n", " "))

driver.close()

with open("jokes.txt", "w") as f:
    for item in jokes:
        f.write(item + "\n")
