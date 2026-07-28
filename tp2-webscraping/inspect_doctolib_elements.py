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
    '[class*="search-result"]',
    '[class*="result"]',
    '[class*="card"]',
    'article',
    '[class*="doctor"]',
    'a',
    'div',
]
for sel in selectors:
    try:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
    except Exception as e:
        print('ERR', sel, e)
        continue
    print('SELECTOR', sel, 'count', len(els))
    for i, el in enumerate(els[:20]):
        txt = re.sub(r'\s+', ' ', el.text).strip()
        if 'Cardiologue' in txt or 'Dr ' in txt or 'Paris' in txt or 'Disponibilités' in txt:
            print('---', i, 'tag', el.tag_name, 'class', el.get_attribute('class'))
            print(txt[:500])
            print('html', el.get_attribute('outerHTML')[:1000])
            print()
    print('====')

driver.quit()
