
import sqlite3
import sys
from teams_data import mapping_team_cn

conn = sqlite3.connect("baseball.db")
cursor = conn.cursor()

def create_tables():
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS starting_pitchers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team INTEGER NULL,  -- 1:中信象, 2:統一獅, 3:樂天, 4.味全龍, 5.台鋼雄鷹, 6.富邦悍將 --
        name TEXT NOT NULL,
        date TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS player_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team INTEGER NULL,  -- 1:中信象, 2:統一獅, 3:樂天, 4.味全龍, 5.台鋼雄鷹, 6.富邦悍將 --
        team_cn TEXT NULL,  -- 1:中信象, 2:統一獅, 3:樂天, 4.味全龍, 5.台鋼雄鷹, 6.富邦悍將 --
        position TEXT NOT NULL,
        name TEXT NOT NULL
    );
    """)

def add_picther(teamId: int, name: str, date: str):
    try:
        cursor.execute(
            "INSERT INTO pitchers (team, name, date) VALUES (?, ?, ?)",
            (teamId, name, date)
        )
        conn.commit()
        print(f"新增成功：{name}（team={teamId}, date={date}）")
    except Exception as e:
        print("寫入錯誤：", e)

def add_player_list(teamId: int, pos: str, name: str):
    try:
        teamCn = mapping_team_cn(teamId)
        cursor.execute(
            "INSERT INTO player_list (team, team_cn, position, name) VALUES (?, ?, ?, ?)",
            (teamId, teamCn, pos, name)
        )
        conn.commit()
        print(f"新增成功：{name}（team={teamCn}, position={pos}）")
    except Exception as e:
        print("寫入錯誤：", e)

def get_picther_by_team(teamId: int):
    try:
        cursor.execute(
            "SELECT * FROM pitchers WHERE team = ?",
            (teamId)
        )
    except Exception as e:
        print("查詢錯誤")

if __name__ == "__main__": #只有該程式才能使用
    if len(sys.argv) > 1 and sys.argv[1] == "create_tables":
        create_tables()
