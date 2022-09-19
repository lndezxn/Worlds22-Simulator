import csv
import random
import math
import worldsutils

file = open("teams.csv")
raw_teams_file = csv.reader(file)
teams_file = []

for row in raw_teams_file:
    teams_file.append(row)

file = open("draws\\playin.csv")
raw_playin_file = csv.reader(file)
playin_file = []

for row in raw_playin_file:
    playin_file.append(row)


playin = worldsutils.Playin_Stage
playin.init(playin, teams_file, playin_file)
playin.print_group(playin)

playin.match_playin_phase1(playin)
playin.print_group(playin)