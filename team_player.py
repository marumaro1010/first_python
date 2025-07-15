from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from datetime import datetime
from cpbl_db import conn,add_player_list
from teams_data import mapping_team
import time
import argparse


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

parser = argparse.ArgumentParser()
parser.add_argument('--clubNo', type=str, required=True)

args = parser.parse_args()

club_no = args.clubNo
try:
    if mapping_team(club_no) == "NONE":
        raise ValueError("Not found value")
except ValueError as e:
    print(e)
    exit()

url = f"https://www.cpbl.com.tw/team?ClubNo={club_no}"
driver.get(url)
time.sleep(5)

# 取得目前網址
url = driver.current_url
parseUrl = urlparse(url)
params = parse_qs(parseUrl.query)
clubNo = params.get('ClubNo',['N/A'])[0]

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
soup.prettify()

playerList = soup.select('.TeamPlayersList')
for players in playerList:
    player = players.select('.item')
    for player_detail in player:
        teamId = mapping_team(clubNo)
        pos = player_detail.find('div', class_="pos").getText()
        name = player_detail.find('div', class_="name").getText()
        add_player_list(
            teamId=teamId,
            pos=pos,
            name=name
        )
        print(f"球員資料：{pos},{name}）")
# close
conn.close()
driver.quit()
