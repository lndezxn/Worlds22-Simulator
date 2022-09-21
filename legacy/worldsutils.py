import random

class Team:
    def __init__(self, name, region, rank) -> None:
        self.name = name
        self.region = region
        self.rank = rank
        self.win = 0
        self.lose = 0
        self.scr = 0

    def winning(self):
        self.win += 1
        self.scr += 1

    def losing(self):
        self.lose += 1

class Group:
    def __init__(self, name) -> None:
        self.name = name
        self.teams = []
        self.res = []

    def add_team(self, inteam):
        self.teams.append(Team(inteam[0], inteam[1], inteam[2]))
        #print("add", inteam, self.name)

    def match_bo1(self, team_a: Team, team_b: Team):
        rank_a = team_a.rank
        rank_b = team_b.rank
        
        if(rank_a > rank_b):
            print(team_a.name+ " 1 : 0 " + team_b.name)
            team_a.winning()
            team_b.losing()
        else:
            print(team_a.name + " 0 : 1 " + team_b.name)
            team_a.losing()
            team_b.winning()



class Playin_Stage:
    def __init__(self) -> None:
        self.groups = []
        self.seq = []
        for i in range(1):
            self.seq.append(gen_playin_seq())

    def init(self, teams_file, playin_file):
        i = 0
        temp_group_a = Group("A")
        self.groups.append(temp_group_a)
        temp_group_b = Group("B")
        self.groups.append(temp_group_b)
        for row in playin_file:
            for each_name in row:
                for each_team in teams_file:
                    if each_team[0] == each_name:
                        self.groups[i].add_team(each_team)
            i += 1

    def print_group(self):
        sorted_groups_a = sorted(self.groups[0].teams, key=cmp_team, reverse=True)
        sorted_groups_b = sorted(self.groups[1].teams, key=cmp_team, reverse=True)

        print("Group A")
        for each in sorted_groups_a:
            print(each.name.upper() + "\t" + str(each.scr) + "\t" + str(each.win) + "/" + str(each.lose))
        print("\nGroup B")
        for each in sorted_groups_b:
            print(each.name.upper() + "\t" + str(each.scr) + "\t" + str(each.win) + "/" + str(each.lose))

    def match_playin_phase1(self):
        for each_groups in self.groups:
            for each_groupseq in self.seq:
                for each_match in each_groupseq:
                    each_groups.match_bo1(each_groups.teams[each_match[0]], each_groups.teams[each_match[1]])


def gen_playin_seq():
    matches = []
    while(len(matches) < 15):
        contiflag = False
        team_a = random.randint(0, 5)
        team_b = random.randint(0, 5)
        if team_a == team_b:
            continue
        for [a, b] in matches:
            if (a == team_a and b == team_b) or (a == team_b and b == team_a):
                contiflag = True
        if contiflag == True:
            continue

        matches.append([team_a, team_b])
    return matches

def cmp_team(x: Team):
    return x.scr