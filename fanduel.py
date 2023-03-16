import OddsJam  as scraper
from bs4 import BeautifulSoup
from selenium import webdriver
import os

page_source = scraper.Fetch()

if(os.path.isfile("output.html")):
        os.remove("output.html")



tables = []
tables = page_source.find_all('div',id="betting-tool-table-row")


with open("output.html", "a") as f:
            print(tables,file=f)