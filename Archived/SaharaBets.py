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


DateToSearch = "0"+(str)(yourdate.month)+"/0"+(str)(yourdate.day)+"/"+(str)(yourdate.year)

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

selected_events = []
for event in events:
   
   matchdate = event.find('div',class_="time")
   _matchdate = matchdate.find('span')


   datebool =  _matchdate.get_text().__contains__(DateToSearch)
 
   
   if(datebool):
         index+=1
         team_names = []
         team_names = event.findAll('span', class_="name")
         versus_name = str(index) + ".)  " + \
         team_names[0].get_text() + " vs " + team_names[1].get_text()
         print(versus_name)
         selected_events.append(event)
         

   
   

def FetchTeamNamesFromEvent(_event):
    team_names = []
    team_names = _event.findAll('span', class_="name")

    team_names_text = [team_names[0].get_text(), team_names[1].get_text()]
    return team_names_text


with open("output.html", "a") as f:
        print(selected_events,file=f)


if(selected_events == []):
    print("No Matches to show")

else:
    chosen_event = int(input("Enter the match no: "))

    TeamNames = []
    TeamNames = FetchTeamNamesFromEvent(selected_events[chosen_event-1])


    SiteData = []
    SiteData = selected_events[chosen_event-1].findAll('div',class_="flex")
    SiteData.pop(0)



    Spread = []
    Total = []
    Money = []



    tempdata = SiteData[0].findNext('div',class_="currenthandicap")
    Spread.append(tempdata.get_text())

    tempdata = SiteData[0].find('div',class_='selectionprice')
    Spread[0] = ("("+Spread[0] +")"+ tempdata.get_text())

    Spread[0] = Spread[0].replace('\n', '')




    tempdata = SiteData[1].findNext('div',class_="currenthandicap")
    Spread.append(tempdata.get_text())

    tempdata = SiteData[1].find('div',class_='selectionprice')
    Spread[1] = "("+Spread[1] +")"+ tempdata.get_text()
    Spread[1] = Spread[1].replace('\n', '')



    tempdata = SiteData[2].find('div',class_="selectionprice")
    Money.append(tempdata.get_text())


    tempdata = SiteData[3].find('div',class_="selectionprice")
    Money.append(tempdata.get_text())


    tempdata = SiteData[4].find('div',class_="uo-currenthandicap")
    Total.append(tempdata.get_text()+"\n")

    tempdata = SiteData[4].find('div',class_="selectionprice")
    Total[0] = Total[0] + tempdata.get_text()

    tempdata = SiteData[4].find('div',class_="had-value")

    Total[0] = tempdata.get_text()+" "+ Total[0] 


    tempdata = SiteData[5].find('div',class_="uo-currenthandicap")
    Total.append(tempdata.get_text()+"\n")

    tempdata = SiteData[5].find('div',class_="selectionprice")
    Total[1] = Total[1] + tempdata.get_text()

    tempdata = SiteData[5].find('div',class_="had-value")

    Total[1] = tempdata.get_text()+" " +Total[1] 






    dict = {'Team Name': TeamNames,'Spread':Spread,'Total':Total,'Money':Money}

    df = pd.DataFrame(dict)
    df.to_csv('Bets.csv')








driver.quit()

