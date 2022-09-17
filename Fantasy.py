##TODO:
# Expand List function
# Custom VBD
# Custom Values

allImported = True

positions = ["rb","wr","qb","te"]

try:
    import requests
    from bs4 import BeautifulSoup
    import re
    import Player
except ImportError:
    allImported = False

# Finds a player given a name
def getPlayer(name = ""):
    for player in players:
        if player.name == name:
            return player
    print("Exact match not found\nChecking similar names")
    for player in players:
        if re.findall("^" + name, player.name):
            print("Player found")
            return player
    return None

# This method uses ProFootballReference's list of players to populate a big
# of players.
# I don't actually know HTML so I basically made up at where the data was in the HTML code.
def getPlayers(year='2021'):
    playerlist = []
    response = requests.get('https://www.pro-football-reference.com/years/' + year + '/fantasy.htm')
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Internet connection successful")
    lines = str(soup).splitlines()
    #print(lines)
    for line in lines:
        if (re.findall("^<tr><th", line)) or (re.findall("^<tbody><tr><th", line)):  # Finds all HTML lines that begin with the string that indicates a player
            # These two statements find the player's name within the line that contains the player.
            i = line.find("htm\">") + 5
            playerName = line[i:line[i:].find("<") + i].title()

            # These lines find the player's team
            # (Note: Players that played on 2 different teams do not have their teams stored in the same place, and are
            # given the placeholder value "2TM" to indicate that they played on multiple teams.
            i = line.find("/teams/") + 7
            if (i > 6):
                playerTeam = line[i:i + 3].upper()  # if the player's team was found, set player's team value to that
            else:
                # TODO: run 2TM fix
                playerTeam = "2TM" # if team isn't found, set it to "2TM" (because that is the only data on this page)

            #Find the URL for the player's individual page.
            i = line.find("href=\"/players")
            playerUrl = "https://www.pro-football-reference.com" + line[i + 6:i + 25] + "/gamelog/" + year + "/"

            i = line.find("fantasy_pos")
            playerPosition = line[i + 13:i + 15]

            playerlist += [Player.Player(playerName, playerTeam, playerUrl, playerPosition,year)]  # creates a player with a name, url, and team.
    # print(playerlist[:10])
    return playerlist

if allImported:
    print("Note: an internet connection is required to use this program.")
    year = input("Enter a year between 1970 and 2021 to get fantasy data on that year: ")
    while (not year.isdigit() or int(year) < 1970 or int(year) > 2021):
        year = input("Year must be a number between 1970 and 2021. Please re-enter.  ")
    players = getPlayers(year)
    print("Fantasy Data loaded for " + year + ".")

    #TODO: Implement list by position
    while True:
        print("\nTo get data on an NFL fantasy player (for example, Todd Gurley), enter their name, or q to quit.\n")
        name = input("To get a list of the top x players by fantasy value, enter list x. For example, \"list 10\" prints the top 10 fantasy players.  ")
        if name.lower() == "q":
            break
        if name.lower()[0:4] == "list":
            commands = name.split()
            if(len(commands) < 1):
                print("\nPlease separate input with spaces.\nFor example, type \"List 10 RB\", not \"List10RB\"")
            elif len(commands) == 2:
                if commands[1].isdigit():
                    print()
                    i = 0
                    limit = min(int(commands[1]), len(players))
                    while(i < limit):
                        print(players[i].smallRepr())
                        i+=1
                    #for i in range(limit):
                    #    print(players[i].name)
                    print()
                else:
                    print("\nPlease follow the list command with an integer.\n")
            elif len(commands) == 3:
                third = commands[2].lower()
                if commands[1].isdigit():
                    print()
                    if(third in positions):
                        count = 0
                        i = 0
                        while(count < int(commands[1]) and i < len(players)):
                            if(players[i].position.lower() == third):
                                print(players[i].smallRepr())
                                count+=1;
                            i+=1
        elif name.isdigit() and int(name) >= 1970 and int(name) <= 2019:
            year = name
            players = getPlayers(year)
            print("Fantasy Data loaded for " + year + ".")
        else:
            p1 = getPlayer(name.title())
            if p1 is not None:
                p1.getInfo()
                print(p1)
            else:
                print("\nNo player with that name. Please enter another player.\n")
else:
    print("You must have the \"requests\" module and the \"beautifulsoup4\" module to run this program.")
    print("Please install these modules before running the program again. ")
