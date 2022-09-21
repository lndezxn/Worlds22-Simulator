import csv
import random
from functools import cmp_to_key

def readFromCsv(input: str):
    output: list = []
    with open(input) as file:
        raw_file = csv.reader(file)
        for row in raw_file:
            output.append(row)
    return output

def genSeq(units: list) -> list:
    seq: list = []
    idList: list = []
    for each in units:
        idList.append(each.id)
    for a in range(len(units)):
        for b in range(a + 1, len(units)):
            tempPair = [idList[a], idList[b]]
            random.shuffle(tempPair)
            seq.append(tempPair)
    
    random.shuffle(seq)
    return seq

def leftWins(xpwr: float, ypwr: float) -> bool:
    xrealPwr = xpwr
    yrealPwr = ypwr
    if xrealPwr > yrealPwr:
        return True
    else:
        return False

# Original info about team, immutable in single phase.
# Designed not to be used in either Group and Playoff phase,
# but GroupUnit and PlayoffUnit.
class Team:
    def __init__(self, id, name, rgn, oripwr) -> None:
        self.id: int = id
        self.name: str = name
        self.rgn: str = rgn
        self.oripwr: float = oripwr
    

# Smallest unit in group stage, referring a team.
class GroupUnit:
    def __init__(self, team: Team) -> None:
        self.id: int = team.id
        self.wins: int = 0
        self.loses: int = 0
        self.pwr: float = team.oripwr
        self.buff: float = 1

    def power(self) -> float:
        return self.pwr * self.buff


# Smallest unit in playoff stage, referring a pair of team.
class PlayoffUnit:
    def __init__(self, xteam: Team, yteam: Team) -> None:
        self.xid: int = xteam.id
        self.yid: int = yteam.id
        self.scr: list = [0, 0]
        self.xpwr: float = xteam.oripwr
        self.ypwr: float = yteam.oripwr
        self.xbuff: int = 1
        self.ybuff: int = 1


# A single group containing multiple "GroupUnit"s, contained by GroupGame.
# Group.unitList: list<GroupUnit>
# Group.resMatrix: list<list<int>>
# Group.seq: list<[int, int]>
class Group:
    def __init__(self, unitsList: list, seq: list) -> None:
        self.unitList: list = unitsList
        self.seq: list = seq
        self.nxtMatch = 0
        maxId = 0
        for unit in unitsList:
            maxId = max(maxId, unit.id)
        self.resMatrix: list = [[-1] * (maxId + 1) for _ in range(maxId + 1)]

    # There's a "nxtMatch" pointer pointing to the next game to play in "seq"
    # This function returns False when there's no more game to play
    def doNxtMatch(self) -> bool:

        # u, lUnit, rUnit: GroupUnit
        for u in self.unitList:
            if u.id == self.seq[self.nxtMatch][0]:
                xUnit = u
            if u.id == self.seq[self.nxtMatch][1]:
                yUnit = u
        
        # Apply results to units after game.
        if leftWins(xUnit.power(), yUnit.power()):
            xUnit.wins += 1
            yUnit.loses += 1
            self.resMatrix[xUnit.id][yUnit.id] = 1
            self.resMatrix[yUnit.id][xUnit.id] = 0
        else:
            xUnit.loses += 1
            yUnit.wins += 1
            self.resMatrix[yUnit.id][xUnit.id] = 1
            self.resMatrix[xUnit.id][yUnit.id] = 0

        # Sort "unitList" after every game.
        # This will not affect sequence because GroupUnit.id dosnt change.
        self.unitList = sorted(self.unitList, key = cmp_to_key(self.cmpUnit))

        # Return false if there's no more game
        self.nxtMatch += 1
        if self.nxtMatch == len(self.seq):
            return False
        else:
            return True
    
    # Print the "resMatrix"
    def printMatrix(self) -> None:
        for row in self.resMatrix:
            for col in row:
                if col == 1:
                    print("W", end=" ")
                elif col == 0:
                    print("L", end=" ")
                else:
                    print("/", end=" ")
            print()

    def cmpUnit(self, x: GroupUnit, y: GroupUnit):
        if(x.wins > y.wins):
            return -1
        elif(x.wins == y.wins and self.resMatrix[x.id][y.id] == 1):
            return -1
        else:
            return 1


# Where playin and group stage carry on.
# GroupGame.groupList: list<Group>
class GroupGame:
    def __init__(self, unitListInGroup: list, playSeqList: list) -> None:
        self.groupList = []
        for i in range(len(unitListInGroup)):
            self.groupList.append(Group(unitListInGroup[i], playSeqList[i]))


# Where playoff stage carries on.
class PlayoffGame:
    def __init__(self) -> None:
        pass


# The whole Worlds Game.
class Championship:
    def __init__(self) -> None:
        self.teamList: list = []
        self.playin = None
        self.playin2 = None
        self.group = None
        self.playoff = None
        self.groupName = ["A", "B", "C", "D"]

    # Add "Team"s into "teamList", assign index for each of them.
    def initTeam(self, teamListStr: str) -> None:
        teamList = readFromCsv(teamListStr)
        tot = 0
        for each in teamList:
            self.teamList.append(Team(tot, each[0], each[1], each[2]))
            tot += 1

    # Initialize a "GroupGame".
    def initPlayin(self, drawListStr: str) -> None:
        unitListInGroup: list = []
        drawList: list = readFromCsv(drawListStr)
        # Convert str to list<list<GroupUnit>>
        for row in drawList:
            tempList: list = []
            for col in row:
                for teams in self.teamList:
                    if teams.name == col:
                        tempList.append(GroupUnit(teams))
            unitListInGroup.append(tempList)

        # Generate match sequences for each group.
        playSeqList: list = []
        for i in range(len(unitListInGroup)):
            playSeqList.append(genSeq(unitListInGroup[i]))

        # Construct playin: GroupGame
        self.playin = GroupGame(unitListInGroup, playSeqList)

    def doPlayin(self) -> None:
        flag: bool = True
        # Do match by cycle
        while(flag):
            for group in self.playin.groupList:
                # Break if there's no more match to play
                if group.doNxtMatch() == False:
                    flag = False
            self.printGroupStatement(self.playin)
                    

    def printGroupStatement(self, game: GroupGame) -> None:
        for i in range(len(game.groupList)):
            print("Group", self.groupName[i], end="\t\t\t")
        print()
        for j in range(len(game.groupList[0].unitList)):
            for i in range(len(game.groupList)):
                team = game.groupList[i].unitList[j]
                print(self.teamList[team.id].name.upper(), "\t", str(team.wins) + "/" + str(team.loses), end="\t\t")
            print()
        print()