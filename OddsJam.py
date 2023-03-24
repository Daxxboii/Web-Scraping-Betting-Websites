#class to auto-login into oddsjam and scrape positive ev tables and bets
#Note: make sure output window is on fullscreen mode while scraping (16:9)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#import MailHelper
import Credentials
from utils import printoutput
from utils import clearuparray
import time
import os



class Scrape:
  options = webdriver.ChromeOptions()
  sportsbook = 'FanDuel'
  tables = []
  matches = []
  odds = []
  oddscolor = []
  event = []
  novig_odds = []
  novigcolor = []
  index = 0

  #comment when not in a cloud env
  #options.add_argument('--no-sandbox')
  #options.add_argument('--disable-dev-shm-usage')

  #uncomment when not in cloud env
  options.add_argument(
  "--user-data-dir=//Users/dakshdhakad/Library/Application Support/Google/Chrome/"
  )
  #add custom profile
  options.add_argument('--profile-directory=Profile 2')
  driver = webdriver.Chrome(options=options,
                            service=Service(ChromeDriverManager().install()))

  #comment in a local env
  #driver = webdriver.Chrome(options=options)

  #driver.set_window_size(1920, 1080)
  driver.maximize_window()

  #check if oddsjam has id logged in , if not , auto login
  def __init__(self):
    val = ("https://oddsjam.com/auth/login")
    self.driver.get(val)
    time.sleep(5)  #for auto login to happen
    email_input = self.driver.find_elements("id", "login-email")
    if (len(email_input) > 0):
      email_input[0].send_keys(Credentials.Email_Address)
      email_input[0].send_keys(Keys.ENTER)
      time.sleep(5)
      #Dummy For now , to be fetched from email
      _userinput = input("Enter Auth Link: ")
      val = _userinput
      self.driver.get(val)
      time.sleep(20)
      self.Fetch()

    else:
      self.Fetch()

  #fetches  all the positive-ev tables
  def Fetch(self):
    val = ("https://oddsjam.com/betting-tools/positive-ev")
    self.driver.get(val)
    time.sleep(10)
    tables = self.driver.find_elements(By.ID, "betting-tool-table-row")
    for table in tables:
      table.click()
      time.sleep(3)
    page_source = self.driver.page_source
    soup = BeautifulSoup(page_source, features="html.parser")
    soup.prettify()
    self.driver.quit()
    self.Sort(soup)

  #sorts and returns all the positive-ev bets throughout the tables
  def Sort(self, soup):
     additional_tables_data = soup.find_all('div', {'class': "grid gap-2 mb-6"})

     #Fetching odds from boths rows of each table
     for additionaldata in additional_tables_data:
       nestedodds = []
       nestedoddscolor = []
       #only if the match exists for given sportsbook
       if(additionaldata.find('img',{'alt':self.sportsbook})!=[]):
         row_elements = additionaldata.find_all('div', {'role': 'presentation'})
         for element in row_elements:
           para = element.findChildren('p')
           classname = para[0]['data-testid']
           color = element['class']
           color = clearuparray.arraytostring(color)
           if(self.sportsbook in classname):
             nestedodds.append(para[0].getText())
             if("green" in color):
               nestedoddscolor.append("green")
             else:
               nestedoddscolor.append("white")

          

         self.odds.append(nestedodds)
         self.oddscolor.append(nestedoddscolor)
        

     self.odds = clearuparray.cleanup(self.odds)
     self.oddscolor = clearuparray.cleanup(self.oddscolor)
    
     #Fetching all the tables
     self.tables = soup.find_all('div',{'id':'betting-tool-table-row'})
     
     #Fetching the match names from all the tables under the given sportsbook
     for table in self.tables:
       tempnovig_odds = []
       tempnovig_color = []
       if(additional_tables_data[self.index].find('img',{'alt':self.sportsbook})!=[]):
         matchname = table.find('p',{'class':'text-sm text-brand-gray-1 __className_f0a1f4 font-semibold'}).getText()
         self.matches.append(matchname)


       
       novig_panel = table.find('div',{'id':'pos-ev-bets-books-no-vig'})
       novig_text_holder = novig_panel.find_all('div',{'class':'items-center flex'})
       for text in novig_text_holder:
         if(text.find('span',{'class':'text-sm __className_f0a1f4 font-bold text-black min-w-[45px] pr-2 py-1 text-right'})!=None):
          novig_digits = text.find('span',{'class':'text-sm __className_f0a1f4 font-bold text-black min-w-[45px] pr-2 py-1 text-right'}).text
          tempnovig_color.append("green")
         else:
          novig_digits = text.find('span',{'class':'text-sm __className_f0a1f4 font-medium text-brand-gray-1 min-w-[45px] pr-2 py-1 text-right'}).text
          tempnovig_color.append("white")
          
         tempnovig_odds.append(novig_digits)


       self.novig_odds.append(tempnovig_odds)
       self.novigcolor.append(tempnovig_color)
       self.index = self.index+1
       
     printoutput.AppendOutput(clearuparray.arraytostring(self.odds[0][0]),"odds.html") 
     self.index = 0
     self.output()

  def output(self):
     for match in self.matches:
       #Determining offered odds
       matchname = self.matches[self.index]
       sport = self.tables[self.index].find('p',{'class':'text-sm text-brand-gray-1 __className_f0a1f4 font-medium self-center'}).text
       team = ''
       opponent = ''
       
       offered_odds = 0
       if(self.oddscolor[self.index][0]=="white"):
         offered_odds = clearuparray.arraytostring(self.odds[self.index][0])
         opponent = clearuparray.splitteams(matchname)[0]
         team = clearuparray.splitteams(matchname)[1]
         
       else:
         offered_odds = clearuparray.arraytostring[self.odds[self.index][1]]
         opponent = clearuparray.splitteams(matchname)[1]
         team = clearuparray.splitteams(matchname)[0]

       #Determining no vig odds 
       novigodds1 = clearuparray.arraytostring[self.novig_odds[self.index][0]]
       novigodds2 = clearuparray.arraytostring[self.novig_odds[self.index][1]]

       position = ""
       implied_probs = 0

       if(clearuparray.arraytostring[self.novigcolor[self.index][0]]=="white"):
         position = "secong"
         implied_probs = self.novig_odds[self.index][1]
       else:
         position = "first"
         implied_probs = self.novig_odds[self.index][0]
        
       decimaledge = mathutils.MathUtils.calculate_edge_from_vig(novigodds1,novigodds2,position,offered_odds)

       date = self.tables[self.index].find('div',{'class':'self-center'}).text
       market = self.tables[self.index].find('p',{'class':'text-sm text-brand-gray-1 __className_f0a1f4 font-medium self-center'}).text
       sportsbook = self.sportsbook

       
       self.index = self.index+1
      
   


