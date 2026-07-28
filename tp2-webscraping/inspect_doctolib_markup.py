import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)
driver.get('https://www.doctolib.fr/cardiologue/paris')
time.sleep(10)
html = driver.page_source
name = 'Dr Ugo VERGEYLEN'
idx = html.find(name)
print('idx', idx)
if idx != -1:
    start = max(0, idx-3000)
    end = min(len(html), idx+6000)
    print(html[start:end])

for pat in ['Dr Ugo VERGEYLEN', 'href="/praticien', 'href="/medecin', 'data-testid', 'data-test', 'search-result']:
    print(pat, html.find(pat))

driver.quit()
