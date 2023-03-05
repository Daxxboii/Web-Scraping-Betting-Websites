import requests_html
from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()
url = 'https://github.com/kamlesh11?tab=repositories'
response = session.get(url)

container = response.html.find('#user-repositories-list',first=True)
# #user-repositories-list represents id of <div> tag

list = container.find('li')

name = [] # for storing name of repository
lang = [] # language used in code
date = [] # date updated
for item in list:    
    tmp = item.text.split('\n')
    name.append(tmp[0])
    lang.append(tmp[1])
    date.append(tmp[2])

    df = pd.DataFrame({'Name':name,'language':lang,'date':date})
df.to_csv('repositories.csv')