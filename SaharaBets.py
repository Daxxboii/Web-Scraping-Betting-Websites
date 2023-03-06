from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import codecs

import re

from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

val = ("https://az.saharabets.com/sports/navigation/10900.1/10901.1")

wait = WebDriverWait(driver, 10)

driver.get(val)


get_url = driver.current_url
wait.until(EC.url_to_be(val))


if get_url == val:
    page_source = driver.page_source



soup = BeautifulSoup(page_source,features="html.parser")

div_text=[]
div_text = soup.findAll("div",{"class":"event"})


names=[]
names = soup.find_all("span",{"class":"name"})

date = [] 

date = soup.find_all("div",{"class":"date"})





with open("output.html", "a") as f:
        print(date,file=f)


driver.quit()
