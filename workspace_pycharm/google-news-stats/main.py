from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import re

starting_date = datetime.date(2011, 5, 1)
ending_date = datetime.date(2011, 5, 6)
delta = ending_date - starting_date
browser = webdriver.Firefox()

starting_date = datetime.date(2011, 5, 1) #year, month, day

ending_date = datetime.date(2017, 11, 18)
delta = ending_date - starting_date
browser = webdriver.Firefox()

amount_publications = []

for current_date in (starting_date + datetime.timedelta(n) for n in range(0,delta.days+1)):

    current_date_day = current_date.strftime('%d')
    current_date_month = current_date.strftime('%m')
    current_date_year = current_date.strftime('%Y')
    base_url = "https://www.genios.de/dosearch?explicitSearch=true&q=bitcoin&searchRestriction=&dbShortcut=%3A2%3AALLEQUELLENNEU-1_%3A2%3AALLEQUELLENNEU&searchMask=5461&TI%2CUT%2CDZ%2CBT%2COT%2CSE%2CSL=&NN%2CAU%2CMM%2CZ2=&CO%2CC2%2CTA%2CKA%2CVA%2CZ1=&CT%2CZ4%2CKW=&BR%2CGW%2CN1%2CN2%2CNC%2CND%2CSC%2CWZ%2CZ5%2CAI%2CBC%2CKN%2CTN%2CVN%2CK0%2CB4=&Z3%2CCN%2CCE%2CKC%2CTC%2CVC=&timeFilterType=on&DT_from="+current_date_day+"."+current_date_month+"."+current_date_year+"&DT_to="+current_date_day+"."+current_date_month+"."+current_date_year+"&x=70&y=13"
    browser.get(base_url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    items_current = soup.find("div", {"class": "moduleResultTextHeader"}).getText()
    #print(items_current)
    if items_current == "Ihre Suchanfrage ergab 0 Treffer":
        value = 0
    else:
        value = re.search('\(([^\)]+)\)', items_current).group(1)
        value = int(value)
    print(current_date.strftime('%d/%m/%Y') + "\t" + str(value))
    amount_publications.append(value)

    #^.*[ ,\t]+