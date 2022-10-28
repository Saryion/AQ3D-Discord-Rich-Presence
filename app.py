from pypresence import Presence
import json
import time

RPC = Presence("discord app client id here")
RPC.connect()

begin = time.time()

with open("storage/maps.json", "r") as maps:
    maps = json.load(maps)

with open("storage/classes.json", "r") as classes:
    classes = json.load(classes)

def fetch_region(areaname):
    for region in maps:
        for map in maps[region]:
            if areaname in map:
                return region
    return ""

def fetch_class(classid):
    for index in classes:
        if index["ID"] == classid:
            return index
    return ""

def initiate_menu_rpc():
    RPC.update(
        details = "In Main Menu",
        large_image = "mainmenu",
        start = begin)

def initiate_game_rpc(name, classid, areaname, group, groupcount, dungeon, isafk):
    active_class = fetch_class(classid)
    region = fetch_region(areaname)
    large_image = region.replace("'", "").replace(" ", "").lower() if region != "" else "logo"
    status_afk = " <AFK>" if isafk == "true" else ""

    if group == "true":
        if dungeon == "true":
            state = f"In a Group ({groupcount} of 5)"
            large_image = "dungeon"
            large_text = "Exploring a Dungeon"

        else:
            state = f"In a Group ({groupcount} of 5)"
            large_text = f"Roaming {region}"

    elif dungeon == "true":
        state = f"Playing Solo{status_afk}"
        large_image = "dungeon"
        large_text="Exploring a Dungeon"

    else:
        state = f"Playing Solo{status_afk}"
        large_text = f"Roaming {region}"

    RPC.update(buttons=[
        {
            "label": f"{name}'s Char Page",
            "url": f"https://game.aq3d.com/account/Character?id={name}"
        }],
        state = state,
        details = areaname,
        large_image = large_image,
        large_text = large_text,
        small_image = active_class["ClassImage"],
        small_text = f"{active_class['ClassName']}",
        start = begin)

while True:
    with open("storage/presence.json", "r") as jsonData:
        try:
            jsonData   = json.load(jsonData)
            name       = jsonData["Name"]
            classid    = jsonData["ClassID"]
            inmenu     = jsonData["InMenu"]
            areaname   = jsonData["AreaName"]
            dungeon    = jsonData["InDungeon"]
            group      = jsonData["InGroup"]
            groupcount = jsonData["GroupCount"]
            isafk      = jsonData["IsAFK"]

            if inmenu == "true":
                initiate_menu_rpc()

            else:
                initiate_game_rpc(name, classid, areaname, group, groupcount, dungeon, isafk)

            time.sleep(1)

        except ValueError:
            continue
