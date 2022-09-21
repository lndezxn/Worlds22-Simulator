import csv
import csvreader
import random
import math
import worldsutils as wu

teams_file = csvreader.read("data\\teams.csv")
playin_draw_file = csvreader.read("data\\playin_draw.csv")


playin = wu.Playin_Stage()
playin.init(teams_file, playin_draw_file)

playin.match_playin_phase1()
playin.print_group()