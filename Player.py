import requests
from bs4 import BeautifulSoup
import Stat
import FFWeek

def calcPR(comp,att,yds,td,ints):
    a = max(min((comp/att - .3)*5,2.375),0)
    b = max(min((yds/att-3)*.25,2.375),0)
    c = max(min((td/att)*20,2.375),0)
    d = max(min(2.375-(ints/att*25),2.375),0)
    return (a+b+c+d)/6*100


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Player:
    def __init__(self, name = "", team = "" , url = "", position = "", year = 2018):
        self.year = year
        self.name = name
        self.team = team
        self.url = url
        self.scores = []
        self.position = position
        for i in range(0,17):
            self.scores += [0]
        self.scoresPopulated = False
        self.stDev = 0.0
        self.avgDev = 0.0
        self.stDevCalculated = True
        self.avgDevCalculated = True
        self.count = 0
        self.median = -1
        self.total = 0
        self.stats = []
        self.data = []
        self.valueList = []
        self.fanTable = []


    def addScore(self, week, score = 0.0):
        self.scores[week - 1] = score
        if score == 0:
            return
        self.total += score
        self.count += 1
        self.stDevCalculated = False
        self.avgDevCalculated = False

    #TODO: You could make this sorting more efficient (but with max 17 weeks it doesn't matter that much).
    def getMedian(self):
        if self.median < 0:
            sortedScores = []
            for score in self.scores:
                if isinstance(score,float):
                    sortedScores += [score]
            sortedScores.sort()
            if self.count > 0:
                if self.count % 2 > 0:
                    self.median = sortedScores[int(self.count/2)]
                else:
                    self.median = (sortedScores[int(self.count/2) - 1] + sortedScores[int(self.count/2)])/2
        return self.median

    def getAverage(self):
        if self.count > 0:
            return self.total / self.count
        return 0

    def getAvgDev(self):
        if self.avgDevCalculated:
            return self.avgDev
        else:
            average = self.getAverage()
            dev = 0
            for score in self.scores:
                if score != 0:
                    dev += abs(average - score)
            self.avgDevCalculated = True
            self.avgDev = dev / self.count
            return self.avgDev


    #name jindex is used to reflect that in a normal [i][j] indexing format this index would be j
    def getColumn(self, table, jindex):
        result = []
        for i in range(len(table)):
            result += [table[i][jindex]]
        return result

    #name jindex is used to reflect that in a normal [i][j] indexing format this index would be j
    def safeTotal(self, table, jindex):
        column = self.getColumn(table, jindex)
        if len(column) > 1 and column[1].isdigit:
            sum = 0
            for i in range(1, len(column)):
                if(is_int(column[i])):
                    sum += int(column[i])
                elif(is_float(str(column[i]))):
                    sum += float(column[i])

            return round(sum,2)


    def getFanTable(self):
        results = []
        totals = []
        for i in range(0, len(self.data)):
            result = []
            for j in range(len(self.valueList)):
                #checks that this column is going to be part of the fantable
                if not isinstance(self.data[0][j], Stat.Stat) or self.data[0][j].fdisplay:
                    #print(len(self.data),len(self.data[i]))
                    #print(i,j)
                    result += [self.data[i][j]]

            if i == 0:
                result = ["Week", "|", "FP", "|"] + result
            else:
                #print(self.data[i][0])
                result = [str(FFWeek.findWeek(result[0],int(self.year))),"|", str(self.scores[i - 1]),"|"] + result
            results.append(result)

        # This loop calculates the bottom row of the table; the totals
        # TODO: Put in methods for getting efficiency metrics (ypc, y/c, pr) 'totals'
        # Use loop for getting stat in row 0 of the column to get j value, then use that j value to get a total.
        for j in range(0,len(results[0])):
            colName = results[0][j]
            if(colName == 'FP' or isinstance(colName,Stat.Stat) and colName.totalType=='t'):
                total = str(self.safeTotal(results, j))
            elif isinstance(colName,Stat.Stat) and colName.totalType == 'p':
                compl = 0
                att = 0
                yds = 0
                td = 0
                ints = 0
                for k in range(len(results[0])):
                    if isinstance(results[0][k],Stat.Stat):
                        displayName = results[0][k].displayName
                        if displayName == 'Comp':
                            comp= int(totals[k])
                        elif displayName == 'Att':
                            att = int(totals[k])
                        elif displayName == 'Pass Yards':
                            yds = int(totals[k])
                        elif displayName == 'Pass TDs':
                            td = int(totals[k])
                        elif displayName == 'Int':
                            ints = int(totals[k])
                total = str(round(calcPR(comp,att,yds,td,ints),1))
            else:
                total = ''
            totals += [total]
        results += [totals]
        self.fanTable = results




    def getStDev(self):
        if self.stDevCalculated:
            return self.stDev
        else:
            average = self.getAverage()
            variance = 0
            for score in self.scores:
                if score != 0:
                    variance += (score - average)**2
            variance /= self.count
            self.stDev = variance ** 0.5
            self.stDevCalculated = True
            return self.stDev


    """def getStatLabels(self):
        labels = self.data[0]
        for i in range(0, len(labels)):
            newLabel = labels[i]
            if newLabel == "Yds":
                if(labels[i+1] == "")"""
        #return


    def getInfo(self):
        if self.scoresPopulated:
            return
        else:
            newResponse = requests.get(self.url)
            newSoup = BeautifulSoup(newResponse.text, 'html.parser')
            table = newSoup.find('table')
            rows = table.find_all('tr')
            results = []
            #Skips first row, which is useless for our purposes.
            for i in range(1, len(rows)):
                table_headers = rows[i].find_all('th')
                if table_headers:
                    if(i == 1):
                        result = ["Rank", "Date", "Game #", "Age", "Team", "", "Opp", "Result"]
                        for j in range(len(result), len(table_headers)):
                            label = str(table_headers[j])
                            #print(label[16:].find("\""), label)
                            startIndex = label.find("\"") + 1
                            endIndex = label[(startIndex):].find("\"") + startIndex
                            trueLabel = label[startIndex:endIndex]
                            result += [trueLabel]
                        results.append(result)
                    else:
                        for headers in table_headers:
                            results.append([headers.get_text()])

                table_data = rows[i].find_all('td')
                if table_data:
                    results.append([data.get_text() for data in table_data])

                #results = results[1:len(results)]

            ind = 0
            for ind in range(0, len(results)):
                #print(ind, ":", len(results[ind]), ":", results[ind])
                if ind%2 == 1:
                    results[int((ind + 2)/2)] = results[ind] + results[ind + 1]

            results = results[0:int(ind/2)]
            statNames = results[0]
            self.valueList = []
            for j in range(0, len(statNames)):
                curStat = Stat.getStat(statNames[j])
                self.valueList += [curStat.value]
                statNames[j] = curStat
            for i in range(1, len(results)):
                score = 0
                for j in range(0, len(results[i])):
                    curr = results[i][j]
                    if curr.isdigit() or (len(curr) > 0 and curr[0] == "-" and curr[1:].isdigit()):
                        score += self.valueList[j] * int(results[i][j])
                self.addScore(i, round(score,2))

            self.data = results
            self.cleanUp()
            self.getFanTable()
            self.scoresPopulated = True
    #Removes weeks where player did not play
    def cleanUp(self):
        maxlen = 0
        for i in range(0,len(self.data)):
            maxlen = max(maxlen,len(self.data[i]))
        i=0
        while(i<len(self.data)):
            if len(self.data[i]) < maxlen:
                self.data.pop(i)
            else:
                i+=1    

    def tableString(self, table = [""]):
        result = ""
        for i in range(0, len(table[0])):
            maxLen = 0
            for j in range(0, len(table)):
                maxLen = max(maxLen, len(table[j][i]))
            begIndex = 0
            if(type(table[0][i]) != type("")):
                table[0][i].displayName = " " * (maxLen - len(table[0][i])) + table[0][i].displayName
                begIndex = 1
            for j in range(begIndex, len(table)):
                table[j][i] = " " * (maxLen - len(table[j][i])) + table[j][i]
        for i in range(0, len(table)):
            for j in range(0, len(table[i])):
                #print(table[i][j], end="   ")
                result += str(table[i][j]) + "  "
            result += "\n"
        return result


    def __repr__(self):
        result = "Name: " + self.name + "\nGames Played: " + str(len(self.data) - 1) + "\nTeam: " + self.team + "\tPosition: " + self.position + "\nPFR URL: " + self.url
        if self.scoresPopulated:
            #for i in range(0,17):
                #result += "\nWeek " + str(i+1) + ": " + str(self.scores[i])
            result += "\n" + self.tableString(self.fanTable)
            result += "\nAverage Score: " + str(round(self.getAverage(),2)) + "\t\tMedian Score: " + str(round(self.getMedian(),2))
            result += "\nStandard Deviation: " + str(round(self.getStDev(),2)) + "\t\tAverage Deviation: " + str(round(self.getAvgDev(), 2)) + "\n"
            #result += "\n" + str(self.safeTotal(0))
        return result
    def smallRepr(self):
        return (self.name + ": " + self.team + " " +self.position)



