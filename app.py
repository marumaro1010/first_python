from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from cpbl_db import conn, add_pitcher
from teams_data import mapping_team,mapping_team_cn
import time
import re
import urllib.parse as urlparse

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

driver.get("https://www.cpbl.com.tw/")

time.sleep(5)


html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
soup.prettify()
now = datetime.now().strftime('%Y-%m-%d')

print(f"現在時間 : {now}")
TodayMatchup = soup.select('.IndexScheduleGroup')

def clean_name(raw_name):
    return re.sub(r'[^\u4e00-\u9fa5A-Za-z0-9]', '', raw_name)

def get_team_no_from_player_div(player_div):
    team_a = player_div.find('span', class_='team').find('a')
    team_no = None
    if team_a and 'href' in team_a.attrs:
        href = team_a['href']
        parsed = urlparse.urlparse(href)
        params = urlparse.parse_qs(parsed.query)
        team_no = params.get('teamNo', [None])[0]
        if team_no and len(team_no) > 3:
            team_no = team_no[:3]  # 只保留前三碼

    return mapping_team(team_no)

for i in TodayMatchup:
    gameItems = i.find_all('div', class_="game_item")
    for item in gameItems:
        pitcher = item.find_all('div', class_="player")
        placeInfo = item.find('div', class_="PlaceInfo")
        if(placeInfo):
            print(placeInfo.get_text())
        if len(pitcher) == 2:
            for pic in pitcher:
                team_id= get_team_no_from_player_div(pic)
                name = clean_name(pic.get_text())
                # 判斷當天同隊同名是否已寫入
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM pitchers WHERE team = ? AND name = ? AND date = ?", (team_id, name, now))
                exists = cursor.fetchone()
                if not exists:
                    add_pitcher(team_id, name, now)
            away = clean_name(pitcher[0].get_text())
            away_team_id= get_team_no_from_player_div(pitcher[0])
            home = clean_name(pitcher[1].get_text())
            home_team_id= get_team_no_from_player_div(pitcher[1])
            print(f"客場先發 {mapping_team_cn(away_team_id)} {away} "
                  f"@ 主場先發 {mapping_team_cn(home_team_id)} {home}")
        else:
            print(f"尚未公布or今日無賽事")
# close
conn.close()
driver.quit()
