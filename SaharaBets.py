from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import codecs

import re
import os

import csv
import pandas as pd

import datetime
from dateutil import parser


from webdriver_manager.chrome import ChromeDriverManager

IsoDate = (input("Enter Date(ISO Format): "))


yourdate = parser.parse(IsoDate)
print(yourdate.date())


currDate = datetime.datetime.now()
print(currDate.date())





driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


val = ("https://az.saharabets.com/sports/navigation/10900.1/10901.1")

wait = WebDriverWait(driver, 10)

driver.get(val)


get_url = driver.current_url
wait.until(EC.url_to_be(val))


if get_url == val:
    page_source = driver.page_source


soup = BeautifulSoup(page_source, features="html.parser")

events = []
events = soup.findAll("div", {"class": "event"})


index = 0


if os.path.exists("Bets.csv"):
  os.remove("Bets.csv")


print("Teams Playing are:")


def FetchMatchFromEvent(_event, _index):

    team_names = []
    team_names = _event.findAll('span', class_="name")
    versus_name = str(_index) + ".)  " + \
        team_names[0].get_text() + " vs " + team_names[1].get_text()
    return versus_name


def FetchTeamNamesFromEvent(_event):
    team_names = []
    team_names = _event.findAll('span', class_="name")

    team_names_text = [team_names[0].get_text(), team_names[1].get_text()]
    return team_names_text


for event in events:
    index += 1
    print(FetchMatchFromEvent(event, index))




chosen_event = int(input("Enter the match no."))

TeamNames = []
TeamNames = FetchTeamNamesFromEvent(events[chosen_event-1])



dict = {'Team Name': TeamNames}

df = pd.DataFrame(dict)
df.to_csv('Bets.csv')


#print(TeamNames)
# print(MatchName)
# with open("output.html", "a") as f:
#   print(versus_name,file=f)
# date = []

# Website_date = soup.find_all("div",{"class":"date"})


driver.quit()
