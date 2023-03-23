from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#import MailHelper
import Credentials
from utils import printoutput
import time
import os

class Scrape:
    options = webdriver.ChromeOptions()
    options.add_argument(
  "--user-data-dir=/Users/dakshdhakad/Library/Application Support/Google/Chrome/"
   )

    #add custom profile
    options.add_argument('--profile-directory=Profile 2')

    driver = webdriver.Chrome(options=options,
                              service=Service(ChromeDriverManager().install()))
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
           _userinput = input("Enter Auth Link")
           val = _userinput
           self.driver.get(val)
           time.sleep(5)
           self.Fetch()

      else:
          self.Fetch()

     #fetches and sorts all the positive-ev bets
    def Fetch(self):
      val = ("https://oddsjam.com/betting-tools/positive-ev")
      self.driver.get(val)
      time.sleep(5)
      tables = self.driver.find_elements(By.ID, "betting-tool-table-row")
      for table in tables:
        table.click()
        time.sleep(3)
      page_source = self.driver.page_source
      soup = BeautifulSoup(page_source, features="html.parser")
      soup.prettify()
      additional_table_data = soup.find_all('div', {'class': "grid gap-2 mb-6"})
      #for testing
      printoutput.Output(additional_table_data, "output.html")
      self.driver.quit()
      return soup


#init()
Scrape()
  


  
  