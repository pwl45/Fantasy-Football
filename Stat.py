# Converts a pfr stat name into a stat object with useful properties like fantasy value, display name, etc.
def getStat(name=""):
    for stat in statGroups:
        if (name == stat.name):
            return stat
    return Stat(name)

#A Representation of an individual statistic (like rushing yards, rushing TDs, etc.)
class Stat:
    def __init__(self, name, value = 0, number=0, displayName = "", totalType = ""):
        self.fdisplay = False
        self.number = number  # The quantity of this statistic
        self.value = value  # The amount of fantasy points this statistic is worth
        self.name = name  # This statistic's name
        self.displayName = displayName
        self.fdisplay = (self.displayName != "")
        self.totalType = totalType
        if not self.fdisplay:
            self.displayName = name

    def __repr__(self):
        return self.displayName
    def __len__(self):
        return len(self.displayName)


statGroups = []
statGroups += [Stat("Date", displayName= "Date")]
statGroups += [Stat("Rushing Att", displayName= "Rush Att",totalType='t'), Stat("Rushing Yds", 0.1, displayName="Rush Yards",totalType='t'), Stat("Yds/Rushing Att"), Stat("Rushing TD", 6, displayName="Rush TDs",totalType='t')]
statGroups += [Stat("Targets", displayName= "Tgt",totalType='t'), Stat("Receptions", 0.5, displayName= "Rec",totalType='t'), Stat("Receiving Yds", .1, displayName= "Rec Yards",totalType='t'), Stat("Yds/Reception"),Stat("Receiving TD", 6, displayName="Rec TDs",totalType='t'), Stat("Catch Pct"), Stat("Yds/Target")]
statGroups += [Stat("Passes Completed", displayName= "Comp",totalType='t'), Stat("Pass Attempts", displayName= "Att",totalType='t'), Stat("Pass Completion %"), Stat("Passing Yds", .04, displayName= "Pass Yards",totalType='t'), Stat("Passing TD", 6, displayName= "Pass TDs",totalType='t'), Stat("Passes Intercepted", -2, displayName= "Int",totalType='t'), Stat("Passer Rating", displayName= "Rate",totalType='p')]
#statGroups += [Stat("Punt Returns"), Stat("Punt Return Yds"), Stat("Yds/Punt Return"), Stat("Punt Return TD")]
statGroups += [Stat("Fumbles", -2, displayName="Fum",totalType='t'), Stat("Fumbles Forced",totalType='t'), Stat("Fumbles Recovered", 2, displayName="FR",totalType='t'), Stat("Fumble Return Yds", displayName= 'Fum Yds',totalType='t'), Stat("Fumble Return TD", 6, displayName= "FR TD",totalType='t')]
statGroups += [Stat("2-pt. Conv. Made", 2, displayName= "2-Pt",totalType='t'), Stat("Touchdowns"), Stat("Points Scored")]
# Scrimmage TDs do not count for fantasy points because this stat is just the sum of rushing and receiving TDs, which are already accounted for in point totals.
statGroups += [Stat("Solo"), Stat("Assists"), Stat("Combined"), Stat("TFL"), Stat("QB Hits")]
    

