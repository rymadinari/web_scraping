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

selectors = [
    'div[data-test="search-result-card"]',
    'div[data-testid="search-result-card"]',
    '[data-testid*="card"]',
    '[data-test*="card"]',
    'a[href*="/praticien/"]',
    'a[href*="/medecin/"]',
    '[class*="search-result"]',
    '[class*="doctor"]',
    '[class*="praticien"]',
    '[class*="card"]',
]

for s in selectors:
    try:
        els = driver.find_elements(By.CSS_SELECTOR, s)
    except Exception:
        els = []
    print(s, len(els))
    for el in els[:3]:
        try:
            txt = re.sub(r'\s+', ' ', el.text).strip()
        except Exception:
            txt = ''
        if txt:
            print('  ', txt[:200])
    if len(els) > 0:
        print('---')

print('doctor links', len(driver.find_elements(By.CSS_SELECTOR, 'a[href*="/praticien/"]')))
print('medecin links', len(driver.find_elements(By.CSS_SELECTOR, 'a[href*="/medecin/"]')))
body_text = re.sub(r'\s+', ' ', driver.find_element(By.TAG_NAME, 'body').text)
print('body preview', body_text[:3000])

driver.quit()
