from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import codecs

import re

from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

val = ("https://sports.az.betmgm.com/en/sports/basketball-7/betting/usa-9/nba-6004")

wait = WebDriverWait(driver, 10)

driver.get(val)


get_url = driver.current_url
wait.until(EC.url_to_be(val))


if get_url == val:
    page_source = driver.page_source



soup = BeautifulSoup(page_source,features="html.parser")

div_text=[]
div_text = soup.findAll("div",{"class":"participants-pair-game"})




with open("output.html", "a") as f:
        print(div_text,file=f)


driver.quit()
