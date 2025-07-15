from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from cpbl_db import conn, add_picther
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
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(f"現在時間 : {now}")
TodayMatchup = soup.select('.IndexScheduleGroup')
for i in TodayMatchup:
    gameItems = i.find_all('div', class_="game_item")
    for item in gameItems:
        pitcher = item.find_all('div', class_="player")
        placeInfo = item.find('div', class_="PlaceInfo")
        if(placeInfo):
            print(placeInfo.get_text())
        if len(pitcher) == 2:
            for pic in pitcher:
                add_picther(1,pic.get_text(),now)
            away = pitcher[0].get_text()
            home = pitcher[1].get_text()
            print(f" 客場先發 {away} @ 主場先發 {home}")
        else:
            print(f"尚未公布or今日無賽事")
# close
conn.close()
driver.quit()
