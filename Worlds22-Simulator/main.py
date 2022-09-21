from errno import WSAELOOP
import lib

worlds = lib.Championship()
worlds.initTeam("teams.csv")
worlds.initPlayin("playin_draw.csv")
worlds.doPlayin()