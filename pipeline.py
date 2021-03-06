import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import bs4
import time
import requests
import warnings
warnings.filterwarnings("ignore")

for folder in ["indianexpress","ndtv","newsexp"]:
    os.system(f"rm -rf {folder}")
    os.mkdir(folder)

keys = input("Enter a one-word keyword about the topic you want to search: ")

#NEWSEXP - right wing
global_url = "https://www.newindianexpress.com/topic?per_page="
headlines_text=[]
articles_text = []
options = Options()
options.headless = True
options.add_argument("--log-level=3")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
driver2 = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
print("\nExtracting data from Right wing source")

for i in range(4):
    driver.get(f"{global_url}{i}0&term={keys}&request=ALL&search=short")
    page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    headlines = page.find_all('div', {'class':'search-row_type'})
    for headline in headlines:
        if headline.h4.text not in headlines_text:
            headlines_text.append(headline.h4.a.text)
            page= driver2.get(headline.h4.a['href'])
            page = bs4.BeautifulSoup(driver2.page_source,'lxml')
            article = page.find('div',{'class':'articlestorycontent'}).find_all('p')
            articles_text.append(" ".join(i.text for i in article))
    
for i in range(min(50,len(headlines_text))):
    with open(f"newsexp/newsexp_{i}.txt",'w') as file:
        file.write(headlines_text[i])
        file.write("\n")
        file.write(articles_text[i])

#INDIANEXPRESS Neutral
print("\nExtracting data from Neutral source")
global_url = "https://indianexpress.com/page/"
headlines_text=[]
articles_text = []

for i in range(1,3):
    driver.get(global_url + f"{i}/?s=" + f'+{keys}')
    page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    headlines = page.find_all('div', {'class':'details'})
    for headline in headlines:
        if headline.h3.a.text not in headlines_text:
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

#NDTV left wing
print("\nExtracting data from Left wing source")
global_url = "https://www.ndtv.com/search?searchtext="
headlines_text=[]
articles_text = []
driver.get(global_url + keys)

for _ in range(2):
    driver.execute_script("allloadNews();")  
    time.sleep(1)  

page = bs4.BeautifulSoup(driver.page_source, 'html.parser')
headlines = page.find_all('div', {'class':'src_itm-ttl'})
for headline in headlines:
    if headline.a['title'] not in headlines_text:
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