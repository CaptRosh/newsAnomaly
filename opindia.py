import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import bs4
import requests
import warnings
warnings.filterwarnings("ignore")

global_url = "https://www.opindia.com/page/"
headlines_text=[]
articles_text = []


options = Options()
options.headless = True
options.add_argument("--log-level-3")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
keys = ("Lakhimpur", "Farmer")
time.sleep(2)

for i in range(1,4):
    driver.get(global_url+f"{i}/?s="+ "+".join(keys))
    page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    headlines = page.find_all('div', {'class':'tdb_module_loop td_module_wrap td-animation-stack'})
    for headline in headlines:
        headlines_text.append(headline.h3.text)
        page= requests.get(headline.a['href'])
        page = bs4.BeautifulSoup(page.text,'lxml')
        article = page.find_all('p')
        articles_text.append(" ".join(i.text for i in article))
    
for i in range(min(30,len(headlines_text))):
    with open("opindia/opindia_"+ str(i) + ".txt",'w') as file:
        file.write(headlines_text[i])
        file.write("\n")
        file.write(articles_text[i])

driver.close()