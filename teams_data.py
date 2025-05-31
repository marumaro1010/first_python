teamMapping = {
    "ACN": 1,
    "ADD": 2,
    "AJL": 3,
    "AEO": 4,
    "AAA": 5,
    "AKP": 6,
}

teamMappingCn = {
    teamMapping["ACN"]: "中信兄弟",
    teamMapping["ADD"]: "統一獅",
    teamMapping["AJL"]: "樂天",
    teamMapping["AAA"]: "味全",
    teamMapping["AKP"]: "台鋼",
    teamMapping["AEO"]: "富邦",
}

def mapping_team(clubNo):
    return teamMapping.get(clubNo,"NONE")

def mapping_team_cn(teamId):
    return teamMappingCn.get(teamId,0)
