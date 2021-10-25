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

global_url = "https://www.ndtv.com/search?searchtext="
headlines_text=[]
articles_text = []


options = Options()
options.headless = True
options.add_argument("--log-level-3")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
keys = ("Lakhimpur", "Farmer") #Input ka idhar daalna hai string manipulation karke
driver.get(global_url + '-'.join(keys))
page = bs4.BeautifulSoup(driver.page_source, 'html.parser')

page = bs4.BeautifulSoup(driver.page_source, 'html.parser')

headlines = page.find_all('div', {'class':'src_itm-ttl'})


time.sleep(3)
for headline in headlines:
    headlines_text.append(headline.a['title'])
    page = requests.get(headline.a["href"])
    page = bs4.BeautifulSoup(page.text,'lxml')
    article = page.find_all('div','sp-cn ins_storybody')
    articles_text.append(" ".join(i.text for i in article))

for i in range(len(headlines_text)):
    with open(f"ndtv/ndtv_{i}.txt",'w') as file:
        file.write(headlines_text[i])
        file.write("\n")
        file.write(articles_text[i])

driver.close()