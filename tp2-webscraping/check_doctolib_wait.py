import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(options=options)
driver.get('https://www.doctolib.fr/cardiologue/paris')
wait = WebDriverWait(driver, 40)
wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
time.sleep(5)
anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/cardiologue/'], a[href*='/cabinet-medical/']")
print('anchors', len(anchors))
print('body contains cardiologue', 'Cardiologue' in driver.find_element(By.TAG_NAME, 'body').text)
driver.quit()
