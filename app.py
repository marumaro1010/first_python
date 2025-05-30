from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

driver.get("https://www.cpbl.com.tw/")

time.sleep(5)


html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
soup.prettify()

TodayMatchup = soup.select('.IndexScheduleGroup')
for i in TodayMatchup:
    game_items = i.find_all('div', class_="game_item")
    for item in game_items:
        pitcher = item.find_all('div', class_="player")
        placeInfo = item.find('div', class_="PlaceInfo")
        if(placeInfo):
            print(placeInfo.get_text())
        if len(pitcher) == 2:
            away = pitcher[0].get_text()
            home = pitcher[1].get_text()
            print(f" 客場先發 {away} @ 主場先發 {home}")
# close
driver.quit()
