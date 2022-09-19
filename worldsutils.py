
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
    name: str
    teams = []

    def __init__(self, name) -> None:
        self.name = name
        self.teams = []

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
    groups = []

    def __init__(self) -> None:
        self.groups = []

    def init(self, teams_file, playin_file):
        i = 0
        temp_group_a = Group("A")
        self.groups.append(temp_group_a)
        
        temp_group_b = Group("B")
        self.groups.append(temp_group_b)

        print(self.groups)

        for row in playin_file:
            for each_name in row:
                for each_team in teams_file:
                    if each_team[0] == each_name:
                        self.groups[i].add_team(each_team)
            i += 1

        
    def print_group(self):
        print("Group A")
        for each in self.groups[0].teams:
            print(each.name.upper() + "\t" + str(each.scr) + "\t" + str(each.win) + "/" + str(each.lose))
        print("Group B")
        for each in self.groups[1].teams:
            print(each.name.upper() + "\t" + str(each.scr) + "\t" + str(each.win) + "/" + str(each.lose))




    def match_playin_phase1(self):
        for each_groups in self.groups:
            for i in range(6):
                for j in range(i + 1, 6):
                    each_groups.match_bo1(each_groups.teams[i], each_groups.teams[j])
    

