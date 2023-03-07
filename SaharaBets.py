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
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

IsoDate = (input("Enter Date(ISO Format): "))


yourdate = parser.parse(IsoDate)



currDate = datetime.datetime.now()

DateToSearch =""


if(yourdate.date()==currDate.date()):
    DateToSearch = "TODAY"
    
else:
    DateToSearch = "0"+(str)(yourdate.day)+"/"+"0"+(str)(yourdate.month)

Choice = int(input("Enter 1 for NBA , 2 for NCAAB: "))

if(Choice==1):
    val = ("https://az.saharabets.com/sports/navigation/10900.1/10901.1")
else:
    val = ("https://az.saharabets.com/sports/navigation/12248.1/12249.1")





driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))




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


SiteData = []
SiteData = events[chosen_event-1].findAll('div',class_="flex")
SiteData.pop(0)



Spread = []
Total = []
Money = []



tempdata = SiteData[0].findNext('div',class_="currenthandicap")
Spread.append(tempdata.get_text())

tempdata = SiteData[0].find('div',class_='selectionprice')
Spread[0] = "("+Spread[0] +")"+ tempdata.get_text()




tempdata = SiteData[1].findNext('div',class_="currenthandicap")
Spread.append(tempdata.get_text())

tempdata = SiteData[1].find('div',class_='selectionprice')
Spread[1] = "("+Spread[1] +")"+ tempdata.get_text()



tempdata = SiteData[2].find('div',class_="selectionprice")
Money.append(tempdata.get_text())


tempdata = SiteData[3].find('div',class_="selectionprice")
Money.append(tempdata.get_text())


tempdata = SiteData[4].find('div',class_="uo-currenthandicap")
Total.append(tempdata.get_text())

tempdata = SiteData[4].find('div',class_="selectionprice")
Total[0] = Total[0] + tempdata.get_text()

tempdata = SiteData[5].find('div',class_="uo-currenthandicap")
Total.append(tempdata.get_text())

tempdata = SiteData[5].find('div',class_="selectionprice")
Total[1] = Total[1] + tempdata.get_text()







with open("output.html", "a") as f:
     print(Spread,file=f)


dict = {'Team Name': TeamNames,'Spread':Spread,'Total':Total,'Money':Money}

df = pd.DataFrame(dict)
df.to_csv('Bets.csv')


# date = []

# Website_date = soup.find_all("div",{"class":"date"})


driver.quit()

 # -6 -110
  #+6 -110
  #-235
  #+195
  #O 232 -110
  #U 232 -110