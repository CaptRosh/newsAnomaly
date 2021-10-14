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

for folder in ["indianexpress","ndtv","opindia"]:
    os.system(f"rm -rf {folder}")
    os.mkdir(folder)

keys = ["Lakhimpur","Farmers"]

#OPINDIA
global_url = "https://www.opindia.com/page/"
headlines_text=[]
articles_text = []
options = Options()
options.headless = True
options.add_argument("--log-level-3")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)

for i in range(1,4):
    driver.get(global_url+f"{i}/?s="+ "+".join(keys))
    print(global_url+f"{i}/?s="+ "+".join(keys))
    page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    headlines = page.find_all('div', {'class':'tdb_module_loop td_module_wrap td-animation-stack'})
    for headline in headlines:
        headlines_text.append(headline.h3.text)
        page= requests.get(headline.a['href'])
        page = bs4.BeautifulSoup(page.text,'lxml')
        article = page.find_all('p')
        articles_text.append(" ".join(i.text for i in article))
    
for i in range(min(30,len(headlines_text))):
    with open(f"opindia/opindia_{i}.txt",'w') as file:
        file.write(headlines_text[i])
        file.write("\n")
        file.write(articles_text[i])

driver.close()

#INDIANEXPRESS
global_url = "https://indianexpress.com/page/"
headlines_text=[]
articles_text = []
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)

for i in range(1,3):
    driver.get(global_url + f"{i}/?s=" + '+'.join(keys))
    page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    headlines = page.find_all('div', {'class':'details'})
    for headline in headlines:
        headlines_text.append(headline.h3.a.text)
        page = requests.get(headline.h3.a["href"])
        page = bs4.BeautifulSoup(page.text,'lxml')
        article = page.find_all('p')
        articles_text.append(" ".join(i.text for i in article))

for i in range(len(headlines_text)):
    with open(f"indianexpress/indianexpress_{i}.txt",'w') as file:
        file.write(headlines_text[i])
        file.write("\n")
        file.write(articles_text[i])

driver.close()

#NDTV
global_url = "https://www.ndtv.com/search?searchtext="
headlines_text=[]
articles_text = []
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
driver.get(global_url + '-'.join(keys))
page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
headlines = page.find_all('div', {'class':'src_itm-ttl'})

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