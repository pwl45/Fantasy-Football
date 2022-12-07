import datetime
maxyear=2022
weekDates = [['2018-9-12']] * (maxyear-1970+1)

# Compares two dates, returns a positive number if date1 is later than date 2, and a negative number if date1 is earlier
def compDate(date1 = '0000-00-00', date2 = '0000-00-00'):
    yeardiff = int(date1[0:4]) - int(date2[0:4])
    if yeardiff != 0:
        return yeardiff
    monthDiff = int(date1[5:7]) - int(date2[5:7])
    if monthDiff != 0:
        return monthDiff

    return int(date1[8:10]) - int(date2[8:10])

# Returns the week number that a given game occured in.
    # Year parameter seems redundant, since you could just use the first 4 digits of the date
    # HOWEVER, it is necessary, since the season year doesn't always match the date's year.
    # For example, certain games of Week 17 of the '2017' season actually occured in early January of 2018.
def findWeek(date = '0000-00-00',year=2018):
    date = date.strip()
    #Date always > 1970 b/c that's the furthest the data goes back
    weeks = weekDates[year - 1970]
    for i in range(0, len(weeks)):
        if compDate(date, weeks[i]) < 0:
            return i + 1
    return 999

# TODO: You don't really need to store any data except the original date.
# The rest can be extrapolated in the findWeek method
# SEED IS TUESDAY OR WEDNESDAY AFTER WEEK 1
def setWeeks(currYear = 2018, origin = '2018-09-12'):
    weekDates[currYear-1970] = []
    # if currYear < 2021:
    #     maxweek = 18
    # else:
    #     maxweek = 18
    for i in range(0, 18):
        #                              year                                month             day
        weekDates[currYear - 1970] += [str(datetime.date(int(origin[0:4]), int(origin[5:7]), int(origin[8:10])) + datetime.timedelta(days= 7*i))]

setWeeks(2022,'2022-09-13')
setWeeks(2021,'2021-09-15')
setWeeks(2020,'2020-09-15')
setWeeks(2019,'2019-09-11')
setWeeks()
setWeeks(2017,'2017-09-13')
setWeeks(2016,'2016-09-14')
setWeeks(2015,'2015-09-16')
setWeeks(2014,'2014-09-10')
setWeeks(1973,'1973-09-18')


