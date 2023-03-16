from selenium import webdriver
from selenium.webdriver.chrome.service import Service

#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

import time

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/Users/dakshdhakad/Library/Application Support/Google/Chrome/")
options.add_argument('--profile-directory=Profile 2')


driver=webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))

def Fetch():
        val = ("https://oddsjam.com/betting-tools/positive-ev")
        driver.maximize_window()
        driver.get(val)
        time.sleep(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="html.parser")
        soup.prettify()
        driver.quit()
        return soup













