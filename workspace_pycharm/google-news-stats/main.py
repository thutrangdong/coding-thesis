from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import re

starting_date = datetime.date(2011, 5, 1)
ending_date = datetime.date(2011, 5, 6)
delta = ending_date - starting_date
browser = webdriver.Firefox()

for current_date in (starting_date + datetime.timedelta(n) for n in range(-1,delta.days)):

    current_date_day = current_date.strftime('%-d')
    current_date_month = current_date.strftime('%-m')
    current_date_year = current_date.strftime('%Y')
    base_url = "https://www.google.de/search?q=bitcoin&biw=1680&bih=926&source=lnt&tbs=cdr:1,cd_min:"+current_date_month+"/"+current_date_day+"/"+current_date_year+",cd_max:"+current_date_month+"/"+current_date_day+"/"+current_date_year+"&tbm=nws&gws_rd=cr&dcr=0&ei=ZvEmWofaEYTFwALMh7PICQ"
    browser.get(base_url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    items_current = soup.find("div", {"id": "resultStats"}).getText()
    value = re.search('(?<=Ungefähr )(.*)(?= Ergebnisse)', items_current).group(0)
    value = value.replace('.', '')
    value = int(value)
    print(value)

    #^.*[ ,\t]+